# Stirling PDF Toolkit

Each enrollment runs a private copy of [Stirling-PDF](https://www.stirlingpdf.com/), a self-hosted toolkit for working with PDF files. Stirling-PDF is written and maintained by Stirling PDF Inc. and contributors (source: [Stirling-Tools/Stirling-PDF](https://github.com/Stirling-Tools/Stirling-PDF)); the provider of this service is its author. UnitySVC Labs lists the project's official `stirlingtools/stirling-pdf` image, version 3.5.0, the `ultra-lite` variant, pinned by digest, and the platform runs one isolated instance per enrollment. The Stirling-PDF authors were not asked to take part, and nothing here implies endorsement or support.

## Set up

1. Enroll in **base**. It has no settings to fill in and asks for no access to your home.
2. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. A new enrollment has a new address. Starting takes about a minute, because it is a Java application.
3. Open the address in a browser and pick a tool.

## Use it

In the web interface, choose a tool (for example **Merge**), add your PDF files, run it and download the result. The same tools are a REST API under `/api/v1/`; for example, to merge two files from a script:

```bash
curl -o merged.pdf -F fileInput=@a.pdf -F fileInput=@b.pdf -F sortType=orderProvided \
     https://<instance>/api/v1/general/merge-pdfs
```

## What this build leaves out

This is the `ultra-lite` image: the core PDF tools only. According to upstream it has no OCR, and no Office, HTML or ebook conversions, and at startup it reports the OCR, repair, scanner-effect and URL-to-PDF tools as disabled because their helper programs are not in the image. It also has **no login**; the login-capable `latest` image is a different, much larger build.

## Authentication

There is no sign-in, and UnitySVC adds no gate. **Anyone who knows the instance address can open the page and use every tool and the API**, and so can use the instance you pay for. The instance keeps none of your files, so no data is exposed, but keep the address private and stop the instance when you do not need it.

## What is kept, and what is lost

Nothing. Files you upload are processed in the instance's memory and temporary disk and are not stored by the service, which asks for no home access. Stopping or removing the instance loses nothing but settings you changed inside it, and the app has no user settings to change. Stirling-PDF's own anonymous usage statistics (PostHog and Scarf) are switched off with the documented `SYSTEM_ENABLEANALYTICS=false` setting.

## Licence

Stirling-PDF is open-core. Most of it is MIT, but parts of the repository (`app/proprietary/`, `frontend/src/processor/` and others) are under a separate Stirling PDF User License, which allows trial and minimal use and requires a paid subscription for production use. The ultra-lite image does not include the proprietary Java module, but its web interface does include the Processor portal pages. Read upstream's [LICENSE](https://github.com/Stirling-Tools/Stirling-PDF/blob/main/LICENSE) before relying on this service for business use.

## Cost and size

The instance runs on the `small` size (one core, 2 GiB, 5 GiB of temporary disk), which matches upstream's suggested 2 GB for the ultra-lite image, and you pay the platform's cost for it for as long as it runs, including idle time. In a local check the Java process used about 0.5 GiB at idle and about 1.1 GiB after a few merges, because the JVM grows its heap toward the limit. Labs adds no markup and receives no seller payout.
