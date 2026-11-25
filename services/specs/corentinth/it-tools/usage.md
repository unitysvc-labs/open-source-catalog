# IT-Tools Developer Toolbox

Each enrollment runs a private copy of [IT-Tools](https://it-tools.tech), a collection of small tools for developers and people working in IT. IT-Tools is written by [Corentin Thomasset](https://github.com/CorentinTh) and contributors and is released under the GPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the project's image `corentinth/it-tools` (tag `2024.10.22-7ca5933`, pinned by digest), and the platform runs one isolated instance per enrollment. The project publishes only dated tags, `latest` (the same image as that dated tag) and a `nightly` tag; Labs chose the latest dated release. The IT-Tools author was not asked to take part, and nothing here implies endorsement or support.

The instance is a static website served by nginx. The IT-Tools README does not say where the tools run. UnitySVC Labs read the source of the pinned version: the tools are Vue components that compute in the visitor's browser, and the code contains no network request (`fetch`, XMLHttpRequest, WebSocket or beacon calls) for any tool. The page includes an optional Plausible analytics plugin that is disabled unless the image is built with it enabled; this image's configuration leaves it off by default. This is a reading of the source by Labs, not a guarantee from the IT-Tools project.

## Set up

1. Enroll in **base**. It has no settings to fill in and asks for no access to your home.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. A new enrollment has a new address.
3. Open the address in a browser and pick a tool.

## Use it

Open a tool from the list (for example **Base64 string encoder/decoder**, **Hash text** or **JWT parser**), type or paste your input, and copy the result. The input stays in your browser. Some tools remember their last settings in your browser's local storage; that is kept by your own browser, not by the instance.

## Authentication

There is no sign-in. IT-Tools has no accounts, and UnitySVC adds no gate: anyone who knows the instance address can open the page and use every tool. This exposes no data, because the instance keeps none, but a stranger who has the address can use the instance you pay for, so share it only with the people you want to use it. There are no credentials to set.

## What is kept, and what is lost

Nothing. The instance stores no files, settings or history, and the service asks for no home access. Stopping or removing the instance loses nothing, because there is nothing to lose.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check at that limit IT-Tools used about 29 MiB when idle and about 35 MiB after a few dozen page requests; the work happens in the visitor's browser, not on the instance. Labs adds no markup and receives no seller payout.
