# ntfy Push Notifications — Tutorial

Push notifications delivered via HTTP from your own private [ntfy](https://ntfy.sh) server. Publish from any script, CI pipeline, or app, and receive on your phone, desktop, or via API.

The short setup is in **How to use this service**. This guide covers publishing options, subscribing, and troubleshooting.

---

## What you get after enrolling

- A private ntfy server at `https://<enrollment-code>.<apps-domain>` (shown in the instance details; used as `<instance>` below).
- An **access token** (`tk_...`). Every request to the instance must carry it, so your topics are private to anyone who does not have the token.

Your UnitySVC API key is not used with this service, and requests do not pass through the UnitySVC API gateway.

---

## Step 1 — Send your first message

```bash
curl -H "Authorization: Bearer tk_YOUR_TOKEN" \
     -H "Title: Test" -H "Priority: high" -H "Tags: tada" \
     -d "Hello from ntfy!" https://<instance>/alerts
```

`alerts` is the topic; use any name. A successful publish returns the message as JSON (`"event":"message"`).

From Python:

```python
import requests

requests.post(
    "https://<instance>/alerts",
    headers={"Authorization": "Bearer tk_YOUR_TOKEN", "Title": "Hello", "Tags": "wave"},
    data="Sent from Python",
).raise_for_status()
```

---

## Step 2 — Receive messages

### Mobile and desktop apps

Install the official ntfy app.

| Platform | App |
|----------|-----|
| Android | [ntfy on Google Play](https://play.google.com/store/apps/details?id=io.heckel.ntfy) or [F-Droid](https://f-droid.org/packages/io.heckel.ntfy/) |
| iOS | [ntfy on App Store](https://apps.apple.com/us/app/ntfy/id1625396347) |

<img src="images/ntfy-app-store.jpg" alt="ntfy app store listing" width="300">

Add a subscription: tap **+**, enter your topic, choose **Use another server**, enter `https://<instance>`, and sign in with the access token when the app asks for credentials.

> The apps connect directly to your instance. The instance denies anonymous access, so a subscription without the credential fails with 401/403.

> iOS note: a self-hosted server has no direct path to Apple's push service, so iOS notifications can be delayed until the app is opened. Android delivers over a persistent connection.

### HTTP JSON stream

```bash
curl -s -H "Authorization: Bearer tk_YOUR_TOKEN" https://<instance>/alerts/json
```

Output is newline-delimited JSON, one event per line:

```json
{"event":"open","topic":"alerts"}
{"event":"message","topic":"alerts","message":"Hello!","title":"Test","priority":4}
{"event":"keepalive","topic":"alerts"}
```

### WebSocket

```bash
websocat -H "Authorization: Bearer tk_YOUR_TOKEN" wss://<instance>/alerts/ws
```

Browsers cannot set headers on WebSockets; use the `?auth=` query parameter described in the [ntfy docs](https://docs.ntfy.sh/subscribe/api/#authentication).

| Event | Meaning |
|-------|---------|
| `open` | Connection established |
| `message` | A published message |
| `keepalive` | Periodic heartbeat |

---

## Step 3 — Priority, tags, and formatting

```bash
curl -H "Authorization: Bearer tk_YOUR_TOKEN" \
     -H "Title: Deploy finished" -H "Priority: 4" -H "Tags: rocket,white_check_mark" \
     -H "Click: https://example.com/deploys/123" \
     -H "Delay: 30m" \
     -d "Version 1.2.3 is live" https://<instance>/alerts
```

| Header | Purpose |
|--------|---------|
| `Title` | Notification title |
| `Priority` | 1 (min) to 5 (max), or `min`, `low`, `default`, `high`, `max` |
| `Tags` | Comma-separated emoji short codes or labels |
| `Click` | URL opened when the notification is tapped |
| `Delay` | Deliver later (`30m`, `2h`, or a timestamp) |
| `Actions` | Up to three action buttons |
| `Attach` | URL of a file to show with the message |

You can also publish a JSON body to the instance root (`POST https://<instance>/`) with `topic`, `message`, `title`, `priority`, `tags`, `click`, `actions` fields; see the [ntfy docs](https://docs.ntfy.sh/publish/#publish-as-json).

---

## Use case: CI/CD notification

```yaml
# .github/workflows/deploy.yml
- name: Notify
  if: always()
  run: |
    curl -H "Authorization: Bearer ${{ secrets.NTFY_TOKEN }}" \
         -H "Title: Deploy ${{ job.status }}" \
         -d "${{ github.repository }}@${{ github.sha }}" \
         https://<instance>/deploys
```

---

## Endpoints reference

All paths are on your instance, `https://<instance>`.

| Method | Path | Description |
|--------|------|-------------|
| `POST` / `PUT` | `/<topic>` | Publish a message |
| `GET` | `/<topic>/json` | Subscribe via HTTP JSON stream |
| `GET` | `/<topic>/sse` | Subscribe via server-sent events |
| `GET` | `/<topic>/ws` | Subscribe via WebSocket |
| `GET` | `/v1/health` | Health check (no token needed) |

---

## Limits

- **Message size**: 4 KB max per message.
- **Message retention**: 12 hours.
- **Temporary storage**: cached messages are lost when the instance is replaced, stopped or deleted. Clients that were offline during that time will not receive them.
- **Access token**: one token per instance. Changing it restarts the instance.

---

## Troubleshooting

### 401 / 403

- The `Authorization: Bearer tk_...` header is missing or the token is wrong. Use the token you saved when you enrolled; the platform does not show it again, but you can set a new one in the enrollment's parameters.
- The token must be `tk_` followed by 29 letters, digits, `-` or `_`.

### Cannot connect, or the instance is not ready

- The instance takes a short while to start after enrolling or after changing the token. Check its status in the enrollment details.

### Messages not appearing on mobile

- Confirm the server URL is `https://<instance>` and the app has the access token set.
- Messages older than 12 hours, or published before an instance restart, are gone.

---

## Further reading

- [ntfy documentation](https://docs.ntfy.sh/)
- [Publishing options](https://docs.ntfy.sh/publish/)
- [Subscribe API](https://docs.ntfy.sh/subscribe/api/)
