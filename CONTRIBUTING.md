# Contributing a recipe

A recipe is the set of files that lets UnitySVC run an open-source project as a private container for each customer who enrolls. You do not need a seller account, seller credentials, infrastructure or a backend service ID to contribute one. Open a PR; Labs reviews it and publishes it.

Not sure this is the right route? See [For authors](README.md#for-authors) for the Developer-seller and commercial-seller alternatives.

## The recommended way: ask your coding assistant

If you use a coding assistant (Claude Code, Codex, Qoder, Qwen, DeepSeek or similar), let it write the recipe and open the PR. Fill in the angle-bracket parts and give it this prompt, from a working directory where it can fork and clone repositories (for example with the GitHub CLI signed in to your account):

```text
Create a pull request for https://github.com/unitysvc-labs/unitysvc-compute-services that adds <PROJECT NAME> as a container recipe.

Read about the software from <UPSTREAM REPO OR DOCS URL> (its README, documentation, license and container image page: <IMAGE PAGE URL, if you have one>). Use what you read, not your memory, to write the descriptions, find the official image and tag, the port, how it is configured and authenticated, and the settings a customer may want to change. <If the upstream has a Compose file: use <URL> as the instance spec by link.> I am <the upstream author | a community maintainer, not the author>. The demo I want a customer to be able to try: <one sentence, optional>.

Fork the repository, work on a branch, and read first, in this order:
1. CONTRIBUTING.md and README.md in the repository (the rules, the pricing policy, the checklist).
2. The two existing recipes under services/specs/ (services/specs/kadxy/weixin-ilink-gateway is the smallest complete one; services/specs/binwiederhier/ntfy-sh shows many parameters). Copy their structure and conventions.
3. The compute sizes: https://unitysvc.com/docs/sizes
4. The container services guide: https://github.com/unitysvc/unitysvc-sellers/blob/main/docs/guides/container-services.md

Then:
- Create services/specs/<provider>/<project>/ with provider.json, offering.json, listing.json, compose.yaml (or an instance_spec link) and usage.md. The provider is the software's author, with their own homepage; never invent a contact address or imply the author supports or endorses this.
- Check the license is OSI-approved and record its SPDX identifier. Stop and tell me if it is not.
- Pricing is fixed: listing.json has {"list_price": {"type": "base_cost"}} and offering.json has {"payout_price": {"type": "constant", "price": "0"}}. No dollar prices, markups or other payout.
- Keep the Compose file plain: no {{ params }} in it. Put per-customer settings in the channel's environment as {{ params.NAME }}, declared under params.schema with descriptions, validation, a safe default or generated token, and testing_defaults. No password or token shared by every customer.
- Choose the smallest size from the sizes page that really runs the software, and explain how you checked.
- Use the container_connectivity preset for the connectivity test.
- Do not add a service.json, and do not upload, publish or merge anything.
- Run `usvc_seller specs validate`, `usvc_seller specs format --check services` and `python scripts/check_channel_binding.py`, and run the container locally with Docker if you can. Fix what they report.
- Write the descriptions, parameters and usage guide from the upstream documentation you read, in the style of the existing recipes. If the upstream does not say something you need (license, official image, port, authentication, a size that fits), ask me instead of guessing.

Open the PR with the repository's template filled in, including the license, the image, the size choice and the check output.
```

What you give the assistant is a link to the project (and its image page), and whether you are the author. It reads the upstream documentation and writes the recipe from it; you do not spell out the descriptions or settings. It should come back with questions rather than guess a license, a contact address or a size. Read its PR before you submit it: you are vouching for the recipe.

## Before you start

- **License.** The project must use an OSI-approved open-source license, identified by its SPDX identifier and linked to the upstream license text. An exception needs an explicit catalog-policy decision from Labs.
- **Image.** Use the project's documented image, one the platform can pull and run on its supported architecture. Name the tag in the recipe; Labs reviews the image and the platform reports the digest it pulled.
- **Credit.** Name the software's author accurately as the provider, with the project's own homepage. Never invent a contact address, and do not imply that the author offers support or endorses the recipe. If a contact is missing or unclear, say so in the PR and reviewers will settle it.
- **Who you are.** State whether you are the upstream author or a community maintainer. A community recipe is listed as unofficial unless the author takes part.

## What to add

Under `services/specs/<provider>/<project>/`:

| File | What it holds |
| --- | --- |
| `provider.json` | The software author as provider: name, homepage, license/terms link, contact only if the project publishes one |
| `offering.json` | The technical spec: the container channel, its entries, parameters and size, and the zero payout |
| `listing.json` | What customers see: the bare `base_cost` price, documents and the connectivity-test preset |
| `compose.yaml` | The Compose file (the offering's `instance_spec`): a file in the recipe, or an upstream file referenced by URL. See [The Compose file](#the-compose-file) |
| `usage.md` | How to use the service: setup, authentication, a demo step, what it costs and how to stop it, and what is lost when the instance stops |

Use [`services/specs/kadxy/weixin-ilink-gateway`](services/specs/kadxy/weixin-ilink-gateway) as the smallest complete reference recipe. Do not add a `service.json`: the platform creates a new service's identity. Never edit an existing one.

### The Compose file

Every channel of a recipe runs the offering's one Compose file, so channels differ in size and parameters, not in stack. It can be a file in the recipe folder (`"instance_spec": "compose.yaml"`) or an upstream project's own Compose file (`"instance_spec": "https://github.com/<owner>/<repo>/blob/<commit-sha>/compose.yaml"`), so you can reuse a project's generic file as it is instead of copying it.

#### Using an upstream file

- Link a commit-SHA permalink, not a branch. The platform fetches the URL once when the service is uploaded and stores those bytes, so what customers run is what was reviewed, and a branch link can change after you tested it. A change upstream reaches customers only when Labs re-uploads.
- To pin the exact bytes, add the file's SHA-256 to the document form (`meta.sha256`); an upload of a different file is refused.
- The link must be https, at most 1 MiB, on a public host. The tools download it themselves to validate and test it.
- You cannot edit an upstream file. Anything the platform ignores or refuses (below) has to be something the upstream file already satisfies; otherwise copy the file into the recipe and change the copy, and say what you changed.

#### What the platform does with each Compose key

The platform reads the file with an allowlist: every key is honored, ignored (with a warning) or rejected, and anything not listed is rejected, so a new Compose feature never slips through silently. `usvc_seller specs validate` reports each one.

| | Keys |
| --- | --- |
| **Honored** | `image`, `command`, `entrypoint`, `environment`, `ports` (the container port only), `healthcheck`, `working_dir`, `user`, `read_only`, named `volumes` |
| **Ignored** | `container_name`, `restart`, `labels`, `logging`, `networks`, `expose`, `profiles`, `links`, `x-*` extension fields, the top-level `name`, `version` and `networks`, the host side of a published port, `healthcheck.start_interval` |
| **Ignored, with a loud warning** | `env_file` (the file is not part of the recipe, so its values are missing and the service may not start), `depends_on` (there is no start ordering: each service must retry until its dependencies answer) |
| **Ignored, replaced by the channel** | `deploy.resources`, `mem_limit` and `cpus` come from the channel's size (`resources`), not the file. `deploy.resources` can stay for local Docker; `mem_limit` and `cpus` are rejected |
| **Rejected** | `build` (give an `image`), `privileged`, `cap_add`, `devices`, `network_mode`, `pid`, `ipc`, `security_opt`, `sysctls`, `runtime`, `extra_hosts`, `volumes_from`, `extends`, `include`, `secrets`, `configs`, host paths and bind mounts, and any key not listed above |

Other behaviors to know:

- **Storage is scratch space.** A named or anonymous volume becomes a writable path that survives a container restart but not a replacement of the instance. It counts against the size's `ephemeral-storage`.
- **Images.** A tag is accepted; the platform runs it as written and records the digest it pulled. Write `image@sha256:...` if you need exactly the bytes you tested.
- **Service names** must be DNS labels (lowercase letters, digits and `-`): siblings reach each other by name.
- **Public entries.** The recipe's `entries` choose a Compose service and its container port. Customers reach it over HTTPS on port 443, not through Compose `ports`.

#### How channel variables reach the containers

The Compose file stays plain Compose that also runs with Docker. Per-customer values come from the channel instead, and no `{{ params.NAME }}` may appear in the Compose file (it is rejected):

1. The channel's `params.schema` declares each parameter a customer can set at enrollment, with a description, validation and a default or a generated token.
2. The channel's `environment` maps each Compose service name to the variables it receives, and writes the parameter into the value: `"environment": {"gateway": {"API_KEY": "{{ params.WEIXIN_API_KEY }}"}}` (the Weixin recipe).
3. At enrollment the platform fills in `{{ params.NAME }}` from what the customer entered, then adds the result to that service's own `environment` from the Compose file. **The channel's value wins** for the same name. The file itself is never edited.
4. A bare `KEY` in the file's `environment` takes the channel's value for it, so a file can leave a setting for the channel to supply.
5. Only `environment` can be set this way, and every service named in the channel's `environment` must exist in the Compose file.
6. `${UNITYSVC_INSTANCE_API_KEY}` is the per-instance key the platform generates; use it as a value (for example `API_KEY: "${UNITYSVC_INSTANCE_API_KEY}"`) for an app that checks a bearer key. Other `${VAR}` references are kept as written and are not bound to anything, so do not rely on them for secrets. The old Document `meta.environment` form is not used by this catalog.

The values from your file's own `environment` are the defaults when a channel does not set them. Local Docker tests use each parameter's `testing_defaults` so a check needs no one to fill in the form.

### Pricing: fixed by policy

Every recipe has `{"list_price": {"type": "base_cost"}}` in its listing and `{"payout_price": {"type": "constant", "price": "0"}}` in its offering. Do not write dollar prices, markups, surcharges or a nonzero or missing payout. The platform charges its published compute cost for the size you choose. See [Catalog pricing policy](README.md#catalog-pricing-policy).

### Parameters and secrets

- Keep the Compose file literal. Put `{{ params.NAME }}` bindings in the channel's `environment` map and declare each parameter under the channel's `params.schema` with a description, validation and a safe default or generated token.
- Add `testing_defaults` so the checks can run the recipe without a person filling in the form.
- Say which settings are required and what a change does to a running instance.
- Do not put credentials in Compose, and do not ship a fixed password or token that every customer would share. Generate one per enrollment or let the customer supply it.

### Choosing a size

Look at the [compute sizes](https://unitysvc.com/docs/sizes) and pick the smallest one the software actually runs well on, based on its documented minimums and what you observe at startup and under a demo load. Account for every service in a stack. Local Docker limits are not the platform's size limits, so a recipe that starts locally can still not fit the size you chose; say how you checked.

### Tests

Use the standard `container_connectivity` preset from `unitysvc-data` for the connectivity test.

## Check your work

Install the current `unitysvc-sellers` CLI with `unitysvc-core>=0.3.19`, then:

```bash
usvc_seller specs validate
usvc_seller specs format --check services
python scripts/check_channel_binding.py
```

Local container checks need Docker. Never upload, publish or merge from your own environment; Labs does that after review.

## The PR

Fill in the PR template. Reviewers check the license, the attribution, the size choice, that pricing is the standard pair above, and that the recipe starts and answers its connectivity test.
