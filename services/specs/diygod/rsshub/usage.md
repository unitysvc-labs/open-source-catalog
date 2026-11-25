# RSSHub Feed Generator

Each enrollment runs a private [RSSHub](https://github.com/DIYgod/RSSHub) instance. RSSHub is written and maintained by [DIYgod](https://github.com/DIYgod) and its contributors and is released under the GNU Affero General Public License v3 (AGPL-3.0); the provider of this service is its author. UnitySVC Labs lists the official `diygod/rsshub` image (tag `2026-11-25`, pinned by digest), and the platform runs one isolated instance per enrollment. Nothing here implies that the RSSHub author takes part in this listing or supports it.

## Read this first: what works and what does not

- **Many routes are blocked by their sites.** RSSHub reads the target site itself, from the platform's network. Large sites often refuse requests that come from cloud addresses, or ask for a sign-in, a captcha or a key. Such a route answers with an error or an empty feed, and nothing in this recipe can change that. Expect some routes to work and others not, and try a route before you rely on it. In a local check from a home network, routes for GitHub issues, Hacker News, YouTube, Telegram, Bilibili and Instagram returned feeds, and others (Pixiv among them) failed; from the platform's addresses the results can differ.
- **Routes that need a browser do not work.** About 130 of the route files (of roughly 4,100) use a headless browser, for example the Douyin routes. This recipe runs the plain image, which has no browser, and it is not paired with the separate browser service that upstream's compose file adds. Those routes answer `503`. The `chromium-bundled` image is not used: it is about four times larger, and a browser needs more memory than the size this recipe runs on.
- **Routes that need a site's own credentials** (an account cookie, a token) cannot be given those here, because the recipe passes only the access key to the instance.

## Set up

1. Enroll in **base**. There is nothing to approve: the instance asks for no access to your home or storage.
2. The form shows a generated **Access key**. Keep it or enter your own (at least 12 characters; use letters, digits, `-` and `_` so it needs no escaping in an address). Save it; it is also shown in the enrollment's instance details. It is an application credential, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address**, so feed readers that use the old one need the new one.
4. Open the address. The home page opens without the key; every feed needs it.

## Make a feed

1. Pick a route from the [RSSHub route list](https://github.com/DIYgod/RSSHub#readme) (the project's documentation site lists every route and its parameters) and put it after the address, then add `?key=<access key>`:

   ```bash
   curl "https://<instance>/hackernews/best?key=<access key>"
   curl "https://<instance>/github/issue/DIYgod/RSSHub?key=<access key>&limit=5"
   ```

2. The default output is RSS. Add `&format=atom` for Atom or `&format=json` for JSON Feed. (A `.json` suffix on the path is read as part of the last parameter, so use `format`.)
3. Subscribe to the full address, with the key, in a feed reader. Because the key is part of the address, anyone who sees the address can use the instance; use a key you do not reuse.

## Authentication

Upstream RSSHub has **no authentication by default**: anyone who can reach the address could use the instance, and it would fetch whatever sites they ask for, from the platform's network and at your cost. This recipe therefore sets RSSHub's own `ACCESS_KEY` from the form. In a local check:

- A request without the key, or with a wrong key, is refused with `403` (including `/healthz`).
- A request with `?key=<access key>` is answered. RSSHub also accepts `?code=<md5 of the route path followed by the key>` instead of the key; it lets a reader subscribe without the key itself being in the address. This is read from RSSHub's source; it was checked there and in a local request.
- The home page (`/`) is open without a key; it only says RSSHub is installed.

UnitySVC adds no other gate. Changing the key restarts the instance, and the old key stops working.

## What is kept, and what is lost

Nothing is kept. RSSHub holds fetched pages in memory for a few minutes (its memory cache; no Redis is used) and writes only log and temporary files in the instance's temporary disk. All of it is lost when the instance stops, restarts or is replaced, and a feed is simply fetched again. Your enrollment's settings (the access key) are the only thing that carries over.

## Limits to know

- A route reads a third-party site; when that site changes its pages, or blocks the platform's network addresses, the route can fail until upstream fixes it.
- The instance fetches on request and caches briefly, so a feed is as fresh as the last request that reached it.
- The image runs its process as `root` inside the container (upstream's image sets no other user). It is isolated per enrollment, and it persists nothing.
- The home page loads a stylesheet and fonts from public content-delivery networks; the feeds do not depend on them.

## Cost and size

The instance runs on the `small` size (one core, 2 GiB) and you pay the platform's cost for it for as long as it runs, including idle time. RSSHub uses a lot of memory for what it does: about 420 MiB at idle, about 450 MiB under a 512 MiB limit and up to about 560 MiB with more room, after fetching ten feeds, in a local check. The `nano` size (512 MiB) would be too tight, so this recipe does not offer it. Labs adds no markup and receives no seller payout.
