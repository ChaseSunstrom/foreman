---
name: cache-invalidation
title: Cache invalidation
area: design
tags: [cache, invalidation, ttl, stampede, consistency, redis]
detect: []
related: [caching, read-replicas, event-driven, consistent-hashing, outbox-pattern]
---
Pick an invalidation strategy per entry type, bound staleness with a TTL, and stop races from writing stale values back.

## Verify
- `pytest -q -k cache`: staleness, race and stampede tests.
- `redis-cli --scan --pattern 'user:*' | head`: key naming is consistent and scoped (run only against a dev instance).
- `git grep -nE "cache\.(set|delete)" -- src`: every write path also invalidates or updates the cache.

## Test first
A slow reader must not overwrite a newer invalidation.
```python
def test_stale_fill_does_not_overwrite_invalidation(cache, db):
    db.set("u1", "old")
    fill = cache.begin_fill("u1")              # reader loads "old" from db
    value = db.get("u1")
    db.set("u1", "new"); cache.invalidate("u1")
    fill.commit(value)                          # late write of "old"
    assert cache.get("u1") in (None, "new")     # never "old"

def test_stampede_single_loader(cache, loader):
    run_concurrently(16, lambda: cache.get_or_load("hot", loader))
    assert loader.calls == 1
```

## Do
- Default to cache-aside: read, miss, load, set with a TTL. On write, update the DB first, then delete the key (not set it).
- Always set a TTL, with jitter, as the backstop for missed invalidations.
- Version keys (`user:1:v7`) or store a version in the value, and reject older fills.
- Collapse concurrent misses (single flight, lock or probabilistic early refresh) to stop stampedes.
- Cache negative results briefly, so missing keys do not hammer the DB.
- Publish invalidations from the write path through the outbox or CDC for multi-node and multi-service caches.
- Namespace keys by tenant and schema version so deploys can bust cleanly.

## Avoid
- Updating cache before the DB commit: a rollback leaves a phantom value. Write DB, then invalidate.
- Set on write from a concurrent writer: last writer wins out of order. Delete and let reads refill, or compare versions.
- No TTL: one missed event is stale forever. Add TTL.
- Same TTL on many keys: synchronized expiry stampede. Add jitter.
- Caching per-user data under a shared key: data leak. Include the identity in the key.

## Review
- [ ] Each cached entity has a documented invalidation path and TTL.
- [ ] Fill race handled by version or delete-after-write.
- [ ] Stampede protection on hot keys.
- [ ] Keys include tenant and user scope where relevant.
