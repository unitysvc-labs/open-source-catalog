# PhotoPrism Private Photo Library

This unofficial community recipe runs the upstream `photoprism/photoprism:latest` image, pinned by digest. PhotoPrism and contributors publishes the software under [AGPL-3.0](https://github.com/photoprism/photoprism/blob/develop/LICENSE). No author endorsement or support commitment is implied.

## First photo

1. Enroll in **base**, approve access to `photoprism/` in your home and save the generated administrator password. The channel uses **small-2x** (two cores, 4 GiB) for indexing and image processing.
2. Open the HTTPS instance address and sign in with the administrator name and password. Update **Public address** to the assigned URL before making share links.
3. Upload a small JPEG, wait for processing, open it and add it to an album. Larger videos and batches can exhaust memory or temporary disk; start small. TensorFlow classification is disabled, so do not expect the automatic labels/faces associated with that subsystem. Paid editions, external AI services and hardware acceleration are not included.
4. Keep existing accounts' passwords in PhotoPrism. The enrollment password initializes a fresh account and is not an existing-password reset. No SMTP service is provided.

## Persistence and deletion

Originals are kept in `photoprism/originals/`; metadata, SQLite, thumbnails and application settings are kept in `photoprism/storage/`. Both are needed for restoration. SQLite uses rollback-journal mode; transient journals are excluded from the copy. Keep independent copies of irreplaceable photos.

The storage copy never deletes files. A deleted original may return on disk after a stop/start and can be indexed again in a later scan. Empty files, symlinks and individual files above 1 GiB are not retained. The site and sign-in page are publicly reachable; private library operations require PhotoPrism authentication. Deliberately shared albums follow the application's sharing permissions. UnitySVC adds no separate authentication gate.

## Storage and stopping

Stop the instance from UnitySVC when finished; closing the browser does not stop billing. Only one active enrollment per customer uses this recipe's home folder. Do not run another instance against that folder or edit it while this instance runs.

The platform restores persisted files before startup, copies changed files about every 30 seconds, and makes a final copy on a normal stop. A crash can lose recent changes. Copies add and replace files; they never delete. Deleted files may return on a later start. Empty files, symbolic links and individual files over 1 GiB are not stored. Nothing removes the home folder when you cancel enrollment; remove it yourself when it is no longer needed. Export important data from the application as an independent backup.

## Cost and support

The **base** channel uses **small-2x**. Pay the current platform compute base rate for the time the instance runs, including idle time. Labs adds no markup and receives no payout. Stop the instance when finished. Consult the [upstream documentation](https://github.com/photoprism/photoprism#readme) for application behavior; this recipe does not promise author support.
