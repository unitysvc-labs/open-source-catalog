# CLAUDE.md — open-source-catalog

This repository is the **UnitySVC Open Source Catalog**: container recipes for
open-source software. UnitySVC Labs is the seller; the software author is the
provider. Contributors submit PRs without becoming sellers.

Read [README.md](README.md), [CONTRIBUTING.md](CONTRIBUTING.md) and the
[container reference](docs/container-recipes.md) before editing a recipe.
The [unitysvc-sellers docs](https://github.com/unitysvc/unitysvc-sellers/tree/main/docs)
define the service-data format; these files define catalog-specific requirements.

## Recipe layout and names

Add `services/specs/<provider>/<software_name>/` with `provider.json`,
`offering.json`, `listing.json`, an application `usage.md`, and either a local
`compose.yaml` or an upstream commit-pinned Compose URL. Keep published names
stable. Do not add or edit backend-written `service.json` identity sidecars; the Test Recipes workflow commits a new recipe's to the pull request.

- `listing.name`: `<provider>/<software_name>`, matching the catalog path.
- `offering.name`: the bare `<software_name>`.
- `display_name`: a descriptive, human-readable name for the container service,
  up to 200 characters. The listing can override the offering's display name.
- `offering.summary`: a required one-line catalog teaser, **at most 200
  characters**, also used by frontend search.
- `offering.description`: details beyond the summary. Start with what the
  service does in depth, then explain how to use it (channels, instance access
  and parameters), and cover pricing/support where useful. Point to **How to
  use this service** for full setup. Usually two or three paragraphs suffice;
  separate them with `\n\n`. There is no fixed paragraph count or 200-character
  description limit. Do not repeat the summary as a teaser paragraph.

See [names and marketplace copy](CONTRIBUTING.md#names-and-marketplace-copy).

## Channels, parameters, environment and compute sizes

Declare container channels under `offering.upstream_access_config`. Every
channel uses `access_method: container` and has its **own**:

- `params.schema`: enrollment settings, descriptions, validation and appropriate
  defaults; `params.testing_defaults` supplies sample values for test tooling.
- `environment`: per-container environment variables bound to that channel's
  parameters with `{{ params.NAME }}`. Container names must match Compose services.
- `resources`: a named compute size for one container (for example `nano`), or a
  complete per-service map such as `{"web": "small", "redis": "nano"}` for a stack.
  Choose suitable active sizes from the [size table](https://unitysvc.com/docs/sizes)
  using upstream requirements and measured startup/workload needs.

All channels share the offering's **one Compose instance spec**. Offer different
channels for different compute sizes, parameters/defaults or environment values;
declare each channel's settings explicitly. Use a separate recipe for a different
stack. See [sizes and channels](docs/container-recipes.md#sizes-and-channels).

In a stack, declare `ports` on every service another service connects to (a database's `5432`, a cache's `6379`): a service without ports has no name inside the instance and its ports are closed to its siblings, although Docker Compose lets it work. See [stacks](docs/container-recipes.md#stacks-services-that-talk-to-each-other).

Keep Compose literal. Bind configurable application settings through channel
parameters and `environment`; do not rely on Compose `${VAR}` interpolation,
`.env` files, `.env.example`, `env_file`, a seller-secret manifest, or
`${ customer_secrets.* }` for container configuration.

Application keys, tokens and passwords are parameters too. Defaults can generate
application credentials where appropriate; customers supply external-provider
credentials their application needs. Authentication belongs to the application:
UnitySVC adds no application security gate or built-in instance-key variable.
See [parameters and environment](docs/container-recipes.md#parameters-and-environment).

## Catalog requirements

- Use an OSI-approved open-source license and documented container image; credit
  the author as provider without inventing contact details or implying endorsement
  or promised support. Identify the tested image version; prefer a digest to pin it.
- Every listing uses `{"list_price": {"type": "base_cost"}}`; every offering uses
  `{"payout_price": {"type": "constant", "price": "0"}}`. Labs adds no markup and
  receives no seller payout.
- Capabilities are matching official IDs or `name | annotation`. The frontend
  shows the name as a badge and the annotation on hover, as a seller claim.
  Follow the [capability contract and limits](CONTRIBUTING.md#capabilities).
- Include a `container_connectivity` test preset and the shared public guide
  `"Using container services": {"$doc_preset": "container_description"}`
  (`unitysvc-data>=0.2.18`) in every container listing.
- Include the application's own **How to use this service** document, covering
  setup, authentication, first use, runtime cost, stopping and temporary storage.

## Local checks require no seller credentials

Install `unitysvc-sellers` with `unitysvc-core>=0.3.20` and
`unitysvc-data>=0.2.18`, then run from the repository root:

```bash
usvc_seller specs validate
usvc_seller specs format --check services
python scripts/check_channel_binding.py
```

Do not source a seller environment or create an environment example/secret
manifest. These checks need no seller account, API key or seller-provided secrets.
For local Docker checks, supply explicit test parameter values and record startup,
readiness and authentication results, with credentials redacted. The current CLI
runner's parameter-binding limitation is documented in the
[contribution checks](CONTRIBUTING.md#check-your-work). Local Docker evidence does
not prove the platform's named size fits.

## Publication belongs to Labs maintainers

Contributors open PRs; they do not upload to staging/production, change service
status, publish or merge as part of recipe development. Labs' protected workflows
hold publication credentials. Maintainers preserve service identities and record
new backend IDs through PRs after publication.

See [the maintainer guide](docs/maintaining.md) for publication and identity work.
Notification integrations remain in
[`unitysvc-services-notify`](https://github.com/unitysvc-labs/unitysvc-services-notify).
