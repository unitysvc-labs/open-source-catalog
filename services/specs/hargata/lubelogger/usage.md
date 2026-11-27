# LubeLogger Vehicle Maintenance and Fuel Tracker

Each enrollment runs a private [LubeLogger](https://lubelogger.com) server. LubeLogger is written and maintained by [Hargata Softworks](https://github.com/hargata) and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `ghcr.io/hargata/lubelogger` image (version 1.7.5, pinned by digest), and the platform runs one isolated instance per enrollment. The author was not asked to take part in this listing, and nothing here means the author endorses it or supports it.

Your vehicles and records are kept in the `lubelogger` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `lubelogger/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one LubeLogger instance at a time.
2. The form shows a **Root user name** (default `admin`) and a generated **Root password**. They are the sign-in of LubeLogger's root user, the built-in administrator. Save the password now: the platform keeps it as a secret and does not show it again. They are application credentials, not your UnitySVC API key. **Locale** sets the currency symbol and the number and date formats (default `en_US.UTF-8`).
3. Wait for the instance to become ready; a start takes a few seconds. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.** LubeLogger needs no setting for it.
4. Open the address and sign in with the root user name and password.

## Use it

1. In the **Garage**, choose **Add New Vehicle** and enter its year, make, model and license plate.
2. Open the vehicle and add records on its tabs: service, repairs, upgrades, fuel, odometer, taxes, notes, supplies and the planner. A record can carry attached files (by default `.png`, `.jpg`, `.jpeg`, `.pdf`, `.xls`, `.xlsx` and `.docx`).
3. Add **reminders** by date or by distance; the vehicle's dashboard and the garage show what is due. Reminders are shown in the interface only: no mail server is set up, so none are emailed.
4. The **Reports** tab shows costs and fuel economy, and each tab can import and export its records as CSV.
5. **Settings** holds the display options (units, dark mode, visible tabs, language), a backup you can download and restore, and the server settings.

LubeLogger has a REST API under `/api`. The root user signs in to it with HTTP Basic authentication:

```bash
curl -u "admin:<password>" https://<instance>/api/vehicles
curl -u "admin:<password>" -d "date=2026-11-27" -d "odometer=12345" -d "notes=first reading" \
     "https://<instance>/api/vehicle/odometerrecords/add?vehicleId=1"
```

The [LubeLogger documentation](https://docs.lubelogger.com) describes the API, API keys and the other features.

## Authentication

LubeLogger checks every request itself: the web interface needs a sign-in and the API needs a user's credentials or an API key. Only the sign-in pages and `/health` (which reports the version and the database status) answer without one. Anyone who knows the instance address can reach the sign-in page, so keep the root password strong; LubeLogger does not lock an account after failed attempts. UnitySVC adds no other gate.

Upstream LubeLogger starts with authentication **off**, and turns it on from three documented settings: `EnableAuth`, and the SHA-256 hashes of the root user's name and password (`UserNameHash`, `UserPasswordHash`). This recipe sets `EnableAuth` and, at every start, hashes your **Root user name** and **Root password** with the `sha256sum` tool of the image and passes the hashes to LubeLogger; the container stops if either value is missing. The instance therefore requires sign-in from its first start.

- **When the parameters stop applying.** The first time the root user saves any setting in LubeLogger, it writes its sign-in settings (the same hashes) to `config/userConfig.json` in your data, and that file takes precedence from then on. After that, changing the **Root user name** or **Root password** of the enrollment has no effect, also in a later enrollment that finds the file in your home.
- **Changing the root password later** is done in LubeLogger: in **Settings**, switch **Enable Authentication** off and on again, and enter the new name and password. Between the two steps (and about a second after each) the instance has **no sign-in at all**, and anyone who knows the address can read and change everything. Do it quickly, and do not leave authentication off: this instance is reachable from the internet.
- **More people.** Self-registration is closed. As root, open **Admin**, generate a registration token for the person's email address, and give them the token; they register at `https://<instance>/Login/Registration` with that email address and token. Their sign-in cookie, like yours, survives a restart.
- **No email.** LubeLogger emails registration tokens, password-reset tokens and the token a user needs to change their own name, email or password. With no mail server none of these arrive: "Forgot password" does nothing, and generating a token with the notify option reports that the email failed (the token is still created). The root user can read every pending token in **Admin** and pass it on, and can reset a user's password there (LubeLogger shows the new one once).
- Single sign-on (OpenID Connect) is not configured by this recipe.

Upstream states that LubeLogger is not designed for serious enterprise deployments.

## What is kept, and what is lost

Two folders are persistent, both under `lubelogger/` in your home, where you can see them in your files while the instance is stopped: `data/` holds the LiteDB database (`cartracker.db`, with the vehicles, records, users and tokens), the uploaded `documents/` and `images/`, `translations/`, `themes/`, `temp/` and the settings in `config/`; `keys/` holds the keys that encrypt the sign-in cookie, so a restart does not sign you out. The platform restores them before LubeLogger starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- LiteDB's transaction log (`cartracker-log.db`) is not stored. LiteDB empties it into the database after each change, and leaving it out keeps an old log from being restored beside a newer database.
- **Files are copied, never deleted from your home.** A document or photo you remove in LubeLogger can stay in `lubelogger/data/`; LubeLogger no longer shows it. The same holds for `temp/`: uploads that were never attached to a saved record and the backup and export archives you create collect there, and the **Clear Temp Files** action in LubeLogger's settings does not remove them from your home. Delete what you no longer want from `lubelogger/data/temp/` yourself while the instance is stopped.
- Do not edit the other files in `lubelogger/` while the instance is stopped: the next start restores them as they are. Deleting `data/config/userConfig.json` makes the enrollment's root user name and password apply again.
- Empty files, symbolic links and files over 1 GiB are not stored. LubeLogger does not depend on any of them.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `lubelogger/` folder yourself when you no longer want the data.
- Settings you change on LubeLogger's server settings page are kept in `config/serverConfig.json`. Do not set a PostgreSQL connection or a listening address there: this recipe runs one container with the embedded database on port 8080.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check LubeLogger used about 40 MiB after starting and under 90 MiB at its peak while serving pages, API calls and an 8 MB upload. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
