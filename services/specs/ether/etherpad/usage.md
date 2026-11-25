# Etherpad Collaborative Editor

Each enrollment runs a private [Etherpad](https://etherpad.org/) server. Etherpad is written and maintained by the Etherpad Foundation and contributors ([source](https://github.com/ether/etherpad)) and is released under the Apache License 2.0; the provider of this service is its author. UnitySVC Labs lists the official `etherpad/etherpad` image (version 3.3.22, pinned by digest), and the platform runs one isolated instance per enrollment.

Your pads are kept in the `etherpad` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `etherpad/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Etherpad instance at a time.
2. The form shows a generated **Administrator password** (the password of the Etherpad user `admin`), two generated **sign-in secrets** that Etherpad uses internally and you never type, a **Require sign-in to open pads** choice (default `false`) and a generated **User password** (used only when sign-in is required). Save the passwords; they are also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so links you shared need the new one.

## First use

1. Open `https://<instance>/` and type a pad name, or open `https://<instance>/p/<any-name>` directly. A pad is created the first time its address is opened.
2. Send the pad's address to the people who should edit it. Everyone who opens it edits the same text at once.
3. The admin pages (settings and plugin list) are at `https://<instance>/admin-auth/`. Sign in with the user name `admin` and the administrator password.
4. You can export a pad's text from its address, for example `https://<instance>/p/<name>/export/txt`.

## Authentication

By default **anyone who knows the instance address can create, open and edit any pad**, and anyone who guesses a pad name can read it. Etherpad has no pad passwords unless you add a plugin. Treat pad names as secrets or restrict access.

To require a sign-in for every pad, enroll with **Require sign-in to open pads** set to `true`. Etherpad then asks everyone for a user name and password: `user` with the user password, or `admin` with the administrator password. All people who edit share that one user password. This is a single shared account, not a per-person login. The admin pages always need the `admin` password, whichever setting you choose. UnitySVC adds no other gate.

The passwords and the setting are read when Etherpad starts, so a change you make to them takes effect the next time the instance starts.

## What is kept, and what is lost

Etherpad keeps its pads in a database file, `dirty.db`, in a folder that the platform stores in `etherpad/` in your home, where you can see it in your files while the instance is stopped. This is Etherpad's default `dirty` database, a plain file that Etherpad appends to; it is not SQLite and Etherpad itself warns that it is not recommended for production. The platform restores the folder before Etherpad starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, and because the database is appended to, a copy taken mid-write may lose the last few edits. A normal stop loses nothing.
- Files are copied, never deleted from your home.
- Do not edit the files in `etherpad/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `etherpad/` folder yourself when you no longer want the data.

Do not rely on plugins. Etherpad installs plugins into its program folder, which is not part of the kept data, so a plugin you install from the admin pages is expected to be gone when the instance is replaced. This was not tested.

## Cost and size

The instance runs on the `small` size (one core, 2 GiB, plus temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check Etherpad used about 330 to 360 MiB at idle and up to about 430 MiB after a few pads were opened, which is too close to the 512 MiB of `nano`, so this channel uses `small`. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
