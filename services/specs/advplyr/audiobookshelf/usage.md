# Audiobookshelf Audiobook and Podcast Server

Each enrollment runs a private [Audiobookshelf](https://www.audiobookshelf.org/) instance. Audiobookshelf is written and maintained by [advplyr](https://github.com/advplyr) and contributors and is released under the GPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `ghcr.io/advplyr/audiobookshelf` image (version 2.38.0, pinned by digest), and the platform runs one isolated instance per enrollment.

**Read "Your media files" below before you plan to use this as your audiobook library.** The database is kept; the audio files are not.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `audiobookshelf/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Audiobookshelf instance at a time. There are no settings to fill in.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so bookmarks and the server address in the mobile apps need the new one.
3. **Open the address and create the root account immediately.** A new Audiobookshelf has no account, and its setup page is open to anyone who reaches the address. The first account you create is the root administrator, and the setup page is refused once it exists. If somebody else created it first, stop the instance, delete the `audiobookshelf/` folder in your home and start again.

## First use

1. Sign in with the account you created. There is no administrator password parameter: the password is the one you chose on the setup page.
2. Open **Settings > Libraries** and add a library. Choose the folder `/audiobooks` (or `/podcasts` for a podcast library); these are the only media folders the instance has.
3. Upload your files in the web interface (the upload page, as the root or an upload-enabled user), into that library. Audiobookshelf scans them, reads their tags and, if you ask, looks up metadata and covers online. Listen in the web player, or add the instance address as the server in the Audiobookshelf mobile apps. Other options (users, backups, OIDC sign-in, podcast feeds and downloads) are in its settings and are described in the [Audiobookshelf documentation](https://www.audiobookshelf.org/docs); features that reach outside services need the settings you give them there.

## Your media files

Only folders of your home can be kept between runs, and this service keeps just two of them: the database and the generated metadata. **The audio files are not kept.** `/audiobooks` and `/podcasts` are temporary scratch space inside the instance: about 1 GiB in total (this also holds the transcoding cache), and everything in them is gone when the instance stops or is replaced.

What that means in practice:

- Files you upload exist only until the instance stops. After the next start Audiobookshelf still lists your books, progress and users from the database, but the files are gone: once a library scan runs, the items are marked missing until you upload the files again.
- A single audiobook is often several hundred MiB, so one or two books fill the space. This is not a place to keep a library of any size. It suits listening to a few books or podcast episodes during one run, or trying Audiobookshelf out.
- It was not made durable because a persisted folder is copied back **in full** at every start and again whenever it changes, files over 1 GiB are not stored at all, and everything restored takes room in the instance's 1 GiB of temporary disk. For an audiobook library that is a bad fit on this size.
- Podcast downloads (a podcast library fetches episodes from the feed) land in `/podcasts` and are temporary in the same way. Feeds and subscriptions are in the database and are kept.

## Authentication

Audiobookshelf checks every request itself: the web interface and the apps need a sign-in, except that cover images are served without one (they are addressed by random identifiers). Anyone who knows the instance address can reach the sign-in page, so use a strong password. UnitySVC adds no other gate.

## What is kept, and what is lost

Two folders are persistent: `/config` (the SQLite database with users, libraries and listening progress, stored in `audiobookshelf/config` of your home) and `/metadata` (covers, item metadata, backups and logs, in `audiobookshelf/metadata`). The platform restores them before Audiobookshelf starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folders belong to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes (for example the last listening position). A normal stop loses nothing.
- Files are copied, never deleted from your home. A cover or backup Audiobookshelf removes can come back after a restart.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Audiobookshelf and this keeps the stored database consistent.
- Do not edit the files in `audiobookshelf/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `audiobookshelf/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Audiobookshelf used about 106 MiB at idle and about 120 MiB after scanning a library and starting an ffmpeg stream, in a local check with a one-book library; a library with thousands of items will use more. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
