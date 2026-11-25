# HedgeDoc Collaborative Markdown Notes

Each enrollment runs a private [HedgeDoc](https://hedgedoc.org/) server, a real-time collaborative Markdown editor. HedgeDoc is written and maintained by the HedgeDoc project and contributors ([source](https://github.com/hedgedoc/hedgedoc)) and is released under the GNU Affero General Public License v3.0; the provider of this service is its author, who was not asked to take part and does not endorse or support this listing. UnitySVC Labs lists the official `quay.io/hedgedoc/hedgedoc` image, version 1.12.0 (the HedgeDoc 1.x line, pinned by digest), and the platform runs one isolated instance per enrollment.

HedgeDoc 2 is a rewrite that is still an alpha release and runs as separate backend and frontend programs, so this service uses the stable 1.x line, which is one program with a SQLite database. Version 1.12.0 is the newest 1.x image the project publishes; 1.12.1 and 1.12.2 were withdrawn upstream, so the security fixes listed in the 1.12.1 release notes are not in it.

Your notes are kept in the `hedgedoc` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `hedgedoc/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one HedgeDoc instance at a time.
2. The form shows a generated **Session secret** (HedgeDoc signs its login cookies with it; you never type it), and two choices, **Allow use without signing in** and **Allow anyone to register**, both `true` by default. See Who can create notes below before you leave them on.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so links you shared need the new one.

## Who can create notes

HedgeDoc 1.x has **no administrator account**, and no password can be set at enrollment. Access control is the two choices above and the permission of each note:

- With the defaults, **anyone who can reach the address can open the editor and create notes without signing in, and can register an account** with any email and password (HedgeDoc sends no mail and does not verify addresses). Anyone who registers can also create and own notes. Keep the address private and treat it like a shared secret.
- Set **Allow use without signing in** to `false` to make the editor need an account. Set **Allow anyone to register** to `false` to close the registration form. If both are `false` and you have not registered yet, nobody can sign in. So register your own account first, then restart the instance with registration closed. Accounts that already exist keep working. Both settings are read when HedgeDoc starts, so a saved change takes effect the next time the instance starts.
- Each note has its own permission (owner, signed-in users, guests), set from the note's permission menu. The note's owner sets it; a note created without signing in has no owner.
- A note's address is its only protection if it is open to guests: anyone who has the link can read it.

## First use

1. Open `https://<instance>/`, register an account (the form is on the sign-in dialog), and sign in. Click **New guest note** to create a note without signing in, or create one from your account.
2. Send the note's address to the people who should edit it. Everyone who opens it edits the same text at once, with a live preview. Use the permission menu to say who may edit.
3. Images pasted or dragged into a note are uploaded to the instance and kept with your data.

## What is kept, and what is lost

HedgeDoc keeps its notes and accounts in a SQLite database and uploaded images in a folder. The platform stores both in the `hedgedoc/` folder of your home (`hedgedoc/db` and `hedgedoc/uploads`), where you can see them while the instance is stopped. It restores them before HedgeDoc starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- The database's temporary write-ahead files (`*-wal`, `*-shm`) are not copied, so a copy holds the database as it was at the last full write.
- Files are copied, never deleted from your home. Do not edit the files in `hedgedoc/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `hedgedoc/` folder yourself when you no longer want the data.

## Limits and notes

- The instance address is not known when the instance is configured, so HedgeDoc's `CMD_DOMAIN` setting is left unset. HedgeDoc logs a warning about it and builds its redirects as relative paths, which work at any address. Features that need an absolute address, such as the third-party sign-in providers HedgeDoc supports, are not set up.
- Only email and password accounts are offered; there is no way to add other sign-in providers or an SMTP server in this recipe.
- Keep the generated session secret. Changing it signs everyone out.

## Cost and size

The instance runs on the `nano` size (0.5 core, 512 MiB, plus temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check with a 512 MiB limit HedgeDoc used about 190 MiB at idle. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
