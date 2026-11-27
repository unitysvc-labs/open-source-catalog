# Forgejo Self-Hosted Git Forge

Each enrollment runs a private [Forgejo](https://forgejo.org/) server. Forgejo is written and maintained by the Forgejo Authors and contributors, under the umbrella of Codeberg e.V., and is released under the GNU General Public License, version 3 or later (GPL-3.0-or-later); the provider of this service is its author. UnitySVC Labs lists the official `codeberg.org/forgejo/forgejo` rootless image (version 17.0.2, pinned by digest), and the platform runs one isolated instance per enrollment.

Why the rootless image: it runs as the unprivileged user `git` (uid 1000) from the start and keeps everything in one folder, which suits the platform, instead of starting as root and dropping privileges.

**Git over SSH is not available.** The platform exposes one HTTPS entry per instance, so Forgejo's SSH server is switched off. Clone, fetch and push over HTTPS (`https://<instance>/<owner>/<repo>.git`) with your user name and password or an access token. SSH keys you add in the settings do nothing.

Your users, repositories, issues and settings are kept in the `forgejo` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `forgejo/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Forgejo instance at a time.
2. The form shows an **Administrator name** (default `owner`), an **Administrator email**, a generated **Administrator password**, a **Secret key**, an **Internal token** and an **Instance address**. Forgejo reserves the name `admin` and a few others (`user`, `org`, `repo`, ...), so the form refuses them. The administrator is created the **first time** Forgejo runs on your data, when it creates its database. If a database is already there, because you enrolled before or restarted, the three administrator values are ignored and the existing password still applies; change it in Forgejo's own settings. Keep the secret key: Forgejo encrypts values such as two-factor secrets with it, so replacing it later, or enrolling again with a newly generated one, makes those values unreadable. Save the password and the secret key now: the platform keeps them as secrets and does not show them again. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready (under 10 seconds in a local check). Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so remotes and scripts that point at the old one need the new one.
4. Open the address and sign in with the administrator name and password. There is no installation wizard: it is already done.
5. Replace **Instance address (ROOT_URL)** with that address, for example `https://abc123.example.app/`, and save. It starts as the placeholder `https://instance.invalid/` (the platform needs a value there). Saving restarts the instance; your data stays. Do this again after every new enrollment. See **Address** below for what works before you do.

## Create a repository and push

1. In the web interface choose **+** then **New repository**, or create one with the API:

   ```bash
   curl -u owner:<password> -X POST https://<instance>/api/v1/user/repos \
        -H 'Content-Type: application/json' -d '{"name":"demo"}'
   ```

2. Push an existing project over HTTPS:

   ```bash
   git remote add origin https://<instance>/owner/demo.git
   git push -u origin main
   ```

   Git asks for the user name and password. For scripts, create an access token in **Settings, Applications** and use it as the password.
3. Other users: public registration is switched off, so create them in **Site administration, User accounts**.

## Address

Forgejo does not find out its public address from the requests it receives: it uses the fixed `ROOT_URL` setting, and a new enrollment gets a new address that is not known in advance. With the placeholder still in place, a local check behind an HTTPS proxy showed:

- **Works:** signing in, the web interface, the REST API, and cloning, fetching and pushing over HTTPS at the real address.
- **Wrong until you set it:** the clone address shown on a repository page and in API answers (it begins with `https://instance.invalid/`; use your instance address instead), user avatars and other absolute links, Git LFS transfers and the addresses Forgejo gives to web hooks and package clients. Administrators also see a notice that the instance is served from a different address than the configured one.

Forgejo sends no email from this instance (no mail server is configured), so password reset by email and notifications do not work. Changing your own password in **Settings, Account** and creating users as the administrator do not need email.

## Authentication

Forgejo checks every request itself. Anyone who knows the instance address can see the sign-in page and any repository you make public, so keep the administrator password strong and keep access tokens private. Public registration is switched off, so only users the administrator creates can sign in. UnitySVC adds no other gate.

## What is kept, and what is lost

Forgejo's folder is persistent: the SQLite database (`data/forgejo.db`), the Git repositories, `custom/conf/app.ini` (its configuration, with the signing keys Forgejo generates itself), attachments, avatars, packages and search indexes. They are stored in `forgejo/` in your home. The platform restores them before Forgejo starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a push just made. A normal stop loses nothing.
- **Files are copied, never deleted from your home.** A file Forgejo removes can come back after a restart: the files of a deleted repository stay in your home (Forgejo no longer lists the repository, but the space is not freed), and so do old pack files that Git has since repacked, old indexes and removed attachments. Delete such leftovers from `forgejo/` yourself, while the instance is stopped, if they matter.
- The database runs in SQLite's rollback-journal mode rather than Forgejo's default write-ahead mode, so that the stored `forgejo.db` holds all the data. SQLite's temporary files (`*-journal`, `*-wal`, `*-shm`) are not stored.
- Empty files and empty folders are not stored. Git needs a few empty folders in every repository; this recipe recreates them at each start, so a repository that had no commits when the instance stopped still works afterwards.
- Do not edit the files in `forgejo/` while the instance is stopped: the next start restores them over what you changed.
- Symbolic links and files over 1 GiB are not stored. A single file over 1 GiB in the data folder, such as a very large pack file, LFS object or package, therefore cannot be kept; keep repositories well below that size.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `forgejo/` folder yourself when you no longer want the data.
- Forgejo Actions has no runner here. Workflows need a separate Forgejo Runner that you operate elsewhere and register with this instance.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Forgejo used about 100 MiB idle and peaked at about 150 MiB while creating repositories and pushing 6 MB to them, in a local check with the same memory and CPU limits. Large repositories and many users need more than this size; this recipe offers only `nano`. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
