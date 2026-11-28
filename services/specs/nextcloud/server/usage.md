# Nextcloud Private File Sync Server

This unofficial community recipe runs the upstream `nextcloud:35.0.3-apache` image, pinned by digest. Nextcloud GmbH and contributors publishes the software under [AGPL-3.0](https://github.com/nextcloud/server/blob/master/COPYING). No author endorsement or support commitment is implied.

## Set up and upload a file

1. Enroll in **base**, approve read/write access to `nextcloud/` in your home and save the initial administrator password. First installation is automatic; the public installer is not needed. Existing databases keep their users and passwords.
2. Open the HTTPS instance address, sign in and upload a small text file. Download it again and check its contents. Use the same server address with the Nextcloud desktop/mobile clients. WebDAV is available at `/remote.php/dav/files/<user>/`; create an application password in Nextcloud for client software.
3. Replace **Trusted hostnames** `*` with the hostname shown in your instance details. The initial wildcard accommodates the address being unknown at enrollment; the instance is isolated behind the platform proxy, but narrowing hostnames prevents unintended Host headers. A new enrollment has a new hostname, so update this setting and your clients.
4. Change existing passwords inside Nextcloud. Changing the initial administrator password parameter does not reset an existing account. No SMTP server is configured, so email recovery and email notifications are unavailable.

## Scope and storage

The **small-2x** channel uses two cores and 4 GiB for the first installation and normal personal use. SQLite suits a small installation; high concurrency and large libraries need a separately designed database-backed deployment. Background work uses Nextcloud's AJAX mode while people visit the site; this recipe includes no cron sidecar. Office editing, full Talk infrastructure, external storage and arbitrary application requirements are not supplied.

`nextcloud/data/` contains the SQLite database and user files; `nextcloud/config/` contains installation keys and settings; `nextcloud/apps/` contains installed custom applications. Keep these together. Core application code comes from the pinned image. A single file over 1 GiB cannot be persisted. Deleted files, obsolete applications and trash contents can return on disk because the platform copy never deletes; the database may no longer reference them. Export important files separately. The login and deliberately shared files are public; account data and WebDAV require Nextcloud authentication, with no additional platform gate.

## Storage and stopping

Stop the instance from UnitySVC when finished; closing the browser does not stop billing. Only one active enrollment per customer uses this recipe's home folder. Do not run another instance against that folder or edit it while this instance runs.

The platform restores persisted files before startup, copies changed files about every 30 seconds, and makes a final copy on a normal stop. A crash can lose recent changes. Copies add and replace files; they never delete. Deleted files may return on a later start. Empty files, symbolic links and individual files over 1 GiB are not stored. Nothing removes the home folder when you cancel enrollment; remove it yourself when it is no longer needed. Export important data from the application as an independent backup.

## Cost and support

The **base** channel uses **small-2x**. Pay the current platform compute base rate for the time the instance runs, including idle time. Labs adds no markup and receives no payout. Stop the instance when finished. Consult the [upstream documentation](https://github.com/nextcloud/server#readme) for application behavior; this recipe does not promise author support.
