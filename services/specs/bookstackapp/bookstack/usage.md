# BookStack Wiki and Documentation Platform

Each enrollment runs a private [BookStack](https://www.bookstackapp.com/) with its own MariaDB database. BookStack is written and maintained by [Dan Brown](https://danb.me/) and contributors and is released under the MIT license; the provider of this service is its author, who was not asked to take part. BookStack publishes no container image of its own: UnitySVC Labs lists the community image its documentation points to, `lscr.io/linuxserver/bookstack` by LinuxServer.io (BookStack 26.09.3), and the official `mariadb` image (11.4), both pinned by digest. The platform runs one isolated stack per enrollment. MariaDB is released under the GPL-2.0 license.

## Set up

1. Enroll in **base**. The enrollment asks for access to its own storage (`service:storage`, read and write). Approve it, or the instance does not start.
2. The form shows an **Administrator email** (default `admin@example.com`), a generated **Administrator password**, a generated **Application key** and a generated **Database password**. Enter the email address you want to sign in with and save the password: the platform keeps the generated values as secrets and does not show them again. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address and empty data.**
4. Open the address. BookStack redirects to its sign-in page; sign in with the administrator email and password.

BookStack's installer creates a published default account, `admin@admin.com` with the password `password`. On the first start this recipe replaces that account's email and password with the ones from the enrollment, using BookStack's own `bookstack:create-admin --initial` command, before the web server starts. The default login never works on your instance. On later starts the two values are ignored: change your email or password in BookStack under **My Account**.

## First use

1. Create a book under **Books > Create New Book**, then add a page to it and save.
2. Add more people under **Settings > Users**. Set a password for each user yourself: the invitation email option does not work here (see below). Public registration is off by default.
3. To use the REST API, create a token under **My Account > Access & Security > API Tokens** and send it as `Authorization: Token <id>:<secret>`. The API documentation is at `/api/docs` on your instance.

See the [BookStack documentation](https://www.bookstackapp.com/docs/) for the rest.

## The instance address

BookStack normally needs its address in a setting (`APP_URL`). The address of an instance is known only after enrollment, so this recipe leaves `APP_URL` unset: BookStack then builds every link from the address you open it at. This worked in Labs' tests behind an HTTPS proxy (pages, styles, sign-in, uploads, exports), but it is not how BookStack's documentation describes a production setup. Two consequences:

- The address of an uploaded image is written into the page with the full instance address at the time of the upload. An enrollment keeps its address, so this only matters if you move content to another BookStack.
- A new enrollment has a new address and starts empty; content does not follow you to it.

## No email

The instance has no mail server and no mail settings, so BookStack cannot send anything. In Labs' test the "Forgot Password?" form answered with an error page (HTTP 500). Invitation emails, email confirmation and notification emails are not sent either. **A lost administrator password cannot be reset**: keep it safe, and consider a second administrator account as a spare.

## Authentication

BookStack checks every request itself: pages, the API and attachments need a sign-in or an API token unless you turn on public access in **Settings**. Anyone who knows the instance address can reach the sign-in page, so keep the passwords strong; BookStack also offers multi-factor authentication under **My Account**. UnitySVC adds no other gate. The database is reachable only from inside the instance.

**Uploaded images are served by their address without a sign-in.** This is BookStack's default storage mode: image addresses are long and hard to guess, but anyone who has one can open the image. Attachments are checked against your permissions.

## What is kept, and what is lost

Three folders are persistent, in the enrollment's storage: a backup of the MariaDB database (books, pages, revisions, users and settings), the uploaded images and the attachments. The database itself runs on temporary disk; the instance writes a backup of it every five minutes and once more when it stops, and restores that backup when it starts. The platform copies the three folders to storage about every 30 seconds while the instance runs and once more when it stops. Stopping therefore takes a moment longer while the backup and the copy finish.

- A normal stop loses nothing. A crash, or a node failure, can lose the changes made since the last backup, up to five minutes. Export books you cannot lose (**Export** on a book, or the ZIP export) from time to time.
- The backup is one file and must stay under 1 GiB, the largest file the platform's storage copy keeps. Page text and revisions rarely reach that; images and attachments are stored as separate files and do not count.
- **Deleted uploads come back.** The copy only adds and replaces files and never deletes them from storage. An image or attachment you delete in BookStack is removed from the database, but its file returns at the next start, and a deleted image can again be opened by anyone who still has its address. Do not upload images you may need to remove completely.
- Empty files, symbolic links and files over 1 GiB are not stored. Uploads are limited to 100 MB by the image's PHP settings and to 50 MB per attachment by BookStack's default.
- Sessions, caches, logs and custom themes are not kept. After a restart everyone signs in again.
- Removing the enrollment removes its storage. Enrolling again starts with an empty BookStack, a new address and new passwords.

## Cost and size

Each of the two containers (BookStack and MariaDB) runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for both for as long as the instance runs, including idle time. In a local check with those limits BookStack used about 60 MiB idle and up to about 90 MiB while pages were edited, searched and exported to PDF, and MariaDB about 110 MiB, up to about 125 MiB. A first start took 26 seconds on half a core. A wiki with many simultaneous editors may need more than this size offers. Labs adds no markup and receives no seller payout.
