# Wallos Subscription Tracker

Each enrollment runs a private [Wallos](https://wallosapp.com/) instance. Wallos is written and maintained by [Miguel Ribeiro](https://github.com/ellite) and contributors and is released under the GPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `bellamy/wallos` image (version 5.11.3, pinned by digest), and the platform runs one isolated instance per enrollment.

Your subscriptions, account and uploaded logos are kept in the `wallos` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `wallos/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Wallos instance at a time.
2. The form shows a **Time zone** (default `UTC`). Use an IANA name such as `Europe/Lisbon`. It is read each time the instance starts.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so bookmarks need the new one.
4. **Open the address and register immediately.** A new Wallos has no account, and the registration page is open to anyone who reaches the address. The first account you create becomes the administrator, and Wallos closes registration once it exists. If somebody else registers first, stop the instance, delete the `wallos/` folder in your home and start again.

## First use

1. Sign in with the account you registered. There is no administrator password parameter: the password is the one you chose on the registration page.
2. Add a subscription: name, price, currency, billing cycle, next payment date, category and payment method. Wallos lists them with the next payment date and the monthly and yearly totals.
3. Wallos can also upload a logo for each subscription; the files are kept with the database. Notification, currency-rate and other options are in its settings and are described in the [Wallos documentation](https://github.com/ellite/Wallos); features that reach outside services, such as email or exchange-rate lookups, need the settings and credentials you give them there.

## Authentication

Wallos checks every request itself: the web interface needs your sign-in. Anyone who knows the instance address can reach the sign-in page, so use a strong password. Once your account exists, registration is closed. UnitySVC adds no other gate.

## What is kept, and what is lost

Two folders are persistent: the SQLite database (`wallos/db` in your home) and the uploaded logos (`wallos/logos`). The platform restores them before Wallos starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folders belong to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. A logo Wallos removes can come back after a restart. This is cosmetic.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Wallos and this keeps the stored database consistent.
- Do not edit the files in `wallos/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `wallos/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Wallos used about 45 MiB in a local check. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
