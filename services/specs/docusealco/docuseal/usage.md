# DocuSeal Document Signing

Each enrollment runs a private [DocuSeal](https://www.docuseal.com/) server, the open-source edition. DocuSeal is written and maintained by the DocuSeal team and contributors, and the source is at [github.com/docusealco/docuseal](https://github.com/docusealco/docuseal); the provider of this service is its author. UnitySVC Labs lists the official `docuseal/docuseal` image (version 3.4.0, pinned by digest), and the platform runs one isolated instance per enrollment on DocuSeal's built-in SQLite database. No other service is needed.

## Set up

1. Enroll in **base**. The enrollment asks for access to the storage of this enrollment (`service:storage`, read and write). Approve it, or the instance does not start.
2. The form shows a generated **Secret key**. DocuSeal uses it for sessions and to encrypt its stored settings and its signing certificate. **Save it now**: the platform keeps it as a secret and does not show it again. Do not change it later: with another key the stored data cannot be decrypted and DocuSeal stops working (in a local check, sign-in failed and the settings were unreadable). It is an application secret, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it.
4. **Open the address at once and fill in the setup form.** The first visit shows a setup form (name, email, password, company, **App URL**) with no password or login before it. Whoever submits it first becomes the administrator, so do it as soon as the instance is ready. The setup page is closed after the first account exists. There is no public sign-up: further users are added by the administrator in the settings.
5. In **App URL** enter the instance address from step 3, with `https://`. DocuSeal does not know its own address before it exists, and uses this value in the links of signing-request emails, in document links returned by the API and in the audit trail. If you get it wrong, the administrator can change it later in the account settings. **A new enrollment has a new address**, so a link sent from an old instance points to that old instance.

## Create and send a document

1. In the web interface, upload a PDF, place fields (signature, date, text, checkbox, file and more) and add the signers' roles.
2. Send it: DocuSeal gives each signer a link (`https://<instance>/s/<slug>`) to fill and sign on any device. Copy the link and send it yourself, or let DocuSeal send the email.
3. When all signers are done, the signed PDF and an audit trail are available for download from the submission, and the free API (`X-Auth-Token` header, token under Settings, API) can list and download them.

**Emails need your own SMTP server.** The instance has no mail server and no SMTP settings. Add yours in the DocuSeal settings (email/SMTP). Until then no email is sent, but you can still copy signing links by hand. Sending through an external SMTP server was not tested here.

## What is not in this edition

DocuSeal has an open-source (free) edition and paid **Pro** features. This is the open-source image; the project lists these as Pro: company logo and white-label, user roles, automatic reminders, invitation and identity verification by SMS, conditional fields and formulas, bulk send from CSV or XLSX, SSO and SAML, template creation by API from HTML, or from PDF or DOCX with field tags, and the embedded signing form and form builder. We checked one of them: creating a template through the API (`POST /api/templates/pdf`) answers "This feature is available in Pro Edition". Pro licenses are bought from DocuSeal, and this recipe does not include one.

## Authentication

DocuSeal checks every request itself: the web interface needs your sign-in, and the API needs your token. A signing link opens a document to anyone who holds it, so send it only to the signer. Anyone who knows the instance address can reach the sign-in page, so keep the administrator password strong. UnitySVC adds no other gate.

## What is kept, and what is lost

DocuSeal's data folder is persistent: the SQLite database (`db.sqlite3`: users, templates, submissions, settings) and the uploaded and signed documents (`attachments/`). They are stored in the storage of this enrollment. The platform restores them before DocuSeal starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes.

- **The data belongs to this enrollment.** When you cancel the enrollment it goes away from your view, and a new enrollment starts empty, with a new secret key and a new address. Download the documents you need to keep (and the audit trails) before cancelling.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, and more of the newest database writes, because SQLite's temporary write-ahead files (`*-wal`, `*-shm`) are not stored. A normal stop loses nothing.
- Files are copied, never deleted from storage. Empty files, symbolic links and files over 1 GiB are not stored.
- DocuSeal starts as root in its container, fixes the owner of the data folder and then runs as user 2000; the recipe restores files as 2000:2000 to match.

## Licence

DocuSeal is licensed under the GNU Affero General Public License v3.0, with an additional term under its section 7(b): a covered work must keep the original DocuSeal attribution in its interactive user interface. Do not remove that attribution. This service runs the unmodified upstream image. If you modify DocuSeal and offer it over a network, the AGPL requires you to offer your users its source.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check with the same limits, DocuSeal used about 190 MiB idle and about 300 MiB after a template and one completed signing; rendering large PDFs may use more. Labs adds no markup and receives no seller payout. The data in storage is not billed while that feature is in preview.
