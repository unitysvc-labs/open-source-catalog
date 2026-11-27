# Homebox Home Inventory

Each enrollment runs a private [Homebox](https://homebox.software) server. Homebox is maintained by [SysAdmins Media](https://github.com/sysadminsmedia) and contributors, as the continuation of the original Homebox project, and is released under the AGPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `ghcr.io/sysadminsmedia/homebox` image (version 0.27.1, the upstream `rootless` variant, pinned by digest), and the platform runs one isolated instance per enrollment. The author was not asked to take part in this listing, and nothing here means the author endorses it or supports it.

Your inventory (the database and the attached files) is kept in the `homebox` folder of your **home**, not in the enrollment. It survives stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `homebox/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Homebox instance at a time.
2. The form has two settings. **API key pepper** is generated; keep it or enter your own (at least 32 characters), and save it now: the platform keeps it as a secret and does not show it again. It is not a sign-in password and not your UnitySVC API key; Homebox mixes it into the stored hashes of the API keys you create. **Allow registration** starts as `true`.
3. Wait for the instance to become ready; it starts in a few seconds. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. **Open the address and register your account.** Homebox has no administrator account that an enrollment could set: you choose **Register**, and enter a name, an email and a password. No email is sent and the address is not verified; it is only your sign-in name. If your data is already in your home from an earlier enrollment, skip this step and sign in with the account you registered then.
5. **Close registration.** Edit the enrollment, set **Allow registration** to `false`, and save. The instance restarts and keeps your data. Until you do this, anyone who finds the instance address can register an account too (see **Authentication** below for what that exposes).
6. Sign in, create a location (for example `Garage`), and add your first item to it.

## Use it

- **Items and locations** in the web interface: nested locations, tags, quantities, serial and model numbers, purchase and warranty details, maintenance logs and custom fields.
- **Attachments**: add photos, receipts and manuals to an item. One upload can be up to 10 MB (the Homebox default).
- **Labels, import and export**: print QR-code labels for items and locations, and import or export the inventory as CSV, from the **Tools** page.
- **REST API.** Create an API key in your profile, then send it as a bearer token. The interactive reference is at `https://<instance>/swagger/index.html`.

  ```bash
  curl -H "Authorization: Bearer <api key>" https://<instance>/api/v1/entities
  ```

- **More people.** With registration closed, the owner of a collection can still create an invitation link in the collection settings, and a person who opens it registers into that collection. This follows the upstream code and documentation; it was not checked for this recipe.

The [Homebox documentation](https://homebox.software/en/) describes the rest.

## Authentication

Homebox checks every request itself: the web interface needs your sign-in, and the API needs a session or an API key; without one it answers 401. UnitySVC adds no other gate, so anyone who knows the instance address can reach the sign-in page. Use a strong password.

Be clear about what is open before you close registration:

- While **Allow registration** is `true`, anyone who reaches the address can register an account. Each registration creates its **own, separate collection**: in a local check a second account saw an empty inventory and got "not found" for the first account's item. A stranger therefore cannot read your inventory by registering, but can use your instance and fill the storage in your home.
- There is no "first account is the administrator" step to race for, and no default account or password.
- With **Allow registration** set to `false`, a new registration is refused ("user registration disabled") and existing accounts still sign in. Accounts registered before you closed it remain; Homebox has no page to list all accounts of an instance.
- This recipe configures no mail server, so Homebox cannot email a password reset. Keep your password safe.

## The API key pepper

Homebox does not start without a pepper of at least 32 characters. It is used only for API keys: if the value changes, every API key created before is refused (checked locally: the same key answered 200 before and 401 after a change), while password sign-in and the inventory are unaffected. Because your data outlasts the enrollment and a new enrollment generates a new pepper, enter your saved value when you enroll again, or create new API keys afterwards.

## What is kept, and what is lost

Homebox's data folder is persistent: the SQLite database (`homebox.db`) and the attachments. They are stored in `homebox/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before Homebox starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- The instance keeps the database in one self-contained file (SQLite's rollback-journal mode instead of the image's default write-ahead log), so the copy in your home is complete. SQLite's temporary files (`*-wal`, `*-shm`, `*-journal`) are not stored.
- Files are copied, never deleted from your home. An attachment you delete in Homebox can remain as a file in the folder. This is cosmetic: the item no longer refers to it.
- Do not edit the files in `homebox/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored. Homebox's own data has none of these; uploads are limited to 10 MB each.
- The two enrollment settings are read at every start, so changing one takes effect after the restart. Your account and its password live in the database, not in the settings.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `homebox/` folder yourself when you no longer want the data. Export your inventory first if you want a copy.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check Homebox used about 20 MiB when just started and 90 to 215 MiB after sign-ins and uploads (hashing a password takes memory for a moment). Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
