# Docmost Collaborative Knowledge Base

This unofficial community recipe runs the upstream `docmost/docmost:0.98.0` image, pinned by digest. The community core is published under [AGPL-3.0](https://github.com/docmost/docmost/blob/main/LICENSE); the official image also includes separately licensed Enterprise code. No author endorsement or support commitment is implied.

## Create your workspace

1. Enroll in **base**, approve `docmost/` home access and save the database password and application secret. This stack uses an application container, PostgreSQL and Valkey; all three incur runtime cost.
2. Set **Public address** to the HTTPS address shown in instance details and save, then open it immediately. The first visitor can create the workspace and owner. There is no pre-created account or platform authentication gate. Complete setup before sharing the URL.
3. Create a page, add text and an attachment, reload it, then invite other users through the workspace controls. With no SMTP service, do not depend on invitation emails or password-reset email; use available application-generated links. Preserve the owner password separately.
4. The community core is AGPL-3.0. The upstream image bundles Enterprise code under separate terms; this recipe supplies community functionality and no paid-feature entitlement. Do not assume SSO, Enterprise MFA, audit or paid features are included.

## Persisted content

Pages, workspaces and users live in the PostgreSQL dump under `docmost/db-backup/`; attachments live in `docmost/uploads/`. Both are needed. Deleted attachment files can return as orphan files after a restart because the platform copy never deletes. A new enrollment gets a new address, so update Public address and distributed links. Application login protects private content; the sign-in and setup pages are public.

## Database backup and restart behavior

PostgreSQL's live directory is scratch. A compressed dump is persisted in the home folder every five minutes and on SIGTERM. A fresh scratch directory restores the dump before the database opens its network port. A crash can lose up to five minutes of database changes. The dump must remain below the platform's 1 GiB single-file limit. Keep the database credential and application secrets across re-enrollment, and keep independent exports of important content. Redis/Valkey is a scratch cache/task broker; queued background work is not durable across an instance replacement. Finish uploads and processing before stopping.

## Storage and stopping

Stop the instance from UnitySVC when finished; closing the browser does not stop billing. Only one active enrollment per customer uses this recipe's home folder. Do not run another instance against that folder or edit it while this instance runs.

The platform restores persisted files before startup, copies changed files about every 30 seconds, and makes a final copy on a normal stop. A crash can lose recent changes. Copies add and replace files; they never delete. Deleted files may return on a later start. Empty files, symbolic links and individual files over 1 GiB are not stored. Nothing removes the home folder when you cancel enrollment; remove it yourself when it is no longer needed. Export important data from the application as an independent backup.

## Cost and support

The **base** channel runs **small** for app, **nano** for db, **nano** for redis. All containers incur runtime charges. Pay the current platform compute base rate for the time the instance runs, including idle time. Labs adds no markup and receives no payout. Stop the instance when finished. Consult the [upstream documentation](https://github.com/docmost/docmost#readme) for application behavior; this recipe does not promise author support.
