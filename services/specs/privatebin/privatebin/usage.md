# PrivateBin Encrypted Pastebin

Each enrollment runs a private [PrivateBin](https://privatebin.info/) server. PrivateBin is maintained by the [PrivateBin project](https://github.com/PrivateBin) and contributors, based on ZeroBin by Sébastien Sauvage, and is released under the Zlib license; the provider of this service is its author. UnitySVC Labs lists the official `privatebin/nginx-fpm-alpine` image (version 2.1.1, pinned by digest), and the platform runs one isolated instance per enrollment. The PrivateBin project was not asked to take part, and nothing here implies endorsement or support.

PrivateBin is a pastebin where the server cannot read what is pasted. Your browser encrypts the text with 256-bit AES before sending it, and the key is the part of the link after the `#`, which a browser does not send to the server. The instance stores only the encrypted paste.

Your pastes are kept in the `privatebin` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same pastes.

## Set up

1. Enroll in **base**. It has no settings to fill in. The enrollment asks for access to the `privatebin/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one PrivateBin instance at a time.
2. Wait for the instance to become ready; the first start took about 6 seconds in a local check. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
3. Open the address. You land on the paste editor; there is nothing to sign in to.

## Create a paste and share it

1. Type or paste the text. Choose the format (plain text, source code or Markdown) and when the paste **expires**: 5 minutes, 10 minutes, 1 hour, 1 day, 1 week (the default), 1 month, 1 year or never.
2. Optionally tick **Burn after reading** (the paste is deleted the first time it is opened), tick **Open discussion** (readers can add comments), or set a **password** that the reader must also enter and that you tell them by another route.
3. Press **Create**. PrivateBin shows the link to the paste, a QR code for it and a separate **delete link**. Send the paste link; keep the delete link if you want to remove the paste before it expires.

The whole link is the secret: whoever has it, including the part after the `#`, can read the paste (and needs the password too, if you set one). After a new enrollment the address changes, so replace the host in an old link with the new address; the part from `?` onwards stays the same.

PrivateBin also has a JSON API, used by its command-line and editor clients; the client does the encryption. The [PrivateBin wiki](https://github.com/PrivateBin/PrivateBin/wiki) describes the API and lists clients.

## Authentication: who can use this instance

PrivateBin has no accounts, no sign-in and no administrator, so this service has no password or key to set. **Anyone who knows the instance address can create pastes and add comments where a paste allows them.** Nothing else is open to them: there is no list of pastes, a paste can be read only with its own link, and it can be deleted only with its delete link. UnitySVC adds no other gate, so give the address to the people who should use it, and stop or delete the enrollment when you no longer need it.

## Limits of this instance

PrivateBin is configured by a file inside the image, not by settings the platform can pass in, so the instance runs PrivateBin's default configuration and it cannot be changed:

- **No file attachments.** Text only, up to 10 MiB for each paste.
- **One new paste or comment every 10 seconds, for all visitors together.** PrivateBin limits each visitor address, and behind the platform's HTTPS front end it sees every visitor as the same address. A second paste inside 10 seconds is refused with "Please wait 10 seconds between each post."
- No URL shortener, and the name, theme and default expiry are PrivateBin's defaults.

## What is kept, and what is lost

PrivateBin's data folder is persistent: one file for each encrypted paste and its comments, the server salt (it makes the delete links work) and the rate limiter's state. They are stored in `privatebin/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before PrivateBin starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **A burned, deleted or expired paste can come back.** Files are copied to your home, never deleted from it. When PrivateBin deletes a paste (burn after reading, its delete link, or expiry), the copy in your home stays, and the next time the instance is stopped and started it is restored. A restored burn-after-reading paste can then be opened once more with its link; an expired one is refused and deleted again when someone opens it. A plain restart of the running instance does not bring anything back. If a paste must be gone for good, delete its file from `privatebin/` in your home while the instance is stopped (the file is named after the identifier between `?` and `#` in the link, under two folders named after its first four characters), or do not stop the instance while such pastes are outstanding.
- **The stored files are ciphertext.** Neither the instance nor your home holds the key, which exists only in the link. Each file does show when the paste expires and whether it is burn-after-reading.
- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a paste just created. A normal stop loses nothing.
- Do not edit the files in `privatebin/` while the instance is stopped, other than deleting pastes: the next start restores them as they are.
- Empty files, symbolic links and files over 1 GiB are not stored. PrivateBin's data has none of these.
- Nothing is deleted from your home automatically, including when you cancel the enrollment, so the folder only grows. Delete the `privatebin/` folder yourself when you no longer want the pastes; doing so also invalidates every old paste and delete link.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. PrivateBin used about 75 MiB in a local check, idle and after storing and reading a 7 MiB paste; the encryption happens in the visitor's browser. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
