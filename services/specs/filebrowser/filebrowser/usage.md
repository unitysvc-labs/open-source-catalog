# File Browser Web File Manager

Each enrollment runs a private [File Browser](https://github.com/filebrowser/filebrowser) server. File Browser was written and maintained by [Henrique Dias](https://github.com/hacdias) and contributors and is released under the Apache-2.0 license; the provider of this service is its author. UnitySVC Labs lists the official `filebrowser/filebrowser` image (version v2.63.23, pinned by digest), and the platform runs one isolated instance per enrollment.

**The project is archived.** Upstream stopped development and made the repository read-only on 2026-09-01. v2.63.23 is the last release: there will be no further bug fixes or security fixes, and upstream offers no support. Read [Authentication and security](#authentication-and-security) before you put anything sensitive here.

The files you manage and File Browser's database are kept in the `filebrowser` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `filebrowser/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one File Browser instance at a time.
2. The form shows an **Administrator name** (default `admin`) and a generated **Administrator password**. They create the administrator account the **first time** File Browser runs on your data, when it creates its database. If the database already exists, because you enrolled before or restarted, the parameters are ignored and the existing users and passwords still apply; change a password in File Browser's own settings. Save the password now: the platform keeps it as a secret and does not show it again. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready; it starts in a few seconds. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Open the address and sign in with the administrator name and password.

## Use it

- **Upload** files or folders with the upload button or by dragging them into the window. Open a file to preview it; text files open in an editor.
- **Rename, move, copy, delete and download** with the toolbar; a folder downloads as an archive.
- **Share** a file or folder to get a link that works without signing in, with an optional password and expiry. A share link uses the instance address, so it stops working when the instance is stopped and changes with a new enrollment.
- **Settings** holds your password, and for the administrator the user accounts (each with its own permissions and folder) and the global settings.

The files are also in `filebrowser/files/` in your home, where the rest of the platform can read them.

## Authentication and security

File Browser checks every request itself: the web interface and its API need a sign-in, and only share links you create are public. Anyone who knows the instance address can reach the sign-in page. UnitySVC adds no other gate.

Because the project is archived, weigh these before you use it:

- **No security fixes.** Upstream lists its published advisories at <https://github.com/filebrowser/filebrowser/security/advisories> and will not fix new ones.
- **Upstream advises against exposing it directly to the internet**, and recommends a reverse proxy that does its own authentication in front. This service does not add one: the instance is on a public HTTPS address with File Browser's sign-in only. Use a long administrator password, do not keep files here that you could not afford to have exposed, and stop the instance when you are not using it.
- **Sessions cannot be revoked.** A sign-in is a self-contained token; signing out or changing a password does not invalidate a token already issued, which stays valid until it expires. This is a known issue upstream will not fix.
- **Command execution stays off.** File Browser's command runner and hooks have known vulnerabilities; they are disabled by default and this recipe leaves them disabled.

## What is kept, and what is lost

Two folders are persistent: the files File Browser serves (`filebrowser/files/` in your home) and its database with the users, settings and share links (`filebrowser/database/filebrowser.db`). The platform restores them before File Browser starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **Deleting and renaming do not reach your home.** Files are copied, never deleted from your home. A file you delete in File Browser comes back at the next start, and a file you rename or move is there under both names. To remove a file for good, also delete it from `filebrowser/files/` in your home.
- **Empty files and empty folders, symbolic links and files over 1 GiB are not stored.** They exist while the instance runs and are gone after a stop.
- **Space.** While the instance runs, the files are held on its temporary disk, 1 GiB on this size. Keep the total below that.
- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- You can add files to `filebrowser/files/` in your home while the instance is stopped; they appear at the next start. Do not change `filebrowser/database/`.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `filebrowser/` folder yourself when you no longer want the data.
- To start over with a new administrator account, stop the instance, delete `filebrowser/database/filebrowser.db` from your home and start it again; the administrator name and password of the enrollment then apply. Your files are not affected, but share links and other users are gone.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check File Browser used about 13 MiB of memory idle and 18 MiB after a 200 MB upload. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
