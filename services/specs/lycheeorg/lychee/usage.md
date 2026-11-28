# Lychee Private Photo Gallery

This unofficial community recipe runs the upstream `lycheeorg/lychee:v7.13.1` image, pinned by digest. Lychee Organisation and contributors publishes the software under [MIT](https://github.com/LycheeOrg/Lychee/blob/master/LICENSE). No author endorsement or support commitment is implied.

## Upload an album

1. Enroll in **base**, approve access to `lychee/` in your home, save the generated **Application encryption key** and choose the first administrator name and password. The key must be exactly 32 characters; keep it with your backups and use it again when re-enrolling over this data.
2. Wait for the instance to become ready. On a fresh database the startup wrapper migrates a temporary SQLite database and runs Lychee's `lychee:create_user` command before atomically installing it. A failed setup does not expose a half-initialized service.
3. Open the HTTPS address, sign in, create an album and upload a small photo. Verify that a signed-out browser cannot see private photos. Album sharing is controlled by Lychee; publishing an album deliberately gives others access. The sign-in page and public information endpoints remain reachable without credentials.
4. Change existing passwords inside Lychee. Enrollment's initial administrator values never reset a restored user. No mail server, external identity provider, face-recognition service or supporter license is supplied.

## Storage and workload limits

The SQLite database is kept under `lychee/database/` and originals/thumbnails under `lychee/uploads/`. Both are required to restore a gallery. The application key is an enrollment parameter, so keep it separately and reuse it. Database journals and partial first-run databases are excluded from persistence. Do not stop the instance during an upload or while images are being processed.

This recipe uses **small** (one core, 2 GiB) for image processing. Very large images, videos or large batches can exceed its memory or temporary-disk capacity. Files larger than 1 GiB cannot be persisted even if an upload succeeds. Removed photos can return as orphan files on disk because the home copy never deletes; their database entries stay deleted. Use independent photo backups and do not treat this as the sole copy of your library. HTTPS proxy headers are trusted inside the isolated instance; no additional application authentication gate is supplied.

## Storage and stopping

Stop the instance from UnitySVC when finished; closing the browser does not stop billing. Only one active enrollment per customer uses this recipe's home folder. Do not run another instance against that folder or edit it while this instance runs.

The platform restores persisted files before startup, copies changed files about every 30 seconds, and makes a final copy on a normal stop. A crash can lose recent changes. Copies add and replace files; they never delete. Deleted files may return on a later start. Empty files, symbolic links and individual files over 1 GiB are not stored. Nothing removes the home folder when you cancel enrollment; remove it yourself when it is no longer needed. Export important data from the application as an independent backup.

## Cost and support

The **base** channel uses **small**. Pay the current platform compute base rate for the time the instance runs, including idle time. Labs adds no markup and receives no payout. Stop the instance when finished. Consult the [upstream documentation](https://github.com/LycheeOrg/Lychee#readme) for application behavior; this recipe does not promise author support.
