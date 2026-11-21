# UnitySVC Open Source Catalog

Let people run your open-source project on their own private [UnitySVC](https://unitysvc.com) instance, for a quick try or for long-term use. Contribute a container recipe; [UnitySVC Labs](https://github.com/unitysvc-labs) reviews it, and customers pay the platform compute cost while they run it.

This repository is the catalog of those recipes. Each one is a small, reviewed set of files (a Compose file, enrollment parameters and a guide) that UnitySVC turns into a private container for every customer who enrolls.

## Services

| Service | What it provides | Definition |
| --- | --- | --- |
| `binwiederhier/ntfy-sh` | A private ntfy container for each enrollment, with ntfy access-token authentication | [Container service](services/specs/binwiederhier/ntfy-sh), [setup and operation](docs/ntfy.md) |
| `kadxy/weixin-ilink-gateway` | A private Weixin iLink gateway per enrollment, with QR login, messaging, media and webhooks | [Container service](services/specs/kadxy/weixin-ilink-gateway), [setup and operation](services/specs/kadxy/weixin-ilink-gateway/usage.md) |

Notification integrations, including `labs/msg-to-ntfy`, `labs/msg-to-weixin` and `labs/weixin-to-msg`, remain in [unitysvc-services-notify](https://github.com/unitysvc-labs/unitysvc-services-notify).

## For customers

1. Find the published service in the UnitySVC catalog.
2. Enroll and choose a channel and size.
3. Configure the parameters.
4. Start the instance and use the software, for a quick try or for as long as you need it.
5. **Stop the instance when you are done.** Closing a browser tab does not stop it.

Stopping or replacing an instance discards its temporary storage, so messages, logins and caches kept inside it are lost. Each service's guide lists what it keeps and what it does not.

### What it costs

You pay the platform's published compute base cost for your running instance. UnitySVC Labs adds no margin and receives no seller payout. A `nano` instance costs about $3 a month, so:

| Use | Approximate cost |
| --- | --- |
| One-hour trial | under 1¢ |
| Left running for a day | about 10¢ |
| Left running for a month | about $3 |
| A $5 top-up | over 1,000 one-hour trials |

Stopping the instance stops the charge. See the [compute sizes and rates](https://unitysvc.com/docs/sizes) for the current figures; they follow the platform's rules and can change. The base cost is the published platform charge, not a claim that cloud infrastructure is free or billed at a third-party provider's price.

A run keeps the price it had when it started. A new price applies the next time an instance starts, and a running instance is never restarted or re-priced because of a catalog change.

## For authors

There are three ways to put your software in front of customers. They differ in who owns the listing and who can earn money.

| Route | Publishing and approval | Pricing and payout | Additional services |
| --- | --- | --- | --- |
| **1. Contribute a recipe to this catalog** | Open a PR. Labs reviews, approves and publishes it under its seller account. You need no seller account and no infrastructure. | Platform compute base cost only; no Labs margin and no payout to you. | The contribution is the demo recipe. You cannot attach your own services or paid support to Labs' listing. |
| **2. Become a Developer-tier seller** | You own the seller account and publish from your own repository. Services go live automatically when their tests and the Developer policy checks pass. No catalog PR is needed. | At cost only; you cannot set a markup and receive no payout. | You can publish your own container services and talk to customers through [Rooms](https://github.com/unitysvc/unitysvc-sellers/blob/main/docs/seller-lifecycle.md). Paid services need route 3. |
| **3. Become a seller with payout options** | You complete seller and payout onboarding and maintain your own catalog. | You set commercial prices under platform rules and can receive payouts. | You can sell a premium edition, managed service and support, using Rooms to talk to customers. |

See [Getting started](https://github.com/unitysvc/unitysvc-sellers/blob/main/docs/getting-started.md) and [After you publish](https://github.com/unitysvc/unitysvc-sellers/blob/main/docs/seller-lifecycle.md) for routes 2 and 3. Labs sells no extras on these recipes and promises no support from the upstream author.

### Contribute a recipe (route 1)

The recommended way is to ask your coding assistant (Claude Code, Codex, Qoder, Qwen, DeepSeek or similar) to do it: [CONTRIBUTING.md](CONTRIBUTING.md#the-recommended-way-ask-your-coding-assistant) has a prompt to fill in and paste. To do it by hand:

1. Pick an upstream project and its container image.
2. Add the source and license attribution, the Compose file, enrollment parameters, size choice and tests under `services/specs/<provider>/<project>/`.
3. Open a PR. Automatic checks run, then Labs reviews.
4. After the merge, Labs publishes the service through the normal platform process.

You do not need seller credentials or a pre-existing backend service ID: the platform creates the identity for a new service when Labs publishes it. [CONTRIBUTING.md](CONTRIBUTING.md) has the details, and the PR template lists what a reviewer will check.

Community-maintained recipes are welcome as well as submissions from the upstream author. A community recipe is marked as unofficial unless the author has taken part; a public repository or email address is not evidence of the author's endorsement, and Labs does not claim that the author supports the demo.

## Layout

```text
services/
  specs/binwiederhier/ntfy-sh/       private ntfy instance, Compose file and guides
  specs/kadxy/weixin-ilink-gateway/  private Weixin gateway, Compose file and guide
  seller.secrets.txt               seller-secret manifest (none currently needed)
scripts/
  generate_ntfy_params.py           regenerate ntfy environment parameters
  check_channel_binding.py          check credential and enrollment binding
docs/ntfy.md                        container service guide
```

Keep each provider's identity and service name independent of this repository's name. Commit the backend-written `service.json` / `*.service.json` sidecar so moving files or adding services does not create a new marketplace identity.

## Validate and test

Install the current `unitysvc-sellers` CLI with `unitysvc-core>=0.3.19` and `unitysvc-data>=0.2.17`, then run from the repository root:

```bash
usvc_seller specs validate --has-service-id
usvc_seller specs format --check services
python scripts/check_channel_binding.py
```

Local container tests need Docker. Use `usvc_seller specs run-tests kadxy/weixin-ilink-gateway --force` or the commands in [the ntfy guide](docs/ntfy.md). Both services use enrollment parameters for application credentials; neither requires seller-secret defaults. Configure real seller/customer credentials for tests against UnitySVC.

Known tooling limitation: the local container-test runner in `unitysvc-sellers` 0.3.24 still follows the older Document-environment path and does not bind a channel's `testing_defaults` or the named sizes ([unitysvc-sellers#240](https://github.com/unitysvc/unitysvc-sellers/issues/240)). Until that is fixed, a local Docker check is evidence about the container, not about the platform's size limits. Direct Docker checks passed for both services at migration: ntfy covered health, anonymous-access refusal, and token-authenticated publish/subscribe; Weixin covered health, `/console`, rejection of absent/incorrect API keys, and authenticated `/status` without logging into a Weixin account.

CI uses UnitySVC Labs' shared validation, formatting and upload workflows. Staging uploads are manual; production uploads run manually or after a pull request merges. Configure seller API credentials through GitHub Actions secrets.

## Catalog pricing policy

Every service in this catalog has the same two commercial settings, and nothing else:

```json
// listing.json
{"list_price": {"type": "base_cost"}}
// offering.json
{"payout_price": {"type": "constant", "price": "0"}}
```

A bare `base_cost` list price makes the platform charge its published compute cost for the channel's size, with no markup, fixed dollar amount or per-request surcharge, and the explicit zero payout makes Labs earn nothing. A missing payout would default to the whole charge, so it is always written out. Do not write dollar prices or size limits in this repository; the platform owns them. Different channels can use different sizes and parameters and still resolve to their own platform cost.

## Adding a service

Follow [CONTRIBUTING.md](CONTRIBUTING.md).

## Migration

This repository continues the history of `unitysvc-labs/unitysvc-services-ntfy`, renamed to serve the whole compute catalog. The `kadxy/weixin-ilink-gateway` definition moved here from [unitysvc-services-notify](https://github.com/unitysvc-labs/unitysvc-services-notify), preserving its existing service ID. The ntfy notification integration remains in that catalog.
