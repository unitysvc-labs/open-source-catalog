# Apache Answer Q&A Platform

Each enrollment runs a private [Apache Answer](https://answer.apache.org/) site. Answer is written and maintained by the Apache Software Foundation project community and released under the Apache-2.0 license; the provider of this service is its author. This recipe is unofficial: the Apache Software Foundation was not asked to take part and does not endorse or support it. UnitySVC Labs lists the official `apache/answer` image (version 2.0.3, pinned by digest), and the platform runs one isolated instance per enrollment.

Your database, settings and uploads are kept in the `answer` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `answer/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Answer instance at a time.
2. The form shows the site name, site address, contact email, an **Administrator name**, an **Administrator email** and a generated **Administrator password**. They install the site and create the administrator the **first time** Answer runs on your data. If the data already exists, because you enrolled before or restarted, they are ignored and the existing site, administrator and password still apply; change them in Answer's own settings. Save the values; they are also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so links that point at the old one need the new one.
4. Open the address and sign in with the administrator **email** and password.
5. The enrollment cannot know its own address in advance, so **Site address** defaults to the placeholder `https://instance.invalid`. Open the admin area, go to **General** and set **Site URL** to the instance address. Answer uses it for links it writes into emails and pages. In a local check the site served pages and the API normally with the placeholder.

## Use it

Ask a question from the web interface, answer it, vote, comment and tag. The administrator can moderate content, manage users, change branding and review settings in the admin area. Answer also has a REST API under `/answer/api/v1/`; for example, `POST /answer/api/v1/user/login/email` with `{"e_mail": "...", "pass": "..."}` returns an access token that goes in the `Authorization` header.

## Authentication

Answer checks every request itself. The administrator account created at the first start is the one you configured; there is no web installer to claim, because the instance installs itself. **Registration is open by default**: new visitors can sign up unless you turn it off in the admin area (**Login** settings), and the instance has no mail server configured, so features that send email (verification, notifications, password reset) need an SMTP server set up in the admin area. UnitySVC adds no other gate. Keep the administrator password strong and private.

## What is kept, and what is lost

The data folder holds the SQLite database (questions, answers, users, settings), `conf/config.yaml`, uploaded files, a cache file and the language files Answer copies in at its first start (about 3 MB in a fresh install). All of it is stored in `answer/` in your home, where you can see it in your files while the instance is stopped. The platform restores it before Answer starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a question just posted. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file Answer removes, such as a purged upload, can come back after a restart. This is cosmetic.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Answer and this keeps the stored database consistent.
- Do not edit the files in `answer/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `answer/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Answer used about 180 MiB in a local check, idle and after a few requests. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
