---
name: blue-green-deploys
title: Blue-green deploys
area: ops
tags: [deploy, blue-green, rollback, release, zero-downtime, migrations]
detect: []
related: [canary-releases, load-balancing, database-failover, runbooks]
---
Run two identical environments, verify the idle one, switch traffic atomically, and keep the old one hot for instant rollback.

## Verify
- `curl -fsS https://green.internal.example.com/healthz`: the idle environment is healthy before the switch.
- `curl -fsS https://green.internal.example.com/version`: it runs the intended build id.
- `curl -s -o /dev/null -w '%{http_code}\n' https://svc.example.com/healthz`: production answers after the switch.
- `kubectl get svc app -o jsonpath='{.spec.selector}'`: which color the Service selects (Kubernetes).
- `for i in $(seq 50); do curl -s https://svc.example.com/version; done | sort | uniq -c`: all traffic lands on one version after cutover.

## Test first
Make the smoke suite run against green before any traffic moves, and make the rollback a tested command.
```sh
set -e
BASE=https://green.internal.example.com
curl -fsS "$BASE/healthz"
[ "$(curl -fsS "$BASE/version")" = "$BUILD_ID" ]
curl -fsS -X POST "$BASE/api/orders" -d @fixtures/order.json -H 'Idempotency-Key: smoke-1' >/dev/null
```
Then time the switch and the switch back in staging; both must finish in seconds with no failed requests.

## Do
- Make the switch one step: a load balancer target, a router weight, a Service selector, or a DNS alias with a low TTL.
- Warm green first (caches, connection pools, JIT) and run smoke tests with synthetic traffic.
- Keep database changes backward compatible across both versions: expand, deploy, migrate data, then contract in a later release.
- Drain connections on blue rather than cutting them; keep it running through the observation window.
- Watch error rate, latency, and key business metrics for a defined window before decommissioning blue.
- Automate rollback to the same one-step switch, and rehearse it.
- Share external dependencies (queues, caches) carefully: both colors may consume at once, so make consumers idempotent.
- Stamp the build id in `/version` and in logs, so you know which color served each request.

## Avoid
- A destructive migration in the same release as the switch: rollback is impossible. Use expand and contract in separate releases.
- Decommissioning blue immediately: no way back. Hold it until the observation window passes.
- Sessions pinned in blue's memory: users are logged out at cutover. Externalize sessions.
- Both colors running schedulers or cron: jobs run twice. Run singletons on one color, or use leader locks.
- DNS-based switching with a high TTL: part of the world stays on blue for hours. Switch at the load balancer, or lower the TTL ahead.
- Skipping smoke tests on green because it "is identical": config and secret drift is the usual cause of failure. Test it.

## Review
- [ ] Green passes health and smoke tests before traffic moves.
- [ ] The migration is compatible with the previous version.
- [ ] Rollback is a single rehearsed command.
- [ ] Observation window and metrics are defined, with owners.
- [ ] Singleton jobs and consumers are safe with two live colors.
