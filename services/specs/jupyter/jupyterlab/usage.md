# JupyterLab Notebooks

Each enrollment runs a private [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/), the notebook environment of [Project Jupyter](https://jupyter.org). JupyterLab and the [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/) images are written and maintained by the Project Jupyter contributors and are released under the BSD 3-Clause license; the provider of this service is its author. UnitySVC Labs lists the official `quay.io/jupyter/minimal-notebook` image (tag `2026-11-23`, pinned by digest: JupyterLab 4.6.6, Jupyter Server 2.21.1, Python 3.13), and the platform runs one isolated instance per enrollment. The author was not asked to take part, and this listing does not mean that Project Jupyter endorses or supports it.

Your notebooks and files are kept in the `jupyterlab` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it opens the same files.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `jupyterlab/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one instance at a time.
2. The form shows a generated **Access token**. Keep it or enter your own (at least 16 characters), and save it now: the platform keeps it as a secret and does not show it again. It is an application credential, not your UnitySVC API key. Changing it later restarts the instance, and the new token applies from then on.
3. Wait for the instance to become ready; it starts in a few seconds. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.**
4. Open the address, enter the token in **Password or token**, and JupyterLab opens on your work folder.

## First use

1. In the launcher, choose **Notebook > Python 3**. Type `print(6 * 7)` in the first cell and press Shift+Enter; the kernel runs it in the container and shows `42`.
2. Save the notebook (Ctrl+S). It is written to the work folder, `/home/jovyan/work`, which is the folder the file browser shows.
3. The image is the small "minimal" one: Python, JupyterLab, `pip`, `mamba`, `git`, `curl` and a text editor, without the scientific libraries. Install what you need from a notebook cell or from a terminal (**File > New > Terminal**):

   ```
   %pip install pandas matplotlib
   ```

   Installed packages are **not** kept when the instance stops (see below). Keep a `requirements.txt` in the work folder and run `pip install -r requirements.txt` after each start.

The terminal and the kernels run as the user `jovyan` (uid 1000, group `users`), with no `sudo`: you can install Python and conda packages, but not system packages with `apt`.

To call the Jupyter Server REST API, send the token in a header:

```bash
curl -H "Authorization: token <token>" https://<instance>/api/contents
```

## Authentication, and what it protects

Jupyter Server checks every request itself. Without the token, `/` leads to the sign-in page, and the REST API, the kernels and the terminals answer `403`; a wrong token is refused. Only the sign-in page, its static files and `/api` (which returns the server version) answer without it. The token is the only credential: setting a separate password on the sign-in page is switched off, because it would be stored outside the work folder and lost on stop. A link of the form `https://<instance>/lab?token=<token>` also signs in; do not share such a link, since it contains the token.

Once signed in, you can **run any code in the container**: notebooks and the terminal can read and change every file there, start any program, and open network connections. Anyone who has the token has that power, so treat it like a password to a shell, never reuse one, and do not put your other passwords or keys into notebooks unless you accept that. The container is not privileged and has no `sudo`.

The container can reach whatever the platform allows an instance to reach, including the internet. Outbound traffic from it is billed and attributed to you, and so is anything a notebook or an installed package runs. The platform adds no sign-in in front of the instance: anyone who knows the address reaches the sign-in page.

## What is kept, and what is lost

Only the work folder (`/home/jovyan/work`) is kept, in `jupyterlab/` in your home, where you can see the files while the instance is stopped. The platform restores it before JupyterLab starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- **Not kept:** packages installed with `pip`, `mamba` or `conda`, JupyterLab extensions and settings (theme, shortcuts), running kernels and their variables, open terminals, shell history, the git configuration in the home directory, and every file outside the work folder. They are lost when the instance stops or is replaced, and survive only a container restart. Install packages again after a start, and save anything you want to keep inside the work folder.
- A crash, or a node failure, can lose up to the last 30 seconds of changes. A normal stop loses nothing that was saved; unsaved notebook edits and kernel state are lost on any stop.
- Files are copied, never deleted from your home. A notebook or file you delete in JupyterLab can come back after the instance is stopped and started. Delete it from the `jupyterlab/` folder of your home as well, while the instance is stopped.
- Empty files and symbolic links are not stored. A new empty text file disappears on the next start unless you put something in it, and so do an empty `__init__.py` or `.gitkeep`. A Python virtual environment or a conda environment created inside the work folder contains symbolic links and does not come back complete; re-create environments after a start instead of storing them.
- Files over 1 GiB are not stored. Keep large datasets elsewhere and download them when needed.
- The instance also has temporary disk (5 GiB on the `small` size), shared by the packages you install, caches and the work folder. A full disk stops the instance from writing.
- Do not edit the files in `jupyterlab/` while the instance is running: the next copy from the instance replaces what you changed.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `jupyterlab/` folder yourself when you no longer want the files.

## Cost and size

The instance runs on the `small` size (one core, 2 GiB of memory, 5 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time and while no browser tab is open. In a local check the server used about 75 MiB idle and about 145 MiB with one empty Python kernel; after `pip install pandas matplotlib` and a 76 MiB data frame it used about 640 MiB, and the same steps filled the 512 MiB of the smaller `nano` size. Each running kernel holds its data in memory until you shut it down (**Kernel > Shut Down Kernel**), and a kernel that needs more memory than the instance has is stopped by the platform. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
