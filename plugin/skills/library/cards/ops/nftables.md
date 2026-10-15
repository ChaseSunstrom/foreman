---
name: nftables
title: nftables
area: ops
tags: [firewall, nftables, linux, network, security]
detect: [file:*.nft, file:nftables.conf]
related: [linux-hardening, wireguard, load-balancing]
---
nftables rulesets: default-drop inbound, stateful accept, atomic loads, checked before they are applied.

## Verify
- `nft -c -f /etc/nftables.conf`: syntax and semantics check without applying.
- `nft list ruleset`: the live rules, in order, with chain policies.
- `nft list chain inet filter input`: one chain, with the policy visible.
- `nft -a list ruleset`: rule handles, needed for `nft delete rule`.
- `ss -tlnH`: listeners the ruleset must account for.

## Test first
Prove the default is drop before adding allows: from another host, a port scan must show only the intended ports.
```sh
nft -c -f ./fw.nft                       # must exit 0
# on a test host or netns:
nft -f ./fw.nft
nc -zv -w2 $HOST 22   && echo "ssh open (expected)"
nc -zv -w2 $HOST 5432 && { echo "db exposed"; exit 1; }
```
Keep the file in the repo and run the check in CI; test lockout recovery with a timed rollback (below).

## Do
- Use the `inet` family so one table covers IPv4 and IPv6.
- Write `type filter hook input priority 0; policy drop;`, then `ct state established,related accept`, `ct state invalid drop`, `iif lo accept`.
- Accept ICMP and ICMPv6 selectively; IPv6 breaks without neighbor discovery (`icmpv6 type { nd-neighbor-solicit, nd-neighbor-advert, nd-router-advert } accept`).
- Name sets for addresses and ports (`set admins { type ipv4_addr; flags interval; }`) instead of repeating rules.
- Load the whole file atomically with `nft -f`, starting with `flush ruleset` only when the file is the complete truth.
- Rate-limit new SSH connections with `limit rate` or a meter, and log drops with a prefix and a rate limit.
- Remote change safety: `nft -f new.nft; sleep 60; nft -f last-good.nft &` style rollback, or `at`, cancelled after you confirm access.

## Avoid
- A drop policy loaded before the SSH accept: you lock yourself out. Order accepts first in the same atomic file and keep a timed rollback.
- Mixing iptables and nftables rules on one host: packets hit both and debugging is guesswork. Pick one and remove the other.
- Forgetting `ct state established,related`: replies get dropped. Add it first.
- Forwarding or NAT rules without `net.ipv4.ip_forward=1` in a sysctl drop-in: rules look right but nothing moves.
- `flush ruleset` in a file that does not define everything (Docker, libvirt, or fail2ban tables vanish): scope flushes to your own table.
- Unlimited `log` rules: they fill the journal during a scan. Add `limit rate 5/minute`.

## Review
- [ ] `nft -c -f` passes in CI.
- [ ] Input and forward chains have `policy drop`, with explicit accepts.
- [ ] IPv6 is covered by the same rules.
- [ ] The ruleset persists (`nftables.service` enabled) and reloads cleanly.
- [ ] A rollback path existed for the last remote change.
