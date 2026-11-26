# CyberChef Data Toolkit

Each enrollment runs a private copy of [CyberChef](https://gchq.github.io/CyberChef/), the "Cyber Swiss Army Knife": a web app for encoding, encryption and data analysis. CyberChef is written and maintained by GCHQ and contributors and is released under the Apache-2.0 license; the provider of this service is its author. UnitySVC Labs lists the project's own image `ghcr.io/gchq/cyberchef` (version 11.6.0, pinned by digest), published by the project's release workflow, and the platform runs one isolated instance per enrollment. The CyberChef authors were not asked to take part, and nothing here implies endorsement or support. The project states that no guarantee is offered for the correctness or security of CyberChef, in particular of its cryptographic operations.

The instance is a static website served by nginx. According to the CyberChef README, none of your recipe configuration or input (text or files) is ever sent to the web server; all processing is carried out within your browser. That is the upstream's claim; this service does not add to it or verify it for every operation.

## Set up

1. Enroll in **base**. It has no settings to fill in and asks for no access to your home.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. A new enrollment has a new address.
3. Open the address in a browser.

## Use it

Type or paste text into **Input**, or drop a file onto it (the README says files up to around 2 GB work, depending on the browser). Drag operations from the list on the left into **Recipe**, set their options, and read the result in **Output**. For example, search for `From Base64`, add it to the recipe and paste `U28gbG9uZyBhbmQgdGhhbmtzIGZvciBhbGwgdGhlIGZpc2gu` as input. The **magic** wand can suggest how an unknown encoding might be decoded. The page address contains your recipe and input after the `#`, so a link you copy carries them; share such a link only with people you want to see that data. The first page load downloads a large script (about 13 MB), so it takes a moment.

## Authentication

There is no sign-in. CyberChef has no accounts, and UnitySVC adds no gate: anyone who knows the instance address can open the page and use every operation. This exposes no data, because the instance keeps none, but a stranger who has the address can use the instance you pay for, so share it only with the people you want to use it. There are no credentials to set.

## What is kept, and what is lost

Nothing. The instance stores no files, settings or history, and the service asks for no home access. Stopping or removing the instance loses nothing, because there is nothing to lose. Anything you load or produce stays in your browser tab (CyberChef can also save its output to a file on your computer).

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. CyberChef used about 29 MiB after a few page requests in a local check; the heavy work happens in the visitor's browser, not on the instance. Labs adds no markup and receives no seller payout.
