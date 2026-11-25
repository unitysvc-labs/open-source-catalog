# Memos Note-Taking App

Each enrollment runs a private [Memos](https://usememos.com/) server. Memos is written and maintained by the [usememos project](https://github.com/usememos/memos) and contributors and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `neosmemo/memos` image (version 26.11.2, pinned by digest), and the platform runs one isolated instance per enrollment.

Your notes, attachments and users are kept in the `memos` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. It has no settings to fill in. The enrollment asks for access to the `memos/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Memos instance at a time.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so anything that points at the old one needs the new one.
3. **Open the address and register your account immediately.** On a new instance the first account registered becomes the administrator, and there is no password to protect that step. Anyone who reaches the address before you could register first and take the administrator account. If that happens, stop and remove the instance, delete the `memos/` folder of your home, and enroll again.
4. After you have registered, open the instance settings and turn on the option that disallows user registration, so that nobody else can create an account. Through the API this is the `disallowUserRegistration` field of the `instance/settings/GENERAL` setting; with it on, a new sign-up is refused ("user registration is not allowed"). Leave registration open only if you want others to sign up.

## Write and read notes

1. In the web interface type a note in Markdown; use `#tags` to organise it, and set its visibility (private by default).
2. To use the REST API, create an access token in your account settings, or sign in with `POST /api/auth/signin`, then send the token as a bearer header:

   ```bash
   curl -X POST "https://<instance>/api/memos" \
        -H "Authorization: Bearer <access token>" \
        -H "Content-Type: application/json" \
        -d '{"content": "Buy milk #todo", "visibility": "PRIVATE"}'
   ```

3. `GET /api/memos` lists notes. Without a token the API answers 401. The [Memos documentation](https://usememos.com/docs) describes the rest.

## Authentication

Memos checks every request itself: the web interface needs your sign-in and the API needs an access token. Anyone who knows the instance address can reach the sign-in page, so use a strong password and keep tokens private, and turn off registration as described above. UnitySVC adds no other gate.

## What is kept, and what is lost

Memos's data folder is persistent: the SQLite database (users, notes, settings) and uploaded attachments. They are stored in `memos/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before Memos starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a note just written. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file Memos removes, such as a deleted attachment, can come back after a restart.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Memos and this keeps the stored database consistent.
- Do not edit the files in `memos/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `memos/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Memos used about 70 MiB in a local check. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
