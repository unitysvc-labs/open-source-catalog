# Excalidraw Whiteboard

Each enrollment runs a private copy of [Excalidraw](https://excalidraw.com/), a virtual whiteboard for hand-drawn style diagrams. Excalidraw is written and maintained by the Excalidraw authors and contributors and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the project's official image `excalidraw/excalidraw` and the platform runs one isolated instance per enrollment. The project publishes only the `latest` tag (built 6 May 2026), so the image is pinned by its digest rather than a version number. The Excalidraw authors were not asked to take part, and nothing here implies endorsement or support.

The instance is a static website served by nginx. The drawing happens in the visitor's browser. This is a single-user whiteboard: the official image does not include a collaboration server.

## Set up

1. Enroll in **base**. It has no settings to fill in and asks for no access to your home.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. A new enrollment has a new address.
3. Open the address in a browser and start drawing.

## Use it

Pick a tool (rectangle, arrow, text, freehand and others), draw, and use the menu to export as PNG or SVG, or to save an `.excalidraw` file you can open again later with **Open**. The page can be installed as a web app, and works offline after its first load.

## What does not work

- **Live collaboration.** It needs a separate room server. The image is built to use the one run by excalidraw.com, not a server of your instance, and your instance does not run one. We did not test it; do not rely on it.
- **Shareable links, the public shape-library site and the AI features.** The page is built to call excalidraw.com's hosted services for these. Your instance provides none of them and we did not test them; the data they send would go to those services, not to your instance.
- Other users cannot see your drawing on the instance; there is no shared board.

## Authentication

There is no sign-in. Excalidraw has no accounts, and UnitySVC adds no gate: anyone who knows the instance address can open the page. This exposes no drawings, because the instance keeps none, but a stranger who has the address can use the instance you pay for, so share it only with the people you want to use it. There are no credentials to set.

## What is kept, and what is lost

Nothing on the instance. It stores no drawings, settings or history, and the service asks for no home access, so stopping or removing it loses nothing. Your drawing is saved automatically by **your browser**, for this address only: the scene in the browser's local storage, and images and your library in its IndexedDB. Clearing the browser's site data, using a private window, or opening the page on another browser or device starts you with an empty board, and a new enrollment has a new address and therefore an empty board. Export the drawings you want to keep.

## Privacy note

Besides your instance, the visitor's browser also loads fonts from excalidraw's CDN (`excalidraw.nyc3.cdn.digitaloceanspaces.com`), and in our local test it requested a Simple Analytics script (`scripts.simpleanalyticscdn.com`) and sent a page-view image request. These come from the upstream image, not from the instance; the instance itself fetches nothing for the visitor.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. Excalidraw used about 29 MiB when idle and about 31 MiB after loading the page, drawing and reloading in a local check; the work happens in the visitor's browser. Labs adds no markup and receives no seller payout.
