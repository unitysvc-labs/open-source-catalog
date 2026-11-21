# Contributing a recipe

A recipe is the set of files that lets UnitySVC run an open-source project as a private container for each customer who enrolls. You do not need a seller account, seller credentials, infrastructure or a backend service ID to contribute one. Open a PR; Labs reviews it and publishes it.

Not sure this is the right route? See [For authors](README.md#for-authors) for the Developer-seller and commercial-seller alternatives.

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
| `compose.yaml` | The Compose file: portable, literal values only |
| `usage.md` | How to use the service: setup, authentication, a demo step, what it costs and how to stop it, and what is lost when the instance stops |

Use [`services/specs/kadxy/weixin-ilink-gateway`](services/specs/kadxy/weixin-ilink-gateway) as the smallest complete reference recipe. Do not add a `service.json`: the platform creates a new service's identity. Never edit an existing one.

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
