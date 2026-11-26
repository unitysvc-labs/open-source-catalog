#!/usr/bin/env python3
"""Generate the ntfy-sh enrollment parameters from ntfy's own configuration reference.

Every ntfy environment variable the container accepts is an enrollment parameter, except the ones the
service owns (EXCLUDED: where ntfy listens, its TLS, its storage files and database, its cluster mode,
and the authentication that NTFY_ACCESS_TOKEN provisions). Each parameter's default is the value ntfy
itself defaults to, so an enrollment that changes nothing runs the stock configuration, and every
variable is always set (the channel environment cannot omit one). An option that ntfy leaves unset by
default is not a parameter at all: the platform treats an empty value as missing and will not start the
instance, and a placeholder would switch the feature on.

Usage (rewrites the `params` and `environment` of the base channel in offering.json):

    scripts/generate_ntfy_params.py [--version v2.38.1] [--docs path/to/config.md]

The documentation table is fetched from the ntfy repository at the given tag unless --docs names a
local copy. Run `usvc_seller specs format` afterwards.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path

OFFERING = Path(__file__).resolve().parent.parent / "services/specs/binwiederhier/ntfy-sh/offering.json"
DOCS_URL = "https://raw.githubusercontent.com/binwiederhier/ntfy/{version}/docs/config.md"

# Variables the service owns, with why. They are not parameters.
EXCLUDED = {
    # Where ntfy listens: one HTTP entry on port 80 behind the platform's HTTPS, no sockets, no TLS.
    "NTFY_LISTEN_HTTP": "the one public entry is port 80",
    "NTFY_LISTEN_HTTPS": "TLS ends at the platform",
    "NTFY_LISTEN_UNIX": "no unix socket is reachable",
    "NTFY_LISTEN_UNIX_MODE": "no unix socket is reachable",
    "NTFY_EXPERIMENTAL_LISTEN_ADMIN_UNIX": "no unix socket is reachable",
    "NTFY_KEY_FILE": "TLS ends at the platform",
    "NTFY_CERT_FILE": "TLS ends at the platform",
    "NTFY_BEHIND_PROXY": "always behind the platform's proxy",
    # Storage is SQLite files in /tmp; a database URL excludes them, and a cluster needs a database.
    "NTFY_CACHE_FILE": "the message cache is a fixed file in /tmp",
    "NTFY_AUTH_FILE": "the user database is a fixed file in /tmp",
    "NTFY_DATABASE_URL": "storage is SQLite in /tmp (a database URL excludes the file options)",
    "NTFY_DATABASE_REPLICA_URLS": "storage is SQLite in /tmp",
    "NTFY_EXPERIMENTAL_CLUSTER_NODE_ID": "one instance, no cluster",
    "NTFY_EXPERIMENTAL_CLUSTER_LISTEN": "one instance, no cluster",
    "NTFY_EXPERIMENTAL_CLUSTER_ADVERTISE_URL": "one instance, no cluster",
    "NTFY_EXPERIMENTAL_CLUSTER_SECRET": "one instance, no cluster",
    "NTFY_EXPERIMENTAL_CLUSTER_BATCH_LINGER": "one instance, no cluster",
    "NTFY_EXPERIMENTAL_CLUSTER_ROLE": "one instance, no cluster",
    "NTFY_EXPERIMENTAL_CLUSTER_DRAIN_DELAY": "one instance, no cluster",
    "NTFY_EXPERIMENTAL_CLUSTER_DRAIN_DURATION": "one instance, no cluster",
    # Authentication is provisioned from NTFY_ACCESS_TOKEN; anonymous access stays denied.
    "NTFY_AUTH_DEFAULT_ACCESS": "anonymous access is denied; the access token is the credential",
    # Needs a file the instance cannot be given, or a port nothing reaches.
    "NTFY_FIREBASE_KEY_FILE": "a Firebase key file cannot be mounted",
    "NTFY_SMTP_SERVER_LISTEN": "no port 25 is reachable",
    "NTFY_SMTP_SERVER_DOMAIN": "no port 25 is reachable",
    "NTFY_SMTP_SERVER_ADDR_PREFIX": "no port 25 is reachable",
}

# Documented defaults that are not a plain literal in the table.
DEFAULT_OVERRIDES = {
    # The table shows the example value; ntfy's real default is unset (and setting it requires a base URL).
    "NTFY_UPSTREAM_BASE_URL": "",
    "NTFY_GLOBAL_TOPIC_LIMIT": "15000",
    "NTFY_BAN_WEIGHTS": "42909:2,50701:0.05,41002:0.05",
    "NTFY_UPSTREAM_ACCESS_TOKEN": "",
}
UNSET = {"-", "", "*system default*"}


def clean(text: str) -> str:
    """Markdown to plain text: links to their label, no emphasis or code ticks, no credential-shaped examples.

    The documentation's examples (a Twilio account SID, access tokens) look like real credentials to
    secret scanners, and GitHub's push protection refuses them, so they are shortened.
    """
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*]", "", text).strip()
    text = re.sub(r"\b([A-Z]{2})[0-9a-fA-F]{30,}\b", r"\1...", text)  # Twilio SIDs: AC..., VA...
    text = re.sub(r"\btk_[A-Za-z0-9_-]{8,}\.*", "tk_...", text)
    return re.sub(r"\b[0-9a-f]{24,}\b", "...", text)


def parse(markdown: str) -> list[dict[str, str]]:
    rows = []
    for line in markdown.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not cells[1].startswith("`NTFY_"):
            continue
        rows.append(
            {
                "option": cells[0].strip("`"),
                "env": cells[1].strip("`"),
                "format": clean(cells[2]),
                "default": cells[3],
                "description": clean("|".join(cells[4:])),
            }
        )
    return rows


def default_of(row: dict[str, str]) -> str:
    if row["env"] in DEFAULT_OVERRIDES:
        return DEFAULT_OVERRIDES[row["env"]]
    value = clean(row["default"])
    if value in UNSET or value.startswith("="):
        return ""
    return value


def build(rows: list[dict[str, str]]) -> tuple[dict, dict, list[str]]:
    properties: dict[str, dict] = {}
    environment: dict[str, str] = {}
    skipped: list[str] = []
    for row in rows:
        env = row["env"]
        if env in EXCLUDED:
            continue
        default = default_of(row)
        if default == "":
            # The platform treats an empty parameter value as missing (`missing_parameter`) and refuses
            # to start the instance, and the channel environment cannot leave a variable out. So an option
            # whose ntfy default is unset (SMTP sender, Stripe, Twilio, web push, a base URL, ...) cannot be
            # a parameter: it needs a value to mean anything, and a placeholder would switch the feature on.
            skipped.append(env)
            continue
        prop: dict = {
            "type": "string",
            "title": row["option"],
            "default": default,
            "description": f"{row['description']} (NTFY option {row['option']}; format: {row['format']}).",
        }
        if "bool" in row["format"].lower():
            prop["enum"] = ["true", "false"]
        properties[env] = prop
        environment[env] = "{{ params." + env + " }}"
    return properties, environment, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", default="v2.38.1", help="the ntfy tag whose docs to read")
    parser.add_argument("--docs", type=Path, help="a local copy of docs/config.md")
    args = parser.parse_args()
    markdown = (
        args.docs.read_text()
        if args.docs
        else urllib.request.urlopen(DOCS_URL.format(version=args.version)).read().decode()  # noqa: S310
    )
    properties, environment, skipped = build(parse(markdown))

    offering = json.loads(OFFERING.read_text())
    channel = offering["upstream_access_config"]["base"]
    schema = channel["params"]["schema"]
    token = schema["properties"]["NTFY_ACCESS_TOKEN"]
    defaults = channel["params"].get("testing_defaults", {})
    schema["properties"] = {"NTFY_ACCESS_TOKEN": token, **dict(sorted(properties.items()))}
    schema["required"] = ["NTFY_ACCESS_TOKEN"]
    channel["environment"]["ntfy"] = {
        **{k: v for k, v in channel["environment"]["ntfy"].items() if k in ("NTFY_AUTH_USERS", "NTFY_ACCESS_TOKEN")},
        **dict(sorted(environment.items())),
    }
    channel["params"]["testing_defaults"] = defaults
    OFFERING.write_text(json.dumps(offering, indent=2, ensure_ascii=False) + "\n")
    print(f"{len(properties)} parameters, {len(EXCLUDED)} variables owned by the service, {len(skipped)} with no default left out")


if __name__ == "__main__":
    main()
