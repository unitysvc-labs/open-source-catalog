# Beszel Server Monitoring Hub

Each enrollment runs a private [Beszel](https://beszel.dev/) hub. Beszel is written and maintained by [henrygd](https://github.com/henrygd) and contributors and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `henrygd/beszel` image (version 0.21.2, pinned by digest), and the platform runs one isolated instance per enrollment.

Beszel has two parts. This service is the **hub**: the web dashboard that stores and shows the figures. The **agent** is a small program you install yourself on each server you want to watch; it is not part of this service and does not run on the platform.

The hub's data (your accounts, systems, tokens, history and the hub's key pair) is kept in the `beszel` folder of your **home**, not in the enrollment. It survives stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Read this first

- **It records only while it runs.** Agents send their figures to the hub. While the instance is stopped nothing is recorded, no alert is sent, and the charts show a gap. Agents keep retrying and reconnect by themselves when the hub is back at the same address.
- **A crash can lose more than a few seconds.** Beszel's database keeps recent changes in a write-ahead file, which is not stored in your home. A normal stop saves everything. After a crash or a node failure the hub comes back as it was at the last checkpoint, and if there has been none since the data folder was created, as a new empty hub. See [What is kept, and what is lost](#what-is-kept-and-what-is-lost) for how to keep that window short.
- **Agents connect out to the hub.** Only this mode works here. The older mode, in which the hub dials each agent over SSH on port 45876, is not offered: this recipe does not depend on what the platform's network lets a container reach.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `beszel/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Beszel hub at a time.
2. The form shows a **Sign-in email** (default `admin@example.com`) and a generated **Password**. They create the first account the **first time** the hub runs on an empty data folder. If your home already holds a Beszel database, because you enrolled before or restarted, they are ignored and the existing accounts and passwords still apply. Save the password now: the platform keeps it as a secret and does not show it again. They are application credentials, not your UnitySVC API key. The email is only a sign-in name; the hub sends no mail to it.
3. Wait for the instance to become ready; it starts in a few seconds. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Open the address and sign in with the email and the password.

The same email and password also create a second account: the **PocketBase administrator**, at `https://<instance>/_/`. Beszel is built on PocketBase, and its admin pages are where users are added, passwords are changed and backups are made. The two accounts have separate passwords from then on.

## Add a server

1. In the hub choose **Add System** and give the server a name. The **Host / IP** field is only a label in this mode; enter the server's name or address.
2. The dialog shows a ready command for Docker (a Compose file or `docker run`) or for a binary install. It already contains three values: `HUB_URL` (this instance's address, taken from your browser), `KEY` (the hub's public key) and `TOKEN` (made for this system).
3. Run it on your server. The agent connects out to `HUB_URL` over HTTPS and keeps a WebSocket open; your server needs outbound access to port 443 and no inbound port. The system turns green in the hub within a few seconds and the charts start to fill.

For a server running Docker, the agent looks like this (take the real values from the dialog):

```yaml
services:
  beszel-agent:
    image: henrygd/beszel-agent
    restart: unless-stopped
    network_mode: host
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./beszel_agent_data:/var/lib/beszel-agent
    environment:
      LISTEN: 45876
      HUB_URL: https://<instance>
      TOKEN: <token from the dialog>
      KEY: "<public key from the dialog>"
```

**After a new enrollment** the address is different. The key and the tokens come back with your data, so on each server change only `HUB_URL` to the new address and restart the agent.

The [Beszel documentation](https://beszel.dev/guide/what-is-beszel) describes the agent's other settings, alerts, extra disks and GPU monitoring.

## Accounts, passwords and email

- **No email is sent.** The platform provides no mail server, so "forgot password" and email verification do not work, and one-time-password sign-in is not enabled.
- **Change a password** in the PocketBase admin pages: open `https://<instance>/_/`, sign in, open the `users` collection, edit the user and set a new password. A user cannot change their own password inside Beszel. Change the administrator's own password under `_superusers` in the same place.
- **Add users** in the same `users` collection, with the role `user`, `admin` or `readonly`. Self-registration is off.
- **Links in alerts.** Notifications link back to the hub using PocketBase's application URL, which starts as `http://localhost:8090`. Set it to your instance address in `/_/` under Settings > Application, and again after a new enrollment. It does not affect sign-in or the agents.
- **Alerts** go to the notification URLs you enter in Beszel's settings (webhook-style services such as Discord, Slack, ntfy or Gotify). Email alerts need an SMTP server of your own, entered in `/_/` under Settings > Mail.

## Authentication

Beszel checks every request itself. The dashboard and its API need a signed-in user, the admin pages at `/_/` need the PocketBase administrator, and an agent is accepted only with a valid token and after proving it holds the fingerprint first seen for that token; the agent in turn checks the hub's key. Anyone who knows the instance address can reach the sign-in pages, so keep the passwords strong. UnitySVC adds no other gate.

## What is kept, and what is lost

Beszel's data folder is persistent: the databases (`data.db` with accounts, systems, tokens, settings and history; `auxiliary.db` with logs), the hub's key pair (`id_ed25519`) and any backups (`backups/`). They are stored in `beszel/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before the hub starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **A normal stop loses nothing.** When the hub stops it writes everything into `data.db`, and that file is copied to your home.
- **A crash or node failure loses the changes since the last checkpoint, not just the last 30 seconds.** While it runs, the hub writes changes to a write-ahead file (`data.db-wal`) and moves them into `data.db` only at a checkpoint: when it stops, when a backup is made, once a day, or when the write-ahead file has grown large. The write-ahead file is not stored in your home, because an old copy restored beside a newer database could corrupt it. In a local test, a new hub that was killed before its first checkpoint came back as an empty hub: the first account was created again from the enrollment's current email and password, and the systems, tokens and history were gone. The key pair was kept.
- **Keep the window short with scheduled backups.** In `/_/` under Settings > Backups, turn on auto backups, for example every hour (`0 * * * *`), and keep a small number. Each backup is also a checkpoint, so `data.db` in your home is then at most that old, and the backup itself is a zip in `beszel/backups/` that you can download. Make one backup by hand right after you add your first systems.
- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- Files are copied, never deleted from your home. Backups that PocketBase removes to stay within its limit remain in `beszel/backups/` in your home and come back at the next start; delete old ones yourself while the instance is stopped.
- Do not edit the files in `beszel/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored. Beszel thins out old history by itself (one-minute figures are kept for an hour, coarser ones for up to 30 days), so the database stays small for a modest number of servers.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `beszel/` folder yourself when you no longer want the data.
- Changing the email or password parameter after the first start has no effect, because the account already exists.

## Limits of this recipe

- Only the hub runs here. The hub does not monitor the platform or itself; a system appears only when you install an agent somewhere.
- Only the web address (HTTPS, port 443) is exposed. Agents must use the outgoing WebSocket connection described above.
- The image contains only the hub program. There is no shell, so the `beszel` command line (for example `superuser upsert`) is not available; use the admin pages at `/_/` instead.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check the hub used about 14 MiB when idle with one agent connected and about 20 MiB after a burst of requests. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
