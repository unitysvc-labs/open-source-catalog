# draw.io Diagram Editor

Each enrollment runs a private copy of [draw.io](https://www.drawio.com/) (diagrams.net), a diagramming and whiteboarding editor that works in the web browser. draw.io is developed by draw.io Ltd (formerly JGraph) and draw.io AG; its source code is released under the Apache License 2.0 (the project's icon sets and stencil libraries carry an extra restriction that bars their use in Atlassian products; diagrams you export are not affected). UnitySVC Labs lists the project's self-hosted image `jgraph/drawio` (version 32.7.7, pinned by digest), and the platform runs one isolated instance per enrollment. The draw.io authors were not asked to take part, and nothing here implies endorsement or support. The project describes this image as a test version of draw.io for evaluating and trying it out, with a paid production version available from them.

The instance is a Tomcat web server that serves the editor as static files. It runs as the non-root user `tomcat` and keeps no diagrams.

## Set up

1. Enroll in **base**. The only setting is the default editor language (default `en`); it asks for no access to your home.
2. Wait for the instance to become ready (in a local check Tomcat was serving within about 25 seconds). Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. A new enrollment has a new address.
3. Open the address in a browser. The editor opens on a blank diagram.

## Use it

Draw as in the hosted draw.io: drag shapes from the left panel, connect them, and use **File** to save or export. When you save, choose **Device** (the browser asks where to put the `.drawio` file), **Browser** (kept in your browser's own storage) or **Download**. PNG, JPEG and SVG export are rendered in your browser. PDF export opens your browser's print dialog, because this image ships no export server. To keep your work, save it to your device: the instance does not store it.

Saving to **Google Drive, OneDrive, Dropbox, GitHub, GitLab or Trello is not available**: those need OAuth client credentials registered with each provider, and none are configured here, so the image leaves them off.

In the default setup the editor loads everything it needs from the instance itself. In a local check the page and the editor made no requests to draw.io's servers or to any third-party host when opened and when a shape was drawn and the save dialog opened. Some optional features (for example shape libraries or templates that link to online resources, or images you add by URL) make your browser fetch from the address you choose. The instance disables draw.io's usage logging.

## Authentication

There is no sign-in. draw.io has no accounts, and UnitySVC adds no gate: anyone who knows the instance address can open the editor. This exposes no data, because the instance keeps none, but a stranger who has the address can use the instance you pay for, so share it only with the people you want to use it. There are no credentials to set. Real-time collaboration is not supported by this version of draw.io.

## What is kept, and what is lost

Nothing on the instance. It stores no diagrams, settings or history, and the service asks for no home access. Stopping or removing the instance loses nothing, because there is nothing to lose. Diagrams you save to your device are yours; what draw.io remembers for a visitor (recent files, preferences, the **Browser** storage) is kept by that visitor's own browser, and clears with it.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. The Java server used about 185 MiB when idle and about 195 MiB after the editor was opened, a diagram was drawn and a few heavy files were requested, in a local check limited to 512 MiB. Labs adds no markup and receives no seller payout.
