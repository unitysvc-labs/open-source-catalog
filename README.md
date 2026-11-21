# UnitySVC Labs compute services

The catalog for compute services published by [UnitySVC Labs](https://github.com/unitysvc-labs). Add new container-backed services here, under `services/specs/<provider>/<service>/`.

## Services

| Service | What it provides | Definition |
| --- | --- | --- |
| `binwiederhier/ntfy-sh` | A private ntfy container for each enrollment, with ntfy access-token authentication | [Container service](services/specs/binwiederhier/ntfy-sh), [setup and operation](docs/ntfy.md) |
| `labs/msg-to-ntfy` | Gateway delivery of the unified `msg` envelope to an ntfy destination, including ntfy.sh or a private instance | [Service parameters](services/specs/labs/msg-to-ntfy.json) |

The gateway companion uses the local `services/templates/msg-to-channel/` template. Both services retain their existing names, prices, documents and backend service IDs.

## Layout

```text
services/
  specs/binwiederhier/ntfy-sh/   private ntfy instance, Compose file and guides
  specs/labs/msg-to-ntfy.json    gateway companion parameters
  templates/msg-to-channel/     gateway companion template
  seller.secrets.txt           documented mock/test secret defaults
scripts/
  generate_ntfy_params.py       regenerate ntfy environment parameters
  check_channel_binding.py      check credential and enrollment binding
docs/ntfy.md                    container service guide
```

Keep each provider's identity and service name independent of this repository's name. Commit the backend-written `service.json` / `*.service.json` sidecar so moving files or adding services does not create a new marketplace identity.

## Validate and test

Install the current `unitysvc-sellers` CLI with `unitysvc-core>=0.3.19` and `unitysvc-data>=0.2.17`, then run from the repository root:

```bash
usvc_seller specs validate --has-service-id
usvc_seller specs format --check services
python scripts/check_channel_binding.py
```

For local upstream tests, load `services/seller.secrets.txt` and use the commands in [the ntfy guide](docs/ntfy.md). Its values are mock defaults; configure real seller/customer credentials for the environment being tested. The ntfy container test needs Docker.

Known tooling limitation at migration: `unitysvc-sellers` 0.3.23 with core 0.3.19 raises `validate_instance_spec() got an unexpected keyword argument 'environment'` in its local container-test runner. Direct Docker verification passed with the committed environment defaults, including health, anonymous-access refusal, and token-authenticated publish/subscribe. Both gateway companion connectivity probes also passed.

CI uses UnitySVC Labs' shared validation, formatting and upload workflows. Staging uploads are manual; production uploads run manually or after a pull request merges. Configure seller API credentials through GitHub Actions secrets.

## Adding a compute service

1. Add a provider, offering, listing and restricted Compose specification under `services/specs/<provider>/<service>/` (or use the standard template/parameter layout).
2. Credit the software's author as provider and declare its license, resource sizes, enrollment parameters, price and application authentication.
3. Use `unitysvc-data` presets for connectivity tests and keep public setup documentation beside the service.
4. Validate and format, test locally and on staging, then commit the identity sidecar written by upload.

## Migration

This repository continues the history of `unitysvc-labs/unitysvc-services-ntfy`, renamed to serve the whole compute catalog. The `labs/msg-to-ntfy` definition and its required template/test defaults moved from [unitysvc-services-notify](https://github.com/unitysvc-labs/unitysvc-services-notify). Notification services for other destinations remain in that catalog.
