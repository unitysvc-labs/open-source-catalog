# Mailpit Email Testing Inbox

Each enrollment runs a private [Mailpit](https://mailpit.axllent.org/) server. Mailpit is written and maintained by [Ralph Slooten](https://github.com/axllent) and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `axllent/mailpit` image (version 1.34.0, pinned by digest), and the platform runs one isolated instance per enrollment.

Mailpit catches the mail of an application under test and shows it in a web inbox, so nothing reaches a real recipient.

**SMTP is not available from outside the instance.** The platform publishes an instance over HTTPS on port 443 only. Mailpit's SMTP port (1025) is not reachable from your application, your CI or your computer, so you cannot point an application's SMTP settings at this service. Mail is delivered with Mailpit's HTTP send API instead, described below. If your application can only send by SMTP, run Mailpit next to it instead of using this service.

## Set up

1. Enroll in **base**. The form shows a **Sign-in name** (default `admin`) and a generated **Sign-in password**. Save the password now: the platform keeps it as a secret and does not show it again. They are application credentials, not your UnitySVC API key.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. A new enrollment has a new address.
3. Open the address. The browser asks for the sign-in name and password (HTTP basic authentication), then shows the empty inbox.

## Deliver mail: the send API

Post a message as JSON to `/api/v1/send`, with the sign-in name and password:

```bash
curl -u admin:<password> -H "Content-Type: application/json" \
     -d '{
           "From": {"Email": "app@example.com", "Name": "My App"},
           "To": [{"Email": "user@example.com"}],
           "Subject": "Welcome",
           "Text": "Hello from the test run",
           "HTML": "<p>Hello from the test run</p>"
         }' \
     https://<instance>/api/v1/send
```

The answer is `{"ID": "..."}` and the message appears in the inbox at once. The body also takes `Cc`, `Bcc`, `ReplyTo`, `Headers`, `Tags` and `Attachments` (base64 content); the [send API reference](https://mailpit.axllent.org/docs/api-v1/view.html#post-/api/v1/send) lists every field. In the application under test, add a test-only mail transport that makes this request instead of opening an SMTP connection. A message can be at most 10 MB.

A request that carries an `Origin` header of another site, as a browser sends from a web page, is refused with `403`. Call the send API from server-side code or from a test runner.

## Read mail

- **Web inbox.** Open a message to see its HTML and text parts, headers, raw source and attachments, the HTML compatibility check and the link check. New mail appears without reloading.
- **REST API,** for automated tests, with the same credential:

  ```bash
  curl -u admin:<password> "https://<instance>/api/v1/messages?limit=10"
  curl -u admin:<password> "https://<instance>/api/v1/search?query=to:user@example.com"
  curl -u admin:<password> "https://<instance>/api/v1/message/<ID>"
  curl -u admin:<password> -X DELETE "https://<instance>/api/v1/messages"
  ```

  The last call empties the inbox, which is a useful first step of a test run. The [API documentation](https://mailpit.axllent.org/docs/api-v1/) describes the rest.

## Authentication

Mailpit checks every request itself with HTTP basic authentication: the web interface, the live-update connection and every API call, including the send API, answer `401` without the sign-in name and password. There is one credential; whoever has it can both deliver and read mail. Only the health routes `/livez` and `/readyz` answer without it, and they show nothing. Anyone who knows the instance address can reach the sign-in prompt, so keep the password strong. To change the password, change the enrollment's parameter; the instance restarts with the new one. UnitySVC adds no other gate.

## What is kept, and what is lost

The inbox is temporary by design, like a default Mailpit.

- Mailpit keeps the newest 500 messages and prunes older ones about once a minute.
- The inbox survives a restart of the container, but **stopping the instance empties it**, and so does anything that replaces the instance, such as changing a parameter. Nothing is stored in your UnitySVC home or storage, and the service asks for no access to them.
- The messages share the instance's 1 GiB of temporary disk. Many messages with large attachments can fill it; delete messages you no longer need.
- Captured mail is never relayed: Mailpit's "release" and forwarding features are not configured.
- The link check and the HTML check make requests from the instance to addresses found in a message. Screenshots and spam scoring need other services and are not set up.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check Mailpit used about 10 MiB idle and under 30 MiB while receiving 600 messages. Stop the instance when a test session is over; the next start gives an empty inbox at the same address. Labs adds no markup and receives no seller payout.
