---
name: redis-locks
title: Redis distributed locks
area: data
tags: [redis, lock, mutex, fencing, redlock, concurrency]
detect: []
related: [redis, redis-caching, postgres-locking, etcd]
---
Redis locks for efficiency, not correctness: SET NX PX with token-checked release, expiry handling and fencing.

## Verify
- `redis-cli SET lock:job1 token123 NX PX 30000`: returns OK for the first holder and nil for the second.
- `redis-cli PTTL lock:job1`: a positive remaining lease, never -1.
- `redis-cli EVAL "if redis.call('get',KEYS[1])==ARGV[1] then return redis.call('del',KEYS[1]) else return 0 end" 1 lock:job1 wrongtoken`: returns 0, a non-owner cannot release.

## Test first
Test mutual exclusion, owner-only release, and expiry.
```python
def test_lock_exclusive_and_owner_release(r):
    assert r.set("l", "a", nx=True, px=500)
    assert not r.set("l", "b", nx=True, px=500)
    assert release(r, "l", "b") == 0       # wrong token
    assert release(r, "l", "a") == 1
    assert r.set("l", "b", nx=True, px=500)
```

## Do
- Acquire in one command: `SET key <random-token> NX PX <ttl>`. The token is unique per acquisition.
- Release with the compare-and-delete Lua script above, so you only delete your own lock.
- Pick a TTL longer than the worst-case critical section, and extend it with a token-checked `PEXPIRE` if work runs long.
- Retry with backoff and jitter, and give up after a deadline.
- For correctness-critical writes add a fencing token: an `INCR` counter value that the protected resource checks and rejects if older.
- Prefer a database row lock or `pg_advisory_xact_lock` when the data is already in Postgres.
- Use a maintained library (redis-py `Lock`, redisson) over hand-rolled code, and still pass a timeout.

## Avoid
- `SETNX` then `EXPIRE` as two calls: a crash between them leaves a lock forever. Use one `SET NX PX`.
- Releasing with a plain `DEL`: after your lease expired you delete someone else's lock. Check the token.
- Assuming a lock is exclusive after a GC pause or slow call: the lease may have expired. Use fencing or make the work idempotent.
- Locking across a Redis failover: async replication can lose the key and two holders appear. Do not rely on it for money or uniqueness; use a DB constraint.
- Using wall-clock-derived tokens or fixed values: collisions. Use random bytes.
- Blocking forever on acquire: always bound the wait.

## Review
- [ ] Acquisition is a single atomic SET NX with expiry.
- [ ] Release is token-checked.
- [ ] Work is idempotent or protected by a fencing token.
- [ ] TTL, renewal and retry bounds documented.
- [ ] Correctness does not depend on the lock alone.
