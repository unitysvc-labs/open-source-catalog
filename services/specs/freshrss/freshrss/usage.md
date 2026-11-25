# FreshRSS Feed Reader

Each enrollment runs a private [FreshRSS](https://freshrss.org/) server. FreshRSS is written and maintained by [Alexandre Alapetite](https://github.com/Alkarex) and contributors and is released under the AGPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `freshrss/freshrss` image (version 1.31.0, pinned by digest), and the platform runs one isolated instance per enrollment. FreshRSS keeps its data in a SQLite database; this recipe uses no separate database server.

Your feeds, articles, users and settings are kept in the `freshrss` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `freshrss/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one FreshRSS instance at a time.
2. The form shows an **Administrator name** (default `admin`), a generated **Administrator password** and a generated **API password**. They create the account the **first time** FreshRSS starts on an empty data folder. If the data already exists, because you enrolled before or restarted, the three values are ignored and the existing account and passwords still apply; change passwords in FreshRSS's own settings. Save the values; they are also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key. Passwords are 12 to 72 characters of letters, digits and `_ . + -`.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so apps that point at the old one need the new one.
4. Open the address and sign in with the administrator name and password. The reader starts empty: add feeds with **Subscription management**, or import an OPML file there.

## Read feeds from an app

The Google Reader compatible and Fever APIs are enabled. In a feed-reader app that supports them, use the address of your instance (the API is at `https://<instance>/api/greader.php`), your user name, and the **API password**. The web password does not work for the APIs. The Fever API is at `https://<instance>/api/fever.php`. Only the Google Reader login request was checked here (the API password is accepted, the web password is refused); no Fever client or mobile app was tried.

## Refreshing and the base URL

A built-in cron job refreshes all feeds at minutes 17 and 47 of every hour, as long as the instance runs. A stopped instance refreshes nothing, and articles that the feeds dropped meanwhile are not recovered.

FreshRSS has an optional `base_url` setting, used to build absolute links, for example for WebSub (PubSubHubbub). It is empty here and the reader works without it. If you want to set it, it can only be set in the `config.php` file in `freshrss/data/` in your home, while the instance is stopped; use the instance address, which changes with every enrollment. WebSub is off by default and was not tried.

## Authentication

FreshRSS checks every request itself: the web interface needs your sign-in and the APIs need the API password. Anyone who knows the instance address can reach the sign-in page, so keep both passwords strong. UnitySVC adds no other gate.

## What is kept, and what is lost

Two folders are persistent: `freshrss/data/` (configuration, users, the SQLite databases, caches) and `freshrss/extensions/` (FreshRSS extensions; empty until you add some). They are stored in your home, where you can see them in your files while the instance is stopped. The platform restores them before FreshRSS starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folders belong to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file FreshRSS removes, such as an old cache file, can come back after a restart. This is cosmetic.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by FreshRSS and this keeps the stored database consistent.
- Do not edit the files in `freshrss/` while the instance is stopped, except as described above: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `freshrss/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. FreshRSS used about 50 to 100 MiB in a local check. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
