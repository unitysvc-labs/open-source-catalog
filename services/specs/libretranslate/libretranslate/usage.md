# LibreTranslate Machine Translation Server

Each enrollment runs a private [LibreTranslate](https://libretranslate.com/) server. LibreTranslate is written and maintained by [Piero Toffanin](https://github.com/pierotofy) and contributors and is released under the GNU AGPL v3; the provider of this service is its author. UnitySVC Labs lists the official `libretranslate/libretranslate` image (version 1.10.0, pinned by digest) and runs it unmodified, and the platform runs one isolated instance per enrollment. The authors were not asked to take part, and nothing here implies their endorsement or support.

Text is translated on your instance with open Argos Translate models. It is not sent to a third-party translation service. Translation quality is that of those open models and is usually below the large commercial services, so check important translations.

## Set up

1. Enroll in **base**. The form shows **Languages** (default `en,es`; up to three language codes) and a generated **API key**. Keep or replace the key and save it; it is also shown in the enrollment's instance details. They are application credentials, not your UnitySVC API key.
2. Wait for the instance to become ready. It downloads the language models when it starts, so allow a few minutes. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
3. Call the API, or open the address in a browser, click the key icon in the top bar of the web translator and paste your API key.

## Translate

```bash
curl -X POST "https://<instance>/translate" -H "Content-Type: application/json" \
     -d '{"q": "Hello world", "source": "en", "target": "es", "api_key": "<your API key>"}'
# {"translatedText":"Hola mundo"}
```

`source` can be `auto` to detect the language. `POST /detect` (fields `q`, `api_key`) returns the likely language, and `GET /languages` lists the loaded languages and the directions between them. The [LibreTranslate API documentation](https://docs.libretranslate.com/) describes the other fields, such as `format: "html"` and file translation.

## Authentication

The instance runs with LibreTranslate's API-key database switched on and "under attack" mode: **every request to `/translate` and `/detect` that lacks a valid key is refused** (400 without a key, 403 with a wrong one), in the web translator as well as in the API. The key is checked by LibreTranslate itself; UnitySVC adds no other gate. `GET /languages` and the web page itself load without a key but cannot translate. The key is registered with a limit of 600 requests a minute. Keep it private. Change it by changing the enrollment's parameter; it is read at every start.

## Languages and limits

- Choose the languages at enrollment (`en,es` by default, up to three codes such as `en,fr,de`). Only the codes LibreTranslate publishes models for work. Each language pair direction is a separate download of about 200 MB.
- On the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) a local check with English, Spanish and French used about 550 MB of the disk and stayed within memory. More languages need a bigger size and a different recipe; do not set more than three.
- The instance has half a core, so a long text takes seconds, not milliseconds.

## What is kept, and what is lost

Nothing is kept. The language models and the key database live on temporary storage: they are downloaded or recreated each time the instance starts, and are lost when it stops. The instance stores no translations and no history. Because the models are downloaded at start, the first minutes of every run are spent on the download.

## Cost and size

The instance runs on the `nano` size and you pay the platform's cost for it for as long as it runs, including idle time. In a local check LibreTranslate used about 290 MiB of memory after a few requests with two languages. Labs adds no markup and receives no seller payout.
