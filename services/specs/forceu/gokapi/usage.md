# Gokapi File Sharing Server

Each enrollment runs a private [Gokapi](https://github.com/Forceu/Gokapi) server. Gokapi is written and maintained by Marc Bulling ([Forceu](https://github.com/Forceu)) and contributors and is released under the AGPL-3.0 license ([license text](https://github.com/Forceu/Gokapi/blob/v2.2.4/LICENSE.md)); the provider of this service is its author. UnitySVC Labs lists the official `f0rc3/gokapi` image (version 2.2.4, pinned by digest), and the platform runs one isolated instance per enrollment. The author was not asked to take part, and nothing here implies endorsement or support. See the [Gokapi documentation](https://gokapi.readthedocs.io/en/latest/).

Your files, users and settings are kept in the `gokapi` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up: whoever arrives first becomes the administrator

Gokapi has no setting that creates its administrator, and this service has no enrollment form for one. On first start Gokapi serves a **setup wizard** at its address, and the **first visitor chooses the administrator name and password**. There is no sign-in before that, so **open the address yourself as soon as the instance is ready**, before you share it with anyone. Once the wizard is finished Gokapi never offers it again, and the administrator you chose is stored with your data.

1. Enroll in **base**. The enrollment asks for access to the `gokapi/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Gokapi instance at a time.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
3. Open `https://<instance>/setup/start`. Until the wizard is finished, the address `/` shows only a maintenance page. Go through the steps:
   - **Database:** keep SQLite and its default location (`./data/gokapi.sqlite`).
   - **Webserver:** keep the port. Set **Public Facing URL** to the instance's own address with a trailing slash, `https://<instance>/`: Gokapi builds every download link from it, and it cannot be found out by Gokapi itself. If the address is wrong, links point to the wrong place. A new enrollment has a new address, so after re-enrolling the stored address is the old one and download links keep pointing at it. Gokapi's documentation describes running its setup again to change it; this was not tested here. Leave **Use SSL** off: the platform provides HTTPS.
   - **Authentication:** choose **Username / Password** and enter the administrator name and a password of at least 8 characters. Other methods (OpenID Connect, header authentication) need services this instance does not have; do not choose **Disabled**, which leaves the admin pages open.
   - **Storage:** keep **Local storage**. Cloud storage and end-to-end encryption are not covered by this recipe.
4. Submit, then continue. Gokapi opens its admin page at `https://<instance>/admin`; sign in with the administrator you chose. The credentials are application credentials chosen by you, not your UnitySVC API key. Save them: nothing else records them.

## First use

1. In the admin page, drop a file on the upload area, set the number of downloads and days and an optional password, and upload it.
2. Copy the file's **URL** and send it. Whoever opens the link sees a download page for that file without signing in.
3. When the limit is reached or the days run out, Gokapi deletes the file.
4. The **API** menu creates API keys for uploading from scripts, and **Users** adds further users. The [usage documentation](https://gokapi.readthedocs.io/en/latest/usage.html) describes both.

## Authentication

Gokapi checks every admin request itself; downloads need only the link (and its password if you set one). Anyone who knows the instance address can reach the admin sign-in page, so use a strong password. The wizard is the weak point: it needs no sign-in, so until you finish it, **any visitor can take over the instance**. UnitySVC adds no other gate.

## What is kept, and what is lost

Gokapi's data is persistent: the uploaded files (stored as whole files under `gokapi/data/`), the SQLite database (`gokapi.sqlite`, with users, download links and settings) and the configuration (`gokapi/config/config.json`). The platform restores them before Gokapi starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a file just uploaded or a link just created. A normal stop loses nothing. If the copy of `config.json` were ever missing, Gokapi would start the setup wizard again and the first visitor would claim it.
- Files are copied, never deleted from your home. When a link expires Gokapi deletes the file from its data folder, but the copy already in your home is not removed, so expired files keep using space in your home and are expected to be restored into the folder at the next start. This was not tested. Delete old files from `gokapi/data/` yourself if that matters.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Gokapi and this keeps the stored database consistent.
- Do not edit the files in `gokapi/` while the instance is stopped: the next start restores them over what you changed.
- **Files over 1 GiB are not stored**, and so are empty files and symbolic links. This service therefore limits one upload to **500 MB** (`GOKAPI_MAX_FILESIZE`); a larger file is refused by Gokapi. The instance's temporary disk is only 1 GiB and holds the files as well, so all your files together should stay well below it; Gokapi refuses an upload when less than 100 MB of disk is free.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `gokapi/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Gokapi used about 60 to 70 MiB in a local check, including after a 3 MB upload. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
