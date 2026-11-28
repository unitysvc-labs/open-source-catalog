# Metabase Business Intelligence (open-source edition)

Each enrollment runs a private [Metabase](https://www.metabase.com/) server. Metabase is written and maintained by [Metabase, Inc.](https://github.com/metabase) and contributors; the provider of this service is its author. UnitySVC Labs lists the official open-source edition image `metabase/metabase` (version v0.65.6, pinned by digest), which is released under the AGPL-3.0 license, and the platform runs one isolated instance per enrollment. The paid Metabase editions (the `metabase/metabase-enterprise` image, under a commercial license) and their features are not part of this service.

Metabase's own state (accounts, saved questions, dashboards, and the connection settings of your databases) is kept in the `metabase` folder of your **home**, not in the enrollment. It survives stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

**This service is for evaluation, personal use and small teams.** Metabase stores its state in its embedded H2 database, a single file. Metabase's authors [advise against H2 for production](https://www.metabase.com/docs/latest/installation-and-operation/migrating-from-h2) and recommend PostgreSQL or MySQL instead, which this recipe does not provide. See "What is kept, and what is lost" below.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `metabase/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Metabase instance at a time.
2. The form asks for an **Administrator email (sign-in name)** (default `admin@example.com`; no email is sent to it) and shows a generated **Administrator password**. They create the administrator account the **first time** Metabase runs on your data. If an account already exists, because you enrolled before or restarted, they are ignored and the existing password still applies; change it in Metabase's account settings. Save the password now: the platform keeps it as a secret and does not show it again. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready; Metabase is a Java application and the first start can take a minute or two. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Open the address and sign in with the administrator email and password. There is no setup wizard: the account was created for you before the instance became ready.

## First use

1. Open **Browse > Databases > Sample Database** to try the query builder on the included sample data, or open one of the example questions.
2. To use your own data, go to **Admin > Databases > Add a database**, choose the type (PostgreSQL, MySQL, SQL Server, BigQuery, Snowflake, SQLite and others) and enter the connection details. The instance connects to your database over the internet, so the database must accept connections from outside your network; this service has no private link to it and no fixed outgoing address you could allow by itself. Use a read-only database account.
3. Choose **New > Question** for the visual query builder or **New > SQL query** to write SQL, pick a chart, and save the result. Add saved questions to a dashboard with **New > Dashboard**.
4. Add people under **Admin > People**. Because no email is sent, Metabase shows you a temporary password for each new person; pass it on yourself.

The [Metabase documentation](https://www.metabase.com/docs/latest/) covers all of this in detail.

## Authentication

Metabase checks every request itself: the web interface and the API (`/api/...`) need a signed-in session or an API key created under **Admin > Settings > Authentication > API keys**. Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong. Nothing is public unless an administrator creates a public link or sets up embedding. UnitySVC adds no other gate.

How the administrator is created: a new Metabase has no account, and the first visitor would normally complete a setup wizard and become the administrator. Metabase has no setting that creates the account, so this recipe completes that setup itself, through Metabase's own setup API on the container's local address, with the email and password of your enrollment, as soon as Metabase starts answering. The instance is reported ready, and given its public address, only after that. Passwords need at least 12 characters (this recipe sets Metabase's password rule to length only, because the generated password is not guaranteed to contain a digit).

## No email

This service has no mail server, and Metabase is not configured to send email.

- **"Forgot password" does nothing.** The form accepts the request but no message is sent. An administrator resets another person's password under **Admin > People**; a signed-in user changes their own in **Account settings**. If the only administrator loses the password, there is no way back in from the web interface.
- Invitations, dashboard subscriptions and alerts by email are not sent.
- You can enter your own SMTP server under **Admin > Settings > Email**. Whether outgoing mail from an instance reaches it was not tested.

## The site URL

Metabase records its own address (the **Site URL**, under **Admin > Settings > General**) the first time it is used at its public address, and uses it in public links and embedding code. It is stored with your data. After you remove the enrollment and enroll again, the instance has a new address but still remembers the old one: correct **Site URL** there if you use public links or embedding. Signing in and normal use do not depend on it.

## What is kept, and what is lost

The persistent part is Metabase's application database, the file `metabase.db/metabase.db.mv.db`. It holds accounts, saved questions, dashboards, collections, settings, and the connection details of the databases you added (including their passwords; Metabase stores them unencrypted in this recipe). It is stored in `metabase/` in your home, where you can see it in your files. The platform restores it before Metabase starts, copies it back about every 30 seconds while it changes, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`. Your own data stays in your databases; Metabase only queries it.

- **A single database file, copied while in use.** The copy made while Metabase runs is taken from a file that may be changing. In a local check, eight copies taken during continuous writes all opened and each held a consistent earlier state, but this is not a guarantee, and it is the reason this service is not offered for production use. A normal stop writes a complete copy after Metabase has shut down.
- A crash, or a node failure, can lose the last changes (30 seconds or more) and, in the worst case, leave a copy Metabase cannot open. Keep your own backup: download `metabase/metabase.db/metabase.db.mv.db` from your home while the instance is stopped.
- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- Files over 1 GiB are not stored. If the database file grows past that (long query histories on a busy instance), it is no longer saved.
- Do not edit the file in `metabase/` while the instance is stopped, other than replacing it with your own backup: the next start loads what is there.
- H2's log and temporary files (`*.trace.db`, `*.temp.db`, `*.lock.db`) are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `metabase/` folder yourself when you no longer want the data.
- The sample database, downloaded drivers and caches live outside that folder and are recreated at each start.
- Changing the administrator email or password parameter after the first start has no effect; they are read only when no account exists.

To move to a production installation later, Metabase documents how to [migrate from H2](https://www.metabase.com/docs/latest/installation-and-operation/migrating-from-h2) to PostgreSQL or MySQL with the downloaded file.

## Cost and size

The instance runs on the `small-2x` size (two cores, 4 GiB, 10 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. The size is chosen for start-up time, not memory: Metabase must be ready within about two minutes or the platform restarts it, and in a local check a first start took 22 to 25 seconds on two cores but 40 to 49 seconds on one. It used about 1.3 to 1.4 GiB of memory, idle and after running questions on the sample database; large query results use more. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
