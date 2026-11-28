# Blinko Note Server

Each enrollment runs a private [Blinko](https://blinko.space/) with its own PostgreSQL database. Blinko is written and maintained by [blinkospace](https://github.com/blinkospace) and contributors and is released under the GPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `blinkospace/blinko` image (version 1.8.9) and the official `postgres:16-alpine` image (PostgreSQL license), both pinned by digest, and the platform runs one isolated pair of containers per enrollment.

## Set up

1. Enroll in **base**. The enrollment asks for access to its own storage (`service:storage`, read and write). Approve it, or the instance does not start.
2. The form shows an **Administrator name** (default `admin`), a generated **Administrator password**, a **Token signing secret** and a **Database password**. Keep the generated values or enter your own. Save the administrator password; all four are also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. Blinko starts after its database, so the first start takes a minute or two.
4. Open the address and sign in with the administrator name and password.

Blinko normally lets the first visitor register and become the administrator. Because the address is public, this instance creates the administrator itself at start, from the name and password you gave, and Blinko then refuses further registration. Only users the administrator creates inside Blinko can sign in. The name and password are used only when Blinko first creates its database; after that the stored users apply, and you change the password in Blinko's own settings.

## Use it

Write a note in the editor; use `#tag` or `#parent/child` for tags, drag in a file or image to attach it, and search from the top bar. Blinko's [documentation](https://docs.blinko.space/en/introduction) covers the daily review, sharing a note by link, and the settings page. For the HTTP API, create an access token in **Settings** and send it as `Authorization: Bearer <token>`; the instance serves its own API description at `/api/openapi.json`. Blinko's AI features, S3 storage and single sign-on are off until you configure them in its settings; the AI features need an AI provider of your own.

## Authentication

Blinko checks every request itself: the web interface and the API need your sign-in or an access token. Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong. A note you share by link is readable by anyone with that link. UnitySVC adds no other gate.

## What is kept, and what is lost

Two folders of the enrollment's storage are persistent: a backup of the PostgreSQL database (your notes, tags, users and settings) and Blinko's files folder (uploaded attachments). The database itself runs on temporary disk; the instance writes a backup of it every five minutes and once more when it stops, and restores that backup when it starts. The platform copies both folders to storage about every 30 seconds while the instance runs and once more when it stops. Stopping therefore takes a moment longer, and the instance shows as `draining`.

- The data belongs to this enrollment's storage. It survives stopping and restarting the instance, but removing the enrollment removes it, and a new enrollment starts empty. Copy out what you want to keep first.
- A normal stop loses nothing. A crash, or a node failure, can lose the notes and changes made since the last backup: up to five minutes, plus up to 30 seconds for attachments.
- The backup is one file and must stay under 1 GiB, the largest file the platform's storage copy keeps. A database of notes is far below that; attachments are stored separately and do not count.
- Attachments are copied, never deleted from storage: a file that Blinko removes can come back after a restart.
- Keep the **Database password** as it is. It is used only between the two containers of your instance; a changed value takes effect at the next start after a stop, not while the instance runs.
- Changing the **Token signing secret** signs everyone out and invalidates access tokens.
- Empty files, symbolic links and files over 1 GiB are not stored.

## Cost and size

Both containers run on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk each) and you pay the platform's cost for both for as long as the instance runs, including idle time. In a local check Blinko used about 190 MiB and PostgreSQL about 60-75 MiB. Labs adds no markup and receives no seller payout.
