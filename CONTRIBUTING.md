# Contributing a recipe

You need no seller account, seller credentials, hosting infrastructure or backend service ID. Submit a PR; Labs reviews and publishes the recipe. To publish independently or earn revenue, see the [author options](README.md#for-authors).

## Before you start

- **License:** use an OSI-approved open-source license, with its SPDX identifier and a link to the upstream license. Ask Labs about exceptions.
- **Image:** use the project's documented container image for the platform's supported architecture. Identify the version you tested; a digest pins the exact image.
- **Attribution:** credit the software author as provider. Use published contact details only; flag missing details for review. State whether you are the author or a community contributor, and do not imply unconfirmed author endorsement or support.

## Ask your coding assistant

Fill in this prompt in a workspace where your assistant can fork repositories and open PRs:

```text
Add <PROJECT NAME> from <UPSTREAM PROJECT URL> to
https://github.com/unitysvc-labs/open-source-catalog.
I am <the author | a community contributor>.
Optional documentation/image page: <URL>.
Optional upstream Compose file: <URL>.
Optional use case: <WHAT CUSTOMERS SHOULD BE ABLE TO DO>.

Fork the repo, create a branch, and read README.md, CONTRIBUTING.md and
docs/container-recipes.md. Read the upstream README, docs, license and image
page to write the descriptions, settings and usage guide. Reuse a compatible
upstream Compose file through a commit permalink where possible. Ask me about
missing facts instead of guessing.
Use the existing recipes as structural examples, not authentication templates.

Follow the catalog's pricing, attribution, capability, parameter and testing requirements.
Document the size choice, application authentication, first-use steps and
shutdown/storage behavior. All application keys and tokens are parameters with
defaults where appropriate; UnitySVC supplies no built-in instance key or
application authentication gate.

Run the checks below and collect local Docker evidence where possible. Open a
PR with the template filled in. Do not add or edit service identity sidecars,
upload services, publish or merge.
```

Review the proposed recipe and test results before submitting it.

## What to add

Start with [`services/specs/kadxy/weixin-ilink-gateway`](services/specs/kadxy/weixin-ilink-gateway) as a structural example. Add `services/specs/<provider>/<project>/` with:

| File | Contents |
| --- | --- |
| `provider.json` | Software author, homepage and license/contact references |
| `offering.json` | Marketplace summary and description, container channels, parameters, environment bindings, sizes, entries and zero payout |
| `listing.json` | Customer-facing name, `base_cost` price, documents and the `container_connectivity` preset |
| `compose.yaml` | The offering's instance spec, or use an upstream commit-pinned URL |
| `usage.md` | Setup, authentication, a first-use example, cost, stopping and storage limitations |

Do not add a `service.json` for a new recipe or edit an existing identity sidecar. Labs records the backend-generated ID after publication.

### Names and marketplace copy

| Field | What to write |
| --- | --- |
| `listing.name` | `<provider>/<software_name>`, matching the path under `services/specs/`. Prefer the upstream owner/project names for new recipes; keep published service names stable. |
| `offering.name` | The bare `<software_name>`, without the provider prefix. |
| `display_name` | A descriptive, human-readable name for the container service, up to 200 characters. Set it in the listing; it can fall back to the offering's display name. |
| `offering.summary` | A one-line description of what the service provides, **at most 200 characters**. It appears in catalog previews and is included in frontend search. |
| `offering.description` | Longer customer-facing detail that expands on the summary. Do not repeat the summary as a teaser paragraph. |

The description usually needs two or three short paragraphs, separated by `\n\n`:

1. Explain what this service does in detail: the software it runs, how requests or data flow, and relevant features and limitations.
2. Explain how to use it: available channels, the instance URL or entry, required parameters and defaults. Refer to **How to use this service** for full setup.
3. Explain pricing and support where useful: runtime charges at `base_cost`, no Labs markup or seller payout, and where to find software-specific help. Do not promise author support unless the author has agreed to provide it.

This is a content guide, not a fixed paragraph count. The separate `summary` field carries the catalog teaser; `description` has no 200-character limit.

### Capabilities

Declare what the software does in `offering.json`'s `capabilities` array. Use a
bare [official capability ID](https://github.com/unitysvc/unitysvc-sellers/blob/main/docs/file-schemas.md#capabilities)
only when its documented input/output contract fits, such as `notification-relay`.
Unknown bare names are rejected. `container` describes how the service runs;
it is not a capability.

When no official capability fits, write `name | annotation`:

```json
{
  "capabilities": [
    "text-to-pdf | Converts uploaded UTF-8 text into a PDF document."
  ]
}
```

The frontend shows `text-to-pdf` as the capability badge and its annotation on
hover, marked as described by the seller. Choose a short, lower-case hyphenated
name and explain the input, result and important limits. This is a seller claim,
not a platform verification; an annotation does not inherit an official routing
contract even if its name matches one. Filters match the full entry, so use
consistent wording.

Names are limited to 64 characters, annotations to 500, and an offering to 32
entries. Newlines and control characters are not allowed. Describe only actions
the application actually supports, rather than marketing claims or deployment
features.

### Shared container guide

Every container listing includes the common guide from `unitysvc-data`, alongside
its application-specific `usage.md`:

```json
{
  "documents": {
    "Using container services": {"$doc_preset": "container_description"},
    "How to use this service": {
      "category": "getting_started",
      "file_path": "usage.md",
      "is_public": true,
      "mime_type": "markdown"
    }
  }
}
```

The shared guide covers enrollment, instance access, runtime charges and stopping.
Keep software-specific login, first-use steps and limitations in the application's
own guide. Include the `container_connectivity` test document as well.

### Parameters and authentication

Declare settings under each channel's `params.schema` and bind them in its `environment` map using `{{ params.NAME }}`. Supply descriptions, validation, appropriate defaults and `testing_defaults`. Keep Compose literal; parameter references belong in the channel, not the Compose file.

All application tokens, keys and passwords come from these parameters. A parameter default such as `{{ token_urlsafe(32) }}` can generate a value for the enrollment; the customer can keep it or supply their own. Authentication is the application's responsibility: UnitySVC adds no application security gate or built-in instance-key variable. Do not ship a usable credential shared by all customers.

Recipes need no `.env.example`, `.env` file or seller-secret manifest. Do not load a seller environment or use `${ customer_secrets.* }` for container settings. Declare those settings as channel parameters and bind them to the container's environment. For local Docker checks, pass explicit test values; customers supply any external-provider credentials their application needs when enrolling.

The [container reference](docs/container-recipes.md#parameters-and-environment) shows a complete parameter-binding example. Explain which settings are required and whether changing them restarts the instance.

### Pricing

In `listing.json`:

```json
{"list_price": {"type": "base_cost"}}
```

In `offering.json`:

```json
{"payout_price": {"type": "constant", "price": "0"}}
```

Do not add fixed dollar prices, markups, surcharges or other payouts. The platform resolves `base_cost` from the selected channel's size.

### Sizes and channels

Choose the smallest suitable size from the [current size table](https://unitysvc.com/docs/sizes), based on upstream requirements and observed startup and intended workload. Account for every container in a stack. You can offer several channels with different sizes and parameter defaults; all use the offering's one instance spec. See [sizes and channels](docs/container-recipes.md#sizes-and-channels).

## Check your work

These checks need no seller account, seller credentials or seller-provided secrets.

Install `unitysvc-sellers` with `unitysvc-core>=0.3.20` and `unitysvc-data>=0.2.18`. From the repository root, run:

```bash
usvc_seller specs validate
usvc_seller specs format --check services
python scripts/check_channel_binding.py
```

Use the `container_connectivity` preset and test startup, readiness and application authentication with Docker. Include commands, configuration and results in the PR, with credentials redacted.

The v0.3.24 CLI runner does not bind channel parameters or `testing_defaults` correctly ([#240](https://github.com/unitysvc/unitysvc-sellers/issues/240)). Until fixed, supply test parameter values explicitly for your manual Docker check and report any tooling failure separately. Starting locally does not prove the chosen platform size fits.

Fill in the PR template. Labs reviews the recipe and publishes it through the platform lifecycle after merge; contributors do not upload or publish services.
