# LinkStack Personal Link Page

This unofficial community recipe runs the upstream `linkstackorg/linkstack:v4.8.8` image, pinned by digest. LinkStack and contributors publishes the software under [AGPL-3.0](https://github.com/LinkStackOrg/LinkStack/blob/main/LICENSE). No author endorsement or support commitment is implied.

## Set up your page

1. Enroll in **base**, approve `linkstack/` home access and set the first administrator's email, password and page name. Save the password. The channel uses **nano** (half a core, 512 MiB).
2. Start the instance and wait for setup to finish. The recipe submits LinkStack's setup forms on a private loopback server before opening the HTTP entry. A fresh database gets exactly one administrator and public registration is disabled.
3. Open `https://<instance>/login`, sign in with the administrator email and password, add a link and visit the public profile. The page is public by design; dashboard changes need LinkStack authentication. UnitySVC adds no gate.
4. Change an existing password in LinkStack. Enrollment's initial account parameters are ignored when a database is restored, so changing them is not a password reset. No mail server is configured; do not depend on email verification or password-reset messages.

## Persisted application state

The home folder holds the SQLite database, the generated `.env`/application key, advanced configuration, themes and uploaded images. Code always comes from the pinned image. Keep the whole folder together: losing the application key can invalidate encrypted values and sessions. A new enrollment uses the existing account and page.

The storage copy never deletes files. Removed themes, link images or other assets can return on disk. Startup prunes older avatar/background versions so an old restored image does not hide a newer upload; other removed assets can still remain. Deleting a link changes SQLite and does not by itself delete every uploaded file. Restore is not an application-version upgrade guarantee. Export important content and keep image files below 1 GiB.

## Storage and stopping

Stop the instance from UnitySVC when finished; closing the browser does not stop billing. Only one active enrollment per customer uses this recipe's home folder. Do not run another instance against that folder or edit it while this instance runs.

The platform restores persisted files before startup, copies changed files about every 30 seconds, and makes a final copy on a normal stop. A crash can lose recent changes. Copies add and replace files; they never delete. Deleted files may return on a later start. Empty files, symbolic links and individual files over 1 GiB are not stored. Nothing removes the home folder when you cancel enrollment; remove it yourself when it is no longer needed. Export important data from the application as an independent backup.

## Cost and support

The **base** channel uses **nano**. Pay the current platform compute base rate for the time the instance runs, including idle time. Labs adds no markup and receives no payout. Stop the instance when finished. Consult the [upstream documentation](https://github.com/LinkStackOrg/LinkStack#readme) for application behavior; this recipe does not promise author support.
