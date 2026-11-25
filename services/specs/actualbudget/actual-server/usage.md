# Actual Budget Server

Each enrollment runs a private [Actual Budget](https://actualbudget.org/) server. Actual is written and maintained by James Long and the [Actual Budget project](https://github.com/actualbudget/actual) and its contributors and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `actualbudget/actual-server` image (version 26.11.0, pinned by digest), and the platform runs one isolated instance per enrollment. The server also serves the Actual web app, so the instance address is all you need.

Your budgets and the server password are kept in the `actual` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. It has no settings to fill in. The enrollment asks for access to the `actual/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Actual instance at a time.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so browsers and devices that point at the old one need the new one.
3. **Open the address and set the server password immediately.** On a new instance Actual shows "Welcome to Actual" and asks for a password; the first visitor chooses it, and nothing can preset it. Anyone who reaches the address before you could set the password and so own the server. If the page asks you to sign in when you expected to set a password, someone else got there first: stop and remove the instance, delete the `actual/` folder of your home, and enroll again.
4. Sign in, then choose **Start budgeting** (a new budget), **Import my budget** (from YNAB, another Actual file and others), or **Try the demo**. The web app already points at this server; to use another Actual client, enter the instance address as the server URL.

## What protects your data, and what does not

This server holds your finances, so be clear about it.

- **The server password** is the only gate. Every sync request needs a session from it, and the web app needs it to sign in. Choose a long, unique password. Anyone who learns it can read and change your budgets. Sign-in attempts are rate-limited, but anyone on the internet who knows the address can reach the sign-in page. UnitySVC adds no other gate.
- **End-to-end encryption is optional and is set in the app**, not by the server: in the app's settings (the encryption option of a synced budget; not tested here) you can set a separate encryption password. The budget file is then encrypted on your device before it is uploaded, and the server holds only ciphertext. Without it, the server's stored copy of your budget is not encrypted. Keep that password: Actual cannot recover an encrypted budget without it.
- The data is stored unencrypted at rest in your home, and the instance runs on shared platform infrastructure. Do not rely on the platform to keep it secret from the operator; use the app's end-to-end encryption if that matters to you.
- **HTTPS** is provided by the platform. The Actual web app needs a secure context (HTTPS, or localhost) for some features, so always use the `https://` address.
- Actual supports one server password, or OpenID sign-in for several users; this recipe uses the password only. Its security policy says the server is meant to be run by its owner for people they trust.

## Not included

Automatic bank synchronisation (GoCardless, SimpleFIN, Pluggy.ai, Akahu and Enable Banking) is not set up. It needs your own credentials from those services, entered in the app's settings. The recipe does not configure it or test it. You can import bank files (QIF, OFX, CSV) in the app instead.

## What is kept, and what is lost

The data folder is persistent: `server-files/account.sqlite` (the password hash and sessions) and `user-files/` (each budget's uploaded file and its sync database). They are stored in `actual/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before Actual starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing. Actual is local-first, so your browser also keeps a copy of the budget and resyncs.
- Files are copied, never deleted from your home. A file Actual removes, such as a deleted budget's file, can come back after a restart.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt and this keeps the stored databases consistent.
- Do not edit the files in `actual/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `actual/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Actual used about 100 MiB at idle and after creating a budget in a local check. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
