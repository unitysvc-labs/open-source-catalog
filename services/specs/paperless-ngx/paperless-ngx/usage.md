# Paperless-ngx Document Management with OCR

Each enrollment runs a private [Paperless-ngx](https://docs.paperless-ngx.com/) personal archive with SQLite and a task broker. The [Paperless-ngx team](https://github.com/paperless-ngx) and contributors maintain the GPL-3.0 software. UnitySVC Labs provides this unofficial recipe; the authors have not agreed to participate or provide support. The official Paperless-ngx 3.5.1 and Valkey 9.2.1 Alpine images are pinned by digest. Valkey is BSD-3-Clause licensed.

## Set up

1. Enroll in **base** and approve read/write access to the enrollment's own storage.
2. Save the **Administrator name** (default `admin`), generated **Administrator password** and generated **Secret key** before completing enrollment. Treat enrollment settings as sensitive. The initial account is created only when that user name does not exist. An existing account's password is unchanged by later enrollment edits; change it in Paperless under **My Profile**. Changing the administrator name creates another administrator with the supplied password and leaves the original in place.
3. Wait for readiness, then open the HTTPS address in the instance details and sign in. A new enrollment has a new address and an empty archive. The application accepts its assigned host name without another URL setting.
4. Keep the secret key unchanged: changing it signs everyone out and invalidates the trained matching model. The **OCR language** defaults to `eng`; changing it restarts the instance and affects documents added afterwards.

## First use

Upload a scanned PDF or image using **Upload documents**, or drag it onto the dashboard. Paperless queues OCR, creates a searchable PDF/A copy and thumbnail, and retains the original. Find it under **Documents**, add tags and a correspondent, then search for a word in the scan. Processing time depends on document size. The single worker processes one task at a time.

Create an API token under **My Profile** for REST access:

```bash
curl -H "Authorization: Token <token>" https://<instance>/api/documents/
curl -H "Authorization: Token <token>" -F document=@scan.pdf https://<instance>/api/documents/post_document/
```

Documents arrive through the web interface, API, or an IMAP account you configure under **Mail**. There is no externally accessible consume folder; the folder watcher is disabled. Tags, correspondents, document types, storage paths, custom fields, saved views, workflows and automatic matching are available. See the [upstream documentation](https://docs.paperless-ngx.com/) for their use.

## Authentication and limitations

Paperless checks authentication itself. The web interface requires sign-in, and private API endpoints reject missing or incorrect credentials. Sign-up is closed; administrators create additional users under **Users & Groups**. Share links are accessible to anyone with the link. Anyone who knows the instance address can reach the sign-in page, so use a strong password. UnitySVC adds no other application gate; the broker is internal to the instance.

- This SQLite channel is for a **personal archive with light concurrency**. It is not configured for a busy multi-user service. One background worker limits competing database writes.
- The installed OCR languages are English (`eng`), German (`deu`), French (`fra`), Italian (`ita`) and Spanish (`spa`). Combine codes with `+`, such as `deu+eng`; additional languages cost processing time.
- No outgoing mail server is configured. Password reset emails, emailing documents and email workflow actions do not work. A signed-in administrator can change passwords.
- Office documents and `.eml` conversion require Tika and Gotenberg, which are not included. PDFs, images and plain text are supported.
- AI provider configuration is not exposed by this recipe.

## Storage and stopping

Three folders persist in this enrollment's storage: **media** (originals, searchable copies and thumbnails), **data** (SQLite metadata, users, settings and recognized text), and **model** (the trained matching model). SQLite uses rollback journaling (`DELETE`) with full synchronization, rather than WAL. The search index, logs and scheduler state are excluded from persistence; the full search index is rebuilt from database text before every start becomes ready. Keep the archive small enough that rebuilding fits the platform startup budget. Large archives have not been qualified on this channel.

The platform copies files periodically (about every 30 seconds) and at normal stop. A crash can lose recent changes or interrupt a copy. These file copies are not an application-consistent live database backup; keep independent document exports and do not use this as the only copy of an important archive. Wait for OCR and other writes to finish before stopping. Verify your archive after a restart.

- The storage copy keeps files **below 1 GiB**. Both `data/db.sqlite3` and each original or generated document must stay below that limit. Empty files and symlinks are skipped; Paperless recreates its empty lock files.
- Files are copied, never deleted from storage. Deleting or renaming a document in Paperless removes its database entry or changes its path, but the old files remain in storage and may return as unreferenced files at the next start. Paperless does not automatically add them back to the archive.
- The queue, active OCR jobs, logs and export folder are temporary. Wait for uploads to finish before stopping; retry an interrupted upload. Database task history persists.
- The running web container has 10 GiB of temporary disk, shared by the archive and processing space. Keep well below that limit. Removing the enrollment removes its storage; enrolling again starts empty. Download documents and keep independent exports before removal.

## Cost and size

Paperless runs on `small-2x` (two cores, 4 GiB RAM, 10 GiB temporary disk) and Valkey on `nano` (half a core, 512 MiB RAM). OCR and classifier training need more resources than an idle archive; this channel uses one web worker, one task worker and one OCR thread. You pay platform compute cost for both containers while running, including idle time. Labs adds no markup and receives no seller payout. Stop the instance when it is not needed; retained storage is still subject to the platform's storage terms.
