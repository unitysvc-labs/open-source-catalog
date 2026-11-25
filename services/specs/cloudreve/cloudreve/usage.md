# Cloudreve File Management and Sharing

Each enrollment runs a private [Cloudreve](https://cloudreve.org/) server. Cloudreve is written and maintained by the [Cloudreve project](https://github.com/cloudreve/cloudreve) and contributors and is released under the GPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `cloudreve/cloudreve` image (the Community edition, version 4.19.1, pinned by digest), and the platform runs one isolated instance per enrollment. It runs as one container with SQLite and Cloudreve's built-in cache; there is no PostgreSQL or Redis, and files are stored on the instance's local disk.

Your database, settings and uploaded files are kept in the `cloudreve` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. It has no settings to fill in. The enrollment asks for access to the `cloudreve/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Cloudreve instance at a time.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so anything that points at the old one needs the new one.
3. **Open the address and sign up immediately.** On a new instance the first account registered becomes the administrator, and there is no password to protect that step. Anyone who reaches the address before you could register first and take the administrator account. If that happens, stop and remove the instance, delete the `cloudreve/` folder of your home, and enroll again.
4. Sign in as that account and open the administrator dashboard (**Settings**). Do two things:
   - **Site URL:** set it to the instance address (`https://<enrollment-code>.<apps-domain>`). Cloudreve cannot know it in advance, so it starts with `http://localhost:5212`, and links it builds (share links, direct links, and emails) would point there. A new enrollment has a new address, and the stored value is then wrong: set it again after every re-enrollment.
   - **Registration:** turn off new-user registration, so that nobody else can create an account and store files on your disk. Leave it on only if you want others to sign up.

## Upload and share files

1. Open **My files**, drag files or folders into the page, or use the upload button. Large files are uploaded in 25 MiB chunks.
2. Select a file or folder and choose **Share** to create a link, with an optional password and expiry. The link starts with the site URL from step 4; if it shows `localhost`, set the site URL first.

Without signing in, the file API answers "Login required".

## Authentication

Cloudreve checks every request itself: the web interface needs your sign-in, and a shared link needs its link (and password, if you set one). Anyone who knows the instance address can reach the sign-in page, so use a strong password, keep shared links private, and turn off registration as described above. UnitySVC adds no other gate. This recipe does not use email; account activation and password-reset emails need a mail server configured in the Cloudreve settings, and none is set up.

## What is kept, and what is lost

Cloudreve's data folder is persistent: the SQLite database (users, files, shares, settings), the generated `conf.ini` (which holds the session secret), and the uploaded files in `uploads/`. They are stored in `cloudreve/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before Cloudreve starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **Files over 1 GiB are not kept.** The platform does not store a file over 1 GiB in your home. Cloudreve accepts the upload, but after the instance is stopped or replaced that file is gone. Keep each file under 1 GiB.
- **The instance has 1 GiB of temporary disk** (the `nano` size). Cloudreve writes the database and every uploaded file to that disk, so together they must fit in about 1 GiB; what happens past that limit on the platform was not tested. This service suits a small private file store, not a large archive. Cloudreve's own quota and storage-policy settings are not tied to this limit.
- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a file just uploaded. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file you delete in Cloudreve can come back after a restart; deleting it again removes it.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Cloudreve and this keeps the stored database consistent.
- Do not edit the files in `cloudreve/` while the instance is stopped: the next start restores them over what you changed.
- Empty files and symbolic links are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `cloudreve/` folder yourself when you no longer want the data.
- The image also contains an aria2 download helper (used by Cloudreve's offline download). Only the web port is reachable, so BitTorrent downloads that need incoming connections do not work; this was not tested.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Cloudreve used about 190 MiB in a local check, also after uploading a 120 MB file. Thumbnail generation for large images, video or Office documents, which this image can do, was not tested and may use more. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
