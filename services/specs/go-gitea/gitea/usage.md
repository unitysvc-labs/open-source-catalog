# Gitea Self-Hosted Git Service

Each enrollment runs a private [Gitea](https://about.gitea.com/) server. Gitea is written and maintained by the Gitea Authors and contributors and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `gitea/gitea` rootless image (version 28.4.0, pinned by digest), and the platform runs one isolated instance per enrollment.

Why the rootless image: it runs as the unprivileged user `git` (uid 1000) from the start and keeps everything in one folder, which suits the platform, instead of starting as root and dropping privileges.

**Git over SSH is not available.** The platform exposes one HTTPS entry per instance, so Gitea's SSH server is switched off. Clone, fetch and push over HTTPS (`https://<instance>/<owner>/<repo>.git`) with your user name and password or an access token. SSH keys you add in the settings do nothing.

Your users, repositories, issues and settings are kept in the `gitea` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `gitea/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Gitea instance at a time.
2. The form shows an **Administrator name** (default `admin`), an **Administrator email**, a generated **Administrator password**, a **Secret key** and an **Internal token**. The administrator is created the **first time** Gitea runs on your data. If that user already exists, because you enrolled before or restarted, the three administrator values are ignored and the existing password still applies; change it in Gitea's own settings. Keep the secret key: Gitea encrypts values such as two-factor secrets with it, so replacing it later makes those values unreadable. Save the values; they are also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready (about 10 to 15 seconds in a local check). Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so remotes and scripts that point at the old one need the new one.
4. Open the address and sign in with the administrator name and password. There is no installation wizard: it is already done.

## Create a repository and push

1. In the web interface choose **+** then **New Repository**, or create one with the API:

   ```bash
   curl -u admin:<password> -X POST https://<instance>/api/v1/user/repos \
        -H 'Content-Type: application/json' -d '{"name":"demo"}'
   ```

2. Push an existing project over HTTPS:

   ```bash
   git remote add origin https://<instance>/admin/demo.git
   git push -u origin main
   ```

   Git asks for the user name and password. For scripts, create an access token in **Settings, Applications** and use it as the password.
3. Other users: public registration is switched off, so create them in **Site Administration, User Accounts**.

## Address

Gitea does not know its public address ahead of time, since a new enrollment gets a new one. This recipe lets Gitea take the address from each request (`PUBLIC_URL_DETECTION=auto`), so page links and the clone URLs it shows use the address you opened. In a local check that worked when the proxy sent the `Host` and `X-Forwarded-Proto` headers. If the clone URLs shown on a repository page begin with `http://` instead of `https://`, use `https://` yourself. Gitea sends no email from this instance (no mail server is configured), so password reset by email and notifications do not work.

## Authentication

Gitea checks every request itself. Anyone who knows the instance address can see the sign-in page and any repository you make public, so keep the administrator password strong and keep access tokens private. Public registration is switched off, so only users the administrator creates can sign in. UnitySVC adds no other gate.

## What is kept, and what is lost

Gitea's folder is persistent: the SQLite database, the Git repositories, `app.ini` (its configuration), attachments, avatars and search indexes. They are stored in `gitea/` in your home. The platform restores them before Gitea starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a push just made. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file Gitea removes, such as a deleted repository's files or an old index, can come back after a restart.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Gitea and this keeps the stored database consistent.
- Do not edit the files in `gitea/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored. A single file over 1 GiB in a repository therefore cannot be kept.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `gitea/` folder yourself when you no longer want the data.
- Gitea's Actions runner is not included. Workflows need a separate runner that you operate elsewhere.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Gitea used about 170 MiB idle and about 190 MiB after creating a repository and pushing 6 MB to it, in a local check with the same memory and CPU limits. Large repositories and many users need more than this size; this recipe offers only `nano`. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
