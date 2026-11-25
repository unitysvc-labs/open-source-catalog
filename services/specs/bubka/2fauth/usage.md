# 2FAuth Two-Factor Authentication Manager

Each enrollment runs a private [2FAuth](https://2fauth.app/) server. 2FAuth is written and maintained by [Bubka](https://github.com/Bubka) and contributors and is released under the GNU Affero General Public License v3.0; the provider of this service is its author. UnitySVC Labs lists the official `2fauth/2fauth` image (version 9.0.3, pinned by digest), and the platform runs one isolated instance per enrollment.

Your 2FA accounts, users and settings are kept in the `2fauth` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data, provided it has the same encryption key (see below).

## Read this first: what protects your secrets, and what does not

2FAuth stores the secrets that generate your one-time codes. Whoever can read them can produce your codes, so know what stands between them and a reader.

What protects them:

- **Sign-in.** Every page and API call needs a signed-in user. Passwords are stored hashed. 2FAuth signs you out after a period of inactivity.
- **HTTPS.** The platform serves the instance over HTTPS, so secrets are not sent in clear over the network.
- **Optional encryption in the database.** 2FAuth can encrypt account secrets with the instance's `APP_KEY` before writing them to its database. **It is off by default.** Turn it on in the administration settings, **Protect sensitive data** (see "First use"). In a local check, with it off the secret was stored in the database as plain text; with it on, it was stored encrypted.

What does not protect them:

- **The copy in your home is not encrypted by this recipe.** The platform stores the database file (`database.sqlite`) in the `2fauth/` folder of your home as an ordinary file. Anyone who can read your home folder can read that file. If 2FAuth's encryption is off, the secrets in it are plain text. If it is on, they are encrypted, but only with the key described below.
- **The key is not kept apart from the data.** `APP_KEY` is an enrollment parameter, held by the platform and shown in the instance details. Encryption protects against someone who gets the database file without the key; it does not protect against someone who can read both, and it does not hide the secrets from the running instance, which must decrypt them to show codes.
- **The address is public.** Anyone who knows the instance address can reach the sign-in and registration pages (see below).
- **No separate second factor is added.** Your sign-in password is the barrier. Use a long, unique one. 2FAuth can also sign in with a security key (WebAuthn) once the instance address is set (see `APP_URL`).

Treat this as a convenience service, not a vault. Keep an export of your accounts (2FAuth's Export option) somewhere safe, and remember an export is a plain file of your secrets, so store it as carefully as the service itself, and keep backup codes from each service.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `2fauth/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one 2FAuth instance at a time.
2. The form shows an **Encryption key (APP_KEY)** and an **Instance address (APP_URL)**.
   - **APP_KEY** is generated for you: exactly 32 characters (letters, digits, `-` and `_`). You can enter your own, either 32 characters or a Laravel key of the form `base64:` followed by 44 characters. It signs your sessions and sign-in tokens and encrypts stored secrets when encryption is on. **Save it.** It is also shown in the enrollment's instance details, but your data outlives the enrollment: when you enroll again the form generates a **new** key, and you must replace it with your saved one. If the key differs from the one the data was written with, everyone is signed out and, when encryption is on, the stored secrets cannot be read (2FAuth shows them as `indecipherable` and refuses to produce codes). Going back to the original key restores access. The key lives only in the enrollment parameters; it is not stored in your home.
   - **APP_URL** starts as the placeholder `https://instance.invalid`, because the platform needs a value before the instance exists. Once the instance is created, copy its address from the instance details, put it here and save; this restarts the instance and keeps your data. The instance works without it (sign-in and codes do not need it). 2FAuth uses it to build links and for security-key (WebAuthn) and single sign-on, which need it to match the address you use; those were not tested here.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so bookmarks, the home-screen app and anything that points at the old one need the new one.

## First use

1. Open the address. 2FAuth shows its sign-in page with a **Register** option. **The first account you register becomes the administrator.** Register immediately after the instance is ready, because until the first account exists anyone who finds the address could take it.
2. **Close registration.** In 2FAuth, open **Admin**, then **Authentication**, and turn on **Disable registration**. Registration stays open after the first account, in a local check a second visitor could create their own account until it was turned off, and 2FAuth has no setting in this recipe to start it closed. Each user has their own accounts, but anyone who registers would use your instance.
3. Under **Admin**, **App setup**, turn on **Protect sensitive data** if you want secrets encrypted in the database. Turning it on encrypts the secrets already stored; turning it off decrypts them again. Do this before you add accounts if you can.
4. Add an account: scan or upload a QR code, paste an `otpauth://` link, or fill in the form. Select an account to see its current code.

Sign-in is by email address and password; the email address is only a login name here, because no mail server is configured, so 2FAuth cannot send a reset mail. If you forget the password, the administrator can manage users under **Admin**, **Users**; this was not tested. Your data stays in your home.

## What is kept, and what is lost

2FAuth's data folder is persistent: the SQLite database (users, accounts, groups, settings), the keys it signs sign-in tokens with, uploaded icons and session files. They are stored in `2fauth/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before 2FAuth starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include an account you just added. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file 2FAuth removes, such as an old icon, can come back after a restart. This is cosmetic.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by 2FAuth and this keeps the stored database consistent.
- Do not edit the files in `2fauth/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `2fauth/` folder yourself when you no longer want the data, which also removes the stored copy of your secrets.

Changing `APP_URL` restarts the instance; your data stays. Changing `APP_KEY` also restarts it, but see the warning above before you do.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. 2FAuth used about 130 to 145 MiB in a local check, under a 512 MiB limit. Reading a QR code from an uploaded image can use much more memory in PHP; this was not tested, and if it fails use the form or paste the `otpauth://` link instead. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
