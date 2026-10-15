---
name: redis
title: Redis
area: data
tags: [redis, cache, keyvalue, ttl, locks, queues]
detect: [dep:redis, dep:ioredis, dep:redis-py, dep:aioredis, dep:go-redis/redis, dep:redis-rs, dep:jedis, dep:lettuce-core, dep:StackExchange.Redis, dep:valkey]
related: [rabbitmq, kafka, query-tuning]
---
Redis as cache or fast store: every key gets a TTL policy, atomic commands, no blocking scans.

## Verify
- `redis-cli -u "$REDIS_URL" ping`: server reachable and auth works.
- `redis-cli -u "$REDIS_URL" --scan --pattern 'app:*' | head`: keys follow the prefix convention (SCAN is non-blocking).
- `redis-cli -u "$REDIS_URL" ttl app:key`: TTL is set (-1 means none, -2 means missing).
- `redis-cli -u "$REDIS_URL" info memory`: memory use and `maxmemory-policy` match the intent.

## Test first
Test against a real Redis (container), flush a unique prefix per test.
```python
def test_cache_expires(r):
    cache_set(r, "k", "v", ttl=1)
    assert r.ttl("app:k") > 0
    time.sleep(1.1)
    assert r.get("app:k") is None
```
Fails until the setter applies `EX`.

## Do
- Namespace keys (`app:entity:id`) and set a TTL with the write: `SET k v EX 60` or `SET ... NX EX`.
- Use atomic commands (`INCR`, `HINCRBY`, `SETNX`) or Lua/`MULTI` for compound updates.
- Take locks with `SET lock token NX PX ms` and release with a compare-token Lua script.
- Pipeline batched commands to cut round trips.
- Use `SCAN` with `COUNT`, never iterate with `KEYS` in production.
- Set `maxmemory` and an eviction policy (`allkeys-lru` for cache, `noeviction` for data you cannot lose).
- Use streams (`XADD`, `XREADGROUP`, `XACK`) for durable queues instead of lists when consumers must ack.

## Avoid
- `KEYS *`: blocks the single thread. Use `SCAN`.
- Keys without TTL in a cache: unbounded memory growth. Always expire.
- Releasing a lock with plain `DEL`: can free another holder's lock. Compare the token atomically.
- Read-modify-write in the app (`GET` then `SET`): lost updates. Use atomic commands or `WATCH`.
- Huge values or collections under one key: latency spikes and slow `DEL`. Split keys; use `UNLINK`.
- Treating Redis as the only copy with default persistence: data loss on restart. Enable AOF or keep the source of truth elsewhere.
- Cache stampede on expiry: add jitter to TTLs and a single-flight refill.
- Pub/Sub for work that must not be lost: messages are fire-and-forget. Use streams.

## Review
- [ ] Every cache write sets a TTL, with jitter for hot keys.
- [ ] Locks use token plus expiry and a safe release.
- [ ] No `KEYS`, unbounded `LRANGE`/`SMEMBERS` on big collections.
- [ ] Eviction policy matches how the data is used.
- [ ] Connection is pooled and timeouts are set.
