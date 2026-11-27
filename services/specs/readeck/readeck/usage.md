# Readeck Read-It-Later Archive

Each enrollment runs a private [Readeck](https://readeck.org/en/) server. Readeck is written and maintained by [Olivier Meunier](https://codeberg.org/olivier) and contributors and is released under the GNU Affero General Public License v3.0 (AGPL-3.0-only); the provider of this service is its author. UnitySVC Labs lists the official `codeberg.org/readeck/readeck` image (version 0.23.6, pinned by digest), and the platform runs one isolated instance per enrollment. This listing is unofficial: the Readeck project does not operate or support it.

Your archive is kept in the `readeck` folder of your **home**, not in the enrollment. It survives stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `readeck/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Readeck instance at a time.
2. The form shows an **Administrator name** (default `admin`) and a generated **Administrator password**. They create the administrator account the **first time** Readeck runs on your data. If the account already exists, because you enrolled before or restarted, the parameters are ignored and the existing password still applies; change it in Readeck under **Settings > Security**. Save the password now: the platform keeps it as a secret and does not show it again. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready; it starts in a few seconds. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Open the address and sign in with the administrator name and password. No address setting is needed: Readeck takes its public address from the platform's HTTPS front end.

Readeck on its own lets the first visitor create the administrator on an onboarding page. This recipe does not leave that page open: before the server starts, the instance creates the administrator with Readeck's `readeck user` command, from the two parameters. The account's email address starts as `<name>@localhost`; change it in **Settings > Profile** if you want.

## Use it

1. Paste a link into the field at the top of the bookmark list and save it. Readeck fetches the page from the instance and keeps its readable content and images; an article is ready in a few seconds.
2. Open a saved page to read it, highlight passages, add labels, mark it as a favorite or archive it. Search covers the full text, and a search can be saved as a collection.
3. Export a page or a collection as an EPUB e-book, or point an e-reader at the OPDS catalog at `https://<instance>/opds`, with an API token as its credential.

- **REST API.** Create a token in **Settings > API Tokens**; the API reference is served by the instance at `/docs/api`. Then:

  ```bash
  curl -H "Authorization: Bearer <token>" https://<instance>/api/bookmarks
  curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/json" \
       -d '{"url": "https://example.com/"}' https://<instance>/api/bookmarks
  ```

- **Browser extension and mobile applications** take the instance address and sign you in there; after a new enrollment, give them the new address. The [Readeck documentation](https://readeck.org/en/docs/) describes them, and the import from other services.

## Authentication

Readeck checks every request itself: the web interface needs your sign-in, and the API needs a token (`Authorization: Bearer ...`). Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong. A page you share with a public link is readable without signing in for 24 hours. The administrator can add other users in **Settings > Users**. UnitySVC adds no other gate.

No mail server is configured, so Readeck cannot send a password-recovery email. If you lose the administrator password, change **Administrator name** to a new name and set a new **Administrator password** in the enrollment: the next start creates a second administrator with them, and you can reset the first one from its account.

## What is kept, and what is lost

Readeck's working folder is persistent: `config.toml` (with the generated secret key, which keeps you signed in across restarts), the SQLite database, and one compressed file per saved page. They are stored in `readeck/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before Readeck starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. The file of a page you delete in Readeck stays in `readeck/data/bookmarks/`; Readeck no longer lists it, and it only takes space.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Readeck and this keeps the stored database consistent.
- Do not edit the files in `readeck/` while the instance is stopped: the next start restores them over what you changed. In particular, keep `config.toml` and its secret key.
- Empty files, symbolic links and files over 1 GiB are not stored. Readeck's data does not use them.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `readeck/` folder yourself when you no longer want the data.
- Changing the administrator parameters after the account exists does not change that account (see above).

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check Readeck used under 100 MiB of memory, idle and while saving pages. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
