# Jellyfin Media Server for Video and Music

Each enrollment runs a private [Jellyfin](https://jellyfin.org/) server. Jellyfin is written and maintained by the Jellyfin contributors and is released under the GPL-2.0 license; the provider of this service is its author. UnitySVC Labs lists the official `jellyfin/jellyfin` image (version 12.4, pinned by digest), and the platform runs one isolated instance per enrollment.

Two folders of your **home** are used, not the enrollment: `jellyfin/media` holds your media, and `jellyfin/config` holds Jellyfin's database, settings and artwork. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same files.

## What kind of library fits

Jellyfin has no page for uploading media; it reads files from folders on disk. Your media must be in the `jellyfin/media` folder of your UnitySVC home, put there with the platform's **Files** page. Each time the instance starts, the platform copies the whole folder into the instance, where Jellyfin sees it as `/media`. Read this before you enroll, because it decides whether the service suits your library:

- **Files over 1 GiB are not stored.** Most feature films at full quality are larger than that and are skipped. What fits: music, audiobooks, home videos, clips, and TV episodes or films encoded below 1 GiB per file (a 45-minute episode at 1080p is usually well under it; a two-hour film has to be encoded at about 1 GiB or less, which means a modest bitrate). Empty files and symbolic links are not stored either.
- **Whole files, every start.** A restore copies every file completely, so the start takes longer the larger the library is, and an instance that takes too long to become ready fails. Begin with a few GiB and grow from there.
- **Temporary disk.** The instance has 50 GiB of temporary disk for everything: the restored media, the database and artwork, and the files Jellyfin writes while it converts a video. Keep the library well below that.
- **New media needs a restart.** Files you add to `jellyfin/media` while the instance runs are not copied into it. Stop the instance, start it again, then use **Scan All Libraries** in the Dashboard.
- **Read only.** The media is mounted read only: Jellyfin cannot change or delete your files, and nothing it does touches the copy in your home. Deleting media from within Jellyfin does not work; delete it in the Files page, restart and scan.
- **Converting video is slow.** There is no graphics card: Jellyfin converts ("transcodes") on the processor only, and the instance has one core. In a local check, converting a 1080p HEVC test video to 720p H.264 ran at about three times playback speed on one core and used about 1 GiB of memory; real films are harder to convert, and the platform is slower than that check. Expect one converted stream at a time at best. Prefer files your devices play directly: H.264 video with AAC audio in an MP4 file plays almost everywhere without conversion. If a video stutters, lower the quality in the player, or re-encode the file before uploading it.
- **Streaming goes through the platform's HTTPS front end.** Playback, seeking and Jellyfin's live connection (WebSocket) worked through an HTTPS reverse proxy in a local check. Features that need the local network do not exist here: DLNA, automatic server discovery and Live TV tuners.

Use one folder per library, named as Jellyfin expects, for example:

```
jellyfin/media/movies/Night Walk (2019)/Night Walk (2019).mp4
jellyfin/media/shows/Garden Diary/Season 01/Garden Diary S01E01.mkv
jellyfin/media/music/Artist/Album/01 Track.mp3
```

The [Jellyfin documentation](https://jellyfin.org/docs/general/server/media/movies) describes the naming for each kind of library. An empty or missing `jellyfin/media` folder is fine: Jellyfin starts with no media.

## Set up

1. Put your media in `jellyfin/media` in your home, as described above.
2. Enroll in **base**. The enrollment asks for access to the `jellyfin/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Jellyfin instance at a time. The form has two settings:
   - **Administrator name** (`JELLYFIN_ADMIN_USER`), `admin` unless you change it.
   - **Administrator password** (`JELLYFIN_ADMIN_PASSWORD`), generated for you. Save it when you enroll: the platform keeps it as a secret and does not show it again. Use letters, digits and common punctuation; spaces, quotes and backslashes are not accepted.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so apps that point at the old one need the new one.
4. Open the address and sign in with the administrator name and password.

There is no setup wizard to go through. A new Jellyfin server normally shows one to its first visitor, who creates the administrator. Here the instance completes that wizard itself on its first start, with the name and password from the enrollment, before Jellyfin accepts connections from outside; in a local check the wizard's address answered `401` from the first moment the server was reachable. The wizard's other choices are left at Jellyfin's defaults (English, United States); change the display language in your user settings and the metadata language in each library.

**The two settings are used only once**, when the server is first set up. Your data lives in your home, so on a later start, or a later enrollment, the existing accounts and passwords apply and the values in the form are ignored. Change a password in Jellyfin's own settings (**Profile**, or **Dashboard > Users**).

## First use

1. Open **Dashboard > Libraries > Add Media Library**. Choose the content type (Movies, Shows, Music, ...), give it a name, and add its folder under `/media`, for example `/media/movies`. Jellyfin scans it and the items appear on the home page.
2. Play something in the browser. For other devices, install a [Jellyfin app](https://jellyfin.org/downloads/clients/) and give it the instance address (`https://<instance>`), your user name and your password.
3. Add people in **Dashboard > Users**. Each has their own password, watch state and library access.

Things to know on this platform:

- **A library added just before a stop can lose its content type.** Jellyfin records a library's type as an empty file, and empty files are not kept in your home, so the instance gives each of those files a line of content within a few seconds. If you stop the instance in those few seconds, the library comes back as mixed content: remove it and add it again (your media is not affected).
- **Metadata lookups.** Jellyfin's default is to look up artwork and descriptions at TheMovieDB, MusicBrainz and similar services, which tells them the titles in your library. Switch the providers off per library (**Dashboard > Libraries > Manage library**) if you prefer.
- **No email.** Jellyfin sends none and needs none. **Forgot Password** writes a file `passwordreset<...>.json` containing a PIN into `jellyfin/config` in your home; open it in the Files page (it appears within about 30 seconds), enter the PIN on the Forgot Password page within 30 minutes, and then sign in **with the PIN as the password** and change it. Delete the file from your home afterwards: nothing is ever deleted from your home automatically, so it would otherwise stay there.
- **Jellyfin sees every visitor as the platform's front end.** Its settings that depend on the visitor's network address (remote access per user, address filters, separate limits for remote streaming) do not tell visitors apart here.
- Plugins you install are kept, but a plugin you remove comes back at the next start, because nothing is deleted from your home. Delete its folder under `jellyfin/config/plugins` in the Files page while the instance is stopped.

## Authentication

Jellyfin checks sign-in itself: the web interface, the apps and the API need a user name and password (or the token an app gets after signing in), and a wrong password is refused with `401`. UnitySVC adds no other gate, so anyone who knows the instance address can reach the sign-in page; keep passwords strong and do not add users without one.

**One thing is not protected by the sign-in.** As upstream Jellyfin works today, the addresses that deliver a media file or a picture (`/Videos/<id>/stream`, `/Audio/<id>/stream`, `/Items/<id>/Images/...`) answer without credentials to anyone who has the item's id. In a local check, a video stream requested with no credentials returned the file. The id is a long hexadecimal value, but Jellyfin derives it from the file's path, so somebody who knows your instance address and the exact folder and file name of an item could work it out. Browsing, searching and the lists of items do need a sign-in (`401` without one). Do not publish the instance address, and do not keep media here that must stay confidential even from somebody who has the address.

## What is kept, and what is lost

Jellyfin's data folder is stored in `jellyfin/config` in your home: the SQLite database (users, libraries, items, watch state, playlists), the settings, downloaded artwork and plugins. The platform restores it before Jellyfin starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folders belong to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- **A crash can lose the last 30 seconds.** By default Jellyfin keeps recent changes in SQLite's write-ahead file, which is not stored. This recipe sets Jellyfin's documented `database.xml` option for the rollback-journal mode instead, so changes are written into the database file itself: in a local check, a user created one second before the server was killed was still there after a restore from the stored files alone. A normal stop loses nothing.
- **Not kept:** the cache and the files written while converting video, Jellyfin's logs, and the database backups Jellyfin makes before an upgrade. They are left out because nothing is ever deleted from your home, so they would only pile up. The copy in your home is the backup.
- Files are copied, never deleted from your home. Artwork that Jellyfin removes can come back after a restart; this is cosmetic.
- Do not edit the files in `jellyfin/config` while the instance is stopped, except to delete a file as described above, or to delete the whole folder and start afresh (the enrollment's administrator name and password then apply again).
- Empty files, symbolic links and files over 1 GiB are not stored. Jellyfin recreates the empty marker files it needs at each start.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `jellyfin/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `small-largedisk` size (one core, 2 GiB of memory, 50 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check limited to one core and 2 GiB, Jellyfin used about 300 MiB idle, about 400 MiB while scanning a small library, and about 1 GiB while converting one 1080p video; the first start, including the setup step, took 16 seconds. It does not fit the `nano` size. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
