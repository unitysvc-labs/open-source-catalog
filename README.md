# UnitySVC Labs compute services

The catalog for compute services published by [UnitySVC Labs](https://github.com/unitysvc-labs). Add new container-backed services here, under `services/specs/<provider>/<service>/`.

## Services

| Service | What it provides | Definition |
| --- | --- | --- |
| `binwiederhier/ntfy-sh` | A private ntfy container for each enrollment, with ntfy access-token authentication | [Container service](services/specs/binwiederhier/ntfy-sh), [setup and operation](docs/ntfy.md) |
| `kadxy/weixin-ilink-gateway` | A private Weixin iLink gateway per enrollment, with QR login, messaging, media and webhooks | [Container service](services/specs/kadxy/weixin-ilink-gateway), [setup and operation](services/specs/kadxy/weixin-ilink-gateway/usage.md) |

Both services retain their existing names, prices, documents and backend service IDs. Notification integrations, including `labs/msg-to-ntfy`, `labs/msg-to-weixin` and `labs/weixin-to-msg`, remain in [unitysvc-services-notify](https://github.com/unitysvc-labs/unitysvc-services-notify).

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

Known tooling limitation at migration: `unitysvc-sellers` 0.3.23 with core 0.3.19 raises `validate_instance_spec() got an unexpected keyword argument 'environment'` in its local container-test runner. Direct Docker checks passed for both services: ntfy covered health, anonymous-access refusal, and token-authenticated publish/subscribe; Weixin covered health, `/console`, rejection of absent/incorrect API keys, and authenticated `/status` without logging into a Weixin account.

CI uses UnitySVC Labs' shared validation, formatting and upload workflows. Staging uploads are manual; production uploads run manually or after a pull request merges. Configure seller API credentials through GitHub Actions secrets.

## Adding a compute service

1. Add a provider, offering, listing and restricted Compose specification under `services/specs/<provider>/<service>/` (or use the standard template/parameter layout).
2. Credit the software's author as provider and declare its license, resource sizes, enrollment parameters, price and application authentication.
3. Use `unitysvc-data` presets for connectivity tests and keep public setup documentation beside the service.
4. Validate and format, test locally and on staging, then commit the identity sidecar written by upload.

## Migration

This repository continues the history of `unitysvc-labs/unitysvc-services-ntfy`, renamed to serve the whole compute catalog. The `kadxy/weixin-ilink-gateway` definition moved here from [unitysvc-services-notify](https://github.com/unitysvc-labs/unitysvc-services-notify), preserving its existing service ID. The ntfy notification integration remains in that catalog.
