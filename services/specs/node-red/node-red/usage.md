# Node-RED Flow Automation

Each enrollment runs a private [Node-RED](https://nodered.org/) instance. Node-RED is a project of the [OpenJS Foundation](https://openjsf.org/), written by its contributors and released under the Apache-2.0 license; the provider of this service is its author. UnitySVC Labs lists the official `nodered/node-red` image (version 5.0.10, pinned by digest), and the platform runs one isolated instance per enrollment.

Your flows, their credentials, the settings file and the nodes you install are kept in the `node-red` folder of your **home**, not in the enrollment. They survive stopping the instance, and also removing it and enrolling again: a new enrollment starts a new instance at a new address, and it loads the same data.

## Set up

1. Enroll in **base**. The enrollment asks for access to the `node-red/` folder of your home (`service:home`, read and write). Approve it, or the instance does not start. You can run one Node-RED instance at a time.
2. The form shows an **Administrator name** (default `admin`) and a generated **Administrator password**. They are written into Node-RED's settings file the **first time** Node-RED runs on your data. If `node-red/settings.js` already exists in your home, because you enrolled before or restarted, the parameters are ignored and the existing name and password still apply. Save the password now: the platform keeps it as a secret and does not show it again. They are application credentials, not your UnitySVC API key.
3. Wait for the instance to become ready; a start takes a few seconds. Its address is `https://<enrollment-code>.<apps-domain>` (HTTPS, port 443); the instance details show it. **A new enrollment has a new address.** Node-RED needs no setting for it.
4. Open the address. The editor asks for the administrator name and password before it shows anything.

## Use it

1. Drag an **inject** node and a **debug** node from the palette onto the workspace, wire the first to the second, and press **Deploy**. Click the button on the inject node: the message appears in the **Debug** sidebar.
2. For an HTTP endpoint, wire **http in** (method GET, URL `/hello`) to a **function** or **template** node and then to **http response**, and deploy. `https://<instance>/hello` now answers. See "Authentication" below: such an endpoint is public.
3. Install more nodes under **Manage palette > Install**, for example a dashboard or a scheduler. A large package takes a minute to install on this size.
4. Flows can also be deployed over Node-RED's [admin API](https://nodered.org/docs/api/admin/). Get a token with the administrator's sign-in, then send it as a bearer token (a token is valid for seven days):

   ```bash
   curl -d 'client_id=node-red-admin&grant_type=password&scope=*&username=admin' \
        --data-urlencode 'password=<password>' https://<instance>/auth/token
   curl -H "Authorization: Bearer <token>" https://<instance>/flows
   ```

Only the instance's HTTPS address reaches Node-RED. Everything Node-RED serves on its own port works through it, including websocket nodes and dashboards. Nodes that open another listening port (**tcp in**, **udp in**, an MQTT broker node) cannot be reached from outside. Outgoing connections (HTTP requests, MQTT clients, databases) work. No mail server is provided; an email node needs your own SMTP account.

The [Node-RED documentation](https://nodered.org/docs/) and the [flow library](https://flows.nodered.org/) describe the nodes and the editor.

## Authentication

**The editor and the admin API require sign-in.** A stock Node-RED serves both to anyone who has the address, and the image has no environment setting for a password. This recipe therefore creates `settings.js` before Node-RED first starts: a copy of the image's default settings file with an `adminAuth` block for one administrator with full permissions, whose password is stored as a bcrypt hash made with the library Node-RED ships (the method of its [Securing Node-RED](https://nodered.org/docs/user-guide/runtime/securing-node-red) page). If that step fails the instance does not start. Without a valid sign-in, `/flows`, `/settings`, `/nodes` and the other admin routes answer `401`; the page at `/` only delivers the editor's own files, which then ask for the sign-in.

**What your flows serve is public.** An **http in** endpoint, a dashboard, and a websocket listener are part of your application and Node-RED serves them without a sign-in, as it does everywhere. Anyone who knows the address and the path can call them. To protect them all with one user name and password (HTTP Basic), set `httpNodeAuth` in `settings.js` as the Securing Node-RED page describes, or check a token inside the flow. UnitySVC adds no other gate.

**Changing the password or other settings.** Node-RED has no page for it; the settings file is the place. Stop the instance, edit `node-red/settings.js` in your home, and start it again: the file in your home is what Node-RED reads at the next start. For a new password, make a hash on any computer with Node.js (`npx node-red-admin hash-pw`) and put it in place of the `password` value inside `adminAuth`. Changing the **Administrator password** parameter does not do this. If you lose the password, delete `node-red/settings.js` from your home while the instance is stopped: the next start writes a new one from the parameters, but see the next paragraph about the credential key.

**Credentials stored in nodes** (for example the password of an MQTT broker) are encrypted in `flows_cred.json` with the `credentialSecret` in `settings.js`. The recipe generates a random one when it creates the file, and because the file lives in your home, the key stays the same across restarts and enrollments. It is not an enrollment parameter. If `settings.js` is deleted and created again, the key changes and Node-RED can no longer read the stored credentials; copy the `credentialSecret` line into the new file first, or enter the credentials again.

## What is kept, and what is lost

Node-RED's user directory is persistent: `settings.js`, the flows (`flows.json`), their encrypted credentials (`flows_cred.json`), the editor's sign-in sessions, your library, and the installed nodes (`package.json` and `node_modules`). They are stored in `node-red/` in your home, where you can see them in your files. The platform restores them before Node-RED starts, copies new and changed files back about every 30 seconds while it runs, and makes a last copy when the instance stops. Stopping therefore takes a moment longer while the copy finishes, and the instance shows as `draining`.

- **One instance at a time.** The folder belongs to your account, not to one enrollment, and two running instances would overwrite each other's copy. The service allows one active enrollment per account.
- A crash, or a node failure, can lose up to the last 30 seconds of changes, which may include a deploy just made. A normal stop loses nothing.
- **Context data is in memory.** With the default settings, flow and global context values are lost at every restart, as in any Node-RED. To keep them, enable the `localfilesystem` store under `contextStorage` in `settings.js`.
- **A node you remove comes back.** Files are copied, never deleted from your home. When you remove a node in the palette manager, its folder stays in `node-red/node_modules/` and Node-RED loads it again at the next start. To remove it for good, also delete that folder from your home while the instance is stopped. After updating a node, files that the new version no longer has stay in its folder.
- Empty files and symbolic links are not stored, and file permissions are not kept. `node_modules` has a few of each (the command links in `node_modules/.bin`, some empty placeholder files). In a local check that removed them, a scheduler node, the FlowFuse dashboard and the SQLite node (which has a compiled part) all loaded and worked after the restart. A node that needs one of those files at run time would fail to load; reinstall it from the palette manager.
- npm's download cache (`.npm/`) is not stored.
- Files over 1 GiB are not stored. The instance has 1 GiB of temporary disk, so keep the palette and any files your flows write small.
- Nothing is deleted from your home automatically, including when you cancel the enrollment. Delete the `node-red/` folder yourself when you no longer want the data.
- **Projects** (Node-RED's Git integration) are off, as they are by default upstream.

## Cost and size

The instance runs on the `nano` size (half a core, 512 MiB, 1 GiB of temporary disk) and you pay the platform's cost for it for as long as it runs, including idle time. In a local check Node-RED used about 65 MiB idle, about 100 MiB with a dashboard and a few flows running, and stayed under 300 MiB while installing large nodes. Labs adds no markup and receives no seller payout. The data in your home is not billed while that feature is in preview.
