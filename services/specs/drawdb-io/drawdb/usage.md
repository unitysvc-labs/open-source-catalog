# drawDB Database Diagram Editor

Each enrollment runs a private copy of [drawDB](https://drawdb.app/), a database schema designer that runs in the browser. drawDB is written and maintained by the drawDB contributors and is released under the AGPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `ghcr.io/drawdb-io/drawdb` image (version v1.9.0, pinned by digest), and the platform runs one isolated instance per enrollment. The container serves the application's static files; it runs no database and stores nothing of yours.

## Set up

1. Enroll in **base**. There are no parameters to fill in and no storage access to approve.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
3. Open the address. The editor starts at once; there is no account and no sign-in.

## Use it

Add tables and fields on the canvas, draw relationships between them, and add notes or areas. **Export** produces SQL scripts (MySQL, PostgreSQL, SQLite, MariaDB, SQL Server, Oracle), an image, PDF, JSON or DBML file; **Import** reads a schema from SQL or from a drawDB JSON file. The [drawDB documentation](https://drawdb.app/docs) describes the editor in full.

## Authentication

drawDB has no login. Anyone who knows the instance address can open the editor, but they see only their own browser's diagrams, never yours, because nothing is kept on the server. UnitySVC adds no other gate.

## What is kept, and what is lost

- **Your diagrams live in your browser.** drawDB saves them in the browser's local storage (IndexedDB) for this instance's address. They stay on that computer and browser profile, and clearing site data removes them. Another browser or computer, or a new enrollment (which has a new address), starts empty.
- **Export a copy** (JSON or SQL) for anything you want to keep. Stopping or removing the instance never touches the copy in your browser, but a new address cannot read it.
- The optional drawDB sharing server is not part of this service, so share links are not available.
- Nothing is stored on the platform for this service, so nothing needs to be deleted when you cancel.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. The server used about 30 MiB in a local check. Labs adds no markup and receives no seller payout.
