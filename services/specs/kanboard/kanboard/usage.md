# Kanboard Kanban Project Management

Each enrollment runs a private [Kanboard](https://kanboard.org/) server. Kanboard is written by [Frédéric Guillot](https://github.com/fguillot) and contributors and is released under the MIT license; the provider of this service is its author. Upstream describes Kanboard as being in maintenance mode: it receives fixes and small improvements, not major new features. UnitySVC Labs lists the official `kanboard/kanboard` image (version 1.2.58, pinned by digest), and the platform runs one isolated instance per enrollment.

Your projects are kept in the `kanboard` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `kanboard/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Kanboard instance at a time.
2. The form shows a generated **Administrator password**. It becomes the password of Kanboard's built-in administrator, `admin`, the **first time** Kanboard runs on your data. If the database already exists, because you enrolled before or restarted, the parameter is ignored and the existing password still applies; change it in Kanboard under your avatar > **My profile** > **Change password**. Save the password now: the platform keeps it as a secret and does not show it again. It is an application credential, not your UnitySVC API key.
3. Wait for the instance to become ready; a start takes a few seconds. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.** Kanboard needs no setting for it.
4. Open the address and sign in as `admin` with the administrator password.

## Use it

1. Choose **New project** (or **New personal project**), give it a name, and open its board.
2. Add a task with the **+** at the top of a column, then drag the card from column to column as the work moves on. Open a task to add a description, subtasks, comments, a due date or attached files (up to 32 MB each).
3. In the project's settings, change the columns and their task limits, add swimlanes and categories, and set up automatic actions.
4. To work with other people, create their accounts under **Users management** and add them to a project with a role. Kanboard has no self-registration, so only accounts you create can sign in.

Kanboard also has a JSON-RPC API at `https://<instance>/jsonrpc.php`. A user signs in to it with HTTP Basic authentication, using the user name and password or a personal access token created in the user's profile:

```bash
curl -u "admin:<password>" \
     -d '{"jsonrpc": "2.0", "method": "getMyProjects", "id": 1}' \
     https://<instance>/jsonrpc.php
```

The application-wide API token (user name `jsonrpc`) is shown under **Settings > API**; Kanboard generates it for each instance. The [Kanboard documentation](https://docs.kanboard.org) describes the API, the search language and the other features.

## Authentication

Kanboard checks every request itself: the web interface needs your sign-in and the API needs a user's credentials or an API token. Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong; after three failed attempts Kanboard asks for a captcha and after six it locks the account for 15 minutes. A project or task can be shared by a public link, but only when you turn that on for it. UnitySVC adds no other gate.

A new Kanboard creates the `admin` account with a published default password and has no environment setting to change it. This recipe replaces that password with your **Administrator password** before the application first starts, using Kanboard's own `user:reset-password` command, and the instance does not start if that fails. The default password is therefore never usable on your instance.

## What is kept, and what is lost

Kanboard's data folder is persistent: the SQLite database (`db.sqlite`, which holds the projects, tasks, users, settings and sessions) and the files attached to tasks (`files/`). They are stored in `kanboard/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before Kanboard starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. The file of an attachment you remove in Kanboard can stay in `kanboard/files/`; Kanboard no longer shows it.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Kanboard and this keeps the stored database consistent.
- Do not edit the files in `kanboard/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored. Kanboard does not need any of them: an attachment is at most 32 MB.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `kanboard/` folder yourself when you no longer want the data.
- **Plugins are not kept.** Kanboard's plugin installer is off, as it is by default upstream, and the plugin folder is not persistent.
- **Email is not set up.** Notifications by email need a mail server, which this recipe does not configure. Webhooks and the other notification types work.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check Kanboard used about 25 MiB idle and under 30 MiB while serving pages and API calls. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
