# Vikunja Task Manager

Each enrollment runs a private [Vikunja](https://vikunja.io/) server. Vikunja is written and maintained by [Kolaente](https://github.com/kolaente) and contributors and is released under the AGPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `vikunja/vikunja` image (version 2.8.0, pinned by digest), and the platform runs one isolated instance per enrollment. The image serves the web interface and the API from the same address.

Your accounts, projects, tasks and attachments are kept in the `vikunja` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `vikunja/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Vikunja instance at a time.
2. The form shows **Allow registration** (default `true`) and a generated **Signing secret**. Keep the defaults. The signing secret is application configuration, not a password you type: Vikunja signs its sign-in tokens with it. They are not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so apps and scripts that point at the old one need the new one.
4. Open the address and choose **Register** to create your account with a user name, an email address and a password. Then sign in.

## Registration, and who can create an account

Vikunja has no first-run setup and no built-in administrator: any person who can reach the address can create an account, and each account sees only its own projects. The instance is therefore open to registration until you close it. The address is a long random code, but anyone who learns it can register and use your instance's compute.

- Register your own account straight away.
- Then change **Allow registration** to `false`. Vikunja reads it at every start, so it takes effect when the instance restarts. With registration closed, the register page is gone and the API refuses new accounts.
- Do not close it before you have an account. A closed Vikunja has no way to create a user from the web interface (Vikunja's own `user create` command needs a shell in the container, which the platform does not give you), and this recipe configures no external sign-in (OpenID Connect or LDAP), so you would be locked out.

## Use it

Create a project, add tasks with due dates, labels, assignees and attachments, and switch between the list, table, Gantt and Kanban views. For scripts, create an **API token** in your settings and call the REST API; the [Vikunja documentation](https://vikunja.io/docs/) describes the API and the mobile and CalDAV clients that can point at your instance address.

```bash
curl "https://<instance>/api/v1/projects" -H "Authorization: Bearer <API token>"
```

## Authentication

Vikunja checks every request itself. Anyone who knows the address can reach the sign-in page, so use a strong password and keep API tokens private. UnitySVC adds no other gate. Outgoing email is not configured, so Vikunja sends no reminders or password-reset emails; a forgotten password cannot be reset by email.

## What is kept, and what is lost

Two folders are persistent, both under `vikunja/` in your home: `db/` holds the SQLite database (accounts, projects, tasks) and `files/` holds the task attachments and uploaded images. The platform restores them before Vikunja starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folders belong to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a task you just added. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file Vikunja removes, such as a deleted attachment, can come back after a restart. This is cosmetic.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Vikunja and this keeps the stored database consistent.
- Do not edit the files in `vikunja/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored. Vikunja's own upload limit is 20 MB per file by default.
- Changing the **Signing secret** signs every user out; the data is not affected.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `vikunja/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Vikunja used about 100 MiB in a local check, idle and after a few hundred tasks. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
