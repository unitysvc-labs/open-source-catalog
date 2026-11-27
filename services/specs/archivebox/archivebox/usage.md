# ArchiveBox Web Archive

Each enrollment runs a private [ArchiveBox](https://archivebox.io/) web archive. ArchiveBox is written and maintained by [Nick Sweeting](https://github.com/pirate) and contributors and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `archivebox/archivebox` image (version 0.9.77, pinned by digest), and the platform runs one isolated instance per enrollment.

Your collection (the index and the saved pages) is kept in the `archivebox` folder of your **home**, not in the enrollment. It survives stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same collection.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `archivebox/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one ArchiveBox instance at a time.
2. The form shows an **Administrator name** (default `admin`), and a generated **Administrator password**. The name and password create the administrator account the **first time** ArchiveBox runs on your collection. If the account already exists, because you enrolled before or restarted, they are ignored and the existing password still applies; change it in ArchiveBox's own admin pages. Save the values; they are also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready; the first start takes about half a minute. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Open the address and sign in with the administrator name and password.
5. If sign-in fails with a "CSRF verification failed" page, the platform's proxy did not tell ArchiveBox that the request used HTTPS. Contact UnitySVC support; this recipe has no setting for it.

## Save pages and read them

1. Open **Add** (the `/add/` page), paste one or more URLs, leave the depth at 0 to save just those pages, and submit.
2. ArchiveBox opens each page in a headless Chromium browser and saves it in several forms: the HTML, a single-file copy, a screenshot, a PDF, readable text, response headers, and more. The first capture takes a few minutes while the browser starts; later ones are quicker. Pages that need a login or block automated browsers may save only part of their content.
3. Open the collection from the home page to browse, search and tag snapshots, and open a snapshot to see each saved form.

You can also add URLs from the command line or the REST API (`/api/`); the [ArchiveBox documentation](https://docs.archivebox.io) describes both. Your own API token is created in the web interface.

## Authentication

ArchiveBox checks every request itself. The collection list, the snapshots and the **Add** page all require signing in; nothing is public. Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong. Replay of archived pages runs without JavaScript (ArchiveBox's `safe-onedomain-nojsreplay` mode, the safe choice for one address per instance), so some saved pages look plainer than the original. Saved URLs are not sent to the Internet Archive. UnitySVC adds no other gate.

## What is kept, and what is lost

The data folder of the collection is persistent: the SQLite database (`index.sqlite3`), the saved pages, the logs and ArchiveBox's configuration. They are stored in `archivebox/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before ArchiveBox starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a page just saved. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file ArchiveBox removes, such as a deleted snapshot, can come back after a restart.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by ArchiveBox and this keeps the stored database consistent.
- Do not edit the files in `archivebox/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored; a very large video is left out.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `archivebox/` folder yourself when you no longer want the data.
- The browser and extractor tools come with the image, not from your home. Anything ArchiveBox installs or downloads outside the collection folder is lost when the instance stops.

## Cost and size

The instance runs on the `small` size (one core, 2 GiB, 5 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check ArchiveBox used about 450 MiB idle and well over 1 GiB while saving a page with the browser, so it does not fit the smaller `nano` size. Saving many pages at once, or very large pages, can need more memory than this size has. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
