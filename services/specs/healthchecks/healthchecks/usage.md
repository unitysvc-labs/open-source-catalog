# Healthchecks Cron Job Monitoring

Each enrollment runs a private [Healthchecks](https://healthchecks.io/) server. Healthchecks is written and maintained by [Pēteris Caune](https://github.com/cuu508) and contributors and is released under the BSD 3-Clause license; the provider of this service is its author. UnitySVC Labs lists the official `healthchecks/healthchecks` image (version 5.0.3, pinned by digest), and the platform runs one isolated instance per enrollment. This listing is not the hosted healthchecks.io service.

Your account, checks and ping history are kept in the `healthchecks` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `healthchecks/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Healthchecks instance at a time.
2. The form shows an **Account email** (default `admin@example.com`) and a generated **Account password**. They create a superuser account the **first time** Healthchecks runs on your data; Healthchecks signs you in by email address, and the address does not have to receive mail. If an account with that address already exists, because you enrolled before or restarted, the parameters are ignored and the existing password still applies; change it in the admin pages (see **Authentication**). Save the password now: the platform keeps it as a secret and does not show it again. They are application credentials, not your UnitySVC API key.
3. Keep the generated **Signing secret**. Healthchecks signs its session cookies with it; you never type it.
4. Wait for the instance to become ready; a start takes a few seconds. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
5. Open the address and sign in with the account email and password.
6. Replace **Instance address** with that address, for example `https://abc123.example.app` (no trailing slash), and save. It starts as the placeholder `https://instance.invalid`, because the platform needs a value before the instance exists. Healthchecks builds the ping URLs, badge URLs and links it shows from this setting, not from the address you opened, so until you set it the ping URLs in the interface begin with `https://instance.invalid/ping/` and point nowhere. Sign-in and incoming pings work either way. Saving restarts the instance; your data stays. Do this again after every new enrollment, and update the ping URLs in your jobs, since the address changed.
7. If sign-in fails with a "CSRF verification failed" page, the platform's proxy did not tell Healthchecks that the request used HTTPS (the image reads the `X-Forwarded-Proto` header). Contact UnitySVC support; this recipe has no setting for it.

## Monitor a job

1. Sign in. A first project with one check is already there; open it, or use **Add Check**, and give it a name and a schedule: a simple period with a grace time, or a cron expression with a time zone.
2. Copy the check's ping URL. With the instance address set it reads `https://<instance>/ping/<uuid>`. If you have not set it yet, replace `https://instance.invalid` with your instance address yourself.
3. Request the URL at the end of the job:

   ```bash
   # m h dom mon dow  command
   0 3 * * * /usr/local/bin/backup.sh && curl -fsS -m 10 --retry 5 https://<instance>/ping/<uuid>
   ```

   Append `/start` when the job begins to measure its run time, `/fail` to report a failure, or `/<exit-status>` to report the command's exit code. A request body (up to 10 kB) is kept in the check's log.
4. Open **Integrations** and add where alerts go: a webhook, Slack, Microsoft Teams, Mattermost, Google Chat, ntfy, Gotify, PagerDuty, Opsgenie, Zulip and others. When a ping is later than the schedule plus the grace time, the check goes down and Healthchecks notifies the integrations assigned to it, and again when it comes back up. Integrations do not call private network addresses.

The management REST API (`https://<instance>/api/v3/...`) takes a project API key in the `X-Api-Key` header; create the key in the project's **Settings**. The [Healthchecks documentation](https://healthchecks.io/docs/) describes the API, the ping endpoints and each integration; where it shows `hc-ping.com` or `healthchecks.io`, use your instance address.

## Authentication

Healthchecks checks requests itself. The web interface needs your sign-in, and the management API needs a project API key (without one it answers 401). Sign-up is closed (`REGISTRATION_OPEN=False`), so nobody who finds the address can create an account; more accounts can only be added in the admin pages. Ping URLs need no credentials by design: anyone who knows a check's URL can ping it, so treat the URLs as secrets. Anyone who knows the instance address can reach the sign-in page, so keep the password strong. UnitySVC adds no other gate.

To change the password, open `https://<instance>/admin/`, choose **Users**, open your user and use the password form there. The account created at enrollment is a superuser, so it can use these admin pages, which show every record of the instance. The **Set Password**, **Change Email** and two-factor pages under **Account Settings** first confirm with a code sent by email; this instance sends no email, so they fail with a server error.

## What this instance does not do

- **No email.** No mail server is configured, so the **Email** integration (one is created for your account automatically), the weekly and monthly reports, the sign-in link by email, project invitations, and the confirmation code that **Account Settings** asks for before changing the password, the email address or two-factor settings do not work. Use another integration for alerts, change the password in the admin pages, and keep it safe: a lost password cannot be recovered through the web interface.
- **No pinging by email.** The image's SMTP listener is not started and the instance has only an HTTPS entry.
- **Integrations that need their own application credentials are not set up:** Discord, Telegram, Matrix, Signal, Pushover, Pushbullet, SMS and WhatsApp, Trello, Apprise and shell commands do not appear.
- **Checks are judged only while the instance runs.** A stopped instance receives no pings and sends no alerts. After it starts again, checks whose pings were due while it was stopped are reported down.
- **No two-factor sign-in.** Adding an authenticator app or a security key needs the emailed confirmation code, so neither can be set up.

## What is kept, and what is lost

Healthchecks' SQLite database (`hc.sqlite`) is persistent: accounts, projects, checks, the ping log and integrations. It is stored in `healthchecks/` in your home, where you can see it in your files while the instance is stopped. The platform restores it before Healthchecks starts, copies it back about every 30 seconds while it changed, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a ping just received. A normal stop loses nothing.
- SQLite's temporary files (`*-journal`, `*-wal`, `*-shm`) are not stored. They are rebuilt by Healthchecks and this keeps the stored database consistent.
- Do not edit the files in `healthchecks/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored. Healthchecks keeps the last 100 pings of each check, so the database stays small.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `healthchecks/` folder yourself when you no longer want the data.
- The **Account email** and **Account password** parameters only matter when the account is first created; changing them later does not change an existing account. The **Signing secret** and **Instance address** are read at every start.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. It runs two web workers instead of the image's default four to fit that size; in a local check it used about 240 MiB idle and 270 MiB after a few hundred requests. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
