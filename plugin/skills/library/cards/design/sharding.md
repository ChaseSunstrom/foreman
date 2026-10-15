---
name: sharding
title: Sharding
area: design
tags: [sharding, partitioning, database, shard-key, scaling, routing]
detect: []
related: [consistent-hashing, read-replicas, multi-tenancy, zero-downtime-migrations, multi-region]
---
Split data across databases by a shard key chosen so most queries touch one shard; plan the resharding path before you need it.

## Verify
- `pytest -q -k shard`: routing, cross-shard and migration tests.
- `git grep -nE "shard_for|ShardRouter" -- src`: all data access resolves the shard through one router.
- `psql -c "select pg_size_pretty(pg_database_size(current_database()))"`: run per shard to compare skew.

## Test first
Pin routing determinism and that every row is reachable after a split.
```python
def test_routing_is_stable_and_complete(router, shards):
    ids = range(1000)
    first = {i: router.shard_for(i) for i in ids}
    assert first == {i: router.shard_for(i) for i in ids}
    for i in ids: shards[first[i]].insert(i)
    router.add_shard("s3"); migrate(router, shards)
    assert all(shards[router.shard_for(i)].has(i) for i in ids)
    assert sum(len(s) for s in shards.values()) == 1000    # nothing duplicated or lost
```

## Do
- Shard late: first try indexes, caching, read replicas and partitioned tables on one node.
- Choose a key with high cardinality that appears in most queries (tenant id, user id). Keep related rows together.
- Use a directory (lookup table) or consistent hashing, not `id % N`, so shards can be added.
- Use globally unique ids (UUIDv7, ULID, snowflake) not per-shard auto-increment.
- Keep transactions single-shard; for cross-shard writes use sagas and idempotent steps.
- Resharding: dual-write or copy plus catch-up, verify counts and checksums, flip the route, then delete.
- Run cross-shard reads as scatter-gather with limits and timeouts, or build a separate read model.

## Avoid
- Sharding by timestamp or sequential id: one hot shard. Hash a high-cardinality key.
- Cross-shard joins in request paths: slow and fragile. Denormalise or precompute.
- Hard-coded shard count in code: resharding becomes a rewrite. Keep it in routing config.
- Per-shard schema drift: run migrations through one tool across all shards and track versions.
- Forgetting a hot tenant: one key can swamp a shard. Support moving or splitting a single tenant.

## Review
- [ ] Single router; no ad hoc shard math.
- [ ] Ids unique across shards.
- [ ] Rebalance procedure tested with verification.
- [ ] Cross-shard operations bounded.
