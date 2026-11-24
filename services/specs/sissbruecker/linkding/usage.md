# linkding Bookmark Manager

Each enrollment runs a private [linkding](https://linkding.link/) server. linkding is written and maintained by [Sascha Ißbrücker](https://github.com/sissbruecker) and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `sissbruecker/linkding` image (version 1.47.0, pinned by digest), and the platform runs one isolated instance per enrollment.

Your bookmarks are kept in the `linkding` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `linkding/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one linkding instance at a time.
2. The form shows an **Administrator name** (default `admin`) and a generated **Administrator password**. They create the administrator account the **first time** linkding runs on your data. If the account already exists, because you enrolled before or restarted, the parameters are ignored and the existing password still applies; change it in linkding's own settings. Save the values; they are also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Replace **Trusted origins (instance address)** with that address, for example `https://abc123.example.app`, and save. It starts as the placeholder `https://instance.invalid`, which trusts nothing (the platform needs a value there). linkding refuses a sign-in or any form post from an address it does not trust, and behind the platform's HTTPS front end it does not know its own. Saving restarts the instance; your data stays. Do this again after every new enrollment.
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

- **Browser extensions and the bookmarklet** take the instance address and the token or your sign-in; after a new enrollment, give them the new address. The [linkding documentation](https://linkding.link/) describes them, and the import and export of bookmarks.

## Authentication

linkding checks every request itself: the web interface needs your sign-in, and the API needs your token (`Authorization: Token ...`). Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong. UnitySVC adds no other gate.

## What is kept, and what is lost

linkding's data folder is persistent: the database, the generated secret key (it keeps you signed in across restarts), and the favicons, previews and assets. They are stored in `linkding/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before linkding starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. A favicon or preview linkding removes can come back after a restart. This is cosmetic.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by linkding and this keeps the stored database consistent.
- Do not edit the files in `linkding/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `linkding/` folder yourself when you no longer want the data.
- Optional page snapshots, which the upstream project offers in a separate `-plus` image, are not part of this recipe.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
