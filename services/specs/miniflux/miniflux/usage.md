# Miniflux Feed Reader

Each enrollment runs a private [Miniflux](https://miniflux.app/) with its own PostgreSQL database. Miniflux is written and maintained by [Frédéric Guillot](https://github.com/fguillot) and contributors and is released under the Apache-2.0 license; the provider of this service is its author, who was not asked to take part. UnitySVC Labs lists the official `miniflux/miniflux` image (version 2.3.5) and the official `postgres` image (17, Alpine), both pinned by digest, and the platform runs one isolated stack per enrollment. PostgreSQL is released under the PostgreSQL License.

## Set up

1. Enroll in **base**. The enrollment asks for access to its own storage (`service:storage`, read and write). Approve it, or the instance does not start.
2. The form shows an **Administrator name** (default `admin`), a generated **Administrator password** and a generated **Database password**. The administrator values create the administrator account the **first time** Miniflux runs on the data. Once the account exists the password parameter is ignored and you change the password in Miniflux itself (**Settings**). Save the administrator password now: the platform keeps it as a secret and does not show it again. These are application credentials, not your UnitySVC API key.
3. Leave **Instance address (optional)** as it is. See [The instance address](#the-instance-address) for the few features that need it.
4. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address and empty data.**
5. Open the address and sign in with the administrator name and password.

## First use

1. Choose **Feeds > Add feed**, paste the address of a site or of its feed, and pick a category. Miniflux finds the feed, fetches it and then refreshes it in the background.
2. To bring your subscriptions from another reader, use **Feeds > Import** with an OPML file. **Feeds > Export** writes one.
3. Read under **Unread**; press `?` for the keyboard shortcuts.

For other people, create users under **Settings > Users**. Miniflux has no public sign-up page, and each user has their own feeds.

### Reader apps and the API

- **REST API.** Create a key under **Settings > API Keys** and send it as `X-Auth-Token`:

  ```bash
  curl -H "X-Auth-Token: <key>" https://<instance>/v1/me
  curl -H "X-Auth-Token: <key>" "https://<instance>/v1/entries?status=unread&limit=10"
  ```

  The API also accepts your user name and password as HTTP Basic authentication.
- **Google Reader and Fever compatible APIs.** Both are off until you turn them on under **Settings > Integrations**, where you choose a separate user name and password for the app. Give the reader app the instance address and those credentials.

See the [Miniflux documentation](https://miniflux.app/docs/) for filter rules, full-text fetching, integrations and the API reference.

## The instance address

Miniflux serves its pages with relative links, so sign-in, reading and the APIs work at the instance address without any setting. It uses its configured base address only for:

- passkeys (WebAuthn sign-in), which are bound to that address;
- the absolute links it puts into API answers for feed icons and for images it proxies, which some reader apps display;
- the links in notifications sent by a few integrations (for example ntfy and Telegram).

If you need one of these, set **Instance address (optional)** to your instance address, for example `https://abc123.example.app` with no trailing slash, and save. Saving restarts the instance; your data stays. A new enrollment has a new address, so set it again. Miniflux's sign-in with Google or OpenID Connect is not configured in this recipe.

## Authentication

Miniflux checks every request itself: the web interface needs your sign-in, and the APIs need an API key or your credentials. The sign-in page and a health check at `/healthcheck` are open. An entry you share by link is readable by anyone with that link. Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong. UnitySVC adds no other gate. The database is reachable only from inside the instance.

## What is kept, and what is lost

Miniflux keeps everything in PostgreSQL: feeds, categories, articles, read and starred state, users, settings and API keys. It writes no files of its own. One folder of the enrollment's storage is persistent: a backup of that database. The database itself runs on temporary disk; the instance writes a backup of it every five minutes and once more when it stops, and restores that backup when it starts. The platform copies the backup to storage about every 30 seconds while the instance runs and once more when it stops. Stopping therefore takes a moment longer while the backup and the copy finish.

- A normal stop loses nothing. A crash, or a node failure, can lose the changes made since the last backup, up to five minutes: read marks, new subscriptions and settings changed in that time. Articles are fetched again from their feeds.
- The backup is one file and must stay under 1 GiB, the largest file the platform's storage copy keeps. Miniflux removes read articles after 60 days and unread ones after 180 days by default, which keeps an ordinary set of feeds far below that. Export your subscriptions (**Feeds > Export**) from time to time if you cannot lose them.
- Keep the **Database password** as it is. It is used only between the two containers of your instance.
- Changing the **Administrator name** later creates a second administrator with the **Administrator password** then set, and leaves the first account in place.
- Removing the enrollment removes its storage. Enrolling again starts with an empty Miniflux and new passwords.

Miniflux sends no email, so nothing here depends on a mail server. A forgotten password is reset by an administrator under **Settings > Users**. If the only administrator's password is lost, change the **Administrator name** and **Administrator password** parameters: at the next start Miniflux creates a second administrator with them, and that account can reset the first.

## Cost and size

Each of the two containers (Miniflux and PostgreSQL) runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for both for as long as the instance runs, including idle time. In a local check with those limits Miniflux used about 15 MiB idle and 26 MiB after fetching a feed, and PostgreSQL about 30 MiB. Labs adds no markup and receives no seller payout.
