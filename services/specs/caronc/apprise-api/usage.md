# Apprise Notification API

This unofficial community recipe runs the upstream `caronc/apprise:2.2.0` image, pinned by digest. Apprise (Chris Caron) publishes the software under [MIT](https://github.com/caronc/apprise-api/blob/master/LICENSE). No author endorsement or support commitment is implied.

## First use

1. Enroll in **base**, approve `apprise-api/` home access and save the administrator name and generated password. The application requires HTTP Basic authentication; UnitySVC adds no extra gate.
2. Open `https://<instance>/` and sign in. A request without credentials receives 401. Check readiness with `curl -u '<name>:<password>' https://<instance>/status`.
3. Add a Config ID and a destination URL in the browser, or send a stateless notification:

   ```bash
   curl -u '<name>:<password>' https://<instance>/notify/      -H 'Content-Type: application/json'      -d '{"urls":"<your-apprise-destination-url>","title":"Test","body":"Hello from Apprise"}'
   ```

The destination URL may itself contain a provider token or password: use your own account and treat the URL as a secret. The service does not provide email delivery or other downstream accounts. Do not put real destination secrets in shared examples or public Config IDs. The upstream project documents supported URL formats and APIs.

## Access and storage

`APPRISE_AUTH_REQUIRED=yes` stays enabled. The administrator can manage every Config ID. Upstream supports credentials limited to one configuration and intentionally public tagged notifications; those are application settings you control. Changing the enrollment password changes administrator authentication at the next start. Save configurations before stopping. `/config` is persisted to `apprise-api/`, including destination secrets, access controls and browser-login state. Simple stateful mode means IDs remain stable across enrollments without depending on an enrollment-specific filename key.

Deleted configuration and authentication files can return after a stop/start because the home copy never deletes; remove their corresponding files from the home folder while the instance is stopped if permanent removal is required. Notification delivery is an outbound operation, not a durable message queue or delivery guarantee. Retrying a request can send duplicates. Keep attachments small on this nano-sized instance.

## Storage and stopping

Stop the instance from UnitySVC when finished; closing the browser does not stop billing. Only one active enrollment per customer uses this recipe's home folder. Do not run another instance against that folder or edit it while this instance runs.

The platform restores persisted files before startup, copies changed files about every 30 seconds, and makes a final copy on a normal stop. A crash can lose recent changes. Copies add and replace files; they never delete. Deleted files may return on a later start. Empty files, symbolic links and individual files over 1 GiB are not stored. Nothing removes the home folder when you cancel enrollment; remove it yourself when it is no longer needed. Export important data from the application as an independent backup.

## Cost and support

The **base** channel uses **nano**. Pay the current platform compute base rate for the time the instance runs, including idle time. Labs adds no markup and receives no payout. Stop the instance when finished. Consult the [upstream documentation](https://github.com/caronc/apprise-api#readme) for application behavior; this recipe does not promise author support.
