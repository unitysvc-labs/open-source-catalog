# Kutt Private URL Shortener

This unofficial community recipe runs the upstream `kutt/kutt:v3.2.6` image, pinned by digest. Kutt (The Devs Network and contributors) publishes the software under [MIT](https://github.com/thedevs-network/kutt/blob/main/LICENSE). No author endorsement or support commitment is implied.

## Create a short link

1. Enroll in **base**, approve `kutt/` home access and save the administrator password and token signing secret. The initial public hostname is `instance.invalid` because the instance address is assigned after enrollment.
2. Start the instance, copy its hostname from the instance details, set **Public host name** to that hostname (no `https://` or path) and save. This restarts the instance. Do this before sharing any short URL: the placeholder cannot route visitors to your instance.
3. Open the HTTPS address and sign in with the initial administrator email and password. Create a link to `https://example.com`, copy the short URL and verify its redirect in a signed-out browser. Kutt can show visit statistics and generate API credentials for authenticated link creation.
4. Public registration and anonymous shortening are disabled. An administrator can add accounts. Short-link redirects remain public, except where you enable Kutt's link password. UnitySVC adds no additional gate. There is no SMTP server, email verification or email password recovery.

## Restarts, addresses and data

The SQLite database (accounts, links, domains and statistics) persists in `kutt/` in your home. The wrapper only creates an administrator when Kutt says no user exists; existing passwords are changed in Kutt, not by changing enrollment's initial password. Keep the signing secret across enrollments or existing tokens will stop working.

A new enrollment gets a new hostname. Update the Public host name parameter and redistribute links: URLs containing the old instance address cannot follow you to a new one. Custom-domain DNS/certificate setup and a Redis-backed background queue are outside this recipe. Deleted links stay deleted in the database, while unrelated removed files can return on disk under the platform's additive copy rules. Back up the database independently for important links; journals are excluded and a crash can lose recent changes.

## Storage and stopping

Stop the instance from UnitySVC when finished; closing the browser does not stop billing. Only one active enrollment per customer uses this recipe's home folder. Do not run another instance against that folder or edit it while this instance runs.

The platform restores persisted files before startup, copies changed files about every 30 seconds, and makes a final copy on a normal stop. A crash can lose recent changes. Copies add and replace files; they never delete. Deleted files may return on a later start. Empty files, symbolic links and individual files over 1 GiB are not stored. Nothing removes the home folder when you cancel enrollment; remove it yourself when it is no longer needed. Export important data from the application as an independent backup.

## Cost and support

The **base** channel uses **nano**. Pay the current platform compute base rate for the time the instance runs, including idle time. Labs adds no markup and receives no payout. Stop the instance when finished. Consult the [upstream documentation](https://github.com/thedevs-network/kutt#readme) for application behavior; this recipe does not promise author support.
