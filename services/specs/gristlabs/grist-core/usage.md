# Grist Open Source Spreadsheet Database

This unofficial community recipe runs the upstream `gristlabs/grist-oss:1.7.22` image, pinned by digest. Grist Labs publishes the software under [Apache-2.0](https://github.com/gristlabs/grist-core/blob/main/LICENSE.txt). No author endorsement or support commitment is implied.

## Set up and create a document

1. Enroll in **base**, approve read/write access to `grist/` in your home and save the generated **Administrator boot key** and **Session signing secret**. The channel uses **small** (one core, 2 GiB).
2. Open `https://<instance>/boot`. Enter the boot key, then choose the administrator email when asked. This is Grist's own administrator login; there is no UnitySVC application gate. The boot key grants full control and can also authenticate API requests with `x-boot-key`.
3. Leave the instance **out of service** in Quick setup. This recipe fixes `GRIST_IN_SERVICE=false`, so access remains behind the boot-key gate on each start. Do not configure a default email or unauthenticated login. For this private single-user recipe, use the administrator session to open the home page and create a new document.
4. Add a table and a row, then add a formula column such as `1 + 2`. Import CSV/XLSX files or export a document from its menu. The Pyodide sandbox runs Python formulas without requiring privileged containers or nested gVisor.

## Authentication and scope

An anonymous browser is directed to setup/boot login, and a wrong boot key is refused. This recipe is for one trusted administrator, not a public multi-user deployment. Enabling an external identity provider, sharing documents publicly, or changing authentication through the Admin Panel requires a separate deployment review. Keep the boot key confidential. Use the same home folder and signing secret on re-enrollment; a new boot key can be chosen without deleting documents. Do not share private documents through untrusted custom widgets.

## What is persisted

`/persist` is kept in `grist/`: Grist documents (`.grist` SQLite files), its home database and session database. Temporary SQLite journal files are excluded, and document SQLite uses synchronous mode. Changes saved to a database survive a normal stop; in-flight edits and recent changes can be lost on a crash. A deleted document or old snapshot can return on disk because the home copy never deletes files. Download `.grist` exports for important documents. Individual documents or attachments exceeding the platform's 1 GiB file limit cannot be persisted. Formulas, large imports and simultaneous documents need more memory than the idle server.

## Storage and stopping

Stop the instance from UnitySVC when finished; closing the browser does not stop billing. Only one active enrollment per customer uses this recipe's home folder. Do not run another instance against that folder or edit it while this instance runs.

The platform restores persisted files before startup, copies changed files about every 30 seconds, and makes a final copy on a normal stop. A crash can lose recent changes. Copies add and replace files; they never delete. Deleted files may return on a later start. Empty files, symbolic links and individual files over 1 GiB are not stored. Nothing removes the home folder when you cancel enrollment; remove it yourself when it is no longer needed. Export important data from the application as an independent backup.

## Cost and support

The **base** channel uses **small**. Pay the current platform compute base rate for the time the instance runs, including idle time. Labs adds no markup and receives no payout. Stop the instance when finished. Consult the [upstream documentation](https://github.com/gristlabs/grist-core#readme) for application behavior; this recipe does not promise author support.
