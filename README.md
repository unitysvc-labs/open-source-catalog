# Open Source Containers for the UnitySVC Compute Cloud

Let people try your open-source project without setting up a server. Submit a container recipe; [UnitySVC Labs](https://github.com/unitysvc-labs) reviews and publishes it. Customers run their own instances and pay the platform's compute base cost. Labs adds no markup and receives no seller payout.

A recipe describes the containers, enrollment parameters and steps to try the software.

## For authors

Choose the route that fits what you want to offer:

1. **Share a demo:** [contribute a recipe](CONTRIBUTING.md). You need no seller account or hosting infrastructure. Labs approves and publishes it; you receive no payout and cannot attach additional services or paid support to Labs' listing.
2. **Publish your own at-cost services:** become a **Developer seller**. Maintain your own repository and customer relationships. Eligible container services go live when their tests and Developer policy checks pass. You cannot add a markup or receive payouts, but can support customers through Rooms.
3. **Sell commercial services:** apply for a **seller account with payouts**. Set your own prices and offer premium software, managed services or support. Rooms provides a place to discuss setup and support with customers.

To start selling, sign in at [UnitySVC](https://unitysvc.com), choose **Add a role → Become a seller**, and select Developer or submit a commercial seller application. Follow the [seller quick start](https://github.com/unitysvc/unitysvc-sellers/blob/main/docs/getting-started.md) to create an API key and publish from your repository.

Developer sellers who want to earn revenue must [contact support](https://unitysvc.com/support) for a seller-type change and review; there is no self-service conversion.

Community recipes are welcome alongside author submissions. We mark them as unofficial unless the author participates. Inclusion does not imply author endorsement or a promise of author support.

## For customers

1. Sign in at [UnitySVC](https://unitysvc.com) and add funds if needed.
2. Find the published service in the [catalog](https://unitysvc.com/services).
3. Enroll, choose a channel/size and configure its parameters, including any application keys or tokens.
4. Start the instance and follow the service's guide to try the software.
5. **Stop the instance when finished.** Closing a browser tab does not stop it.

The application handles its own authentication. Stopping or replacing an instance loses its temporary storage; check the service's guide for what this means for messages, logins and other data.

### What it costs

You pay for runtime at the selected channel's [published compute rate](https://unitysvc.com/docs/sizes), with no Labs markup or seller payout. Start an instance when you need it and stop it to end that run's compute charges. Rates depend on the size and can change.

A pricing update does not change an existing run's pinned price; the updated terms apply on its next start.

## Services

| Service | What you can try | Guide |
| --- | --- | --- |
| [`binwiederhier/ntfy-sh`](services/specs/binwiederhier/ntfy-sh) | Push notifications over HTTP, with mobile and streaming clients | [ntfy setup](services/specs/binwiederhier/ntfy-sh/usage.md) |
| [`kadxy/weixin-ilink-gateway`](services/specs/kadxy/weixin-ilink-gateway) | A Weixin iLink gateway with QR login, messaging and webhooks | [Weixin setup](services/specs/kadxy/weixin-ilink-gateway/usage.md) |

## Catalog pricing policy

Every listing uses `base_cost`, and every offering has an explicit zero payout. Each channel is charged at its own size's platform cost. [CONTRIBUTING.md](CONTRIBUTING.md#pricing) gives the required settings.

For recipe details, see the [container reference](docs/container-recipes.md). Repository layout, publication and tooling notes are in the [maintainer guide](docs/maintaining.md).
