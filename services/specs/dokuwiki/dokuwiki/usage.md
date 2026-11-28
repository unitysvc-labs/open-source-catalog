# DokuWiki File-Based Wiki

Each enrollment runs a private [DokuWiki](https://www.dokuwiki.org/). DokuWiki is written by [Andreas Gohr](https://github.com/splitbrain) and the DokuWiki community and is released under the GNU General Public License, version 2; the provider of this service is its author. UnitySVC Labs lists the official `dokuwiki/dokuwiki` image (release 2026-07-14c "Mort", pinned by digest), and the platform runs one isolated instance per enrollment.

Your wiki is kept as files in the `dokuwiki` folder of your **home**, not in the enrollment. It survives stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same wiki.

**Deleted pages and media come back.** The copy in your home is never deleted from, so a page or media file you delete in DokuWiki is there again after the next start, with the content it had when it was last stored. To remove it for good, also delete its file in your home; see [What is kept, and what is lost](#what-is-kept-and-what-is-lost).

## Set up

1. Enroll in **base**. The enrollment asks for access to the `dokuwiki/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one DokuWiki instance at a time.
2. The form shows a **Wiki title**, an **Administrator name** (default `admin`) and a generated **Administrator password**. They are used the **first time** DokuWiki runs on your home folder. If the wiki is already set up, because you enrolled before or restarted, they are ignored and the existing title, users and passwords still apply. Save the password now: the platform keeps it as a secret and does not show it again. It is an application credential, not your UnitySVC API key.
3. Wait for the instance to become ready; a start takes a few seconds. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.** DokuWiki needs no setting for it.
4. Open the address and sign in with the administrator name and password.

## Use it

1. The start page does not exist yet: choose **Create this page**, write some text in [DokuWiki's markup](https://www.dokuwiki.org/wiki:syntax) and save. Link to a page that does not exist, for example `[[projects:roadmap]]`, and follow the link to create it; the part before the colon is a namespace (a folder).
2. **Old revisions** shows every saved version of a page and compares two of them. **Recent Changes**, **Sitemap** and the search box cover the whole wiki. **Media Manager** uploads images and files that pages can embed.
3. Under **Admin**:
   - **User Manager** adds people and puts them in groups. Set their password there: the wiki cannot send it by email.
   - **Access Control List Management** decides who may read, edit, create, upload and delete, per page or namespace. The wiki starts closed: `@ALL` (everyone, signed in or not) has no access and `@user` (signed-in users) may do everything. To publish a namespace, give `@ALL` read access to it.
   - **Configuration Settings** changes the title, language, start page, licence note and the rest.
   - **Extension Manager** installs plugins and templates from the DokuWiki repository. They are downloaded into your home folder and kept.
4. Change your own name, email address and password under **Update Profile**. The administrator's email address starts as the placeholder `admin@example.com`.

The [DokuWiki manual](https://www.dokuwiki.org/manual) describes the markup, the access control lists, the plugins and the remote API (off by default; turn it on in **Configuration Settings**).

## Authentication

DokuWiki checks every request itself. With the closed policy this recipe starts with, pages, media, the search and old revisions all need a sign-in; a visitor sees only the sign-in form. Visitors cannot register. Anyone who knows the instance address can reach the sign-in form, so keep the administrator password strong. UnitySVC adds no other gate.

A new DokuWiki is normally set up through its web installer (`install.php`), where the first visitor names the administrator and chooses the access policy, and it has no environment setting for either. This recipe runs that installer itself before the web server starts, on an address only the container can reach, with your administrator name and password, access control on, the closed policy and registration off; the instance does not start if that fails. The installer is therefore never open to a visitor, and afterwards it refuses to run because the configuration exists.

- **Email is not available.** The image has no mail server and this recipe configures none. **Set new password** ("Forgotten your password?") on the sign-in form therefore fails with an error, and so do change notifications and page subscriptions. An administrator sets a user's password in the User Manager. If you lose the only administrator password, stop the instance, remove `conf/users.auth.php`, `conf/acl.auth.php` and `conf/local.php` from `dokuwiki/` in your home and start again: the wiki is set up anew from the enrollment's parameters and keeps its pages and media, but loses its other users, access rules and settings. Remove all three files; the instance does not start with only some of them, because DokuWiki would run without access control.

## What is kept, and what is lost

The whole storage folder of the image is persistent: `conf/` (your settings, the users and their password hashes, the access control lists), `data/` (pages, media, every old revision, metadata and the search index) and `lib/` (plugins and templates you install). It is stored in `dokuwiki/` in your home, where you can see the pages as plain text files (`data/pages/<namespace>/<page>.txt`). The platform restores the files before DokuWiki starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **Files are copied, never deleted from your home.** DokuWiki deletes a page by removing its text file and noting the deletion in the page's history. The removed file stays in your home and is restored at the next start, so the page is back with the content it had when it was last stored, marked as an external edit in its history. The same holds for a deleted media file, for a page or namespace you rename or move with a plugin (the old one returns beside the new one), and for a plugin or template you uninstall. To remove something for good, delete it in DokuWiki and also delete its file under `dokuwiki/data/pages/`, `dokuwiki/data/media/` or `dokuwiki/lib/plugins/` in your home. Users, access rules and settings are lines in files that DokuWiki rewrites, so removing those lasts.
- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Signed-in users may have to sign in again after the instance restarts.
- The render cache, edit locks, temporary files and DokuWiki's own log files (`data/cache`, `data/locks`, `data/tmp`, `data/log`) are not stored; DokuWiki rebuilds them.
- Empty files, symbolic links and files over 1 GiB are not stored. DokuWiki does not need any of them: the image links its bundled plugins and templates into the folder again at every start, and uploads are limited to 128 MB. A plugin that relies on an empty file or a symbolic link inside its own folder may not survive a restart.
- The image copies its bundled pages (`wiki:welcome`, `wiki:syntax`, `wiki:dokuwiki` and `playground:playground`) into the folder at every start, so a change you make to those four pages is undone by a restart. Keep your own text on other pages.
- A file you add under `dokuwiki/` in your home while the instance is stopped is loaded at the next start; one added while it runs is loaded at the start after that.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `dokuwiki/` folder yourself when you no longer want the wiki.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check DokuWiki used about 35 MiB idle and under 100 MiB while serving several requests at once. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
