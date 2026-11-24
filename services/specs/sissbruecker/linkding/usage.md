# linkding Bookmark Manager

Each enrollment runs its own private [linkding](https://linkding.link/) server. linkding is written and maintained by [Sascha Ißbrücker](https://github.com/sissbruecker) and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `sissbruecker/linkding` image (version 1.47.0, pinned by digest), and the platform runs one isolated instance per enrollment. The instance keeps your bookmarks between runs.

## Set up

1. Enroll in **base**. The enrollment asks for access to your storage (`service:storage`, read and write): linkding's data is kept there so it survives stopping and restarting. Approve it, or the instance does not start.
2. The form shows an **Administrator name** (default `admin`) and a generated **Administrator password**. Keep the password or replace it with your own (at least 12 characters), then save it. They are stored with the enrollment (view and copy them from the instance details) and given to linkding at its first start. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it.
4. Replace **Trusted origins (instance address)** with that address, for example `https://abc123.example.app`, and save. It starts as the placeholder `https://instance.invalid`, which trusts nothing (the platform needs a value there). linkding refuses a sign-in or any form post from an address it does not trust, and behind the platform's HTTPS front end it does not know its own. Saving restarts the instance; your data stays.
5. Open the address, sign in with the administrator name and password, and add a bookmark.

## Use it

- **Add and find bookmarks** in the web interface, with tags, notes, bundles, search and filters.
- **REST API.** The personal token is in **Settings > Integrations**. Then:

  ```bash
  curl -H "Authorization: Token <token>" https://<instance>/api/bookmarks/
  curl -X POST -H "Authorization: Token <token>" -H "Content-Type: application/json" \
       -d '{"url": "https://example.com", "tag_names": ["example"]}' \
       https://<instance>/api/bookmarks/
  ```

- **Browser extensions and the bookmarklet** take the instance address and the token or your sign-in. The [linkding documentation](https://linkding.link/) describes them, and the import and export of bookmarks.

## Authentication

linkding checks every request itself: the web interface needs your sign-in, and the API needs your token (`Authorization: Token ...`). Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong. UnitySVC adds no other gate.

The password parameter applies at the **first start only**. Your account lives in the data that persists, so changing the parameter later does not change the password; change it in linkding's own settings. Changing the administrator name later creates a second administrator and leaves the first.

## What is kept, and what is lost

linkding's data folder is persistent: the database, the generated secret key (it keeps you signed in across restarts), and the favicons, previews and assets. The platform restores it before linkding starts, copies new and changed files to your account's storage about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`. You can see the files in your storage while the instance is stopped.

- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from storage. A favicon or preview linkding removes can come back after a restart. This is cosmetic.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by linkding and this keeps the stored database consistent.
- Do not edit the stored files while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your storage automatically, including when you cancel the enrollment. Delete the files yourself when you no longer want them.
- Optional page snapshots, which the upstream project offers in a separate `-plus` image, are not part of this recipe.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Labs adds no markup and receives no seller payout. The persistent data is kept in your files, which are not billed while that feature is in preview.
