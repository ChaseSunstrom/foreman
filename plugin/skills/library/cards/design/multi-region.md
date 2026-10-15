---
name: multi-region
title: Multi-region
area: design
tags: [multi-region, replication, failover, latency, data-residency, dr]
detect: []
related: [read-replicas, leader-election, crdts, health-checks, data-retention]
---
Choose active-passive or active-active per data class, state the RPO and RTO, and rehearse failover before you need it.

## Verify
- `dig +short SERVICE.example.com`: DNS answers match the expected active region.
- `curl -fsS https://REGION.example.com/healthz`: each region's health endpoint answers independently.
- `pytest -q -k "region or failover"`: routing, residency and write-conflict tests.

## Test first
Kill the primary region: writes must resume elsewhere with no acknowledged write lost beyond the stated RPO.
```python
def test_failover_preserves_acked_writes(cluster):
    acked = [cluster.write(k, k) for k in range(100)]    # returns after sync commit
    cluster.fail_region("eu")
    cluster.promote("us")
    assert all(cluster.read(k, region="us") == k for k in acked)
    assert cluster.write("new", 1)                       # accepts writes post-failover
    cluster.restore_region("eu")
    assert cluster.is_demoted_follower("eu")             # old primary does not resume writing
```

## Do
- Write down RPO and RTO per data class; derive the replication mode (sync, semi-sync, async) from them.
- Active-passive is simplest: one write region, replicas elsewhere, promotion runbook. Active-active needs conflict handling (CRDTs, per-record home region, or partition by tenant).
- Pin each tenant or user to a home region for writes; route others by latency for reads.
- Make cross-region calls idempotent with timeouts; never assume ordering across regions.
- Respect data residency: keep personal data in its region, and have logs and backups follow the same rule.
- Fence the old primary after failover so it cannot accept writes on return.
- Automate failover health decisions with hysteresis; practise game days and time them.
- Keep config, secrets and deploy pipelines regional so one region's outage cannot block rollouts in another.

## Avoid
- Split brain: two regions accept writes for one record. Use fencing and one writer per key.
- Async replication with a claim of zero data loss: RPO is the lag. Measure it.
- Sticky global singletons (one Redis, one queue) in one region: hidden single point of failure. Inventory shared dependencies.
- Untested failover: the runbook rots. Schedule drills.
- Cross-region synchronous calls in the request path: p99 doubles. Replicate or cache locally.

## Review
- [ ] RPO and RTO stated and measured.
- [ ] Single writer per record, with fencing.
- [ ] Residency constraints enforced.
- [ ] Failover drilled recently.
