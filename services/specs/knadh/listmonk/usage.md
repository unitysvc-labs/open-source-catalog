# listmonk Newsletter and Mailing List Manager

Each enrollment runs a private [listmonk](https://listmonk.app/) with its own PostgreSQL database. listmonk is written and maintained by [Kailash Nadh](https://github.com/knadh) and contributors and is released under the AGPL-3.0 license; the provider of this service is its author, who was not asked to take part. UnitySVC Labs lists the official `listmonk/listmonk` image (version 6.2.0) and the official `postgres` image (17, Alpine), both pinned by digest, and the platform runs one isolated stack per enrollment. PostgreSQL is released under the PostgreSQL License.

## Set up

1. Enroll in **base**. The enrollment asks for access to its own storage (`service:storage`, read and write). Approve it, or the instance does not start.
2. The form shows an **Administrator name** (default `admin`), a generated **Administrator password** and a generated **Database password**. The administrator values create the Super Admin account the **first time** listmonk runs on the data; afterwards they are ignored and you change the password in listmonk itself. Save them; they are also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address and empty data.**
4. Open `https://<instance>/admin` and sign in with the administrator name and password.

## First use

1. In **Settings > SMTP** enter the SMTP server you send through (your mail provider's host, port and login). The instance contains no mail server and does not receive mail. Whether the platform lets the instance reach your provider's SMTP port was not checked by Labs; the connectivity test of your own server in Settings shows it.
2. In **Settings > General** set the **Root URL** to the instance address. listmonk puts it in the links of the unsubscribe and opt-in pages and of the mails it sends; the default `http://localhost:9000` is wrong here. A new enrollment has a new address, so set it again.
3. In **Settings > Media** keep the upload path `/listmonk/uploads`: only that folder is kept.
4. Create a list under **Lists**, add or import subscribers, create a campaign and send a test message before you send to the list.

The REST API needs an API user: create one under **Users** and call it with `Authorization: token <user>:<token>`. The administrator password does not work as an API credential. See the [listmonk documentation](https://listmonk.app/docs/) for the rest.

## Authentication

listmonk checks every request itself: the administration interface and the API need your sign-in or an API token. The public subscription form and the unsubscribe pages are open by design. Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong. UnitySVC adds no other gate. The database is reachable only from inside the instance.

## What is kept, and what is lost

Two folders are persistent: the PostgreSQL data directory (subscribers, lists, campaigns, users and settings) and listmonk's `uploads` folder. They are stored in the enrollment's storage. The platform restores them before the containers start, copies new and changed files back about every 30 seconds while the instance runs, and makes a last copy when it stops. Stopping therefore takes a moment longer while the copy finishes.

- The copy of a running database directory is taken file by file, not as a database backup. After a normal stop it is complete. After a crash, or a node failure, up to the last 30 seconds can be lost and PostgreSQL recovers from its write-ahead log on the next start; a copy taken at an unlucky moment is not guaranteed to recover. Export your subscribers and lists from listmonk (**Subscribers > Import / Export**) regularly if you cannot lose them.
- Files are copied, never deleted from storage. A file PostgreSQL removes, such as an old write-ahead segment, can come back after a restart; this is cosmetic.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Removing the enrollment removes its storage. Enrolling again starts with an empty listmonk and new passwords.

## Cost and size

Each of the two containers (listmonk and PostgreSQL) runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for both for as long as the instance runs, including idle time. In a local check with those limits listmonk used about 70 MiB and PostgreSQL about 35 MiB. Labs adds no markup and receives no seller payout.
