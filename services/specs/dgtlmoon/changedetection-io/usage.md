# changedetection.io Web Page Change Monitor

Each enrollment runs a private [changedetection.io](https://changedetection.io/) instance. changedetection.io is written and maintained by [Leigh Morresi (dgtlmoon)](https://github.com/dgtlmoon) and contributors and is released under the Apache License 2.0; the provider of this service is its author. UnitySVC Labs lists the official `ghcr.io/dgtlmoon/changedetection.io` image (version 0.70.4, pinned by digest), and the platform runs one isolated instance per enrollment.

Your settings, watches and page snapshots are kept in the `changedetection` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set a password first

**A new changedetection.io instance has no password.** Anyone who knows the instance address can open it, see every watch and change it, including the notification settings. The address is not secret, so do this before anything else:

1. Enroll in **base** and approve the access to the `changedetection/` folder of your home (`service:home`, read and write). Without it the instance does not start. You can run one instance at a time.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
3. Open the address, go to **Settings**, and enter a password under the password setting. Save. From then on the instance asks for it before showing anything.

The enrollment form has no password setting: changedetection.io can read a pre-hashed password from an environment variable, but it needs a salted hash that the platform cannot generate, so this recipe does not use it. UnitySVC adds no other gate in front of the application.

## Watch a page

1. On the home page, paste a URL into the box and press **Watch**. The new watch is checked on the default schedule, and you can set an interval in its edit page or in Settings.
2. Open the watch's edit page to restrict it to part of the page (CSS, XPath or JSON filter), to ignore text, or to add a notification URL (Apprise syntax, see the [upstream notification documentation](https://github.com/dgtlmoon/changedetection.io/wiki/Notification-configuration-notes)).
3. When the content changes, the watch is marked in the list and its **History** shows the difference between snapshots.

A new instance starts with a few sample watches (the changedetection.io change log and a news site). Delete them if you do not want them fetched.

## No headless browser

changedetection.io fetches pages with plain HTTP requests. It can also drive a real browser (Playwright or Selenium) to read pages that build their content with JavaScript, but that needs a separate browser container, and **this recipe does not include one**. Pages that need JavaScript to show their content, and the browser-steps feature, do not work here.

## What is kept, and what is lost

changedetection.io keeps JSON settings, one folder per watch and compressed page snapshots in its data folder. They are stored in `changedetection/` in your home. The platform restores them before the application starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. A snapshot the application removes, for example when old history is trimmed, can come back after a restart.
- Do not edit the files in `changedetection/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Snapshots grow with every change of every watch. The temporary disk of the `nano` size is 1 GiB, and your home may have its own limit; watch a large number of big pages with care.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `changedetection/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. changedetection.io used about 125 MiB in a local check with a few watches, and about 135 MiB after some requests. Many watches checked often use more memory and CPU. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
