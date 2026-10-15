---
name: read-replicas
title: Read replicas
area: design
tags: [replication, database, replica-lag, read-scaling, consistency, routing]
detect: []
related: [cqrs, caching, sharding, multi-region, optimistic-locking]
---
Route reads that tolerate staleness to replicas, and keep read-your-writes and transactional reads on the primary.

## Verify
- `psql -c "select now() - pg_last_xact_replay_timestamp()"`: run on a Postgres replica; replay lag.
- `psql -c "select pg_is_in_recovery()"`: confirms you are on a replica (true) or primary (false).
- `pytest -q -k replica`: routing and lag-fallback tests.

## Test first
After a write, the same user's next read must see it even while the replica lags.
```python
def test_read_your_writes_with_lagging_replica(primary, replica, router):
    replica.freeze()                                   # stop applying changes
    router.write(user=1, sql="insert into notes values (1, 'hi')")
    assert router.read(user=1, sql="select body from notes where id=1") == "hi"
    assert router.last_target == "primary"             # pinned after write
    assert router.read(user=2, sql="select body from notes where id=1") is None
    assert router.last_target == "replica"             # others stay on replica
```

## Do
- Make routing explicit: a read-only session or decorator, defaulting to primary; opt reads into the replica.
- After a write, pin that session to the primary for a short window, or carry the write's LSN or version and use a replica only once it has caught up.
- Never read from a replica inside a transaction that writes, or for decisions like balance checks and uniqueness.
- Monitor lag and eject a replica above a threshold; fall back to primary instead of serving very stale data.
- Handle replica failure by retrying on another replica or the primary.
- Size the primary for fallback load if replicas drop.

## Avoid
- Read after write on a replica: users miss their own changes. Pin to primary or wait for LSN.
- Assuming lag is small: it spikes during bulk writes and long queries. Alert and bound it.
- Long analytic queries on a replica with conflict cancellation: they get killed on busy primaries. Use a dedicated replica with tuned settings.
- Round robin across replicas with different lag: results go backwards in time. Use sticky sessions per user.
- Using replicas for the check in check-then-write: races. Check on the primary.

## Review
- [ ] Default route is primary; replica reads are explicit.
- [ ] Read-your-writes handled.
- [ ] Lag monitored with a fallback.
- [ ] No writes or decisions depend on replica data.
