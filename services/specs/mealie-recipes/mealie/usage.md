# Mealie Recipe Manager and Meal Planner

Each enrollment runs a private [Mealie](https://mealie.io/) server. Mealie was created by [Hayden](https://github.com/hay-kot) and is maintained by the [mealie-recipes](https://github.com/mealie-recipes) contributors, and is released under the AGPL-3.0 license; the provider of this service is its author. UnitySVC Labs lists the official `ghcr.io/mealie-recipes/mealie` image (version v3.31.0, pinned by digest), and the platform runs one isolated instance per enrollment.

Your recipes, meal plans, users and pictures are kept in the `mealie` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

**Read "The first account" before you start the instance for the first time.** A new Mealie has a published default administrator sign-in until you replace it.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `mealie/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Mealie instance at a time.
2. The form has one setting, **Time zone** (default `UTC`). Mealie uses it for dates and for its daily tasks. Changing it later restarts the instance and keeps your data.
3. Wait for the instance to become ready; it takes well under a minute. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Open the address at once and replace the default account, as described next.

## The first account

Mealie has no setting for the first administrator's password, so this service has no password parameter. On an empty data folder Mealie creates one administrator with the sign-in upstream publishes in its documentation: email `changeme@example.com`, password `MyPassword`. While that account is unchanged, the sign-in page itself shows these two values and fills them in.

**Until you replace it, anyone who reaches the instance address can sign in as the administrator.** The address is not listed anywhere, but it is not a secret either. Do this as soon as the instance is ready:

1. Open the address. The sign-in page has the default email and password already filled in; sign in with them.
2. Mealie opens **First Time Setup**. Continue to **Account details** and enter your own email, user name, name and a password of your choice, then finish the remaining steps. Do not use the link that skips setup ("I'm already set up, just bring me to the homepage"): it leaves the default account as it is.
3. Sign out and sign in with your own email and password. The default sign-in is now refused, and the sign-in page no longer shows it.

If the default sign-in is refused on a first start with an empty `mealie/` folder, or you find recipes or users you did not create, somebody else got there first: stop the instance, delete the `mealie/` folder in your home and start again.

When the data already exists, because you enrolled before or restarted, nothing is created: your own account and password still apply. Change them in Mealie's user profile.

## Use it

- **Import a recipe.** Use the create menu's import option, paste the address of a recipe page and Mealie reads its title, ingredients, steps and picture. Sites that block automated requests or publish no recipe data may not import; write those in the editor instead.
- **Organise and plan.** Give recipes categories and tags, group them in cookbooks, put them on days in the meal planner and build shopping lists from their ingredients.
- **More users.** Public sign-up is off. Create users in the admin pages, or make an invitation link from your profile page and send it yourself. This service configures no mail server, so Mealie sends no invitation or password-reset email; the admin pages report email and the base URL as not configured, and this recipe has no settings for them.
- **REST API.** Create a token in your user profile under **API tokens**, then:

  ```bash
  curl -H "Authorization: Bearer <token>" https://<instance>/api/recipes
  curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/json" \
       -d '{"url": "https://example.com/a-recipe-page"}' \
       https://<instance>/api/recipes/create/url
  ```

  The interactive API reference is at `https://<instance>/docs`. The [Mealie documentation](https://docs.mealie.io) describes the features and backups.

Features that need another service you would have to configure, such as OpenAI-based import, OIDC or LDAP sign-in and email, are not set up by this recipe.

## Authentication

Mealie checks every request itself: the pages need your sign-in and the API needs a token; without one, `/api/recipes` answers 401. The sign-in page, the API reference at `/docs` and a few status routes such as `/api/app/about` answer without signing in. A sign-in lasts 48 hours, and five failed attempts lock an account for a day. Recipes are not readable without signing in unless you share one or make your household public in Mealie's settings. Anyone who knows the instance address can reach the sign-in page, so replace the default account first and keep your password strong. UnitySVC adds no other gate.

## What is kept, and what is lost

Mealie's data folder is persistent: the SQLite database (`mealie.db`), the generated secrets (they keep you signed in across restarts), recipe pictures and assets, user pictures, backups made in the admin pages and the log. They are stored in `mealie/` in your home, where you can see them in your files while the instance is stopped. The platform restores them before Mealie starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. A picture or backup Mealie removes can come back after a restart; delete it from your home while the instance is stopped if you want it gone.
- SQLite's temporary files (`*-journal`, `*-wal`, `*-shm`) are not stored. Mealie rebuilds them and this keeps the stored database consistent.
- Do not edit the files in `mealie/` while the instance is stopped: the next start restores them over what you changed.
- Empty files, symbolic links and files over 1 GiB are not stored; a backup archive larger than that is left out.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `mealie/` folder yourself when you no longer want the data.

## Cost and size

The instance runs on the `small` size (one core, 2 GiB, 5 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check Mealie used about 250 MiB idle, about 400 MiB after importing a recipe, parsing ingredients and making a backup, and reached about 460 MiB while it processed a 12-megapixel picture, which leaves too little room in the 512 MiB of the smaller `nano` size. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
