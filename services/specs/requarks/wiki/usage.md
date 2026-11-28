# Wiki.js 2 Wiki and Documentation Site

Each enrollment runs a private [Wiki.js](https://js.wiki) server. Wiki.js is written and maintained by [requarks.io](https://requarks.io) (Nicolas Giard and contributors) and is released under the AGPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `ghcr.io/requarks/wiki` image (version 2.5.317, pinned by digest), and the platform runs one isolated instance per enrollment.

This is the **2.x** line, which upstream still maintains in [requarks/wiki-v2](https://github.com/requarks/wiki-v2), running on its embedded **SQLite** database. That suits one person or a small team. Upstream does not recommend SQLite for production deployments, and Wiki.js 3 runs on PostgreSQL only, so this instance cannot be upgraded in place to 3.x.

Your wiki is kept in the `wikijs` folder of your **home**, not in the enrollment. It survives stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `wikijs/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Wiki.js instance at a time.
2. The form shows an **Administrator email** (default `admin@example.com`; it is only a sign-in name, no mail is sent) and a generated **Administrator password**. They create the administrator account the **first time** Wiki.js runs on your data. If the database already exists, because you enrolled before or restarted, the parameters are ignored and the existing password still applies; change it in your Wiki.js profile. Save the password now: the platform keeps it as a secret and does not show it again. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Open the address. Wiki.js normally starts with a setup wizard in which the first visitor creates the administrator; here the instance completes that wizard itself, with your email and password, before it is reachable, so you see the welcome page instead. Choose **Login**, sign in, and create the home page.
5. Optional: in **Administration > General**, set **Site URL** to the instance address. It starts as the placeholder `https://wiki.invalid`, because the address is not known when the wizard runs. Signing in, editing and uploads work without it; the Site URL is used for the page address in link previews, for links in comments, and for the callback address of external sign-in providers. Set it again after a new enrollment.

## Who can read the wiki

**A new Wiki.js lets anyone read its pages.** The built-in **Guests** group, which stands for visitors who are not signed in, may read all pages, assets and comments, so anyone who knows the instance address can read what you publish. To make the wiki private, open **Administration > Groups > Guests** and remove its permissions or its page rule; visitors are then sent to the sign-in page. Writing, uploading and the administration area always need an account with the matching permission.

## Use it

- **Write pages** with the Markdown editor, the visual editor or raw HTML. A page has a path, a title, tags and a full history; the page tree and the navigation are built from the paths.
- **Upload images and files** in the editor's asset manager. They are stored in the database with the pages.
- **Search** covers page titles, descriptions and paths (the built-in "Database - Basic" engine). Full-text search needs PostgreSQL or an external search service, which this recipe does not include.
- **Users and groups** are managed in **Administration**. Self-registration is off. Invitations, password-reset and verification mails are **not sent**, because the instance has no mail server: create users with a password you give them, or configure your own SMTP server in **Administration > Mail**.
- **GraphQL API.** Enable the API and create a key in **Administration > API Access**, then:

  ```bash
  curl -H "Authorization: Bearer <api-key>" -H "Content-Type: application/json" \
       -d '{"query":"{ pages { list { id path title } } }"}' \
       https://<instance>/graphql
  ```

The [Wiki.js 2 documentation](https://docs.requarks.io/) describes the editors, permissions, storage targets and the API.

## Authentication

Wiki.js checks every request itself, with its own accounts, groups and page rules; UnitySVC adds no other gate. Reading is open to visitors until you change the Guests group as described above. Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong.

## What is kept, and what is lost

The SQLite database (`wiki.sqlite`) is persistent. It holds everything: pages and their history, uploaded assets, users, groups, API keys, the signing keys that keep you signed in, and all settings. It is stored in `wikijs/` in your home, where you can see it in your files while the instance is stopped. The platform restores it before Wiki.js starts, copies it back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- **Keep the database under 1 GiB.** Files over 1 GiB are not stored, and uploads are inside the database, so a wiki with many large uploads would stop being saved. Keep large files elsewhere and link to them.
- SQLite's temporary files (`*-journal`, `*-wal`, `*-shm`) are not stored. They are rebuilt by Wiki.js and this keeps the stored database consistent.
- Do not edit the files in `wikijs/` while the instance is stopped: the next start restores them over what you changed.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `wikijs/` folder yourself when you no longer want the data. To start again with an empty wiki and a new administrator, stop the instance and delete that folder first.
- Only the database is kept. A local folder you configure in Wiki.js for the **Local File System** or **Git** storage targets, and the page cache, are temporary and are lost when the instance stops; a Git storage target is cloned again from its remote.

## Limits of SQLite

- Several people saving pages at the same moment can collide: in a local check with five saves at once, two pages were stored but showed "Page has no rendered version" until they were opened in the editor and saved again. One or two editors at a time had no such problem.
- High availability, PostgreSQL full-text search and an in-place upgrade to Wiki.js 3 are not available.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check Wiki.js used about 135 MiB idle and up to 280 MiB with two pages being saved at once; every page being saved at the same moment adds about 65 MiB. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
