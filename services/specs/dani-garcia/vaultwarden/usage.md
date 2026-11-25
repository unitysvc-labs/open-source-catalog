# Vaultwarden Password Manager Server

Each enrollment runs a private [Vaultwarden](https://github.com/dani-garcia/vaultwarden) server. Vaultwarden is written and maintained by [Daniel García](https://github.com/dani-garcia) and contributors and is released under the AGPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `vaultwarden/server` image (version 1.37.5, alpine variant, pinned by digest), and the platform runs one isolated instance per enrollment.

**Vaultwarden is unofficial.** It is an independent, community-written server that is compatible with the Bitwarden client API. It is not a Bitwarden product, it is not made, reviewed or supported by Bitwarden, Inc., and it is not affiliated with it. Use the Vaultwarden wiki, discussions and issue tracker for help, never Bitwarden's support. The author of Vaultwarden was not asked to take part in this listing, and nothing here means the author endorses it or supports it.

Your vault is kept in the `vaultwarden` folder of your **home**, not in the enrollment. It survives stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## What protects your secrets

A password manager holds your most sensitive data, so be clear about what protects it.

- **The vault is encrypted by the client, not by the server.** The Bitwarden web vault, browser extension and apps derive a key from your master password on your device and encrypt every item before sending it. The server, the platform and UnitySVC Labs never receive your master password or the key. What is stored is ciphertext.
- **The copy in your home holds only that ciphertext, plus the server's own RSA keys.** The `vaultwarden` folder contains `db.sqlite3` (your users, encrypted items, folders, organizations, and metadata such as emails, item counts and sign-in times) and `rsa_key.pem`, the key Vaultwarden uses to sign sign-in tokens. Anyone who could read that folder and your instance could mint tokens, but still could not read your items without your master password. A weak master password is the weak point: an attacker with the database can try to guess it offline, so choose a long one.
- **What is not encrypted.** Email addresses, the names of organizations and the size and timing of your activity are visible to the server and in the database. Attachments are encrypted by the client, like the items.
- **The admin page is powerful.** Whoever has the admin token can invite and delete users and change server settings. Keep the token private.
- UnitySVC adds no other gate in front of the instance: anyone who knows the address can reach the sign-in page. Vaultwarden checks every request itself.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `vaultwarden/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Vaultwarden instance at a time.
2. The form has three settings. **Admin token** is generated; keep it or enter your own, and save it (it is also shown in the enrollment's instance details). It is not your UnitySVC API key. **Allow open sign-ups** defaults to `false`. **Instance address** is a placeholder, because the address does not exist yet.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Edit the enrollment and set **Instance address** to that address, for example `https://abc123.example.app`, with no trailing slash. The instance restarts and keeps your data. Until you do, sign-up, sign-in and storing items work, but passkey and security-key (WebAuthn) two-step login are expected not to, and links Vaultwarden builds point at the placeholder. After you change the address, devices that were signed in are expected to sign in again.
5. Create your own account. With sign-ups closed, open `https://<instance>/admin`, enter the admin token, choose **Users**, then **Invite User** and enter your email. No email is sent, because no mail server is configured: just open the instance address, choose **Create account** with that same email, and set your master password. (Alternatively set **Allow open sign-ups** to `true`, create your account, then set it back to `false`; while it is `true`, anyone who finds the address can register.)
6. In a Bitwarden client, choose **Self-hosted** on the sign-in screen, enter the instance address as the server URL, and sign in with your email and master password. The web vault at the instance address works in the browser with no client install.

**Write your master password down somewhere safe.** Nobody, including the platform, can recover it, and without it the vault cannot be decrypted. There is no email, so the password hint and the email verification features are not available.

## Authentication

Sign-in to the vault uses the email and master password you registered. The admin page uses the admin token. A plain admin token works, but Vaultwarden logs a notice that it is insecure because it is stored as typed; upstream recommends an Argon2 PHC string (generate one with `docker run --rm -it vaultwarden/server /vaultwarden hash`, then paste the `$argon2id$...` string as the Admin token and sign in with the password you hashed). The generated token is high-entropy, so it is a reasonable default, but it is visible in the enrollment's instance details; the hashed form is not.

## What is kept, and what is lost

Vaultwarden's data folder is persistent: the SQLite database, the RSA keys, attachments, Sends and the icon cache. The platform restores them before Vaultwarden starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which can include an item you just saved. A normal stop loses nothing. After saving something important, wait a minute before relying on it.
- The instance runs with `ENABLE_DB_WAL=false`, so the database is one self-contained file and the copy in your home is complete. The temporary files `*-wal` and `*-shm` are not stored.
- Files are copied, never deleted from your home. An attachment you delete can come back after a restart. This is cosmetic: the item that referred to it is gone.
- Do not edit the files in `vaultwarden/` while the instance is stopped: the next start restores them over what you changed.
- If you save settings on the admin page, Vaultwarden writes them to `config.json` in the data folder, and they then take precedence over the enrollment settings (according to the upstream documentation; not checked here).
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `vaultwarden/` folder yourself when you no longer want the data. Export your vault from the client before you do.
- Keep a regular encrypted export of your vault from the client as a backup of your own.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Vaultwarden used about 50 MiB in a local check. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
