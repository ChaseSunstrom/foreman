---
name: canary-releases
title: Canary releases
area: ops
tags: [canary, release, rollout, metrics, rollback, feature-flags]
detect: []
related: [blue-green-deploys, slos-alerting, load-balancing, distributed-tracing]
---
Send a small slice of traffic to the new version, compare its SLIs to baseline automatically, and abort on regression.

## Verify
- `for i in $(seq 200); do curl -s https://svc.example.com/version; done | sort | uniq -c`: the real traffic split matches the intended percentage.
- `curl -s https://svc.example.com/version -H 'X-Canary: always'`: a forced canary route works for testing.
- `kubectl rollout status deploy/app-canary --timeout=120s`: the canary pods became ready (Kubernetes).
- `promtool query instant http://localhost:9090 'sum(rate(http_requests_total{version="v2",code=~"5.."}[5m])) / sum(rate(http_requests_total{version="v2"}[5m]))'`: the canary's own error ratio.
- `kubectl rollout undo deploy/app`: the rollback command works on this deployment.

## Test first
Write the promotion gate as a script that compares canary to baseline and fails on regression, then feed it a bad build.
```sh
q() { promtool query instant http://prom:9090 "$1" | awk '{print $NF}'; }
base=$(q 'sum(rate(http_requests_total{version="v1",code=~"5.."}[5m]))/sum(rate(http_requests_total{version="v1"}[5m]))')
can=$(q  'sum(rate(http_requests_total{version="v2",code=~"5.."}[5m]))/sum(rate(http_requests_total{version="v2"}[5m]))')
awk -v b="$base" -v c="$can" 'BEGIN{exit !(c <= b*1.5 + 0.001)}' || { echo "canary worse"; exit 1; }
```
Deliberately ship a 500-on-startup build to staging and confirm the gate aborts the rollout.

## Do
- Step the weight (1%, 5%, 25%, 50%, 100%) with a hold at each step long enough to collect meaningful samples.
- Compare canary to baseline at the same time, not to last week; use ratios with minimum request counts.
- Gate on error rate, latency (p95 or p99), saturation, and one business metric.
- Make abort automatic and rollback faster than promotion.
- Tag every metric, log, and trace with the version label so the cohorts are separable.
- Keep sticky routing per user or session so one user does not bounce between versions.
- Use feature flags for risky behavior inside a version; the canary tests the build, the flag tests the feature.
- Keep schema changes backward compatible, since both versions share the database.

## Avoid
- A 1% canary on low traffic: no signal, false confidence. Set a minimum request count or lengthen the hold.
- Judging only by average latency or overall error rate: the canary's slice is diluted. Query by version label.
- Manual promotion by "looks fine": use gates that run unattended.
- Randomly splitting per request for stateful flows: users see mixed behavior. Route by user or session hash.
- Cleaning up the old version before 100% has soaked: no fast rollback. Keep it until the window ends.
- Canarying a migration that breaks the old version: rollback then corrupts. Use expand and contract.

## Review
- [ ] Rollout steps, hold times, and abort thresholds are defined in config.
- [ ] Metrics are labeled by version and queried per cohort.
- [ ] A known-bad build was used to prove the abort works.
- [ ] Rollback is automatic or one command, and rehearsed.
- [ ] Schema and queue changes are compatible with both versions.
