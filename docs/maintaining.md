# Maintaining the catalog

Contributor instructions are in [CONTRIBUTING.md](../CONTRIBUTING.md). This guide covers Labs' publication work.

## Layout and identity

Service definitions live in `services/specs/<provider>/<project>/`. Keep names and backend-written identity sidecars when moving files. Record new IDs after ingest through a PR; contributors do not need an ID before their first submission.

`scripts/generate_ntfy_params.py` regenerates ntfy's environment parameters. The detailed ntfy maintenance notes are in [ntfy.md](ntfy.md). Notification integrations, including `labs/msg-to-ntfy`, `labs/msg-to-weixin` and `labs/weixin-to-msg`, remain in [unitysvc-services-notify](https://github.com/unitysvc-labs/unitysvc-services-notify).

## Checks and publication

Run the [contributor checks](../CONTRIBUTING.md#check-your-work) first. For an already published catalog, also run `usvc_seller specs validate --has-service-id` to check the recorded identities. Do not require that flag for new contributor recipes.

The current v0.3.24 container runner has a [channel-parameter compatibility issue](https://github.com/unitysvc/unitysvc-sellers/issues/240). Manual Docker evidence must identify the parameter values and checks used; it does not establish platform size fit. At migration, manual checks verified ntfy's token-authenticated publish/subscribe and Weixin's health and application-key handling.

CI currently runs schema, format and channel-binding checks. Staging uploads are manual; production uploads run manually or after a PR merges. Labs configures seller credentials through Actions secrets. New PR runtime testing and publication improvements are planned in [the catalog design](https://github.com/unitysvc/unitysvc-llc/issues/81); they are not implemented by this documentation change.

Publication credentials belong to Labs' protected workflows. Contributors do not need them for local validation or recipe development. Recipes carry no `.env.example`, `.env` file or seller-secret manifest; application settings and credentials are enrollment parameters bound to container environment variables.

Each application's keys and tokens are enrollment parameters with appropriate defaults. UnitySVC does not supply built-in instance credentials or add an application authentication gate.

## Testing a pull request on the platform

`.github/workflows/test-recipes.yml` runs for every pull request from a branch of this repository. It uploads to production the ones whose expanded content changed (`specs upload --state`, against the upload state of the last production upload, so the comparison is the one the merge upload uses), and runs the platform's own check on each with `services run-tests`: the platform starts the recipe's container for the service's ops enrollment on a cluster that takes `test` work, fetches its entries over HTTPS and stops it. An image that cannot be pulled, a container that does not start, or an entry that does not answer fails the check.

- The recipes are uploaded, not published: they are not submitted for review or made visible, and the pull request's working copy of the state is not saved, so the merge upload still sends them. A recipe that already exists gets a pending revision.
- The ops enrollment stays active; only the instance is stopped after the check.
- At least one cluster must take `test` placement (`usvc_admin clusters set-placement`); the external cluster is the intended one. With none, the check fails as a platform fault.
- Seller credentials are needed, so a fork's pull request is not tested automatically. A maintainer runs **Test Recipes** by hand on the reviewed commit.
- Runs are serialized (one concurrency group), because they share the production seller account and one test instance per service.

## Repository history

The catalog retains the history of the former `unitysvc-labs/unitysvc-services-ntfy` repository. A pre-migration snapshot is [archived under bo-unitysvc](https://github.com/bo-unitysvc/unitysvc-services-ntfy). The Weixin compute recipe moved here from the notification catalog with its service ID preserved.
