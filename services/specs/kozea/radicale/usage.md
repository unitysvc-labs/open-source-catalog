# Radicale Calendar and Contacts Server

This unofficial community recipe uses the official Radicale 3.9.2 image, pinned by digest. [Kozea and contributors](https://radicale.org) publish Radicale under [GPL-3.0](https://github.com/Kozea/Radicale/blob/master/COPYING.md). No author endorsement or support commitment is implied.

## Set up and sync a calendar

1. Enroll in **base**, approve read/write access to `radicale/` in your home, choose a user name and save the generated password. The channel uses **nano** (half a core, 512 MiB).
2. Open the HTTPS address and sign in with that user name and password. Radicale has a small collection-management page, not a full web calendar. Create a calendar or address book there, then copy its collection URL.
3. Configure your CalDAV/CardDAV client (Apple Calendar/Contacts, Thunderbird, DAVx5 or another supported client) with `https://<instance>/`, the user name and password. A collection URL is `https://<instance>/<user>/<collection>/`. Create an event or contact, sync and verify it in another client.
4. The application checks HTTP Basic authentication on data requests and restricts each user to their own collections. The web sign-in page and healthcheck need no credentials. UnitySVC adds no application authentication gate. There is one configured user; a request as a different user cannot access your collections.

## Passwords and storage

On every start the wrapper creates a bcrypt htpasswd file outside the persisted volume from the enrollment's user name and password. Radicale has no password-change page: change the enrollment password and restart to change the credential. The file is not saved with your calendar data. Keep the same user name on re-enrollment, because collections belong to that user path. A changed user name sees a different collection root.

Calendars and contacts are individual `.ics` and `.vcf` files under `radicale/collections/` in your home. Caches and sync-token state are temporary and rebuilt; clients may need a full sync after restart. The storage copy never deletes files: an event, contact or whole collection you delete can return at the next stop/start. For permanent removal, stop the instance and remove its stored files from your home; keep independent calendar/address-book exports. This limitation also affects privacy-sensitive deletions. Temporary Radicale write files are excluded from persistence.

## Storage and stopping

Stop the instance from UnitySVC when finished; closing the browser does not stop billing. Only one active enrollment per customer uses this recipe's home folder. Do not run another instance against that folder or edit it while this instance runs.

The platform restores persisted files before startup, copies changed files about every 30 seconds, and makes a final copy on a normal stop. A crash can lose recent changes. Copies add and replace files; they never delete. Deleted files may return on a later start. Empty files, symbolic links and individual files over 1 GiB are not stored. Nothing removes the home folder when you cancel enrollment; remove it yourself when it is no longer needed. Export important data from the application as an independent backup.

## Cost and support

Pay the platform's current **nano** base rate while the instance runs, including idle time. Labs adds no markup and receives no payout. Stop it when finished. See the [upstream documentation](https://radicale.org/v3.html) for client setup and application behavior.
