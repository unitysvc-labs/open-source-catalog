# SiYuan Notes and Knowledge Base

Each enrollment runs a private [SiYuan](https://b3log.org/siyuan) server. SiYuan is written and maintained by [Yunnan Liandi Technology Co., Ltd.](https://github.com/siyuan-note) and contributors and is released under the AGPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `b3log/siyuan` image (version 3.8.12, pinned by digest), and the platform runs one isolated instance per enrollment.

Your workspace (settings, notebooks, assets and history) is kept in the `siyuan` folder of your **home**, not in the enrollment. It survives stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same workspace.

> **Deleted and moved documents come back after a stop.** The copy in your home only adds and replaces files; it never deletes one. SiYuan stores each document as one file whose place in the folder tree is its place in the notebook. So after the instance is stopped and started again (not while it runs): a document or notebook you deleted is back, and a document you moved is at its new place **and** at its old place, with the same ID. For such a pair SiYuan showed the old copy in a local check, without the edits made after the move, although the newer file was still stored. Read [What is kept, and what is lost](#what-is-kept-and-what-is-lost) before you reorganise a workspace, and clean up the `siyuan/` folder in your home while the instance is stopped.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `siyuan/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one SiYuan instance at a time.
2. The form shows a generated **Access authorization code**. Keep it or enter your own (at least 12 characters). Save it now: the platform keeps it as a secret and does not show it again. It is an application credential, not your UnitySVC API key.
3. Wait for the instance to become ready; a start takes a few seconds. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Open the address in a browser. SiYuan shows its lock screen; enter the access authorization code. A new workspace opens with a first notebook you can rename or remove.
5. Create a document in the notebook and start writing. Type `/` in the editor for the block menu, and `((` to reference another block.

## Authentication

SiYuan has no user accounts. The access authorization code is the only credential, and whoever has it can read and change the whole workspace, so keep it long and private. Without a session the web interface redirects to the lock screen and the API answers 401; after a few wrong codes the lock screen also asks for a captcha. SiYuan refuses to start in a container without a code, so the instance is never served open. UnitySVC adds no other gate.

SiYuan takes the code from the enrollment at **every** start. To change it, change the parameter: the instance restarts with the new code and existing browser sessions are signed out. A code changed inside SiYuan's own settings is replaced by the enrollment's value at the next start.

For scripts, SiYuan has an HTTP API. The token is in **Settings > Authentication > API token**:

```bash
curl -X POST https://<instance>/api/notebook/lsNotebooks \
     -H "Authorization: Token <token>" -H "Content-Type: application/json" -d '{}'
```

The [API documentation](https://github.com/siyuan-note/siyuan/blob/master/docs/API.md) lists the public calls.

## What this server does not do

- **Browser only.** The SiYuan desktop and mobile apps cannot connect to a server run from the container image. Export to PDF, HTML and Word, and import of Markdown files, are not available in it. These are upstream limits of the image.
- **Paid SiYuan features are not included.** Data sync and backup to the vendor's cloud or to your own S3 or WebDAV storage, cloud asset hosting and the cloud inbox need a paid SiYuan account, sold by the vendor (see [SiYuan pricing](https://b3log.org/siyuan/en/pricing.html)). Everything else, including the editor, databases, flashcards, search, the API and the community marketplace, is part of the open-source server. This service does not sign you in to a SiYuan account and has no part in such a purchase.
- **No email.** SiYuan does not need email for anything in this setup.

## What is kept, and what is lost

The workspace folder is persistent: `conf/` (settings, the API token, installed themes and icons), `data/` (notebooks as `.sy` files, assets, templates, plugins, widgets), and `history/` and `repo/` (document history and local snapshots). They are stored in `siyuan/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before SiYuan starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **Files are copied, never deleted from your home.** Everything SiYuan removes from the workspace is restored at the next start:
  - A deleted document or notebook comes back.
  - A moved document exists twice, at the new place and at the old one, with the same block IDs. In a local check SiYuan indexed the old file: the document opened at its old place without the edits made after the move, and those edits were not found by search, although the newer file was still in the folder at the new place.
  - Removed assets, old history that SiYuan purges, and removed plugins or themes come back too.

  To make a deletion or a move last, stop the instance, delete the stale `.sy` file (and the folder of the same name, which holds its sub-documents) under `siyuan/data/<notebook>/` in your home, and start the instance again. Renaming a document or a notebook is safe: the name is stored inside a file, not in its path.
- **The search index is not stored.** SiYuan keeps its index and caches in SQLite databases under `temp/`; they are left out of the copy and SiYuan rebuilds them from your documents at every start. A large workspace therefore takes longer to become searchable after a start.
- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Do not edit files in `siyuan/` while the instance runs: SiYuan does not see the change, and the next copy overwrites it.
- Empty files, symbolic links and files over 1 GiB are not stored. SiYuan's own empty files (lock and ignore-list files) are recreated at start; an empty asset you upload is lost at the next stop.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `siyuan/` folder yourself when you no longer want the data. A new workspace is about 45 MiB, mostly SiYuan's built-in themes and icons.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check SiYuan used about 50 MiB idle, about 80 MiB with a browser editing, and about 120 MiB with 300 documents; a very large workspace needs more. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
