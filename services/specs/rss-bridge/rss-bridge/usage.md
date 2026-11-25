# RSS-Bridge Feed Generator

Each enrollment runs a private [RSS-Bridge](https://rss-bridge.org/) instance. RSS-Bridge is written and maintained by the [RSS-Bridge community](https://github.com/RSS-Bridge/rss-bridge) and is released into the public domain under the Unlicense; the provider of this service is its author. UnitySVC Labs lists the official `rssbridge/rss-bridge` image (tag `2026-09-30`, pinned by digest), and the platform runs one isolated instance per enrollment. Nothing here implies that the RSS-Bridge community takes part in this listing or supports it.

## Set up

1. Enroll in **base**. There is nothing to approve: the instance asks for no access to your home or storage.
2. The form shows a **Sign-in name** (default `admin`), a generated **Sign-in password**, and **Enabled bridges** (default `*`, all of them). Save the password; it is also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so feed readers that use the old one need the new one.
4. Open the address. The browser asks for the name and password; then you see the list of bridges.

## Make a feed

1. Pick a bridge, fill in its form and choose a format (Atom, MRSS, JSON, HTML or plain text).
2. The page gives you a feed address of the form `https://<instance>/?action=display&bridge=<Name>&...&format=Atom`. Subscribe to it in a feed reader.
3. From a script, the same address works with credentials:

   ```bash
   curl -u "<name>:<password>" "https://<instance>/?action=display&bridge=FeedMerge&feed_1=https%3A%2F%2Fgithub.com%2FRSS-Bridge%2Frss-bridge%2Freleases.atom&format=Atom"
   ```

   A feed reader that cannot send a password can usually take it in the address, `https://<name>:<password>@<instance>/...`. That puts the password in the reader's saved address, so use a password you do not reuse.

## Authentication

Upstream RSS-Bridge has **no authentication by default**: anyone who can reach the address could use the instance, and it would fetch whatever URLs they ask for, from the platform's network and at your cost. This recipe therefore switches on RSS-Bridge's own HTTP basic authentication, with the name and password from the form. Every page and every feed needs them, and a feed reader must be able to send them. UnitySVC adds no other gate. Keep the password strong; if it is shared in a feed address, anyone who sees that address can use the instance.

## Enabled bridges

By default every bridge is enabled (547 in this version). To offer fewer, put a comma-separated list in **Enabled bridges**, for example `Youtube,Reddit,FeedMerge`; any other bridge is hidden and refused. Changing the list, the name or the password restarts the instance. Upstream's other settings (a proxy, the cache type, the admin contact, a custom bridge or a `whitelist.txt` file) need a file or a variable this recipe does not offer, so they cannot be changed.

## What is kept, and what is lost

Nothing is kept. RSS-Bridge stores only a cache of fetched pages, in the instance's temporary disk (about 0.4 MiB after a few feeds in a local check). It is lost when the instance stops or is replaced, and a feed is simply fetched again. Your enrollment's settings are the only thing that carries over to a new enrollment.

## Limits to know

- A bridge reads a third-party site; when that site changes its pages, or blocks the platform's network addresses, the bridge can fail until upstream fixes it. Some bridges need an account or key on the target site that RSS-Bridge's own settings cannot be given here.
- The instance fetches on request and caches briefly, so a feed is as fresh as the last request that reached it.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. RSS-Bridge used about 73 MiB at idle and about 90 MiB after some requests in a local check. Labs adds no markup and receives no seller payout.
