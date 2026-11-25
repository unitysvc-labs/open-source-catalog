# SearXNG Metasearch Engine

Each enrollment runs a private [SearXNG](https://github.com/searxng/searxng), a metasearch engine. SearXNG is written and maintained by the SearXNG community and is released under the GNU AGPL v3 license; the provider of this service is its author. UnitySVC Labs lists the official `searxng/searxng` image (version 2026.11.23-a7163d091, pinned by digest), and the platform runs one isolated instance per enrollment.

SearXNG does not crawl the web itself. Each search is forwarded to many other search engines, and the results are merged into one page. It runs as one container and needs no database or Valkey/Redis server. That is why the limiter (SearXNG's bot protection, which needs Valkey/Redis) is switched off.

## Set up

1. Enroll in **base**. There is nothing to approve: the instance asks for no access to your files.
2. The form shows a **Secret key** (generated) and a **Contact URL** (pre-filled). Keep both or change them. The secret key is not a password: SearXNG uses it to sign internal links, such as the ones for the image proxy. The contact URL is a web page or a `mailto:` address that engines such as Wikipedia, Wikidata and OpenStreetMap require, because they ask the operator of a client to be reachable; without one those engines are switched off. The pre-filled value is this catalog's page, so replace it with your own address if you want those engines to be able to reach you.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Open the address in a browser and search.

## Use it

- Type a query and pick a category (general, images, videos, news, maps, music, files, science, and others) with the tabs under the search box. **Preferences** lets you choose engines, language, safe search and theme. Those choices are saved in your browser, not on the instance, so another browser or a new enrollment starts from the defaults.
- To make it your browser's search engine, add `https://<instance>/search?q=%s` as a custom search engine, or use the OpenSearch entry the page offers.
- A search can also be made with a plain request: `https://<instance>/search?q=open+source+maps` returns an HTML page. The JSON and CSV output formats are **switched off** in SearXNG's default settings, and this recipe has no way to change the settings file, so `format=json` answers 403. Use it from a browser, or read the HTML.

**The base URL.** SearXNG builds a few absolute links (the OpenSearch description and some redirects) from the address the request arrived on, so no base URL has to be set and none is. This was checked with the platform's usual forwarded host and scheme headers.

## Authentication, and what protects the instance

**SearXNG has no sign-in.** Anyone who reaches the instance address can search through it, and you pay for the compute their searches use. The limiter, which would slow down automated use, is **off**, because it needs a Valkey/Redis server this single-container recipe does not have.

What protects it:

- The address contains an enrollment code, so a stranger cannot find it without being given it. Whether that code is hard to guess has not been checked, and an address that is pasted into a chat, a browser history, a link preview or a shared screen is no longer private.
- Nothing else. The secret key is not a password and checks nothing a visitor sends. UnitySVC adds no other gate.

So share the address only with people you trust, and do not put it on a public page. If you need real access control, put SearXNG behind something that has it; this recipe does not.

## Search engines may block a cloud address

SearXNG shows results from engines it does not control. They may answer a cloud address with a CAPTCHA, an error or no results, or rate-limit it after many searches, and SearXNG then marks that engine as unresponsive for a while. In a local check, DuckDuckGo answered with a CAPTCHA while other engines returned results, so you may find some engines empty from time to time and others working. Results also come from many engines at the platform's address, so the more people use the instance, the more likely engines are to throttle it. The Preferences page lets you turn engines off and on.

## What is kept, and what is lost

Nothing is persisted, and the instance asks for no home or storage access. SearXNG keeps no account, search history or database on the server. It writes a generated `settings.yml` into its own filesystem at every start and a small cache folder (empty unless favicons are switched on); both are disposable and are lost when the instance stops or is replaced. A container restart (`docker restart` in the local check) brought it back with the same behavior and nothing to restore.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check with those limits, SearXNG used about 167 MiB at idle, about 197 MiB after five searches and about 242 MiB after twelve searches at once. Labs adds no markup and receives no seller payout.
