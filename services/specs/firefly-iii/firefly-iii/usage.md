# Firefly III Personal Finance Manager

Each enrollment runs a private [Firefly III](https://firefly-iii.org/) server. Firefly III is written and maintained by [James Cole](https://github.com/JC5) and contributors and is released under the GNU Affero General Public License v3.0; the provider of this service is its author. UnitySVC Labs lists the official `fireflyiii/core` image (version 6.7.12, pinned by digest), and the platform runs one isolated instance per enrollment.

Your accounts, transactions, settings and attached files are kept in the `firefly-iii` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

**Read "The first account" before you start the instance for the first time, and "No email" before you change your email address.**

## Set up

1. Enroll in **base**. The enrollment asks for access to the `firefly-iii/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Firefly III instance at a time.
2. The form shows an **Application key (APP_KEY)** and a **Time zone**.
   - **APP_KEY** is generated for you: exactly 32 characters (letters, digits, `-` and `_`). It is not your sign-in password. It signs your sessions and encrypts the keys that sign API tokens, which Firefly III stores in its database. **Save it.** Do it now, because the platform keeps it as a secret and does not show it again, and your data outlives the enrollment: when you enroll again the form generates a **new** key, and you should replace it with your saved one. In a local check with a different key, the accounts, the transactions and the sign-in still worked, but every API token was refused, and going back to the first key did not bring the tokens back: they had to be created again. Two-factor sign-in with a changed key was not tested.
   - **Time zone** (default `UTC`) is an IANA name such as `Europe/Amsterdam`. Firefly III uses it for the dates and times it records and shows. Changing it later restarts the instance and keeps your data.
3. Wait for the instance to become ready; a start takes about ten seconds in a local check. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.** Firefly III needs no setting for it.
4. Open the address at once and register, as described next.

## The first account

Firefly III has no setting for a first user or password, so this service has no password parameter. On an empty database the address opens the registration page, and **the first account registered becomes the owner** of the instance.

**Until that account exists, anyone who reaches the instance address can register it.** The address is not listed anywhere, but it is not a secret either. Do this as soon as the instance is ready:

1. Open the address. It leads to **Register**. Enter an email address and a password of at least 16 characters, twice. The email address is your login name; nothing is sent to it. The optional check box compares the password with a public list of leaked passwords (upstream explains the method on the page).
2. Firefly III signs you in and asks for the name and balance of your main bank account and your language. Fill them in to reach the dashboard.

After the first account, registration is closed: the registration page answers "Registration is currently not available". The owner can open it again under **System settings > Configuration** ("Single user mode"); leave it closed unless you want other people to use your instance.

If the address shows the sign-in page instead of the registration page on a first start with an empty `firefly-iii/` folder, somebody else got there first: stop the instance, delete the `firefly-iii/` folder in your home and start again.

When the data already exists, because you enrolled before or restarted, nothing is created: sign in with your own email address and password. Change the password under **Profile > Change your password**; this needs your current password and no email.

## Use it

- **Accounts and transactions.** Create asset accounts for your bank accounts, then record withdrawals, deposits and transfers. Firefly III creates the expense and revenue accounts as you name them.
- **Organize.** Give transactions budgets, categories and tags, set up bills, subscriptions and piggy banks, and write rules that file new transactions for you. Reports and charts show income, spending and net worth over a period.
- **Attach files** such as receipts to transactions and other records.
- **REST API.** Create a personal access token under **Remote access and tokens** in the user menu, then:

  ```bash
  curl -H "Authorization: Bearer <token>" -H "Accept: application/json" https://<instance>/api/v1/about
  curl -X POST -H "Authorization: Bearer <token>" -H "Accept: application/json" -H "Content-Type: application/json" \
       -d '{"transactions": [{"type": "withdrawal", "date": "2026-11-27", "amount": "12.50", "description": "Groceries", "source_id": "1", "destination_name": "Supermarket"}]}' \
       https://<instance>/api/v1/transactions
  ```

  Tools that work with Firefly III through this API, such as upstream's separate data importer, are not part of this service; they can use your instance's address and a token while the instance runs.
- **Recurring transactions, automatic budgets and bill reminders** depend on a daily job that this recipe does not run by itself. Call it from a scheduler of your own, once a day while the instance runs, with the **Command line token** shown under **Profile**:

  ```bash
  curl https://<instance>/api/v1/cron/<command-line-token>
  ```

  Anyone who has this address can run the job, so treat the token as a secret. Without the call, recurring transactions are not created.

The [Firefly III documentation](https://docs.firefly-iii.org) describes these features and the API.

## Authentication

Firefly III checks every request itself: the web interface needs your sign-in, and the API needs a token (`Authorization: Bearer ...`); a request without one is refused with status 401. Anyone who knows the instance address can reach the sign-in page, so use a long, unique password, and consider two-factor sign-in in your profile. Repeated wrong sign-ins are slowed down by Firefly III. UnitySVC adds no other gate.

## No email

This service configures no mail server, so Firefly III sends no mail. In a local check:

- **Do not change your email address in the profile.** Firefly III locks the account until you open a confirmation link that it sends by email, and that email is never delivered. The sign-in is refused with the old and the new address, and this recipe has no way to unlock it. If it happens, the only way back is to stop the instance, delete the `firefly-iii/` folder in your home and start again, which removes your data. Export your data first if you ever need a different address (see below).
- **"Forgot password" does not work**; the page answers with an error. Keep your password safe, and change it only from the profile while you are signed in.
- Registering, signing in, changing the password and creating API tokens need no email and work.
- Notifications by email, and invitations of other users, are not delivered.

To keep a copy of your transactions outside the instance, use **Export data** in Firefly III, which downloads them as a CSV file.

## What is kept, and what is lost

Two folders of Firefly III are persistent: the SQLite database (`database/database.sqlite`, which holds the users, accounts, transactions, settings and API tokens) and the attached files (`upload/`). They are stored in `firefly-iii/database/` and `firefly-iii/upload/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before Firefly III starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **The copy in your home is not encrypted.** The database and the attached files are ordinary files there, and they hold your financial records. Anyone who can read your home folder can read them.
- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. The file of an attachment you delete in Firefly III stays in `firefly-iii/upload/`; Firefly III no longer shows it. Delete it from your home yourself if it should be gone.
- SQLite's temporary files (`*-journal`, `*-wal`, `*-shm`) are not stored. This keeps the stored database consistent.
- Sessions, caches and logs are temporary: after the instance is stopped and started again you sign in again.
- Do not edit the files in `firefly-iii/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored. Firefly III does not need any of them: the image accepts uploads of up to 100 MB.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `firefly-iii/` folder yourself when you no longer want the data.
- The application key is not stored in your home; it lives only in the enrollment parameters.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check under a 512 MiB limit Firefly III used about 65 to 85 MiB after starting and at most 180 MiB while serving pages and API calls from eight clients at once. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
