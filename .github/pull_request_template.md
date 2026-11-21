## What this PR does

<!-- New recipe, change to an existing one, or catalog tooling? Name the service. -->

## Recipe checklist

<!-- Delete this section for changes that do not touch a recipe. -->

- [ ] **Who:** I am the upstream author / a community maintainer (unofficial unless the author takes part).
- [ ] **License:** OSI-approved, SPDX identifier `____`, upstream license linked.
- [ ] **Attribution:** the provider is the software's author, with their own homepage. No invented contact details, and nothing implies author support or endorsement.
- [ ] **Capabilities:** each entry is a matching official ID or `name | annotation`; the badge label and hover explanation accurately describe supported actions.
- [ ] **Image:** documented upstream image and tag `____`, runs on the platform's supported architecture.
- [ ] **Pricing:** listing has `{"list_price": {"type": "base_cost"}}`; offering has `{"payout_price": {"type": "constant", "price": "0"}}`; no dollar prices, markups or surcharges.
- [ ] **Size:** the smallest size that works (`____`); how I checked: ____. Every service of a stack is accounted for.
- [ ] **Parameters:** application keys/tokens are enrollment parameters with appropriate defaults, bound through the channel's `environment`; no usable credentials shared by customers.
- [ ] **Authentication:** documented which endpoints require credentials and how the application checks them; no platform authentication gate or built-in instance-key variable assumed.
- [ ] **Docs:** `usage.md` covers setup, authentication, a first-use step, cost and stopping, and what is lost on stop.
- [ ] **Shared guide:** the listing includes `{"$doc_preset": "container_description"}` alongside the application guide.
- [ ] **Tests:** the `container_connectivity` preset; manual Docker evidence uses explicit parameter values while the CLI binding issue remains open.
- [ ] No `service.json` added and no existing one edited.

## Checks

```
usvc_seller specs validate
usvc_seller specs format --check services
python scripts/check_channel_binding.py
```

<!-- Paste results and Docker evidence, with credentials redacted. Report tooling failures separately; see CONTRIBUTING.md#check-your-work. -->
