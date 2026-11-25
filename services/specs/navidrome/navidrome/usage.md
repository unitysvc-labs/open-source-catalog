# Navidrome Music Streaming Server

Each enrollment runs a private [Navidrome](https://www.navidrome.org/) server. Navidrome is written and maintained by the Navidrome authors and is released under the GPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `navidrome/navidrome` image (version 0.64.2, pinned by digest), and the platform runs one isolated instance per enrollment.

Two folders of your **home** are used, not the enrollment: `navidrome/music` is your music library, and `navidrome/data` holds Navidrome's database. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same files.

## Where your music comes from

Navidrome has no upload function of its own. Your music must already be in the `navidrome/music` folder of your UnitySVC home (for example folders such as `Artist/Album/01 Track.mp3`), put there with the platform's file access to your home before you start the instance. Each time the instance starts, the platform copies the whole folder into the instance, and Navidrome scans it. This has consequences for a music library:

- **Whole files, every start.** A restore copies every file completely, so the start takes longer the larger the library is. Only a small personal library is practical.
- **Temporary disk.** The `nano` size has 1 GiB of temporary disk for everything in the instance, and the restored music lives there together with the database and Navidrome's caches. Keep the library well below that. Navidrome used under 150 MiB of memory and about 126 MB of disk for a generated library of 406 short files in a local check; a real library of lossless files is much larger.
- **Files over 1 GiB are not stored**, empty files and symbolic links are not stored either. A single very large audio file is skipped.
- **New music needs a restart.** Files you add to `navidrome/music` while the instance runs are not copied into it. Stop the instance and start it again (the scan then runs on startup).
- **Read only.** The library is mounted read only: Navidrome cannot change or delete your files, and nothing it does touches the copy in your home.

An empty `navidrome/music` folder is fine: Navidrome starts with an empty library.

## Set up

1. Put your music in `navidrome/music` in your home.
2. Enroll in **base**. The enrollment asks for access to the `navidrome/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Navidrome instance at a time. The form has two settings: the idle session timeout, and whether Navidrome may use external lookups (see Privacy below).
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so apps that point at the old one need the new one.
4. **Open the address immediately and create the first account.** Navidrome has no environment variable or enrollment parameter for the administrator. On a new database it shows a **Create Admin** page, and whoever reaches the address first creates the account, which becomes the administrator of the whole instance. Do this before you share the address with anyone, and choose a strong password. After the first account exists, the page is closed (a second attempt is refused).
5. Sign in. The library appears when the first scan finishes; this takes a few seconds for a small library.

## Use it

Play music in the web interface, or connect an app. Navidrome speaks the Subsonic and OpenSubsonic API, so many mobile and desktop music apps work: give the app the instance address (`https://<instance>`), your user name and your password. See the [Navidrome documentation](https://www.navidrome.org/docs/) and the [list of apps](https://www.navidrome.org/apps/). The administrator can add more users in the web interface.

## Authentication

Navidrome checks every request itself: the web interface and the Subsonic API both need a user name and password. Anyone who knows the instance address can reach the sign-in page, so keep passwords strong. UnitySVC adds no other gate.

## Privacy

Upstream's anonymous usage statistics (`ND_ENABLEINSIGHTSCOLLECTOR`) are switched off in this recipe. The enrollment setting **Allow external lookups** (`ND_ENABLEEXTERNALSERVICES`) is on by default, as in Navidrome: it looks up artist pictures and biographies at Deezer, which tells that service the artist names in your library, and loads a login background image. Set it to `false` to switch off all external lookups. With the setting off, a local check made no such requests. Last.fm and ListenBrainz are only used if a user configures them.

## What is kept, and what is lost

The data folder holds Navidrome's SQLite database (users, playlists, play counts, favourites). It is stored in `navidrome/data` in your home, where you can see it in your files while the instance is stopped. The platform restores it before Navidrome starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folders belong to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- Navidrome keeps recent changes in SQLite's write-ahead file (`*-wal`), which is not stored. A normal stop writes everything into the database first and loses nothing (a local check confirmed this). After a crash or a node failure you can lose the changes made since Navidrome last wrote them into the database, which can be more than the last 30 seconds: a new playlist or play count, for example. Your music is not affected.
- Files are copied, never deleted from your home.
- Do not edit the files in `navidrome/data` while the instance is stopped: the next start restores them over what you changed.
- Navidrome's image and transcoding caches are not kept: they are rebuilt as needed.
- Changing the session timeout is possible at any time; the administrator account cannot be set by a parameter, only at the first visit.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `navidrome/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Navidrome used about 70 MiB idle, and up to about 145 MiB while scanning a library of 406 files, in a local check. Transcoding many streams at once needs more CPU than half a core. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
