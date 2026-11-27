# MicroBin Pastebin and File Sharing

Each enrollment runs a private [MicroBin](https://microbin.eu/) server. MicroBin is written and maintained by [Dániel Szabó](https://github.com/szabodanika) and contributors and is released under the BSD 3-Clause license; the provider of this service is its author. UnitySVC Labs lists the official `danielszabo99/microbin` image (version 2.1.0, pinned by digest), and the platform runs one isolated instance per enrollment. The author was not asked to take part, and nothing here implies endorsement or support.

MicroBin is a small pastebin, file sharing tool and URL shortener. Its uploads (text, files and redirect links) are kept in the `microbin` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same uploads.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `microbin/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one MicroBin instance at a time.
2. The form shows a **Site user name** (default `microbin`) with a generated **Site password**, and an **Administrator name** (default `admin`) with a generated **Administrator password**. Save both passwords now: the platform keeps them as secrets and does not show them again. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready; it starts in a few seconds. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Open the address. The browser asks for a user name and password: enter the site user name and site password. Type them into the browser's prompt; do not put them in the address (`https://name:password@...`), because when the page was opened that way the upload is saved but the form stays on "Uploading..." instead of showing it (seen in a Chromium browser).

MicroBin reads all four values each time it starts. To change a name or password, change the parameter and save; the instance restarts with the new value and keeps your uploads.

## Create an upload and share it

1. On the **New** page, type or paste text, or attach one file, or both. Choose the **expiration** (1 minute, 10 minutes, 1 hour, 24 hours (the default), 3 days, 1 week, or never), an optional **burn after** count (the upload is removed after that many reads), optional syntax highlighting, and the **privacy** level:
   - **Public**: shown on the **List** page of this instance.
   - **Unlisted**: not on the list; opened with its link.
   - **Read-only**: unlisted, and editing or removing it needs the password you set on the upload.
   - **Private**: unlisted and encrypted on the server with the password you set; reading it needs that password.
   - **Secret**: as private, and also encrypted in your browser before it is sent.
2. Press **Save**. You land on the upload's page; its link has a name made of animal words, such as `/upload/ape-mouse-monkey`. Copy the link from the browser's address bar.
3. To shorten a web address, paste only that address as the text. The upload page then shows it as a link, and `https://<instance>/url/<name>` redirects to it.

An attachment can be up to 256 MB, or 32 MB for a private or secret upload (those are encrypted in memory). Text of an upload can be read raw at `/raw/<name>` and a file at `/file/<name>`. From the command line, give the site name and password with every request:

```bash
curl -u '<site-user>:<site-password>' -F expiration=1week -F burn_after=0 -F privacy=unlisted \
     -F content='hello' -o /dev/null -w '%{redirect_url}\n' https://<instance>/upload
curl -u '<site-user>:<site-password>' https://<instance>/raw/<name>
```

The **Guide** page of the instance and the [MicroBin documentation](https://microbin.eu/docs/intro) describe the features in more detail.

**No copy-link button and no QR codes.** MicroBin shows those only when it is configured with its own public address, and an instance's address is not known until after enrollment, so this recipe leaves it unset. Everything else works without it. The admin page shows a warning about this ("No public URL set"); it is expected.

## Authentication: who can use this instance

- **The whole site is behind HTTP basic authentication.** MicroBin answers `401` to every request without the site user name and password, including shared links, raw text, files and redirect links. A wrong name or password gets `400 Invalid login details` rather than a new prompt; close the tab or clear the saved sign-in and try again. To let someone read an upload, give them the link and the site name and password. Anyone who has them can also create uploads, see the public list, and edit or remove any upload that is not read-only, private or secret. There is one site sign-in, not one per person.
- **The admin page** at `/admin` asks, after the site sign-in, for the administrator name and password. It lists every upload, including unlisted ones, and can remove them.
- **A password on an upload** (read-only, private, secret) is separate again and is set by whoever creates the upload.
- Upload names are short and can be guessed (MicroBin has about 65,000 of them), so a link is not a secret by itself; the site password is what keeps uploads private. Use **private** or **secret** for anything that people who hold the site password should not all read.

UnitySVC adds no other gate. MicroBin's telemetry, its update check and its public server list are turned off in this recipe.

## What is kept, and what is lost

MicroBin's data folder is persistent: the SQLite database (`database.sqlite`, with the text of every upload and its settings) and the `attachments` folder (one folder per upload that has a file). They are stored in `microbin/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before MicroBin starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **The file of a removed, expired or burned upload stays in your home.** Files are copied to your home, never deleted from it. When MicroBin removes an upload, the upload disappears from the database, so its link stops working and its text is gone, and this stays so after a restart. But the copy of its attachment stays in `microbin/attachments/<name>/` in your home, and comes back into the instance's data folder at the next start, where MicroBin no longer serves it. An attachment of a private or secret upload is stored encrypted (`data.enc`); any other attachment is stored as it was uploaded, under its own file name. If a removed file must be gone for good, delete its folder from `microbin/attachments/` in your home while the instance is stopped. The folder only grows until you do.
- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include an upload just made or bring back one just removed. A normal stop loses nothing.
- SQLite's temporary files (`*-journal`, `*-wal`, `*-shm`) are not stored. MicroBin uses SQLite's default rollback journal, so the database file itself holds all the data.
- Do not edit the files in `microbin/` while the instance is stopped, other than deleting attachment folders: the next start restores them as they are.
- Empty files, symbolic links and files over 1 GiB are not stored. An empty attachment would be lost; the size limits above keep attachments well under 1 GiB.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `microbin/` folder yourself when you no longer want the data.
- The names and passwords are not in the data folder; they come from the enrollment's parameters at each start.

Uploads set to never expire are kept until you remove them: this recipe turns off MicroBin's removal of uploads that have not been read for 90 days.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check with memory limited to 512 MiB, MicroBin used about 3 MiB idle and under 100 MiB while taking a 31 MB encrypted attachment and a 250 MB plain one. Attachments live on the instance's temporary disk while it runs, so keep their total well under 1 GiB. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
