# UnitySVC Open Source Catalog

Let people run your open-source project on their own [UnitySVC](https://unitysvc.com) instance, for a quick try, occasional use or long-term use. Submit a container recipe; [UnitySVC Labs](https://github.com/unitysvc-labs) reviews and publishes it. Customers pay the platform's compute base cost while their instances run. Labs adds no markup and receives no seller payout.

A recipe describes the containers, enrollment parameters and how to use the software.

## For authors

Choose the route that fits what you want to offer:

1. **Contribute to this catalog:** [submit a recipe](CONTRIBUTING.md). You need no seller account or hosting infrastructure. Labs approves and publishes it; you receive no payout and cannot attach additional services or paid support to Labs' listing.
2. **Publish your own at-cost services:** become a **Developer seller**. Maintain your own repository and customer relationships. Eligible container services go live when their tests and Developer policy checks pass. You cannot add a markup or receive payouts, but can support customers through Rooms.
3. **Sell commercial services:** apply for a **seller account with payouts**. Set your own prices and offer premium software, managed services or support. Rooms provides a place to discuss setup and support with customers.

For the first route, give your coding assistant [the recipe prompt](CONTRIBUTING.md#ask-your-coding-assistant) and an upstream project URL. It reads the project's documentation and drafts the recipe, descriptions and settings for your review.

To start selling, sign in at [UnitySVC](https://unitysvc.com), choose **Add a role → Become a seller**, and select Developer or submit a commercial seller application. Follow the [seller quick start](https://github.com/unitysvc/unitysvc-sellers/blob/main/docs/getting-started.md) to create an API key and publish from your repository.

Developer sellers who want to earn revenue must [contact support](https://unitysvc.com/support) for a seller-type change and review; there is no self-service conversion.

Community recipes are welcome alongside author submissions. We mark them as unofficial unless the author participates. Inclusion does not imply author endorsement or a promise of author support.

## For customers

1. Sign in at [UnitySVC](https://unitysvc.com) and add funds if needed.
2. Find the published service in the [catalog](https://unitysvc.com/services).
3. Enroll, choose a channel/size and configure its parameters, including any application keys or tokens.
4. Start the instance and follow its guide. Use it briefly or keep it running as long as you need.
5. **Stop the instance when finished.** Closing a browser tab does not stop it.

The application handles its own authentication. Stopping or replacing an instance loses its temporary storage; check the service's guide for what this means for messages, logins and other data.

### What it costs

You pay for runtime at the selected channel's [published compute rate](https://unitysvc.com/docs/sizes), with no Labs markup or seller payout. These recipes have no software subscription fee or extra Labs service charge. Rates depend on the size and can change.

Run an instance continuously or start and stop it on demand. Compute charges accrue while it runs, including idle time, and stop when the instance stops. Occasional use of larger software costs only the runtime you use, rather than a full month of continuous running.

At an illustrative rate of $300 per 30-day month, an hour costs about $0.42 and ten hours about $4.17. Use the current published rate for your chosen size.

A pricing update does not change an existing run's pinned price; the updated terms apply on its next start.

## Services

| Service | What you can run | Guide |
| --- | --- | --- |
| [`binwiederhier/ntfy-sh`](services/specs/binwiederhier/ntfy-sh) | Push notifications over HTTP, with mobile and streaming clients | [ntfy setup](services/specs/binwiederhier/ntfy-sh/usage.md) |
| [`kadxy/weixin-ilink-gateway`](services/specs/kadxy/weixin-ilink-gateway) | A Weixin iLink gateway with QR login, messaging and webhooks | [Weixin setup](services/specs/kadxy/weixin-ilink-gateway/usage.md) |

## Catalog pricing policy

Every listing uses `base_cost`, and every offering has an explicit zero payout. Each channel is charged at its own size's platform cost. [CONTRIBUTING.md](CONTRIBUTING.md#pricing) gives the required settings.

For recipe details, see the [container reference](docs/container-recipes.md). Repository layout, publication and tooling notes are in the [maintainer guide](docs/maintaining.md).
