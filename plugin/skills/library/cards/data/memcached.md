---
name: memcached
title: Memcached
area: data
tags: [memcached, cache, ttl, eviction, hashing, slabs]
detect: [dep:pymemcache, dep:python-memcached, dep:memjs]
related: [redis-caching, redis, n-plus-one]
---
Memcached as a pure cache: key rules, TTLs, consistent hashing, CAS, and eviction and stampede behavior.

## Verify
- `echo stats | nc localhost 11211`: get_hits, get_misses, evictions, curr_connections and bytes.
- `echo "stats slabs" | nc localhost 11211`: slab class usage; one class full while others idle explains evictions.
- `printf 'set k 0 60 2\r\nhi\r\nget k\r\nquit\r\n' | nc localhost 11211`: store and read work with a 60 second TTL.
- `memcached -h | head -1`: the installed server version.

## Test first
Test the cache-aside path and key hygiene.
```python
def test_cache_aside_and_key_limits(mc, repo):
    key = cache_key("user", 1)
    assert len(key) <= 250 and " " not in key
    get_user(1); get_user(1)
    assert repo.loads == 1
```

## Do
- Keep keys at most 250 bytes with no spaces or control characters; hash long or user-supplied parts (`user:v3:` plus a sha256 hex).
- Always pass a TTL; remember a value over 30 days is treated as an absolute Unix timestamp.
- Use client-side consistent hashing (ketama) across nodes so a node change remaps few keys.
- Use `get_many` and `set_many` (multi-get) to cut round trips.
- Use `cas` for read-modify-write on shared counters, or `incr` and `decr` for atomic counters.
- Version keys for invalidation (`v2:`), since flush-all is blunt.
- Cap value size at 1 MB by default; compress or split bigger payloads.
- Add jitter to TTLs and use an `add`-based lock to stop stampedes on hot keys.

## Avoid
- Treating it as durable storage: restarts and evictions lose everything. Keep the source of truth elsewhere.
- Caching without a failure path: a down node must mean slower, not broken. Catch timeouts quickly with short socket timeouts.
- Keys built from raw user input: spaces break the text protocol and can inject commands. Hash or encode.
- `flush_all` in production code paths: wipes every tenant. Use versioned keys.
- Unbounded key variety with no TTL: evicts hot entries. Set TTLs.
- Sharing one instance with no key prefix between apps: collisions. Namespace.
- No auth or network exposure of port 11211: abused for amplification and data access. Bind to a private interface, use SASL or network policy.

## Review
- [ ] Keys are namespaced, versioned, length-safe.
- [ ] TTL and jitter on every set.
- [ ] Timeouts short; app works when the cache is down.
- [ ] Port not publicly reachable.
- [ ] Eviction and hit ratio observed.
