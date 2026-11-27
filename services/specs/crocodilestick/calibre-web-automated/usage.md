# Calibre-Web-Automated E-book Library

Each enrollment runs a private [Calibre-Web-Automated](https://github.com/crocodilestick/Calibre-Web-Automated) (CWA) library. CWA is written and maintained by [CrocodileStick](https://github.com/crocodilestick) and contributors, as a fork of [Calibre-Web](https://github.com/janeczku/calibre-web), and is released under the GPL-3.0 license. The provider of this service is not the author. UnitySVC Labs lists the official `crocodilestick/calibre-web-automated` image (version v4.0.8, pinned by digest), and the platform runs one isolated instance per enrollment.

Your library, settings and users are kept in the `calibre-web-automated` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `calibre-web-automated/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one instance at a time.
2. The form shows a generated **Administrator password**. It is the password of the account named `admin`, set the **first time** the instance runs on your data. If your data already exists, because you enrolled before or restarted, the parameter is ignored and the existing password still applies; change it in the web interface (the user menu, then your profile). Save the value now: the platform keeps it as a secret and does not show it again. It is an application credential, not your UnitySVC API key.
3. Wait for the instance to become ready; the first start takes a minute or two. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so e-reader apps that point at the old one need the new one.
4. Open the address and sign in as `admin` with the password.

## Add and read books

1. In the web interface use the **Upload** button (the upload feature is on for the administrator) and choose one or more e-book files. CWA converts a book to the library's format if needed, reads its metadata, fetches a cover and adds it to the library; the Tasks page shows progress.
2. Browse, search, read in the browser and download from the same interface. For e-reader apps, use the OPDS catalog at `https://<instance>/opds` with your user name and password.
3. Create further users in **Admin**, with the permissions you want. Public registration and anonymous browsing are switched off.
4. The upstream [wiki](https://github.com/crocodilestick/Calibre-Web-Automated/wiki) describes the settings, metadata providers, e-mail delivery and KOReader sync. Features that need other services you run, such as an SMTP server, are yours to configure.

The image also has a folder watched for new files (`/cwa-book-ingest`). It is scratch space inside the instance and you cannot put files in it from outside, so upload through the web interface.

## Authentication

CWA checks every request itself: the web interface and OPDS need your sign-in. Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong. The image ships with a well-known default administrator password; this recipe replaces it before the application first starts, and the instance does not start if that fails. UnitySVC adds no other gate.

## What is kept, and what is lost

Two folders persist: `/config` (the settings and users database, logs, and the kept originals of imported books) and `/calibre-library` (the library: `metadata.db` and one folder of files per book). They are stored in `calibre-web-automated/config/` and `calibre-web-automated/library/` in your home. The platform restores them before CWA starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **An e-book library is made of whole files.** Files over 1 GiB are not stored, and a restore copies every file back before the instance starts, so a large library makes the start slow. A single file also has to fit in the instance's 1 GiB of temporary disk while it is converted.
- **Originals are kept twice.** By default CWA keeps a copy of every imported book in `/config/processed_books`, so each book uses about twice its size in your home. You can change this in CWA's settings.
- **One instance at a time.** The folders belong to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a book just imported. A normal stop loses nothing.
- Files are copied, never deleted from your home. A book you delete can come back after a restart. Delete it in the web interface again, or delete the files in your home while the instance is stopped, and note that the next start restores them over anything you changed.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by CWA and this keeps the stored databases consistent.
- Empty files and symbolic links are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `calibre-web-automated/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `small` size (one core, 2 GiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check the application used about 300 to 330 MiB while starting and settled to 130 to 310 MiB; importing one small EPUB took it to about 590 MiB, and in a 512 MiB container the same import reached the 512 MiB limit, which is why `nano` is not enough. A larger book needs more while it is converted. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
