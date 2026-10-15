---
name: caching
title: Caching
area: design
tags: [cache, ttl, invalidation, stampede, redis, http-cache]
detect: [dep:redis, dep:ioredis, dep:cachetools, dep:django-redis, dep:memcached, dep:caffeine, dep:@upstash/redis]
related: [idempotency, zero-downtime-migrations, concurrency, retries-backoff]
---
Caches with explicit keys, TTLs, invalidation and stampede protection, tested for staleness and failure.

## Verify
- `redis-cli --scan --pattern 'app:v1:*' | head`: keys follow the namespaced, versioned pattern.
- `redis-cli ttl app:v1:user:42`: entries have a TTL (a result of -1 means it never expires).
- `redis-cli info stats | grep -E 'keyspace_(hits|misses)'`: the hit rate is measurable.
- `curl -si localhost:8080/products/1 | grep -iE 'cache-control|etag|vary'`: HTTP cache headers are correct.

## Test first
Prove the stale-read case and the miss path with an injected clock.
```python
def test_cache_expires_and_refetches(clock, cache, source):
    assert get_user(1) == "alice"; source.name = "alicia"
    assert get_user(1) == "alice"          # still cached
    clock.advance(seconds=61)               # TTL is 60
    assert get_user(1) == "alicia"
    assert source.calls == 2
```

## Do
- Build keys as `app:vN:entity:id[:variant]` and include everything the value depends on (tenant, locale, permissions).
- Always set a TTL, with jitter on bulk-loaded keys. Bump the `vN` for format changes.
- Choose per entry: cache-aside (read, miss, load, set), write-through, or write-around. Invalidate on write by deleting the key after the DB commit.
- Collapse concurrent misses (single-flight, lock, or per-key promise) so one loader runs.
- Cache negative results briefly, so missing IDs can't hammer the DB.
- Treat cache failure as a miss: catch errors and fall back to the source with a timeout.
- Set `Cache-Control` explicitly (`private` for user data, `public, max-age=...` for shared), with `ETag` and `Vary` as needed.
- Export hit, miss and eviction metrics, and set a maximum size or memory policy (`maxmemory-policy`).

## Avoid
- Keys without tenant or user dimensions: one user sees another's data. Include them or skip the cache.
- No TTL, relying on invalidation alone: one missed delete serves stale data forever.
- Deleting the key before the DB commit: a concurrent read refills it with the old value. Delete after commit.
- Caching errors or partial results as valid entries: store only successes (and deliberate negatives).
- Stampede on a hot key's expiry: add single-flight or early refresh.
- Python `functools.lru_cache` on methods or per-user functions in a web process: it holds `self`, is per-process and has no TTL. Use an explicit cache.
- `Cache-Control: public` on authenticated responses: shared proxies store them. Use `private` or `no-store`.

## Review
- [ ] Each key includes every input that changes the value, and has a TTL.
- [ ] Invalidation happens after commit, and a test covers staleness.
- [ ] Cache outage falls back to the source and doesn't fail requests.
- [ ] Hot-key stampede is handled, and hit rate is observable.
- [ ] HTTP cache headers are deliberate for public versus private data.
