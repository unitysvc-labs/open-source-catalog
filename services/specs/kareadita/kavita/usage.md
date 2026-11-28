# Kavita Reading Server for Comics, Manga and E-books

Each enrollment runs a private [Kavita](https://www.kavitareader.com/) server. Kavita is written and maintained by the [Kareadita](https://github.com/Kareadita) team and contributors and is released under the GPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `jvmilazz0/kavita` image (version 0.9.1.4, tag `0.9.1`, pinned by digest), and the platform runs one isolated instance per enrollment.

Two folders of your **home** are used, not the enrollment: `kavita/library` holds your books, and `kavita/config` holds Kavita's database, covers and settings. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same files.

## Where your books come from

Kavita has no page for uploading books; it reads them from folders on disk. Your books must be in the `kavita/library` folder of your UnitySVC home, put there with the platform's **Files** page (open `home/`, then `kavita/library/`, and upload). Each time the instance starts, the platform copies the whole folder into the instance, where Kavita sees it as `/library`. This has consequences:

- **Use one folder per library, and one folder per series inside it.** For example `kavita/library/comics/Saga/Saga v01.cbz` and `kavita/library/books/Jane Austen/Emma.epub`. Kavita builds series, volumes and chapters from folder and file names; the [Kavita wiki](https://wiki.kavitareader.com/guides/scanner/) describes the naming it understands. It reads CBZ, CBR, ZIP, RAR, 7z, folders of images, EPUB and PDF.
- **New books need a restart.** Files you add to `kavita/library` while the instance runs are not copied into it. Stop the instance, start it again, then use **Scan library** in Kavita.
- **Whole files, every start.** A restore copies every file completely, so the start takes longer the larger the library is. Only a small personal library is practical.
- **Temporary disk.** The `small` size has 5 GiB of temporary disk for everything in the instance: the restored books, the database and covers, and the pages Kavita unpacks while you read. Keep the library well below that, at a few GiB at most.
- **Files over 1 GiB are not stored**, and neither are empty files and symbolic links. A single very large archive is skipped.
- **Read only.** The library is mounted read only: Kavita cannot change or delete your books, and nothing it does touches the copy in your home. To remove a book, delete it in the Files page, restart the instance and scan.

An empty or missing `kavita/library` folder is fine: Kavita starts with no books.

## Set up

1. Put your books in `kavita/library` in your home, as described above.
2. Enroll in **base**. The enrollment asks for access to the `kavita/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Kavita instance at a time. There are no settings to fill in.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so e-reader apps that point at the old one need the new one.
4. **Open the address immediately and register the first account.** Kavita has no environment variable or enrollment parameter for the administrator. On a new database it opens a **Register** page ("Complete the form to register an admin account"), and whoever reaches the address first creates the account, which becomes the administrator of the whole server. Do this before you share the address with anyone, and choose a strong password (6 characters at least; use many more). The email field does not need a real address. After the first account exists, registration is closed: a second attempt is refused.
5. If the Register page does not appear on a first start with an empty `kavita/config` folder, or you find users or libraries you did not create, somebody else got there first: stop the instance, delete the `kavita/config` folder in your home and start again.

When the data already exists, because you enrolled before or restarted, nothing is created: sign in with your own account.

## First use

1. Sign in, open **Settings > Libraries** and add a library. Give it a name and a type (Manga, Comic, Book and so on) and choose its folder under `/library`, for example `/library/comics`. Kavita scans it at once and the series appear on the home page.
2. Open a series and read it in the browser. Your progress is saved per user.
3. For e-reader apps, copy your OPDS URL from your user settings (**Auth Keys / OPDS**); it contains a personal key, so treat it like a password.
4. To add users, use **Settings > Users > Invite**. This instance has no email service, so Kavita does not send the invitation: it shows a link for you to copy and give to the person. The link starts with `http://`; change it to `https://`, or set **Host Name** in Kavita's email settings to your instance address (`https://...`) so that the links are correct.

Things to know on this platform:

- **No email.** "Forgot password" does not work ("Email is not enabled on this server"). Change your password in your user settings while you are signed in; the administrator can set another user's password. If you lose the only administrator's password there is no reset: delete `kavita/config` in your home and start again (your books stay).
- **Anonymous usage statistics** to the Kavita project are on by default, as upstream ships it. Turn them off in **Settings > General** if you prefer.
- Kavita+ (the paid metadata and scrobbling service of the Kavita project) is not part of this service.
- Folder watching has no effect here, because the library only changes when the instance starts.

## Authentication

Kavita checks every request itself: the web interface and its API need a sign-in, and OPDS and image addresses need a personal key. Without one they answer `401`. Anyone who knows the instance address can reach the sign-in page, so keep passwords strong. UnitySVC adds no other gate.

## What is kept, and what is lost

Kavita's configuration folder is stored in `kavita/config` in your home: the SQLite database (users, libraries, series, reading progress), the key that keeps you signed in across restarts, cover images, bookmarks, themes and fonts. The platform restores it before Kavita starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folders belong to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- **A crash can lose more than the last 30 seconds.** Kavita keeps recent changes in SQLite's write-ahead file (`*-wal`), which is not stored, and has no setting to change that. A normal stop writes everything into the database first and loses nothing (a local check confirmed this). After a crash or a node failure you lose the changes made since Kavita last wrote them into the database, which on a small server can be everything since the instance started: reading progress, new users, new libraries. If that happens on the very first run, even the administrator account can be missing and the Register page is open again; open the address at once and register again. Your books are not affected. Stop the instance normally after setting it up to make sure the setup is saved.
- **Not kept:** the reading cache, temporary files, Kavita's own logs and the backup archives Kavita makes each day. They are left out because nothing is ever deleted from your home, so they would only pile up. The copy in your home is the backup; Kavita's backup files disappear when the instance stops.
- Files are copied, never deleted from your home. A cover image Kavita removes can come back after a restart. This is cosmetic.
- Do not edit the files in `kavita/config` while the instance is stopped, except to delete the whole folder and start afresh.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `kavita/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `small` size (one core, 2 GiB, 5 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check Kavita used about 300 to 420 MiB idle and about 510 MiB while scanning a library of 21 files (1.6 GiB), so it does not fit the `nano` size. A larger library, or several people reading at once, needs more. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
