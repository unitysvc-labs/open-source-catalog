# Password Pusher

Each enrollment runs a private [Password Pusher](https://pwpush.com/) server. Password Pusher is written and maintained by [Peter Giacomo Lombardo](https://github.com/pglombardo) and contributors and is released under the Apache-2.0 license; the provider of this service is its author. UnitySVC Labs lists the official `pglombardo/pwpush` image (version 2.17.4, pinned by digest), and the platform runs one isolated instance per enrollment.

Password Pusher shares a secret through a link instead of through the chat or the email itself. You paste a password, a note or a web address, choose how many views and how many days the link may live, and send the link. The recipient opens it in a browser; once the views or the days run out, the secret is deleted and the link shows an expired page.

## Set up

1. Enroll in **base**. It asks for no access to your home: nothing is stored there.
2. The form shows a generated **Instance secret**. Keep it or replace it with a string of your own of at least 32 characters. The instance uses it to sign cookies and to derive the key that encrypts stored pushes. It is an application secret, not your UnitySVC API key, and you never type it anywhere. The platform keeps it as a secret and does not show it again.
3. Wait for the instance to become ready; the first start took about 20 seconds in a local check. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. A new enrollment has a new address.
4. Open the address. You land on the push form; there is nothing to sign in to.

## Push a secret and open it

In the web interface choose **Password**, **Text** or **URL**, enter the secret, set the expiry (by default 7 days or 5 views, up to 90 days and 100 views; a value outside that range falls back to the default) and press **Push it**. Copy the secret link it gives you and send it. Optionally set a passphrase the recipient must also enter, which you tell them by another route.

From a script, use the JSON API (it needs no token on this instance):

```bash
curl -X POST https://<instance>/api/v2/pushes \
     -H "Content-Type: application/json" \
     -d '{"push": {"kind": "text", "payload": "correct horse battery staple", "expire_after_days": 2, "expire_after_views": 1}}'
```

The reply carries `html_url`, the link to send. Opening that link (or calling `GET /api/v2/pushes/<url_token>` for a push without a retrieval step) counts as a view and returns the secret; when the views are used up the secret is gone. By default a push has a **retrieval step**: the recipient first sees a page with a button, so that a link preview in a chat app does not use up a view. The [Password Pusher documentation](https://docs.pwpush.com/) describes the API and every option.

## Authentication: who can use this instance

This instance runs in Password Pusher's anonymous-only mode (`PWP__DISABLE_LOGINS` and `PWP__DISABLE_SIGNUPS`). There are no accounts and no administrator, and **anyone who knows the instance address can create pushes**. Nothing else is open to them: a push can be read only with its own secret link, there is no list of pushes, and the admin pages and the sign-in and sign-up pages answer not found. UnitySVC adds no other gate, so keep the address to the people who should use it, and delete the enrollment when you no longer need it. Password Pusher limits each visitor to a number of requests per minute.

Why anonymous-only: in this version, a Password Pusher with accounts shows a first-run page that asks for a boot code printed in the container's log, which you cannot count on being able to read on this platform. So accounts are switched off. Two things that need an account are therefore not available: **file pushes** and the per-user dashboard with audit logs. Password, text and URL pushes work.

## What is kept, and what is lost

Nothing is persisted. The pushes are held, encrypted, in a small SQLite database in the instance's temporary storage. They survive a restart of the container, but stopping, replacing or deleting the instance loses all of them. That is a fit for this software: pushes live for days at most, and the encryption key is bound to the enrollment's secret, so a database kept elsewhere could not be read by a new enrollment anyway.

- Send a new link after the instance has been stopped; links made before it are dead.
- Password Pusher deletes the secret of a push when it expires, and, according to its documentation, a background job also expires pushes that nobody opened, every two hours.
- Treat the instance as you would any server that holds secrets for a few days: the pushes are encrypted in its database with a key derived from the instance secret, but the instance and the platform that runs it can read both.

## Cost and size

The instance runs on the `small` size (one core, 2 GiB) and you pay the platform's cost for it for as long as it runs, including idle time. Password Pusher is a Ruby on Rails application with its web server and a background worker in one container, and used about 420 MiB at idle and about 490 MiB after a few requests in a local check, which is too close to the 512 MiB of `nano`. Labs adds no markup and receives no seller payout.
