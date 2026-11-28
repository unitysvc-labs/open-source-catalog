# Shiori Bookmark Manager with Offline Archive

Each enrollment runs a private [Shiori](https://github.com/go-shiori/shiori) server. Shiori was created by [Radhi Fadlillah](https://github.com/RadhiFadlillah) and is maintained by [Felipe Martin](https://github.com/fmartingr) and contributors, and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `ghcr.io/go-shiori/shiori` image (version v1.8.0, pinned by digest), and the platform runs one isolated instance per enrollment. This listing is unofficial: the Shiori project does not operate or support it.

Your bookmarks and archived pages are kept in the `shiori` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

**Read "The first account" before you start the instance for the first time.** A new Shiori has a published default sign-in until you change its password.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `shiori/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Shiori instance at a time.
2. The form has one setting, a generated **Session secret key**. Shiori signs its sign-in tokens with it; keep the generated value. It is not a password and you never type it anywhere.
3. Wait for the instance to become ready; it starts in a few seconds. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.** No address setting is needed.
4. Open the address at once and change the default password, as described next.

## The first account

Shiori has no setting for the first account's password, so this service has no password parameter. Whenever Shiori starts and finds no account at all, it creates one owner account with the sign-in upstream publishes in its documentation: user name `shiori`, password `gopher`. The sign-in page does not show these values, but they are public.

**Until you change that password, anyone who reaches the instance address can sign in as the owner.** The address is not listed anywhere, but it is not a secret either. Do this as soon as the instance is ready:

1. Open the address and sign in as `shiori` with the password `gopher`.
2. Open **Settings** (the gear in the side bar). Under **Accounts**, use the key icon (**Change password**) beside `shiori`, enter `gopher` as the current password and your own password twice, and confirm.
3. Sign out and sign in with your own password. The default password is now refused.

If you prefer another user name, use **Add new account** to create an owner account ("This account is an admin account"), sign in with it, and delete `shiori` with the bin icon beside it. Never delete the last account: with none left, the next start creates `shiori` / `gopher` again.

If the default sign-in is refused on a first start with an empty `shiori/` folder, or you find bookmarks or accounts you did not create, somebody else got there first: stop the instance, delete the `shiori/` folder in your home and start again.

When the data already exists, because you enrolled before or restarted, nothing is created: your own accounts and passwords still apply. Shiori sends no email and has no password recovery; an owner can set another account's password under **Settings > Accounts**.

## Use it

- **Add a bookmark** with the plus button: paste the address, add tags, and tick **Create archive** or **Create Ebook** if you want them. Shiori fetches the page from the instance; the readable text, archive and e-book appear a few seconds later. The defaults for these options are under **Settings > Bookmarks**.
- **Find bookmarks** with the search field. `tag:name` includes a tag and `-tag:name` excludes one.
- **Read offline.** A bookmark's menu opens its readable content, its archive (the saved page with its images and styles) and its EPUB e-book.
- **REST API.** Sign in to get a token, valid for one hour, or thirty days with `"remember_me": true`:

  ```bash
  curl -X POST -H "Content-Type: application/json" \
       -d '{"username": "<name>", "password": "<password>", "remember_me": true}' \
       https://<instance>/api/v1/auth/login
  curl -H "Authorization: Bearer <token>" https://<instance>/api/bookmarks
  curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/json" \
       -d '{"url": "https://example.com/", "create_archive": true, "tags": [{"name": "example"}]}' \
       https://<instance>/api/bookmarks
  ```

  The upstream [API documentation](https://github.com/go-shiori/shiori/blob/master/docs/API.md) lists the other calls.
- Shiori's command-line commands (`shiori add`, `import`, `export`, `pocket` and the others) are not available: the image has no shell and the platform gives no terminal in the instance. Use the web interface or the API.

## Authentication

Shiori checks every request itself: the web interface needs your sign-in, and the API needs a token (`Authorization: Bearer ...`). Anyone who knows the instance address can reach the sign-in page, so use a strong password. Accounts are **owners**, who can add, change and delete bookmarks and accounts, or **visitors**, who can only read. A bookmark with **Make bookmark publicly available** ticked has its readable content, archive and e-book readable without signing in by anyone who has its link; bookmarks are private unless you tick that. UnitySVC adds no other gate.

## What is kept, and what is lost

Shiori's data folder is persistent: the SQLite database `shiori.db` (bookmarks, tags, accounts and the readable text) and the folders `archive/`, `ebook/` and `thumb/`. They are stored in `shiori/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before Shiori starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. Shiori on its own leaves almost all of its data in the write-ahead file, so this recipe starts it with a SQLite connection setting that moves every saved change into `shiori.db` straight away; that one file is complete.
- Files are copied, never deleted from your home. When you delete a bookmark, Shiori removes its archive, e-book and thumbnail, but the copies stay in `shiori/archive/`, `shiori/ebook/` and `shiori/thumb/`. Shiori no longer lists them and bookmark numbers are not reused, so they only take space; delete them from your home yourself if the page should be gone.
- Do not edit the files in `shiori/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored. Shiori's data does not use them.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `shiori/` folder yourself when you no longer want the data.
- Changing the **Session secret key** signs everyone out and changes nothing else.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check Shiori used under 10 MiB of memory idle and about 50 MiB while archiving twelve pages at once. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
