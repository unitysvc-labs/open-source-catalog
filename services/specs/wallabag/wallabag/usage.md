# wallabag Read-It-Later

Each enrollment runs a private [wallabag](https://wallabag.org) server. wallabag is written and maintained by [Nicolas Lœuillet](https://github.com/nicosomb) and the wallabag contributors and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `wallabag/wallabag` image (version 2.6.19, pinned by digest) with its embedded SQLite database, and the platform runs one isolated instance per enrollment.

Your articles and your account are kept in the `wallabag` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `wallabag/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one wallabag instance at a time.
2. The form shows a generated **Password of the wallabag account**. The account's name is always `wallabag`. The password is applied the **first time** wallabag creates its database in your home. If the database already exists, because you enrolled before or restarted, the parameter is ignored and the existing password still applies; change it on wallabag's own **Config** page. Save the password now: the platform keeps it as a secret and does not show it again. It is an application credential, not your UnitySVC API key.
3. Leave **Application secret** as generated, and **Instance address (optional)** as `//` (see below).
4. Wait for the instance to become ready; the first start takes well under a minute. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
5. Open the address and sign in as `wallabag` with the password.

## Use it

- **Save an article:** press **+** in the top bar, paste the page's address and confirm. wallabag fetches the page from the instance and keeps the extracted article. Pages that need a login or block automated requests may be saved without their content.
- **Read and organise:** unread, starred and archived lists, tags and tagging rules, full-text search and annotations.
- **Export** an article, or a whole list, as EPUB, PDF, CSV, JSON, XML or plain text.
- **Import** from Pocket, Instapaper, Pinboard, Readability and browser bookmarks under **Import**. Imports run inside the request (this recipe has no Redis or RabbitMQ worker), so split a very large import.
- **REST API, browser extension and mobile apps:** create an API client under **API clients management**, then give the app your instance address, the client id and secret, the user name `wallabag` and your password. After a new enrollment, give the apps the new address. The [wallabag documentation](https://doc.wallabag.org/) describes the API and the apps.

## The instance address setting

wallabag normally has to be told its public address, and uses it to link its style sheets and scripts. The address of an instance is not known before it exists, so this recipe starts wallabag with the value `//`, which makes those links relative to whatever address you open. The web interface, saving, reading, export and the API all work this way, at any instance address.

A few places print the configured address and are incomplete with `//`: the identifiers inside feeds, the Android app link and QR code on the **Config** page, and the example commands on the API how-to page. If you want them complete, set **Instance address (optional)** to this instance's address, for example `https://abc123.example.app`, with no trailing slash, and save; the instance restarts and keeps your data. A wrong address there makes every page load without its styling, so set it back to `//` if that happens. A new enrollment starts again from `//`.

## Authentication

wallabag checks every request itself: the web interface needs your sign-in, and the API needs an OAuth token obtained with an API client and your password. Public registration is turned off. Anyone who knows the instance address can reach the sign-in page, so keep the password strong. UnitySVC adds no other gate.

- The image's installer creates the account `wallabag` with the well-known password `wallabag`. This recipe replaces that password with your parameter, using wallabag's own `fos:user:change-password` command, before the web server starts, so the default password is never served. If that step fails the instance does not start.
- No mail server is configured, so wallabag cannot send email: the "forgot your password" link and two-factor codes by email do not work. Two-factor authentication with an authenticator app works. If you lose the password, the only way back is to delete the `wallabag/` folder in your home while the instance is stopped and start again empty.
- The account is a wallabag administrator and can add more users under **Users management**.

## What is kept, and what is lost

Two folders are persistent: `wallabag/data` (the SQLite database with your articles, tags, settings and accounts, and the key that encrypts saved site credentials) and `wallabag/images` (article images, if you turn on wallabag's option to download images locally). They are stored in your home, where you can see them in your files while the instance is stopped. The platform restores them before wallabag starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. An image wallabag removes can come back after a restart. This is cosmetic.
- SQLite's temporary files (`*-journal`, `*-wal`, `*-shm`) are not stored. This keeps the stored database consistent.
- Do not edit the files in `wallabag/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored. wallabag does not depend on any inside these folders.
- Sign-in sessions are not kept: after a restart you sign in again.
- The password and the application secret are read from the enrollment at each start, but the password only takes effect when the database is new.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `wallabag/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check with the same limits wallabag used about 75 MiB idle and under 100 MiB while saving and exporting articles. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
