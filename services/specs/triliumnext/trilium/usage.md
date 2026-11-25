# TriliumNext Notes

Each enrollment runs a private [TriliumNext Notes](https://triliumnotes.org/) server (Trilium). Trilium is written and maintained by the TriliumNext contributors (a continuation of Zadam's Trilium) and is released under the AGPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `triliumnext/trilium` image (version 0.107.0, pinned by digest), and the platform runs one isolated instance per enrollment.

Your notes are kept in the `trilium` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `trilium/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Trilium instance at a time.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so bookmarks and sync clients that point at the old one need the new one.
3. **Open the address immediately and set the password.** Trilium has no environment variable or enrollment parameter for its password. On a new database it shows a **Set password** page, and whoever reaches the address first chooses the password for the whole instance. Do this before you share the address with anyone. Choose a strong password, and keep it: Trilium cannot recover it.
4. Log in with that password. A new database comes with a small demo note tree you can delete.

## Use it

Create notes in the tree on the left and pick a note type in the note's header. The [Trilium documentation](https://docs.triliumnotes.org/) covers note types, attributes, search and scripting. To work from the desktop app or a phone, sync it with this server: in the app's sync options enter the instance address and the password you set.

## Authentication

Trilium checks every request itself with the password you set (and the optional two-factor and OpenID settings in its own options). Anyone who knows the address can reach the login page, so keep the password strong. Until the password is set, the set-password page is open to anyone who reaches the address. UnitySVC adds no other gate.

Trilium's scripting features are part of the application: notes of type script can run code in your instance. Backend scripting is switched off by default in the upstream configuration; leave it that way unless you need it.

## What is kept, and what is lost

Trilium's data folder is persistent: the SQLite database (`document.db`, which holds notes, attachments and revisions), `config.ini`, the session secret and logs. They are stored in `trilium/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before Trilium starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- Trilium keeps recent changes in SQLite's write-ahead file (`*-wal`), which is not stored. A normal stop writes everything into the database first and loses nothing. After a crash or a node failure, you can lose the changes made since Trilium last wrote them into the database, which can be more than the last 30 seconds.
- Files are copied, never deleted from your home. A file Trilium removes can come back after a restart. This is cosmetic.
- SQLite's temporary files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Trilium and this keeps the stored database consistent.
- Do not edit the files in `trilium/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored, so a very large attachment is not kept.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `trilium/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Trilium used about 100 MiB in a local check. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
