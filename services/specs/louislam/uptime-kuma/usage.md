# Uptime Kuma Monitoring

Each enrollment runs a private [Uptime Kuma](https://kuma.pet/) server. Uptime Kuma is written and maintained by [Louis Lam](https://github.com/louislam) and contributors and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `louislam/uptime-kuma` image (version 2.5.12, the `slim` variant, pinned by digest), and the platform runs one isolated instance per enrollment.

Your monitors, history, status pages and settings are kept in the `uptime-kuma` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## It only monitors while it runs

Uptime Kuma checks your targets from inside its own container. **When you stop the instance, or it is stopped for any reason, no checks run and no alerts are sent**, and the dashboard shows a gap for that time. A monitor that is down while the instance is stopped is not reported. If you need continuous monitoring, leave the instance running and keep in mind that you pay for it while it runs (see Cost and size).

## Set up

1. Enroll in **base**. The enrollment asks for access to the `uptime-kuma/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Uptime Kuma instance at a time.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so status pages, bookmarks and push-monitor URLs that point at the old one need the new one.
3. **Open the address at once and create the administrator.** On a new data folder Uptime Kuma shows a setup page asking for a user name and a password. There is no preset account and no parameter for it: **whoever opens the address first creates the administrator**, so do this yourself before anyone else could. Choose a strong password. After the first account exists, the setup page is closed and the sign-in page is shown. If your data folder already holds a database (an earlier enrollment), you go straight to sign-in with the account you made then.
4. Sign in and add monitors.

## Add a monitor

1. Choose **Add New Monitor**, a type (for example HTTP(s)), a name and the URL.
2. Pick a check interval (the default is 60 seconds) and, under **Notifications**, set up where alerts go (email, Discord, Telegram, Slack and many more). Notification services are reached from the instance over the internet, so they need their own credentials, which you enter in Uptime Kuma.
3. Save. The monitor starts at once and its status and response times appear on the dashboard.

Status pages and maintenance windows are in the same interface. A status page is served from the instance's own address, so it is reachable only while the instance runs.

## Authentication

Uptime Kuma checks sign-in itself: the dashboard and its websocket need the administrator's login, and a status page you publish is public by design. Anyone who knows the instance address can reach the sign-in page, so use a strong password and turn on two-factor authentication in Settings if you want it. UnitySVC adds no other gate.

## What is kept, and what is lost

Uptime Kuma's data folder is persistent: the SQLite database (`kuma.db`, with your account, monitors and heartbeat history), uploaded images and screenshots. It is stored in `uptime-kuma/` in your home, where you can see it in your files while the instance is stopped. The platform restores it before Uptime Kuma starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include the newest heartbeats or a monitor you just added. A normal stop loses nothing.
- SQLite's temporary write-ahead files (`kuma.db-wal`, `kuma.db-shm`) are not stored. They are rebuilt by Uptime Kuma and this keeps the stored database consistent.
- Files are copied, never deleted from your home. Do not edit the files in `uptime-kuma/` while the instance is stopped: the next start restores them over what you changed.
- Heartbeat history grows with the number of monitors and how often they run (Uptime Kuma keeps 180 days by default, changeable in Settings > Monitor History). A very large database takes longer to copy; files over 1 GiB are not stored at all, so keep the monitor count and the retention modest.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `uptime-kuma/` folder yourself when you no longer want the data.

## Limits of this recipe

- This is the `slim` image: it has no Chromium, so the **Real Browser** monitor type does not work, and no embedded MariaDB; the database is SQLite and cannot be changed.
- The Docker monitor type needs the Docker socket, which a UnitySVC instance does not have, so it is unavailable.
- Checks are made from the instance's network position. They see what the platform's network lets a container reach, so a target on your own private network is not reachable unless it is public.
- Only the web interface is exposed. Push monitors work through the same HTTPS address.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check Uptime Kuma used about 165 MiB when idle and about 185 MiB with five monitors checking every 20 seconds. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
