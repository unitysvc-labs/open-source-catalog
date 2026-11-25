# Gotify Notification Server

Each enrollment runs a private [Gotify](https://gotify.net/) server. Gotify is written and maintained by [Jannis Mattheis](https://github.com/jmattheis) and contributors and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `gotify/server` image (version 3.1.1, pinned by digest), and the platform runs one isolated instance per enrollment.

Your messages, applications and users are kept in the `gotify` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `gotify/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Gotify instance at a time.
2. The form shows an **Administrator name** (default `admin`) and a generated **Administrator password**. They create the administrator account the **first time** Gotify runs on your data. If the database already exists, because you enrolled before or restarted, the parameters are ignored and the existing password still applies; change it in Gotify's own settings. Save the values; they are also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so apps and scripts that point at the old one need the new one.
4. Open the address and sign in with the administrator name and password.

## Send and read messages

1. In the web interface open **Apps**, create an application, and copy its token.
2. Send a message with that token:

   ```bash
   curl "https://<instance>/message?token=<application token>" \
        -F "title=Backup finished" -F "message=All 12 volumes are saved." -F "priority=5"
   ```

3. The message appears in the web interface at once. To read messages elsewhere, create a **client** in the web interface and give its token, with the instance address, to the Gotify Android app or to the command-line client; the [Gotify documentation](https://gotify.net/docs/) describes both, and the WebSocket stream (`/stream?token=<client token>`).

## Authentication

Gotify checks every request itself: the web interface needs your sign-in, sending needs an application token, and reading needs a client token. Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong and keep tokens private. Public registration is switched off, so only users you create can sign in. UnitySVC adds no other gate.

## What is kept, and what is lost

Gotify's data folder is persistent: the SQLite database (users, applications, clients, messages) and the images you upload for applications. They are stored in `gotify/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before Gotify starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a message just sent. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file Gotify removes, such as an old application image, can come back after a restart. This is cosmetic.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Gotify and this keeps the stored database consistent.
- Do not edit the files in `gotify/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `gotify/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Gotify used about 50 MiB in a local check. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
