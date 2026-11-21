# Maintaining the catalog

Contributor instructions are in [CONTRIBUTING.md](../CONTRIBUTING.md). This guide covers Labs' publication work.

## Layout and identity

Service definitions live in `services/specs/<provider>/<project>/`. Keep names and backend-written identity sidecars when moving files. Record new IDs after ingest through a PR; contributors do not need an ID before their first submission.

`scripts/generate_ntfy_params.py` regenerates ntfy's environment parameters. The detailed ntfy maintenance notes are in [ntfy.md](ntfy.md). Notification integrations, including `labs/msg-to-ntfy`, `labs/msg-to-weixin` and `labs/weixin-to-msg`, remain in [unitysvc-services-notify](https://github.com/unitysvc-labs/unitysvc-services-notify).

## Checks and publication

Run the [contributor checks](../CONTRIBUTING.md#check-your-work) first. For an already published catalog, also run `usvc_seller specs validate --has-service-id` to check the recorded identities. Do not require that flag for new contributor recipes.

The current v0.3.24 container runner has a [channel-parameter compatibility issue](https://github.com/unitysvc/unitysvc-sellers/issues/240). Manual Docker evidence must identify the parameter values and checks used; it does not establish platform size fit. At migration, manual checks verified ntfy's token-authenticated publish/subscribe and Weixin's health and application-key handling.

CI currently runs schema, format and channel-binding checks. Staging uploads are manual; production uploads run manually or after a PR merges. Labs configures seller credentials through Actions secrets. New PR runtime testing and publication improvements are planned in [the catalog design](https://github.com/unitysvc/unitysvc-llc/issues/81); they are not implemented by this documentation change.

Each application's keys and tokens are enrollment parameters with appropriate defaults. UnitySVC does not supply built-in instance credentials or add an application authentication gate.

## Repository history

The catalog retains the history of the former `unitysvc-labs/unitysvc-services-ntfy` repository. A pre-migration snapshot is [archived under bo-unitysvc](https://github.com/bo-unitysvc/unitysvc-services-ntfy). The Weixin compute recipe moved here from the notification catalog with its service ID preserved.
