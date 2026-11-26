# ntfy Push Notifications

Each enrollment runs its own private [ntfy](https://ntfy.sh) server. ntfy is written and maintained by [Philipp C. Heckel](https://github.com/binwiederhier) and is dual-licensed Apache-2.0 and GPLv2; the provider of this service is its author. UnitySVC Labs lists the official `binwiederhier/ntfy` image, and the platform runs one isolated instance per enrollment.

1. Enroll in **base**.
2. The enrollment form shows a generated **Access token**; keep it or replace it with your own (the form `tk_` followed by 29 letters, digits, `-` or `_`), then save it somewhere now: the platform keeps it as a secret and does not show it again. It is given to ntfy at start-up. It is an application credential, not your UnitySVC API key. Changing it later restarts the instance with the new token.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it.
4. Publish with the token as a bearer credential:

   ```bash
   curl -H "Authorization: Bearer tk_..." \
        -H "Title: Hello" -H "Priority: high" -H "Tags: wave" \
        -d "Backup finished" https://<instance>/<topic>
   ```

   Any topic name works; pick one that is hard to guess if you share the token widely.
5. Subscribe from the ntfy app (iOS, Android, desktop, web) by adding your instance URL as the server and the token as the credential, or stream with `curl -H "Authorization: Bearer tk_..." https://<instance>/<topic>/json`.

All ntfy publishing features work: priorities, tags, click actions, scheduled delivery, and attachments, with the limits below. The [ntfy documentation](https://docs.ntfy.sh/) describes them.

## Server settings

Every ntfy server setting that has a default is an enrollment parameter, named after its environment variable (`NTFY_CACHE_DURATION`, `NTFY_MESSAGE_SIZE_LIMIT`, `NTFY_VISITOR_REQUEST_LIMIT_BURST`, and so on), with ntfy's own default, so an enrollment that changes nothing runs the stock configuration. The [ntfy configuration reference](https://docs.ntfy.sh/config/) describes each one. Changing a parameter restarts the instance, and a value ntfy rejects stops it from starting, so change one setting at a time.

What you cannot change is what the service owns: the listeners and TLS (the platform serves HTTPS on port 443), the storage files and database options (storage is temporary), the cluster options, and the authentication (anonymous access is denied and the access token is the credential).

Settings that ntfy leaves unset by default are not offered, because the platform cannot start an instance with an empty parameter: the base URL (and with it attachments and web push), email and SMS delivery, Stripe billing and the upstream server for instant iOS notifications.

## Limits and storage

- By default messages are limited to 4096 bytes and kept for 12 hours (settings above).
- Storage is temporary. Stopping, replacing or deleting the instance loses cached messages and any subscription state held on the server. No persistent volume is promised.
- Every request is authenticated; unauthenticated requests are denied. Keep the token private.
- iOS delivery: a self-hosted ntfy server has no direct path to Apple's push service, so iOS notifications can be delayed until the app is opened. Android delivers via a persistent connection.

## Older gateway endpoint

This service no longer routes through the UnitySVC API gateway, and your UnitySVC API key no longer authenticates ntfy requests. Use the instance URL and the access token instead.
