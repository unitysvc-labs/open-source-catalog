# code-server (VS Code in the browser)

Each enrollment runs a private [code-server](https://coder.com/docs/code-server), VS Code in the browser. code-server is written and maintained by [Coder](https://coder.com/) and contributors and is released under the MIT license; the provider of this service is its author. UnitySVC Labs lists the official `ghcr.io/coder/code-server` image (version 4.146.0, pinned by digest), and the platform runs one isolated instance per enrollment. The author was not asked to take part, and this listing does not mean that Coder endorses or supports it.

Your project files are kept in the `code-server/project` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it opens the same files.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `code-server/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one instance at a time.
2. The form shows a generated **Sign-in password**. Keep it or enter your own (at least 12 characters), and save it; it is also shown in the enrollment's instance details. It is an application password, not your UnitySVC API key.
3. Wait for the instance to become ready. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Open the address, enter the password, and VS Code opens on the `project` folder.

## First use

Create a file in the explorer, or open the terminal (**Terminal > New Terminal**) and work as in any shell:

```bash
cd ~/project
git clone https://github.com/<you>/<repo>.git
```

The terminal starts in `/home/coder/project`, runs as the user `coder`, and has `git` and `curl`. You can install extensions from the Open VSX registry in the Extensions view. Microsoft's own Marketplace is not available, so some extensions you know from desktop VS Code are missing. The Chat view needs a GitHub Copilot sign-in of your own; nothing here provides one.

## Authentication, and what it protects

code-server's sign-in page asks for the password, and a wrong password is refused ("Incorrect password"). In a local check about ten wrong attempts in a row were all simply refused, with no lockout visible, so pick a long password and keep the generated one if you are unsure. Once signed in, you reach a **full shell in the container**: the editor can read and change every file there, run any program, and open network connections. The user is `coder` (uid 1000) and the container is not privileged, but the image gives `coder` passwordless `sudo`, so inside the container you are effectively root. Anyone who has the password has that power, so treat it like a root password, never reuse one, and do not put your other passwords or tokens into the container unless you accept that.

Because the editor is a program runner, the container can reach whatever the platform allows an instance to reach, including the internet. Outbound traffic from it is billed and attributed to you, and so is anything you or an extension runs. The platform adds no sign-in in front of the instance: anyone who knows the address reaches the sign-in page.

## What is kept, and what is lost

Only the `project` folder (`/home/coder/project`) is kept. The platform restores it before code-server starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- **Not kept:** editor settings, installed extensions, shell history, the global git configuration, packages installed outside the project, and everything else outside `project`. They are lost when the instance stops or is replaced, and survive only a container restart. Install extensions again, or keep tools inside `project`.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing.
- Files are copied, never deleted from your home. A file you delete in the editor can come back after a restart. Commit your work to git and push it elsewhere; do not treat this folder as your only copy.
- Files over 1 GiB are not stored. Empty files and symbolic links are not stored either, which affects what a project contains: an empty `__init__.py` or `.gitkeep`, and the links in a Python virtual environment or `node_modules/.bin`, are missing after a restore. Re-create those environments after a restart (`npm ci`, `python -m venv`), or keep them outside the project.
- The instance also has temporary disk (1 GiB on the `nano` size; see the platform's size table for `small`), shared by the project, the extensions and caches, and everything you install. A full disk stops the instance from writing.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `code-server/` folder yourself when you no longer want the files.

## Cost and size

The instance runs on the `small` size (1 core, 2 GiB) and you pay the platform's cost for it for as long as it runs, including idle time and while no browser tab is open. In a local check the server used about 125 MiB with no browser connected, and between 350 MiB and about 890 MiB with the editor open, a terminal running and a file open; it needed more than the 512 MiB of `nano`. Builds, language servers and test runs you start in the terminal use memory too. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
