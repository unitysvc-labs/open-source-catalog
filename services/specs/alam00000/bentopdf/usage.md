# BentoPDF PDF Toolkit

Each enrollment runs a private copy of [BentoPDF](https://bentopdf.com/), a PDF toolkit that works in the web browser. BentoPDF is written and maintained by [Alam](https://github.com/alam00000) and contributors and is released under the AGPL-3.0 license, with a separate paid commercial license for closed-source products; the provider of this service is its author. UnitySVC Labs lists the project's self-hosted image `ghcr.io/alam00000/bentopdf-simple` (version 2.8.12, pinned by digest), and the platform runs one isolated instance per enrollment. The BentoPDF author was not asked to take part, and nothing here implies endorsement or support.

The instance is a static website served by nginx. According to the BentoPDF project, all processing happens in the visitor's browser and files are never uploaded to a server. That is the upstream's claim; this service does not add to it or verify it for every tool.

## Set up

1. Enroll in **base**. It has no settings to fill in and asks for no access to your home.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. A new enrollment has a new address.
3. Open the address in a browser and pick a tool.

## Use it

Open a tool (for example **Merge PDF**), drop in your files, and download the result. Your files stay in your browser and are not stored on the instance. Tools that convert Office files or run OCR, compression, PDF/A or similar heavy work download their processing code (WebAssembly) into your browser the first time you use them, so that first use is slower. By default the page loads parts of that code from the jsDelivr CDN (`cdn.jsdelivr.net`), so the **visitor's browser** needs internet access to it; the instance itself does not fetch anything for the visitor. Office conversion needs a secure context and works over the instance's HTTPS address.

## Authentication

There is no sign-in. BentoPDF has no accounts, and UnitySVC adds no gate: anyone who knows the instance address can open the page and use every tool. This exposes no data, because the instance keeps none, but a stranger who has the address can use the instance you pay for, so share it only with the people you want to use it. There are no credentials to set.

## What is kept, and what is lost

Nothing. The instance stores no files, settings or history, and the service asks for no home access. Stopping or removing the instance loses nothing, because there is nothing to lose. What a visitor does in the page (for example, remembered browser preferences) is kept by their own browser, not by the instance.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. BentoPDF used about 9 MiB when idle and about 22 MiB after a few page requests in a local check; the heavy work happens in the visitor's browser, not on the instance. Labs adds no markup and receives no seller payout.
