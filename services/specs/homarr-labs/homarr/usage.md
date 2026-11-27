# Homarr Dashboard

Each enrollment runs a private [Homarr](https://homarr.dev/) dashboard. Homarr is written and maintained by Homarr Labs and contributors and is released under the Apache-2.0 license; the provider of this service is its author. UnitySVC Labs lists the official `ghcr.io/homarr-labs/homarr` image (version 2.14.0, pinned by digest), and the platform runs one isolated instance per enrollment. The image runs Homarr, an nginx proxy and an embedded Redis in the one container; there is no other service to run.

Your boards, users and settings are kept in the `homarr` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `homarr/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Homarr instance at a time.
2. The form shows a generated **Encryption seed**. Homarr turns it into the key that encrypts integration secrets (API keys and passwords you enter for integrations) in its database. **Save it, and use the same seed if you enroll again**: secrets stored under an earlier seed cannot be read with a different one. Do it now: the platform keeps it as a secret and does not show it again. It is an application secret, not your UnitySVC API key and not a login password.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. Homarr takes about a minute to start. **A new enrollment has a new address**, so bookmarks need the new one.
4. **Open the address and complete the setup wizard immediately.** A new Homarr has no administrator, and the wizard that creates one asks for no secret: whoever opens the address first claims it, and while that claim lasts (4 hours) other visitors are refused. Create your administrator name and password in the wizard. If somebody else claimed it first, stop the instance, delete the `homarr/` folder in your home and start again.

## First use

1. In the wizard, choose a language and color scheme, and decide whether to **share anonymous product analytics**. The switch is on by default; switch it off if you do not want Homarr to send usage statistics to its developers. You can change it later under the management pages (Settings).
2. Homarr lists the integrations it could set up. The Docker and Kubernetes integrations are not available here (no Docker socket is provided); add integrations for other tools by their address and credentials.
3. Build your first board: add app tiles, bookmarks and widgets in edit mode. Widgets that fetch data (weather, RSS feeds, update checks, icon lists) reach the internet from the instance; features that call other services need the credentials you give them there.
4. Sign in later with the administrator name and password from the wizard. There is no administrator password parameter. Homarr stores passwords hashed; the encryption seed protects integration secrets only.

## Authentication

Homarr checks every request itself: boards are private to signed-in users unless you make one public, and the management pages need an administrator. Anyone who knows the instance address can reach the sign-in page, so use a strong administrator password. UnitySVC adds no other gate.

## What is kept, and what is lost

The whole `/appdata` folder is persistent: the SQLite database (`homarr/db`), the embedded Redis dump (`homarr/redis`) and any trusted certificates. The platform restores them before Homarr starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file Homarr removes can come back after a restart. This is cosmetic.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Homarr and this keeps the stored database consistent.
- Do not edit the files in `homarr/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `homarr/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `small` size (1 core, 2 GiB, as listed in the platform's size table) and you pay the platform's cost for it for as long as it runs, including idle time. Homarr is a Next.js server with its own proxy and Redis: in a local check it used about 330 MiB at idle and peaked near 420 MiB while it refreshed its icon list at first start, which is too close to the 512 MiB of `nano`. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
