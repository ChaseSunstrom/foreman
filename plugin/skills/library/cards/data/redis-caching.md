---
name: redis-caching
title: Redis caching
area: data
tags: [redis, cache, ttl, stampede, eviction, invalidation]
detect: []
related: [redis, redis-locks, memcached, n-plus-one]
---
Cache-aside with Redis: TTL discipline, stampede control, eviction policy and invalidation.

## Verify
- `redis-cli INFO stats`: keyspace_hits and keyspace_misses give the hit ratio; evicted_keys must be 0 or explained.
- `redis-cli CONFIG GET maxmemory-policy`: allkeys-lru or allkeys-lfu for a pure cache; noeviction would fail writes when full.
- `redis-cli --scan --pattern 'user:*' | head`: key naming is consistent and scoped.
- `redis-cli TTL some:key`: positive value, not -1 (no expiry).

## Test first
Test the miss, hit, and invalidation paths with a fake loader counter.
```python
def test_second_read_hits_cache_and_update_invalidates(cache, repo):
    get_user(1); get_user(1)
    assert repo.loads == 1
    update_user(1, name="x")
    assert get_user(1).name == "x" and repo.loads == 2
```

## Do
- Cache-aside: read, on miss load and `SET key val EX ttl`. Always set a TTL, with random jitter (for example plus or minus 10 percent).
- Namespace and version keys: `v2:user:{id}`; bump the version to invalidate a whole class.
- Stop stampedes: a short `SET lock:key 1 NX EX 10` so one caller recomputes, or serve stale while refreshing.
- Cache negative results briefly (`null` marker, short TTL) to stop repeated misses on absent keys.
- Set `maxmemory` and `maxmemory-policy` explicitly; never rely on the default.
- Serialize compactly and consistently (JSON or msgpack with a version field).
- Prefer `UNLINK` over `DEL` for large keys; use `SCAN`, never `KEYS`, for pattern work.
- Treat Redis as disposable: the app must work, slower, when it is down.

## Avoid
- No TTL on cached values: memory grows until eviction or an outage. Always `EX`.
- Many keys sharing one TTL boundary: simultaneous expiry stampede. Add jitter.
- `KEYS *` in code: blocks the server. Use `SCAN` with COUNT.
- Caching per-user data under a shared key: data leak. Include the user or tenant id in the key.
- Updating the DB then the cache in a racy order: stale value wins. Delete the key after the DB commit.
- Giant values (MBs) and hot keys: latency spikes. Split or compress.
- Caching errors or partial results: cache only success.

## Review
- [ ] Every set has a TTL (with jitter).
- [ ] Key includes version and tenant or user scope.
- [ ] Miss path protected against stampede.
- [ ] Invalidation happens after commit.
- [ ] App degrades gracefully when Redis is unreachable.
