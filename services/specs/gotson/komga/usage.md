# Komga Media Server for Comics, Manga and E-books

Each enrollment runs a private [Komga](https://komga.org/) server. Komga is written and maintained by [Gauthier Roebroeck](https://github.com/gotson) and contributors and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `gotson/komga` image (version 1.30.2, pinned by digest), and the platform runs one isolated instance per enrollment.

Two folders of your **home** are used, not the enrollment: `komga/library` holds your books, and `komga/config` holds Komga's databases. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same files.

## Where your books come from

Komga has no page for uploading books; it reads them from folders on disk. Your books must be in the `komga/library` folder of your UnitySVC home, put there with the platform's **Files** page (open `home/`, then `komga/library/`, and upload). Each time the instance starts, the platform copies the whole folder into the instance, where Komga sees it as `/library`. This has consequences:

- **Use one folder per library, and one folder per series inside it.** For example `komga/library/comics/Saga/Saga v01.cbz` and `komga/library/books/Jane Austen/Emma.epub`. Komga makes a series of each folder that contains books; the [Komga documentation](https://komga.org/docs/guides/libraries) describes this. It reads CBZ, CBR, PDF and EPUB.
- **New books need a restart.** Files you add to `komga/library` while the instance runs are not copied into it. Stop the instance, start it again, then use **Scan library files** in Komga (or turn on **Scan on startup** in the library's options).
- **Whole files, every start.** A restore copies every file completely, so the start takes longer the larger the library is. Only a small personal library is practical.
- **Temporary disk.** The `small` size has 5 GiB of temporary disk for everything in the instance: the restored books, the databases and the search index. Keep the library well below that, at a few GiB at most.
- **Files over 1 GiB are not stored**, and neither are empty files and symbolic links. A single very large archive is skipped.
- **Read only.** The library is mounted read only: Komga cannot change or delete your books, and nothing it does touches the copy in your home. Komga's functions that write to the library (deleting book files, importing books into a series, converting to CBZ, repairing file extensions) therefore fail. To remove a book, delete it in the Files page, restart the instance and scan.

An empty or missing `komga/library` folder is fine: Komga starts with no books.

## Set up

1. Put your books in `komga/library` in your home, as described above.
2. Enroll in **base**. The enrollment asks for access to the `komga/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Komga instance at a time.
3. Settings:

   | Setting | Default | Meaning |
   | --- | --- | --- |
   | Administrator email (sign-in name) | `admin@example.com` | Komga signs users in by email address. It never sends mail to it, so it does not have to be a real one. |
   | Administrator password | generated | Keep the generated value or enter your own, 12 characters at least, without spaces. **Save it when you enroll**: the platform keeps it as a secret and does not show it again. |

4. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so reader apps that point at the old one need the new one. Komga needs no setting for its address.
5. Open the address and sign in with the email address and the password.

Komga has no setting for a first account: on a new server the first visitor "claims" it and becomes the administrator. To close that gap, this service claims the server for you on the first start, with the email address and password of the enrollment, **before the instance is reachable**: Komga is first started on a port that only the container itself can reach, the account is created through Komga's own claim function, and only then does the server open to the network. Nobody else can claim it.

Both settings are used **only when the account is first created**. When the data already exists, because you enrolled before or restarted, nothing is created and nothing is reset: sign in with the account you already have. Changing either setting later restarts the instance and has no other effect. Change your password in Komga under **Account settings**.

## First use

1. Sign in and add a library (the **+** next to **Libraries**). Give it a name and choose its folder under `/library`, for example `/library/comics`. Komga scans it at once and the series appear.
2. Open a book and read it in the browser. Your progress is saved per user.
3. For reader apps, use the OPDS addresses `https://<instance>/opds/v1.2/catalog` or `https://<instance>/opds/v2/catalog` and sign in with your Komga email address and password, or create an API key under **Account settings**.
4. To add users, use **Server > Users**. You set each user's email address, password and the libraries they may see; no mail is sent.

Things to know on this platform:

- **No email.** Komga does not send mail and has no "forgot password" function. An administrator can set another user's password. If you lose the only administrator's password there is no reset: stop the instance, delete the `komga/config` folder in your home and start again with a new enrollment password (your books stay; libraries, users and reading progress are created anew).
- Komga's update check and its announcements page fetch release information from GitHub and komga.org. Komga sends no usage statistics.
- The memory Komga may use for Java objects is limited to 1 GiB, to fit the size. Very large books or PDF files can fail to load with an out-of-memory error in the logs.

## Authentication

Komga checks every request itself: the web interface loads without a sign-in, but the API, OPDS catalogs and book files need a signed-in user (email address and password, a session, or an API key) and answer `401` otherwise. The claim function refuses a second claim. Only `/actuator/health` (an "up" status), the API description at `/v3/api-docs` and the sign-in page are open. Anyone who knows the instance address can reach the sign-in page, so keep passwords strong. UnitySVC adds no other gate.

## What is kept, and what is lost

Komga's configuration folder is stored in `komga/config` in your home: the main database (users, libraries, series, covers, metadata, reading progress, collections and read lists), the tasks and sessions databases, and a small `claimed` marker that records that the administrator account was created. The platform restores it before Komga starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folders belong to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- **A crash can lose the last 30 seconds.** The databases run in SQLite's rollback-journal mode here, not Komga's default write-ahead log, so every finished change is in the database file itself and the copy in your home is complete without other files. A normal stop loses nothing.
- **Not kept:** the search index and Komga's logs. Komga rebuilds the search index by itself at each start (a local check confirmed this); right after a start, search can return nothing for a few seconds.
- Files are copied, never deleted from your home. Komga keeps its data in the databases, so nothing it deletes comes back.
- Do not edit the files in `komga/config` while the instance is stopped, except to delete the whole folder and start afresh. Do not delete `claimed` or a database on its own.
- Empty files, symbolic links and files over 1 GiB are not stored. Komga's databases hold the cover images, so they grow with the library; they must stay under 1 GiB.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `komga/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `small` size (one core, 2 GiB, 5 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Komga is a Java application: in a local check it used about 520 to 540 MiB idle and about 590 MiB after scanning and reading from a library of 7 files (110 MiB), so it does not fit the `nano` size. A larger library, or several people reading at once, needs more. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
