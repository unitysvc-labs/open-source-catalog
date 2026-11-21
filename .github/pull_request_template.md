## What this PR does

<!-- New recipe, change to an existing one, or catalog tooling? Name the service. -->

## Recipe checklist

<!-- Delete this section for changes that do not touch a recipe. -->

- [ ] **Who:** I am the upstream author / a community maintainer (unofficial unless the author takes part).
- [ ] **License:** OSI-approved, SPDX identifier `____`, upstream license linked.
- [ ] **Attribution:** the provider is the software's author, with their own homepage. No invented contact details, and nothing implies author support or endorsement.
- [ ] **Image:** documented upstream image and tag `____`, runs on the platform's supported architecture.
- [ ] **Pricing:** listing has `{"list_price": {"type": "base_cost"}}`; offering has `{"payout_price": {"type": "constant", "price": "0"}}`; no dollar prices, markups or surcharges.
- [ ] **Size:** the smallest size that works (`____`); how I checked: ____. Every service of a stack is accounted for.
- [ ] **Parameters:** `{{ params.NAME }}` bindings in the channel `environment`, declared in `params.schema` with descriptions, validation and `testing_defaults`; no fixed shared credentials.
- [ ] **Docs:** `usage.md` covers setup, authentication, a demo step, cost and stopping, and what is lost on stop.
- [ ] **Tests:** the `container_connectivity` preset; Docker check output below.
- [ ] No `service.json` added and no existing one edited.

## Checks

```
usvc_seller specs validate
usvc_seller specs format --check services
python scripts/check_channel_binding.py
```

<!-- Paste results, and the local Docker evidence for the recipe. -->
