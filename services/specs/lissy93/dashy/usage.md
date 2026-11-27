# Dashy Dashboard

Each enrollment runs a private [Dashy](https://dashy.to/) dashboard. Dashy is written and maintained by [Alicia Sykes](https://github.com/Lissy93) and contributors and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `lissy93/dashy` image (version 4.10.0, pinned by digest), and the platform runs one isolated instance per enrollment.

Your dashboard configuration is kept in the `dashy` folder of your **home**, not in the enrollment. It survives stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same configuration.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `dashy/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Dashy instance at a time.
2. The form shows a **Login name** (default `admin`) and a generated **Login password**. Keep the generated password or enter your own, and save it; it is also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so bookmarks and browser start pages that point at the old one need the new one.
4. Open the address. Your browser asks for the login name and password; enter them. The first time, Dashy shows its starter dashboard (links to the Dashy site, sponsors and a release feed).

## Edit the dashboard

1. Open the config menu at the top right and choose **Edit Config**, or use the visual editor, change `conf.yml` and save. Dashy writes the file and keeps the previous version in `config-backups/`.
2. The [configuring](https://dashy.to/docs/configuring) guide in the Dashy documentation lists sections, items, icons, themes and widgets. Many widgets and status checks call other websites from the instance.
3. You can also change the files in the `dashy/` folder of your home while the instance is **stopped**; the next start restores them.

## Authentication

This service uses Dashy's static credentials (`BASIC_AUTH_USERNAME` and `BASIC_AUTH_PASSWORD`). The server asks for them before it returns your configuration (`conf.yml`), saves a change, runs a status check or reads the configuration API, and your browser caches them for the session. The login is one shared identity: everyone who knows the name and password can edit the dashboard. There are no separate users or roles, and Dashy's own sign-in page, guest mode and single sign-on are not set up here.

The page's code and the `/healthz` health check answer without a login, but they contain none of your configuration. The login name and password are read at every start, so changing them in the enrollment and restarting changes the login. UnitySVC adds no other gate. Keep the password strong: it is the only thing between the internet and your configuration.

## What is kept, and what is lost

Dashy's `user-data` folder is persistent: `conf.yml`, the `config-backups/` folder and any other files you put there, such as icons. They are stored in `dashy/` in your home. The platform restores them before Dashy starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- On the first start in an empty folder, the instance copies Dashy's starter `conf.yml` into it. After that your own file is used and never replaced.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a configuration you just saved. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file Dashy removes, such as an old backup, can come back after a restart. This is cosmetic.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `dashy/` folder yourself when you no longer want the data.
- Settings you keep only in your browser (for example a chosen theme) stay in that browser and are not part of the instance.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Dashy used about 90 MiB in a local check. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
