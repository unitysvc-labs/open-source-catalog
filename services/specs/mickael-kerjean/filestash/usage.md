# Filestash Web File Manager

Each enrollment runs a private [Filestash](https://www.filestash.app/) instance. Filestash is written and maintained by [Mickael Kerjean](https://github.com/mickael-kerjean) and contributors and is released under the AGPL-3.0 license; the provider of this service is its author, who was not asked to take part. UnitySVC Labs lists the official `machines/filestash` image (version v0.6.20261125, pinned by digest; the project publishes only a moving `latest` tag), and the platform runs one isolated instance per enrollment.

Filestash is a web front end for storage you already have. It does not keep your files: they stay on the FTP, SFTP, S3, WebDAV or other server you connect. Only Filestash's own settings are kept in the `filestash` folder of your **home**, so they survive stopping the instance, and also removing it and enrolling again.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `filestash/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. It has no settings to fill in. You can run one Filestash instance at a time.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
3. **Open `https://<instance>/admin` at once and set the administrator password.** A new Filestash has no password: the first person who opens `/admin` is shown a setup page and chooses it, and that person becomes the administrator. The address is not secret-protected, so if you wait, someone else who has the address could take it. In a local test an unauthenticated request set the password the same way, and once a password existed the same request was refused (403).
4. In the administrator console (`/admin`) add your storage. The console's **configuration wizard** offers presets, and **Storage** lets you enable storage types (FTP, SFTP, S3, WebDAV, SMB, Dropbox, Google Drive, Git and more) and the authentication middleware. Until you configure storage, the sign-in page at `/` shows an error and visitors cannot connect to anything.
5. Open `https://<instance>/` and sign in as you set it up; browse, upload, download, preview and share files.

The administrator password is a Filestash password, not your UnitySVC API key. Keep it somewhere safe: this recipe has no tested way to reset it.

## Credentials and security

- **The address is reachable by anyone who has it.** Filestash checks sign-in itself and UnitySVC adds no other gate. Set the administrator password first, and keep the address private until you have.
- **Storage details entered in the console are stored in plain text.** In a local test, a storage entry with a password added through the administrator interface was written unencrypted to `config/config.json`, and the instance's unauthenticated `/api/config` request returned that entry, password included. That entry was written directly through the admin API; whether the console's own forms behave the same was not tested. Treat it as possible: do not put a password you cannot afford to lose into a stored storage entry.
- The same `config.json` is copied to the `filestash/` folder of your home, where you can read it, and it also holds Filestash's secret key.
- Prefer the least access that works: a dedicated account or access key for this instance, limited to the folders you need and read-only if you only browse, and one you can revoke or rotate. Do not use an account that can reach more than you intend to share.
- Filestash's wizard also offers presets in which each visitor signs in with their own storage credentials instead of one stored in the configuration (for example "SFTP Storage - Use existing credentials"). They were not tried, so what they save is not known.
- The administrator console warns that the connection is not encrypted. That is the container's own port: the platform serves the instance over HTTPS.
- Enable only the storage types you need. Whether a visitor could use an enabled type to reach other servers was not tested.

## What is not included

- **No document editing.** The upstream Docker example adds a second container (Collabora Online) for editing office documents in the browser. This recipe runs the Filestash container only, so that is not available. Filestash's built-in office viewer plugin is a different thing and was not tested.
- **Paid features.** The image is the AGPL build. The project's pricing page lists features for paid plans only, so you should not expect them: for example Azure Blob, Google Cloud Storage and Virtual FS storage, SAML, OIDC, LDAP and multi-factor sign-in, database logins (MySQL, Postgres, Oracle), the SFTP and S3 gateways, antivirus scan, quotas, geo and IP filtering, versioning, fine-grained access control, audit logs, and environment-variable configuration. The administrator console of the AGPL build also says that production use in a commercial environment needs a Filestash enterprise licence. Which of these features the image actually refuses was not tested; check the [pricing page](https://www.filestash.app/pricing/) and the [documentation](https://www.filestash.app/docs/) before you rely on one.

## What is kept, and what is lost

Filestash's state folder (`/app/data/state`) is persistent: `config/config.json` (the administrator password hash, the secret key and your storage entries), the SQLite databases in `db/` (file metadata, shared links, workflows), logs, certificates and plugins. They are stored in `filestash/` in your home, where you can see them while the instance is stopped. The platform restores them before Filestash starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, such as a link you just shared. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file Filestash removes can come back after a restart.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Filestash and this keeps the stored databases consistent.
- Do not edit the files in `filestash/` while the instance is stopped, except as described above: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored. The log file grows in your home.
- Anything outside `/app/data/state` is temporary: that includes Filestash's cache and thumbnails, which are rebuilt. Do not use a local-disk storage type for files you want to keep.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `filestash/` folder yourself when you no longer want the data, bearing in mind it holds any stored storage password.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Filestash used about 93 MiB when idle and about 98 MiB after 60 page requests in a local check; large uploads, thumbnails and video transcoding were not tried. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
