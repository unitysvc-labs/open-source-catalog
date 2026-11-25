# Slash Link Shortener

Each enrollment runs a private [Slash](https://github.com/yourselfhosted/slash) server. Slash is written and maintained by the [yourselfhosted project](https://github.com/yourselfhosted) and contributors and is released under the AGPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `yourselfhosted/slash` image (version 1.0.0-rc.3, a release candidate, pinned by digest), and the platform runs one isolated instance per enrollment.

Your shortcuts, collections and users are kept in the `slash` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. It has no settings to fill in. The enrollment asks for access to the `slash/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Slash instance at a time.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so anything that points at the old one (shortcuts you shared, the browser extension) needs the new one.
3. **Open the address and sign up immediately.** On a new instance the first account registered becomes the administrator, and there is no password to protect that step. Anyone who reaches the address before you could register first and take the administrator account. If that happens, stop and remove the instance, delete the `slash/` folder of your home, and enroll again.
4. After you have signed up, sign in as the administrator, open the workspace settings and turn on the option that disallows user registration, so that nobody else can create an account. Through the API this is the `disallowUserRegistration` workspace setting; with it on, a new sign-up is refused ("sign up is not allowed"). Leave registration open only if you want others to sign up themselves; every account that signs up while it is open can read what you share with signed-in users.

## Make and use shortcuts

1. In the web interface create a shortcut: a short name such as `docs`, the URL it stands for, optional tags, and its visibility (private to you, shared with signed-in users of this instance, or public).
2. A shortcut is reached at `https://<instance>/s/<name>`. Public shortcuts open for anyone who has the address; the others need a sign-in.
3. A collection groups several shortcuts under one name that you can share. Each shortcut keeps a view count (`viewCount` in the API).
4. To call the API, sign in with `POST /api/v1/auth/signin` (email and password as query parameters; the access token comes back in the `slash.access-token` cookie, also visible as the `Grpc-Metadata-Set-Cookie` header) and send it as a bearer header:

   ```bash
   curl -X POST "https://<instance>/api/v1/shortcuts" \
        -H "Authorization: Bearer <access token>" \
        -H "Content-Type: application/json" \
        -d '{"name": "docs", "link": "https://example.com/docs", "visibility": "PUBLIC"}'
   ```

5. `GET /api/v1/shortcuts` lists your shortcuts; without a token the API answers 401. Slash also has browser extensions that turn `s/name` typed in the address bar into the link; point them at your instance address. The [Slash documentation](https://github.com/yourselfhosted/slash/tree/main/docs) describes the rest.

## Authentication

Slash checks every request itself: the web interface and the API need your sign-in, except for public shortcuts. Anyone who knows the instance address can reach the sign-in page, so use a strong password and keep tokens private, and turn off registration as described above. UnitySVC adds no other gate.

## Limits of Slash's free plan

Slash's own documentation says its free plan is meant for personal use: an instance can have 5 accounts, 100 shortcuts and 5 collections. Slash sells larger limits and extra features (single sign-on, advanced analytics) as paid plans under a license key you enter in its settings; this service does not include or provide such a key. Check the [Slash subscription page](https://github.com/yourselfhosted/slash/blob/main/docs/getting-started/subscription.md) for what applies to your use.

## What is kept, and what is lost

Slash's data folder is persistent: the SQLite database (users, shortcuts, collections, settings). It is stored in `slash/` in your home, where you can see it in your files while the instance is stopped. The platform restores it before Slash starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a shortcut just created. A normal stop loses nothing.
- Files are copied, never deleted from your home.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Slash and this keeps the stored database consistent.
- Do not edit the files in `slash/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `slash/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Slash used about 25 MiB in a local check. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
