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

Images must already be built. A tag is accepted; use a digest to pin the image you tested. Check the target architecture. Compose service names must be DNS labels: lowercase letters, digits and hyphens.

Volume mounts provide scratch storage, not persistent storage. It survives a container restart but is lost when the instance is stopped or replaced, and counts against ephemeral-storage limits.

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

Do not rely on `${VAR}` placeholders or a built-in instance-key variable. Do not place `{{ params.NAME }}` in Compose or use the older Document `meta.environment` form.

`testing_defaults` provides sample parameter values for test tooling. The current v0.3.24 local runner does not apply channel bindings correctly; supply these values explicitly when checking Compose with Docker. See [the contribution checks](../CONTRIBUTING.md#check-your-work).

## Sizes and channels

Consult the [current sizes and rates](https://unitysvc.com/docs/sizes). A single-container channel can name one size, such as `"resources": "nano"`. A stack needs a complete per-service map, for example `"resources": {"web": "small", "redis": "nano"}`. Verify that the named sizes are active and appropriate for each service.

Offer separate channels for size choices or different parameter defaults. For example, `base` might use `nano` and `larger` might use `small`, where both sizes are suitable and available. Each channel declares its own parameters and environment; every channel uses the same Compose spec and the listing's bare `base_cost` price. Use a separate recipe for a different stack.

Record upstream minimums and observed CPU, memory and scratch-disk needs at startup and under the intended workload. Local Docker does not reproduce the platform's named-size limits, so report what you measured and what still needs platform verification.
