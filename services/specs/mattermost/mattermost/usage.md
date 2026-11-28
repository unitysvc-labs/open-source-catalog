# Mattermost Team Edition Chat Server

Each enrollment runs a private [Mattermost](https://mattermost.com/) server with its own PostgreSQL database. Mattermost is written and maintained by [Mattermost, Inc.](https://github.com/mattermost) and contributors; the provider of this service is its author, who was not asked to take part. This service runs **Team Edition**, the open-source edition: Mattermost, Inc. releases its compiled Team Edition builds under the [MIT license](https://github.com/mattermost/mattermost/blob/master/LICENSE.txt) (the source code is AGPL-3.0, with Apache-2.0 parts). UnitySVC Labs lists the official `mattermost/mattermost-team-edition` image (version 12.1.0) and the official `postgres` image (17, Alpine, PostgreSQL License), both pinned by digest, and the platform runs one isolated stack per enrollment. Features that need a Mattermost commercial license are not part of Team Edition, and some of the plugins shipped in the image stay inactive without one.

## Set up

1. Enroll in **base**. The enrollment asks for access to its own storage (`service:storage`, read and write). Approve it, or the instance does not start.
2. The form shows an **Administrator name** (default `admin`), an **Administrator email** (default `admin@example.com`; enter your own if you like), a generated **Administrator password** and a generated **Database password**. Save the administrator password when you enroll: the platform keeps it as a secret and does not show it again. These are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready; the first start takes a minute or two, because Mattermost can only start once its database answers and is restarted until it does. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address and empty data.**
4. Open the address and sign in with the administrator name (or email) and password.

Mattermost normally makes the first person who signs up the system administrator. Because the address is public, this instance creates that account itself, a few seconds after Mattermost starts, from the name, email and password you gave. After that Mattermost refuses sign-up without an invitation. The three values are used only on an empty database; later you change them in your Mattermost profile.

## First use

1. Mattermost asks you to create a team. Do so, then write in **Town Square**.
2. Open **System Console > Environment > Web Server** and set **Site URL** to the instance address (`https://<enrollment-code>.<apps-domain>`, no trailing slash). The instance does not know its address ahead of time. In a local check behind an HTTPS proxy, sign-in, posting, file upload and the live WebSocket connection worked with the Site URL empty, but Mattermost logs an error until it is set, and links it generates (invitations, notifications, integrations) and some plugins need it. The setting is kept. A new enrollment has a new address, so set it again there.
3. Invite people with **Invite People > Copy invite link** and send them the link yourself. A person who opens the link creates an account with an email address and password; the address is not verified. Without the link nobody can register.
4. To use the desktop or mobile app, enter the instance address as the server URL.

For the API, create a personal access token (enable them in **System Console > Integrations > Integration Management**, then **Profile > Security**) or a bot account, and send it as `Authorization: Bearer <token>`:

```bash
curl -H "Authorization: Bearer <token>" https://<instance>/api/v4/users/me
```

See the [Mattermost documentation](https://docs.mattermost.com) for webhooks, slash commands and administration.

## Email

The instance contains no mail server, and none is configured. Until you enter an SMTP server of your own in **System Console > Environment > SMTP**:

- **Forgot password** fails ("Failed to send password reset email"). A system administrator can set another user's password in **System Console > Users**. If you lose the only administrator password, there is no way to recover it from outside the instance.
- **Invite by email** reports success but sends nothing; use the invite link.
- Email notifications are not sent. Signing up, signing in and changing your own password or email address work without mail.

Whether the platform lets the instance reach your provider's SMTP port was not checked by Labs.

## Authentication

Mattermost checks every request itself: the web interface, the API and the WebSocket need a sign-in or a token. Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong and treat invite links as secrets: whoever has one can join that team. Incoming webhook URLs accept posts from anyone who knows them. UnitySVC adds no other gate. The database is reachable only from inside the instance.

## What is kept, and what is lost

Three folders are persistent, in the enrollment's storage: a backup of the PostgreSQL database (users, teams, channels, messages), Mattermost's `data` folder (uploaded files, profile pictures, installed plugin bundles) and its `config` folder (`config.json`, everything you set in the System Console). The database itself runs on temporary disk; the instance writes a backup of it every five minutes and once more when it stops, and restores that backup when it starts. The platform copies the folders to storage about every 30 seconds while the instance runs and once more when it stops. Stopping therefore takes a moment longer while the backup and the copy finish.

- A normal stop loses nothing. A crash, or a node failure, can lose the messages and changes made since the last backup: up to five minutes, plus up to 30 seconds for uploaded files.
- The backup is one file and must stay under 1 GiB, the largest file the platform's storage copy keeps. Message text is small and uploaded files are stored separately and do not count, but a large, busy server can reach it over time; this service suits a team of modest size.
- Files are copied, never deleted from storage: a file Mattermost deletes from its `data` folder (for example a removed plugin bundle or an attachment of a permanently deleted post) can come back on disk after a restart. Messages are in the database and are not affected.
- Keep the **Database password** as it is. It is used only between the two containers of your instance.
- Empty files, symbolic links and files over 1 GiB are not stored. Mattermost's default upload limit is 100 MB per file.
- Removing the enrollment removes its storage. Enrolling again starts with an empty server, a new address and new passwords.

## Cost and size

Mattermost runs on the `small` size (one core, 2 GiB of memory, 5 GiB of temporary disk) and PostgreSQL on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk). You pay the platform's cost for both for as long as the instance runs, including idle time. In a local check with those limits Mattermost used about 310 to 390 MiB with a handful of users and PostgreSQL about 60 MiB; Mattermost's own documentation asks for 2 GiB for a small team. Labs adds no markup and receives no seller payout.
