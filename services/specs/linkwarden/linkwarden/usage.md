# Linkwarden Bookmark Manager and Page Archive

Each enrollment runs a private [Linkwarden](https://linkwarden.app) with its own PostgreSQL database. Linkwarden is written and maintained by [Daniel31x13](https://github.com/daniel31x13) and contributors and is released under the AGPL-3.0 license; the provider of this service is its author, who was not asked to take part, and nothing here implies endorsement or support. UnitySVC Labs lists the official `ghcr.io/linkwarden/linkwarden` image (version 2.17.0) and the official `postgres:16-alpine` image (PostgreSQL License), both pinned by digest, and the platform runs one isolated stack per enrollment. Linkwarden's own paid cloud service is a different product; this is the self-hosted software.

## Set up

1. Enroll in **base**. The enrollment asks for access to its own storage (`service:storage`, read and write). Approve it, or the instance does not start.
2. The form shows an **Administrator name** (default `admin`), a generated **Administrator password**, a **Session signing secret**, a **Database password** and an **Instance address**. Keep the generated values or enter your own. The name and password create the first account the **first time** Linkwarden runs on the data, when its database has no users; afterwards they are ignored and you change the password in Linkwarden itself. Save the password and the secrets now: the platform keeps them as secrets and does not show them again. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. Linkwarden starts after its database and applies its database migrations first, so the first start takes a minute or two. **A new enrollment has a new address and empty data.**
4. Open the address and sign in with the administrator name and password.
5. Replace **Instance address** with that address, without a trailing slash, for example `https://abc123.example.app`, and save. It starts as the placeholder `https://instance.invalid` (the platform needs a value there). Saving restarts the instance; your data and your session stay. See **Address** below for what works before you do.

Linkwarden normally lets anyone who reaches it register, and treats the first account as the administrator. Because the address is public, this instance creates that first account itself at start, from the name and password you gave, before it listens on the network, and public registration is switched off: the **Register** page says so and the registration API answers `Registration is disabled.` The administrator adds other users under **Server Administration > User Administration** in the profile menu.

## First use

1. Choose **New Link**, paste an address and pick a collection. Linkwarden opens the page in the headless browser inside the instance and, within a minute or so, keeps a screenshot, a PDF, a single-file HTML copy and a readable text version. Open the link's menu to see each preserved format. Pages that need a login or block automated browsers may be saved only in part.
2. Organise links in collections and sub-collections, add tags, pin links to the dashboard, and highlight or annotate text in the reader view.
3. Import bookmarks from a browser export or another tool under **Settings > Import & Export**. The instance archives two pages at a time, so a large import takes a while to be fully preserved.
4. For the browser extension, the mobile app or your own scripts, create a token under **Settings > Access Tokens** and send it as `Authorization: Bearer <token>`; give the extension your instance address. The [Linkwarden documentation](https://docs.linkwarden.app) describes the API.

## Address

Linkwarden does not find out its public address from the requests it receives: its sign-in library uses the fixed `NEXTAUTH_URL` setting, which this recipe builds from **Instance address**, and a new enrollment gets a new address that is not known in advance. With the placeholder still in place, a local check with a real browser behind an HTTPS proxy showed:

- **Works:** signing in (and refusing a wrong password), the web interface, saving and archiving links, creating users, changing a password and the API, all at the real address.
- **Wrong until you set it:** **Logout** signs you out but then sends the browser to `https://instance.invalid`, which shows an error page; go back to your instance address by hand. Single sign-on, if you were to configure it, needs the real address too.

After you set the real address, Logout returns to the sign-in page. A new enrollment has a new address, so set it again.

## Authentication

Linkwarden checks every request itself: the web interface and the API need your sign-in or an access token, and answer `401` without one. Anyone who knows the instance address can reach the sign-in page, so keep the passwords strong. A collection you make public is readable, with its preserved pages, by anyone who has its link. UnitySVC adds no other gate. The database is reachable only from inside the instance.

## What is not included

- **No email.** The instance has no mail server and none is configured, so Linkwarden sends no password-reset or verification mails, and the **Forgot password** page has no effect. A user who knows the current password changes it under **Settings > Password**; for a forgotten one, the administrator deletes and re-creates the account under **Server Administration > User Administration** in the profile menu. Keep the administrator password safe: there is no way to reset it from outside.
- **No Meilisearch.** Upstream's Compose file adds a Meilisearch container for search. This recipe leaves it out to keep the stack to two containers. Search still works, through the database: it finds links whose name, address, description or tags contain the words you type. What you lose is search inside the saved text of the pages, Meilisearch's typo-tolerant ranking and its advanced search operators.
- **No AI tagging, single sign-on or S3 storage.** These need settings this recipe does not expose.

## What is kept, and what is lost

Two folders are persistent: a backup of the PostgreSQL database (links, collections, tags, highlights, users, access tokens and settings) and Linkwarden's data folder (the preserved copies of your pages, uploaded files and avatars). They are stored in the enrollment's storage. The database itself runs on temporary disk; the instance writes a backup of it every five minutes and once more when it stops, and restores that backup when it starts. The platform copies both folders to storage about every 30 seconds while the instance runs and once more when it stops. Stopping therefore takes a moment longer while the backup and the copy finish.

- A normal stop loses nothing. A crash, or a node failure, can lose the links and changes made since the last backup, up to five minutes. Export your links under **Settings > Import & Export** regularly if you cannot lose them.
- The backup is one file and must stay under 1 GiB, the largest file the platform's storage copy keeps. Linkwarden stores the readable text of every saved page in the database, so a collection of many tens of thousands of links can approach that; the preserved screenshots, PDFs and HTML copies are stored separately and do not count.
- Preserved copies are copied, never deleted from storage: the files of a link you delete stay in storage and come back to the data folder after a restart. Linkwarden no longer shows them, but they still take space.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Keep the **Database password** as it is. Changing the **Session signing secret** signs everyone out and invalidates access tokens.
- Removing the enrollment removes its storage. Enrolling again starts with an empty Linkwarden, new passwords and a new address.

## Cost and size

Linkwarden runs on the `small` size (one core, 2 GiB) because of its bundled headless browser, and PostgreSQL on the `nano` size (half a core, 512 MiB). You pay the platform's cost for both for as long as the instance runs, including idle time. In a local check with those limits Linkwarden used about 350 to 450 MiB idle and up to about 1.1 GiB while archiving two large pages at once, and PostgreSQL 55 to 90 MiB. Very large pages can need more memory than this size has; such a page may fail to archive, and Linkwarden then keeps the link without its copies. Labs adds no markup and receives no seller payout.
