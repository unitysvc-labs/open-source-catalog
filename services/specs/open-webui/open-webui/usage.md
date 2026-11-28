# Open WebUI AI Chat

This unofficial recipe runs the official Open WebUI **v0.13.5 slim** image, pinned by digest. [Open WebUI Inc., Timothy J. Baek and contributors](https://github.com/open-webui/open-webui) maintain the software. Inclusion does not imply their endorsement or a support agreement.

## License and branding

Open WebUI uses the [Open WebUI License](https://github.com/open-webui/open-webui/blob/v0.13.5/LICENSE), with earlier contributions retaining their original licenses as described in [LICENSE_NOTICE](https://github.com/open-webui/open-webui/blob/v0.13.5/LICENSE_NOTICE). The current custom license is identified here as `LicenseRef-Open-WebUI`; it is not OSI-approved. The catalog maintainer approved a project-specific exception on 2026-11-28. This recipe retains the original Open WebUI name, logos, copyright notices and interface branding, with no white-label changes. Inclusion grants no additional right to alter that branding; follow the upstream terms.

## Enroll and sign in

1. Choose **base** and approve read/write access to this enrollment's storage.
2. Set the **Administrator email**, save the generated **Administrator password**, and keep the generated **Application secret** unchanged. These are Open WebUI credentials, separate from UnitySVC credentials. Treat enrollment settings as sensitive and save credentials securely; password fields are not a secret vault.
3. Enter the **Model provider base URL**, including its version path (for example `https://api.openai.com/v1`), and your own **Model provider API key**. Use an externally reachable OpenAI-compatible API. For a provider that deliberately requires no key, enter `unused`. No model inference or provider credits are included. Requests and their authorization key are sent to the configured provider; its own terms and charges apply.
4. Start the instance, open its HTTPS address from the instance details, and sign in with the administrator email and password. Select an available model and send a message. No separate instance URL setting is needed for ordinary chat.

The administrator is created only when the database has no users. Editing its enrollment email or password later does not reset an existing account; change the account in Open WebUI. Public sign-up is disabled, so the first visitor cannot claim the instance. Administrators can manage additional users.

## Settings and supported features

This is a chat front end for an external model API, with saved conversations, model selection and application user accounts. Chat content is sent to your model provider; this recipe does not make an external provider private or local.

Provider URL/key changes in enrollment settings restart the instance and apply on its next start. The recipe disables persistent application configuration so those enrollment values remain authoritative. **Admin Panel configuration changes are temporary and revert on restart**; use enrollment settings for the provider connection. Users, passwords, conversations and uploaded files are separate database records and remain stored. Keep the application secret unchanged; replacing it invalidates signed credentials and can make protected settings unreadable.

The [official slim image](https://docs.openwebui.com/getting-started/quick-start/#why-choose-slim) omits local models and document/speech runtimes. No Ollama, GPU, embedding server, vector database, document conversion server or mail server is included. Basic chat needs only your model API. Knowledge retrieval needs both an embedding provider and PostgreSQL/pgvector; PDF/Office extraction and speech need external services. Those integrations are not configured here. Do not expect file upload alone to enable retrieval. Local speech, local embedding and bundled model inference are unavailable. No password-reset email service is configured.

## Authentication

Open WebUI checks its own sign-in and private API requests. Missing or incorrect credentials are rejected; the login page, health checks and some public application metadata remain reachable without sign-in. Anyone knowing the instance address can reach that page. UnitySVC adds no application authentication gate. Use a strong password and grant administrator access only to people you trust. Public chat sharing, tools and functions have their own upstream permissions and behavior; enabling them is an administrator decision.

## Storage and stopping

`/app/backend/data` is kept in this enrollment's storage, except caches and transient SQLite journal files. It contains the SQLite database (users, passwords, conversations and database records) and uploaded files. Native SQLite rollback journaling is enabled with synchronous `FULL`; no WAL file is needed for a cleanly closed database. One web worker is configured for this modest personal/light-use channel.

The platform copies files periodically (about every 30 seconds) and at normal stop. Recent changes can be lost on a crash, and a live file copy is not an application-consistent database backup. Keep independent chat exports and file backups; finish active chats and uploads before stopping, then verify important data after restart.

- Each copied file, including `webui.db`, must remain below **1 GiB**. Empty files, symlinks and larger files are skipped. Caches are temporary and may be recreated.
- Storage copies never delete old files. Deleting a conversation removes its database record, but deleted or renamed uploaded files can remain in enrollment storage and return as unreferenced files after restart. Do not rely on application deletion as erasure from platform storage.
- Active requests and background jobs stop with the instance. Retry an interrupted request or upload. The running container has **10 GiB temporary disk**, shared by its restored data and processing space; keep well below that limit.
- Removing the enrollment removes its storage. A new enrollment starts empty with a new address and credentials. Export conversations and download files before removal.

## Cost and support

The single container uses `small` (one CPU, 2 GiB RAM). It runs the chat interface and stores data; inference runs at your external provider. You pay platform compute base cost while this instance runs, including idle time, and your provider separately for its API use. Labs adds no markup and receives no seller payout. Stop the instance when finished; closing the browser does not stop it. See [upstream documentation](https://docs.openwebui.com/) and [discussions](https://github.com/open-webui/open-webui/discussions) for software help.
