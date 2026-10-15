---
name: leader-election
title: Leader election
area: design
tags: [leader-election, consensus, leases, failover, coordination, singleton]
detect: []
related: [distributed-locks, health-checks, graceful-shutdown, multi-region, background-jobs]
---
Exactly one instance acts as leader at a time via a renewable lease; the leader must stop acting the moment it cannot renew.

## Verify
- `pytest -q -k leader`: failover, no-split-brain and step-down tests.
- `kubectl get lease -n NAMESPACE`: when using the Kubernetes Lease API, the holder identity and renew time are as expected.
- `git grep -nE "is_leader|leader\(\)" -- src`: every leader-only action re-checks leadership.

## Test first
Partition the leader from the store: it must step down before a second leader can act.
```python
def test_leader_steps_down_before_successor_acts(store, clock):
    a = Elector("a", store, lease=10, clock=clock); a.tick()
    b = Elector("b", store, lease=10, clock=clock); b.tick()
    assert a.is_leader and not b.is_leader
    store.partition("a")
    clock.advance(6); a.tick()
    assert not a.is_leader                   # steps down at half lease
    clock.advance(5); b.tick()
    assert b.is_leader
    assert not (a.is_leader and b.is_leader)
```

## Do
- Use an existing coordinator: Kubernetes Lease, etcd or ZooKeeper sessions, Consul sessions, or a DB row with an expiry. Do not hand-roll consensus.
- Renew at a fraction of the lease (about a third); the leader steps down if renewal is not confirmed within its own deadline, on a monotonic clock.
- Attach a fencing token (epoch) to leader actions so downstream rejects an old leader.
- Keep leader work small and idempotent; followers stay warm and ready to take over.
- Add jitter to election retries to avoid dueling candidates.
- Expose the current leader and epoch in metrics and logs.

## Avoid
- Checking leadership once at startup: a paused leader keeps acting. Re-check before each side effect.
- Lease shorter than worst-case pause (GC, network): flapping. Size the lease against measured pauses.
- Relying on synchronised wall clocks: use the store's expiry plus fencing.
- A singleton cron on every replica "because only one will win": use a lease or a DB lock.
- Even-sized clusters for the coordinator: no majority on split. Use an odd number.

## Review
- [ ] Uses an existing coordination primitive.
- [ ] Leader steps down on failed renewal.
- [ ] Downstream actions carry an epoch.
- [ ] Failover time measured against the lease.
