# Spoolman Filament Inventory

Each enrollment runs a private [Spoolman](https://github.com/Donkie/Spoolman) server, an inventory for 3D-printer filament: vendors, filaments and spools, with the weight left on each spool. Spoolman is written and maintained by Daniel Hultgren ("Donkie") and contributors and is released under the MIT license. UnitySVC Labs lists the official `ghcr.io/donkie/spoolman` image (version 0.27.1, pinned by digest), and the platform runs one isolated instance per enrollment. The author was not asked to take part in this listing.

## Read this first: Spoolman has no login

Spoolman has **no authentication at all**, and UnitySVC adds none. Anyone who can reach the instance address can read your whole inventory and create, change or delete anything in it, through the web interface or the API, without a password or a token. The upstream documentation says the same ([Security wiki page](https://github.com/Donkie/Spoolman/wiki/Security)): Spoolman is designed for a trusted home network, and the thing that protects the data there is the network.

What you can do about it:

- **Keep the instance address private.** Do not post it, put it in a public page or paste it into a shared document. The address is the only thing between your data and anyone else.
- Do not store anything in Spoolman that you would mind someone else reading or changing.
- Nothing in the app can add a login. There is no setting for it, and the enrollment form has no password because Spoolman has nowhere to use one.
- Keep your own copy of anything important (see Backups below).

Spoolman does refuse writes that another website tries to make through your browser, and it refuses WebSocket connections from other websites. That protects you from a malicious page you visit; it does not stop someone who has the address and calls the API directly.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `spoolman/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Spoolman instance at a time.
2. Two settings have working defaults; change them only if you want to. **Nightly database backup** (`SPOOLMAN_AUTOMATIC_BACKUP`, default `TRUE`) and **Log level** (`SPOOLMAN_LOGGING_LEVEL`, default `INFO`). Changing either restarts the instance.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so printer software and scripts that point at the old one need the new one.
4. Open the address. The web interface opens straight away; there is no sign-in.

## First use

In the web interface add a vendor, a filament and a spool. Spoolman can also fill in filament definitions from the community [SpoolmanDB](https://github.com/Donkie/SpoolmanDB) catalog; the instance fetches it from the internet when it starts and about once an hour. The same can be done with the API:

```bash
curl -X POST "https://<instance>/api/v1/filament" -H "Content-Type: application/json" \
     -d '{"name": "PLA White", "material": "PLA", "density": 1.24, "diameter": 1.75, "weight": 1000}'
curl -X POST "https://<instance>/api/v1/spool" -H "Content-Type: application/json" \
     -d '{"filament_id": 1, "remaining_weight": 900}'
curl "https://<instance>/api/v1/spool"
```

Printer software that supports Spoolman (for example Moonraker) takes the instance address as its Spoolman server; the [Spoolman documentation](https://github.com/Donkie/Spoolman/wiki) describes the integrations. Remember that anything that has the address can write to the inventory.

## What is kept, and what is lost

Spoolman's data folder is persistent: the SQLite database (`spoolman.db`), its nightly backups (`backups/`, the five newest), the log and the SpoolmanDB cache. They are stored in `spoolman/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before Spoolman starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. A backup that Spoolman has rotated out can come back after a restart, so the folder can hold more than five backups. This is cosmetic.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Spoolman and this keeps the stored database consistent.
- Do not edit the files in `spoolman/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `spoolman/` folder yourself when you no longer want the data.
- The nightly backup is a copy in the same folder, so it protects against a bad edit, not against losing your home. Everything in it can be read through the API (`GET /api/v1/spool` and the other list endpoints), so keep your own copy of anything you cannot recreate.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Spoolman used about 135 MiB in a local check, at idle and after adding a few spools. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
