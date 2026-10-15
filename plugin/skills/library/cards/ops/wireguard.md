---
name: wireguard
title: WireGuard
area: ops
tags: [wireguard, vpn, network, linux, keys]
detect: [file:wg*.conf]
related: [nftables, linux-hardening, dns, secrets-rotation]
---
WireGuard tunnels: one key pair per peer, tight AllowedIPs, handshakes checked rather than assumed.

## Verify
- `wg show`: peers, endpoints, last handshake and transfer counters.
- `wg show wg0 latest-handshakes`: a handshake within about two minutes proves the tunnel is live.
- `ping -c3 <peer tunnel ip>`: traffic crosses the tunnel.
- `ip route get <remote subnet>`: the route points at `wg0`, not the default path.
- `wg-quick strip wg0`: the config as the kernel will see it, with wg-quick-only keys removed.

## Test first
A tunnel test fails until a handshake happens and a packet returns.
```sh
set -e
ip link show wg0 >/dev/null
now=$(date +%s)
hs=$(wg show wg0 latest-handshakes | awk '{print $2}' | sort -n | tail -1)
[ $((now - hs)) -lt 180 ] || { echo "no recent handshake"; exit 1; }
ping -c2 -W2 10.8.0.1 >/dev/null
```
Run it as a monitoring probe too: a peer that stops handshaking is the early signal.

## Do
- Generate keys on the host that uses them: `wg genkey | tee private | wg pubkey > public`; `umask 077` first and keep the private key file at mode 600.
- Set `AllowedIPs` to exactly the peer's addresses (a /32 per client on the server); it is both routing table and ACL.
- Add `PersistentKeepalive = 25` on peers behind NAT so mappings stay open.
- Optionally add a `PresharedKey` per peer for post-quantum resistance in depth.
- Set `MTU` explicitly if you see stalls on large transfers (start near 1380 for double-NAT paths and test).
- Pair with a firewall: allow only the UDP `ListenPort` inbound, and filter what arrives on `wg0` like any untrusted interface.
- Enable at boot with `systemctl enable wg-quick@wg0`, and test a reboot.
- Rotate a peer by adding the new key, confirming a handshake, then removing the old one.

## Avoid
- Overlapping `AllowedIPs` between peers: the kernel routes to only one, and the other silently breaks. Keep each prefix unique.
- `AllowedIPs = 0.0.0.0/0` without a route and DNS plan: you lose SSH to the host. Test from a console, and exempt the endpoint route.
- Private keys in git or in the config checked into a repo: use a secrets store or `PostUp = wg set ... private-key <(...)` from a protected file.
- Judging health by the interface being up: UDP is stateless. Check `latest-handshakes`.
- Editing the config and expecting live change: run `wg syncconf wg0 <(wg-quick strip wg0)` or restart the unit.
- Forgetting `net.ipv4.ip_forward=1` on a gateway peer: handshakes work, traffic does not forward.

## Review
- [ ] Each peer has a unique key pair, and private keys are mode 600 and out of version control.
- [ ] `AllowedIPs` are minimal and non-overlapping.
- [ ] A handshake probe runs and alerts.
- [ ] The firewall allows only the WireGuard UDP port inbound.
- [ ] Key rotation steps are written down and were tried once.
