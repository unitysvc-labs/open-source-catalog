# SilverBullet Markdown Notes

Each enrollment runs a private [SilverBullet](https://silverbullet.md/) server. SilverBullet is written and maintained by [Zef Hemel](https://github.com/zefhemel) and contributors and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `ghcr.io/silverbulletmd/silverbullet` image (version 3.0.0, the slim variant without Chromium, pinned by digest), and the platform runs one isolated instance per enrollment. The slim image has no Chromium, so SilverBullet's optional Runtime API is not available.

Your server configuration, pages and attachments are kept in the `silverbullet` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `silverbullet/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one SilverBullet instance at a time.
2. The form shows a **Sign-in name** (default `admin`) and a generated **Sign-in password**. Save them; they are also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so anything that points at the old one needs the new one.
4. **Complete the one-time upgrade on a new instance.** Opening the address on a brand-new instance shows the text "This SilverBullet server needs a one-time upgrade". Open `https://<instance>/.setup/migrate/`, sign in with the sign-in name and password, leave the suggested settings (space name `Notes`, no access for visitors without an account), tick "I have a backup of this folder" (the folder holds only the starter page) and press **Migrate**. This turns the folder into SilverBullet's multi-space layout and creates the administrator account with your name and password. Then open the address again and sign in to your space.

Why this extra step: SilverBullet 3 starts an empty data folder in a setup wizard that has no password, where the first visitor creates the administrator, and it ignores `SB_USER` there. To avoid that, the recipe writes one starter page into an empty data folder before SilverBullet starts. A folder with a page but no configuration is treated as an older single-space install, which SilverBullet serves only behind the `SB_USER` name and password until it is migrated. Without the password, the instance would be open to anyone who reaches its address: the first visitor to the setup wizard would become the administrator.

On a later start, when the data already exists, none of this happens: the instance starts directly at the sign-in page. The sign-in name and password parameters are then ignored (SilverBullet logs "SB_USER is ignored"), so change the password in the Dashboard (`/.dashboard`), not in the enrollment.

## Use it

1. Sign in at `https://<instance>/`. The first page is `index`; use the document picker or `[[double brackets]]` to create and link pages. Pages are Markdown files in your space.
2. To add accounts or spaces, or to issue an API token, open the Dashboard at `https://<instance>/.dashboard` as the administrator.
3. For scripting access, sign in with an API token sent as `Authorization: Bearer <token>`; for example `GET /.fs/index.md` returns the `index` page. The [SilverBullet documentation](https://silverbullet.md/Administration/Server/Docker) describes the rest, including Space Lua.

## Authentication

SilverBullet checks every request itself. A visitor who is not signed in gets no access to the space (the migration chose "No access"), and there is no self-service sign-up: only accounts the administrator creates can sign in. Anyone who knows the instance address can reach the sign-in page, so keep the password strong. UnitySVC adds no other gate. Do not change the space's access for visitors to read or write unless you want it public.

## What is kept, and what is lost

The data folder is persistent: the configuration (`users.json`, `spaces.json`), the space's pages and attachments under `spaces/`, and the search index. They are stored in `silverbullet/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before SilverBullet starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. A page you delete can come back after a restart.
- Do not edit the files in `silverbullet/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `silverbullet/` folder yourself when you no longer want the data. Delete the whole folder, not parts of it.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. SilverBullet used about 20 MiB in a local check with a small space; a large space and its search index use more. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
