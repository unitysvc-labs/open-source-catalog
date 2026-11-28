# Container recipe reference

For the contribution steps and required pricing, start with [CONTRIBUTING.md](../CONTRIBUTING.md).

## The instance spec

An offering has one Compose instance spec, shared by all its channels. Set `"instance_spec": "compose.yaml"` for a local file, or reference an upstream file with an HTTPS commit permalink. Remote specs must be publicly accessible and no larger than **256 KiB**. Upload snapshots the bytes; later upstream changes require a new upload. The Document form can also pin those bytes with `meta.sha256`.

If the upstream file uses unsupported features, copy it into the recipe, adapt it and describe the changes in your PR.

### Compose support

The [core instance-spec validator](https://github.com/unitysvc/unitysvc-core/blob/main/src/unitysvc_core/instance_spec.py) defines the supported Compose subset. Run `usvc_seller specs validate` for the current rules. In particular:

| Behavior | Settings |
| --- | --- |
| Used by the platform | `image`, `command`, `entrypoint`, `environment`, container ports, `healthcheck`, `working_dir`, `user`, `read_only` and scratch-volume mounts |
| Ignored | Local names, restart policies, logging, labels, network declarations, `expose`, profiles, links and host port bindings |
| Ignored with important limitations | `env_file` values are not uploaded; `depends_on` does not establish startup order. Supply environment values through the channel and make services retry their dependencies. |
| Resource settings | The channel's named size controls resources. `deploy.resources` is ignored; `mem_limit` and `cpus` are rejected. |
| Unsupported | Builds, privileged/host access, bind mounts, Compose secrets/configs, and other keys rejected by the validator |

### Stacks: services that talk to each other

Each Compose service runs as its own pod. Two rules follow that Docker Compose does not have, so a stack that works under Docker can still fail on the platform:

- **Declare the port of every service another service connects to**, with `ports` (the container port alone, for example `- 5432`), even when it is never published. A service gets its name inside the instance only when it declares ports, and only declared ports are open between an instance's services. A database with no `ports` cannot be reached: its name does not resolve, and the application waits for it forever. `expose` is ignored and does not count.
- **There is no start order.** `depends_on` is ignored, so an application must wait for or retry its dependencies itself.

### Start-up time and `start_period`

A Compose `healthcheck` becomes the container's start-up and readiness check. The platform **restarts a container that has not passed its check by the end of `start_period`**, and an instance that is not ready within about three minutes fails. Start-up there is several times slower than under Docker on a workstation: the container is sandboxed and gets only its size's share of a core. Timings measured locally are therefore not a guide.

- Set `start_period` generously, up to the maximum of `120s`. A short one (20 or 30 seconds) is the usual reason a recipe that works locally never becomes ready on the platform: PostgreSQL's first initialisation alone took about 29 seconds there.
- A service with no `start_period` gets 60 seconds.
- If the first start cannot finish in two minutes on the chosen size (an application that installs or migrates itself at first start), choose a larger size: more CPU is the only way to shorten it. wallabag needs `small` for this reason, not for memory.
- After a failed start, wait about ten minutes before testing the same recipe again. The failed instance is still being removed, and a new test in that time is refused with `409 busy: the instance is still handling its stop request`, which hides the real failure.

Give each service its size in the channel's `resources` map, and name in `entries` only the service customers reach.

Images must already be built. A tag is accepted; use a digest to pin the image you tested. Check the target architecture. Compose service names must be DNS labels: lowercase letters, digits and hyphens.

A named volume is scratch storage by default. It survives a container restart but is lost when the instance is stopped or replaced, and counts against ephemeral-storage limits. To keep a volume's files between runs, persist it in the channel (below); the Compose file stays the same and runs unchanged under Docker.

### Persistent volumes

The channel's `volumes` says which named volumes of the Compose file persist, keyed by the volume's name. Persistence is the channel's offer, not the file's, so one Compose file can back a channel that persists a volume and another that does not.

```json
"volumes": {
  "data": {
    "type": "persist",
    "source": "{{ storage.path }}/data",
    "mode": "rw",
    "exclude": ["*-wal", "*-shm"]
  }
}
```

- The key must be a top-level named volume of the Compose file that a service mounts. `type` is `persist` (or `scratch`, the default); `source` is `{{ storage.path }}/<folder>` (the enrollment's own folder in the customer's storage, the default: the data goes away from the customer's view with the enrollment, and a new enrollment starts empty) or `{{ home.path }}/<folder>` (a folder of the customer's home: the data belongs to the customer, and a later enrollment of the service finds it, so allow one active enrollment per customer with `service_options.enrollment.limit_per_customer: 1`); `mode` is `rw` or `ro`; `exclude` lists globs left out both ways; `uid` and `gid` give the owner of the restored files, for an image that runs as a non-root user.
- The channel must ask the customer for the storage access it needs, in `customer_access_requests`: a required `service:storage` with `read` and `write` (`read` alone for `mode: ro`), or `service:home` with a `path` that covers the folder.
- Files are restored before the application starts, copied while it runs (about every 30 seconds) and once more when it stops. Copying only adds and replaces: nothing is deleted from storage, empty files, symbolic links and files over 1 GiB are not stored, and a crash can lose the last 30 seconds.
- An application that keeps a SQLite database in WAL mode should exclude `*-wal` and `*-shm`. Copying never deletes, so an earlier copy of a write-ahead file would be restored beside a newer database, and SQLite's documentation warns that mixing a database with a write-ahead file from another point in time can corrupt it.
- Say in `usage.md` what is kept, what is lost on a crash, and that changing a parameter that is only read at first start (for example an initial password) has no effect afterwards.

Validating a recipe that persists needs `unitysvc-core>=0.3.20`.

Public `entries` select a Compose service and container port. Customers reach the instance over HTTPS on port 443. The application handles access control; naming an entry does not add an authentication gate.

## Parameters and environment

Keep Compose literal. Declare enrollment parameters in each channel's `params.schema`, then map them to container variables in that channel's `environment`. Channel values override the same names in the Compose file; every named service must exist in the spec.

Do not add `.env.example`, `.env` files or seller-secret manifests. Configurable container settings belong in the recipe's channel parameters; local Docker checks use explicit test values.

For an application whose `gateway` container reads an `API_KEY` variable, the relevant channel fields are:

```json
{
  "environment": {
    "gateway": {"API_KEY": "{{ params.API_KEY }}"}
  },
  "params": {
    "schema": {
      "type": "object",
      "properties": {
        "API_KEY": {
          "type": "string",
          "title": "Application API key",
          "description": "Keep the generated key or supply your own. The application checks this credential.",
          "minLength": 12,
          "default": "{{ token_urlsafe(32) }}"
        }
      },
      "required": ["API_KEY"]
    },
    "testing_defaults": {"API_KEY": "local-test-key-only"}
  }
}
```

The default mechanism generates a parameter value; it is not an implicit platform credential. UnitySVC substitutes the saved parameter when starting the instance. The software must actually use the key and enforce authentication. Apply the same pattern to tokens, passwords and other settings, using formats supported by the application.

A parameter bound in `environment` needs a **non-empty** value: the platform treats an empty string as missing, so an instance whose enrollment (or `testing_defaults`) leaves one empty fails to start with `missing_parameter` and its connectivity test fails. Give an optional setting a harmless non-empty default, or leave it out of `environment`.

Do not rely on `${VAR}` placeholders or a built-in instance-key variable. Do not place `{{ params.NAME }}` in Compose or use the older Document `meta.environment` form.

`testing_defaults` provides sample parameter values for test tooling. The current v0.3.24 local runner does not apply channel bindings correctly; supply these values explicitly when checking Compose with Docker. See [the contribution checks](../CONTRIBUTING.md#check-your-work).

## Sizes and channels

Consult the [current sizes and rates](https://unitysvc.com/docs/sizes). A single-container channel can name one size, such as `"resources": "nano"`. A stack needs a complete per-service map, for example `"resources": {"web": "small", "redis": "nano"}`. Verify that the named sizes are active and appropriate for each service.

Offer separate channels for size choices or different parameter defaults. For example, `base` might use `nano` and `larger` might use `small`, where both sizes are suitable and available. Each channel declares its own parameters and environment; every channel uses the same Compose spec and the listing's bare `base_cost` price. Use a separate recipe for a different stack.

Record upstream minimums and observed CPU, memory and scratch-disk needs at startup and under the intended workload. Local Docker does not reproduce the platform's named-size limits, so report what you measured and what still needs platform verification.
