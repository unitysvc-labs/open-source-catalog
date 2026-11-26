# Grafana Dashboards and Alerting

Each enrollment runs a private [Grafana](https://grafana.com/) server. Grafana is written and maintained by [Grafana Labs](https://grafana.com/) and the Grafana contributors and is released under the AGPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `grafana/grafana` image (open-source edition, version 13.3.2, pinned by digest), and the platform runs one isolated instance per enrollment. The image contains no metrics or logs: you connect your own data sources.

Your dashboards, data sources, users and settings are kept in the `grafana` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `grafana/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Grafana instance at a time.
2. The form shows an **Administrator name** (default `admin`), a generated **Administrator password** and an optional **Public address**. The name and password create the administrator account the **first time** Grafana runs on your data. If the database already exists, because you enrolled before or restarted, they are ignored and the existing password still applies; change it in Grafana's profile settings. Grafana's default `admin` / `admin` login does not exist here. Save the values; they are also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. Grafana needs about 15 to 30 seconds to start. **A new enrollment has a new address**, so bookmarks and scripts that point at the old one need the new one.
4. Open the address and sign in with the administrator name and password.
5. Optional: once you know the address, put it (`https://<enrollment-code>.<apps-domain>/`) into **Public address** and save. Left at its default, `http://localhost:3000/`, it is Grafana's own default. Grafana uses this setting for the links in alert notifications and emails, for sharing and for single sign-on callbacks. Signing in, dashboards and data sources work without it; those links and callbacks point at `localhost` until you set it. The change takes effect when the instance restarts.

## Add a data source and a dashboard

In the web interface, open **Connections**, add a data source and build a dashboard from it. To try Grafana without any data, add the built-in **TestData** data source. The same works through the HTTP API with the administrator credentials (or a service-account token you create in Grafana):

```bash
curl -u "<admin>:<password>" -H "Content-Type: application/json" \
     -d '{"name":"td","type":"grafana-testdata-datasource","access":"proxy"}' \
     https://<instance>/api/datasources
```

The instance can reach data sources that are reachable over the internet; it cannot reach private networks that are not exposed. The image does not download extra plugins at start (the plugins built into the image, for example Prometheus, Tempo, CloudWatch and TestData, are available); you can install more from the web interface if the instance can reach grafana.com, and they are kept in your home.

## Authentication

Grafana checks every request itself: the web interface and the API need your sign-in, and a service-account token works for scripts. Anonymous access and public sign-up are switched off, so only users the administrator creates can sign in. Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong. UnitySVC adds no other gate.

## What is kept, and what is lost

Grafana's data folder is persistent: the SQLite database (users, dashboards, data sources, alert rules, API keys) and plugins you install. They are stored in `grafana/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before Grafana starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file Grafana removes, such as an uninstalled plugin, can come back after a restart.
- SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. They are rebuilt by Grafana and this keeps the stored database consistent.
- Do not edit the files in `grafana/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `grafana/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `small` size (one core, 2 GiB) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check Grafana used about 0.45 GiB at idle when limited to 512 MiB, and sat at the limit after a few queries, which is why the smaller `nano` size is not offered; with 2 GiB it settled near 1.1 GiB. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
