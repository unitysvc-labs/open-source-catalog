# Immich Private Photo and Video Library

This unofficial community recipe runs the upstream `ghcr.io/immich-app/immich-server:v3.4.2` image, pinned by digest. Immich (Alex Tran and contributors) publishes the software under [AGPL-3.0](https://github.com/immich-app/immich/blob/main/LICENSE). No author endorsement or support commitment is implied.

## Upload your first photo

1. Enroll in **base**, approve `immich/` home access and keep the database password. The stack uses **small-2x** for the server, **small** for PostgreSQL and **nano** for Valkey.
2. Open the HTTPS instance address immediately and create the first administrator before sharing it. The first visitor can claim that account. Existing databases retain their users and passwords. UnitySVC adds no separate authentication gate.
3. Upload a small JPEG, inspect its thumbnail, create an album and download the original. Configure the Immich mobile app with the same HTTPS address to upload from a phone. Shared albums and links follow Immich's application permissions.
4. Machine learning is disabled because the separate model service is not included. Face recognition and semantic search are unavailable. There is no GPU, mail service or external backup destination; keep independent copies of original media.

## Library storage

The complete `/data` library persists under `immich/library/`, including originals, thumbnails, profile files and application backup files. PostgreSQL metadata and accounts are persisted separately in `immich/db-backup/`. The pinned database image includes the vector extensions needed by this Immich version. Do not combine this library with a different database or run concurrent enrollments against it.

Deleted files can return on disk after restart because the home copy never deletes, while database deletions remain. Individual media files above 1 GiB cannot be persisted. Large transcodes, libraries and bulk jobs can exceed memory or temporary disk. Finish processing before stopping; in-flight jobs and the scratch broker are not durable. A new enrollment has a new hostname, so update clients and shared links.

## Database backup and restart behavior

PostgreSQL's live directory is scratch. A compressed dump is persisted in the home folder every five minutes and on SIGTERM. A fresh scratch directory restores the dump before the database opens its network port. A crash can lose up to five minutes of database changes. The dump must remain below the platform's 1 GiB single-file limit. Keep the database credential and application secrets across re-enrollment, and keep independent exports of important content. Redis/Valkey is a scratch cache/task broker; queued background work is not durable across an instance replacement. Finish uploads and processing before stopping.

## Storage and stopping

Stop the instance from UnitySVC when finished; closing the browser does not stop billing. Only one active enrollment per customer uses this recipe's home folder. Do not run another instance against that folder or edit it while this instance runs.

The platform restores persisted files before startup, copies changed files about every 30 seconds, and makes a final copy on a normal stop. A crash can lose recent changes. Copies add and replace files; they never delete. Deleted files may return on a later start. Empty files, symbolic links and individual files over 1 GiB are not stored. Nothing removes the home folder when you cancel enrollment; remove it yourself when it is no longer needed. Export important data from the application as an independent backup.

## Cost and support

The **base** channel runs **small-2x** for app, **small** for db, **nano** for redis. All containers incur runtime charges. Pay the current platform compute base rate for the time the instance runs, including idle time. Labs adds no markup and receives no payout. Stop the instance when finished. Consult the [upstream documentation](https://github.com/immich-app/immich#readme) for application behavior; this recipe does not promise author support.
