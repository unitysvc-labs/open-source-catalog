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

`.github/workflows/test-recipes.yml` judges a pull request before it is merged, so a recipe the platform rejects is found there and not in a second pull request that repairs the first. It is the production upload, run on the pull request:

1. The three validation workflows (data, format, channel binding) run first; nothing is uploaded unless they pass.
2. It uploads the recipes whose expanded content changed (`specs upload --submit --state`, against the upload state of the last production upload, the comparison the merge upload uses). A failed upload fails the check.
3. A new recipe gets its `service.json` committed to the pull request's branch.
4. It waits (up to 40 minutes) for the platform's activation tests to decide each uploaded service. `active` or `review` passes; `rejected`, or no decision in time, fails. A change to a live service is a pending revision, and its status is the one read. The report (`recipe-test-report.md`) is in the step summary and kept as an artifact.

- It does not publish. Visibility is set only by "Upload Data to Production" on merge. A recipe that passes is left in review or active; one that fails is left rejected.
- The pull request's working copy of the upload state is not saved, so the merge upload still sends the recipes.
- The tests need a cluster that takes `test` work (`usvc_admin clusters set-placement`); the external cluster is the intended one.
- Seller credentials are needed, so a fork's pull request is not tested automatically. A maintainer runs **Test Recipes** by hand on the reviewed commit; that run commits no sidecar.
- Runs are serialized (one concurrency group), because they share the production seller account.
- A pull request closed without merging leaves its services in review or rejected; nothing removes them yet.

## Repository history

The catalog retains the history of the former `unitysvc-labs/unitysvc-services-ntfy` repository. A pre-migration snapshot is [archived under bo-unitysvc](https://github.com/bo-unitysvc/unitysvc-services-ntfy). The Weixin compute recipe moved here from the notification catalog with its service ID preserved.
