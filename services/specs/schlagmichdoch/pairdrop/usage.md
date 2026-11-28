# PairDrop Browser File and Text Transfer

This unofficial community recipe runs the upstream `ghcr.io/schlagmichdoch/pairdrop:v1.11.3` image, pinned by digest. PairDrop (Florian and contributors) publishes the software under [GPL-3.0](https://github.com/schlagmichdoch/PairDrop/blob/master/LICENSE). No author endorsement or support commitment is implied.

## First transfer

1. Enroll in **base**, start the instance and open its HTTPS address on both devices. No password or account is configured. Anyone with the address may connect; UnitySVC adds no application authentication gate.
2. If discovery does not find the other device, use **Pair devices**: show the six-digit code on one device and enter it on the other. Temporary public rooms are another upstream option. A proxy may group visitors under the same address, so recognize the receiving device before sending.
3. Select the receiving device, choose a small file, then accept it on the receiving device and save the download. Click a device's name to send text instead. PairDrop needs both browser pages open.

## Networking, privacy and limits

The page and signaling use HTTPS/WSS on port 443. Files normally travel directly between the browsers through WebRTC. PairDrop uses upstream STUN configuration to discover peers; some networks need a TURN relay that this recipe does not include. Enabling `WS_FALLBACK` helps a browser with no WebRTC API; it does not guarantee fallback for every failed ICE negotiation. If both devices support WebRTC but cannot connect, try another network or disable WebRTC in a dedicated browser to use the fallback.

In fallback mode the instance relays the transfer through its WebSocket connections and can see its contents; do not assume end-to-end encryption. Large fallback transfers can exceed the nano size's 512 MiB memory, and browsers also need memory for received files. Start with small files. No directory of uploaded files, account database or persistent server volume exists. Pairing information may live in your browser; clearing site data removes it. Restarting disconnects active transfers, which must be sent again.

## Cost and support

The **base** channel uses **nano**. Pay the current platform compute base rate for the time the instance runs, including idle time. Labs adds no markup and receives no payout. Stop the instance when finished. Consult the [upstream documentation](https://github.com/schlagmichdoch/PairDrop#readme) for application behavior; this recipe does not promise author support.
