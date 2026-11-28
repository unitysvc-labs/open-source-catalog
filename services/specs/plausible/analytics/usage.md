# Plausible Community Web Analytics

This unofficial community recipe runs the upstream `ghcr.io/plausible/community-edition:v3.2.2` image, pinned by digest. Plausible Analytics and contributors publishes the software under [AGPL-3.0](https://github.com/plausible/analytics/blob/master/LICENSE.md). No author endorsement or support commitment is implied.

## Create your analytics account

1. Enroll in **base**, approve `plausible/` home access and keep the database credentials and application signing secret. The stack uses **small** for Plausible, **nano** for PostgreSQL and **small-2x** for ClickHouse.
2. Set **Public address** to the assigned HTTPS instance URL and save. Open it immediately and create the initial owner account before sharing the URL: the first visitor can claim setup. No platform authentication gate is added.
3. Add your website and copy Plausible's tracking snippet to that site's HTML. Visit a tracked page and confirm that the dashboard records the view. Counts may take a short time to appear. Only collect analytics on websites you administer or have authorization to instrument.
4. Registration is invite-only after the first account. Email verification is disabled and no SMTP service is supplied; emailed invitations, reports and password recovery are unavailable. Keep the owner password independently. Paid cloud features and external Google services are outside this recipe.

## Two database backups

PostgreSQL holds accounts and site configuration; ClickHouse holds event data. Their live directories are scratch. PostgreSQL writes a compressed dump and ClickHouse writes one native ZIP backup under the persisted home folders, every five minutes and on a normal stop. Fresh directories restore those exports before the application is allowed to migrate or serve requests. The application waits for ClickHouse's bootstrap-ready table, so it cannot race an event restore. Keep both exports together.

A crash can lose up to five minutes of events and account changes. Each export must be smaller than 1 GiB, making this recipe suitable for small sites rather than large analytics deployments. The native ClickHouse backup preserves its own file layout inside one archive; the platform never copies the live event directory. ClickHouse is limited to IPv4 and modest background pools for the sandbox. The UI, tracker and event endpoint are public; dashboards require Plausible authentication unless you deliberately share them.

The app data folder contains local application state under `plausible/app/`. Deleted files outside the two archive files may return because the home copy never deletes. New enrollments have new addresses: update Public address and tracking snippets. Keep independent exports for important data.

## Storage and stopping

Stop the instance from UnitySVC when finished; closing the browser does not stop billing. Only one active enrollment per customer uses this recipe's home folder. Do not run another instance against that folder or edit it while this instance runs.

The platform restores persisted files before startup, copies changed files about every 30 seconds, and makes a final copy on a normal stop. A crash can lose recent changes. Copies add and replace files; they never delete. Deleted files may return on a later start. Empty files, symbolic links and individual files over 1 GiB are not stored. Nothing removes the home folder when you cancel enrollment; remove it yourself when it is no longer needed. Export important data from the application as an independent backup.

## Cost and support

The **base** channel runs **small** for app, **nano** for db, **small-2x** for events. All containers incur runtime charges. Pay the current platform compute base rate for the time the instance runs, including idle time. Labs adds no markup and receives no payout. Stop the instance when finished. Consult the [upstream documentation](https://github.com/plausible/analytics#readme) for application behavior; this recipe does not promise author support.
