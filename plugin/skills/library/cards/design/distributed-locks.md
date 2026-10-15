---
name: distributed-locks
title: Distributed locks
area: design
tags: [locks, fencing, redis, leases, concurrency, consistency, ttl]
detect: []
related: [leader-election, optimistic-locking, idempotency, timeouts, concurrency]
---
A lock is a lease that can expire while the holder is still running, so the protected resource must check a fencing token.

## Verify
- `pytest -q -k lock`: expiry, stale-holder and contention tests.
- `git grep -nE "SETNX|set\(.*nx=True|pg_advisory" -- src`: each acquisition site has a TTL and a release path.
- `git grep -nE "fence|fencing|token" -- src/locks`: a fencing token reaches the resource.

## Test first
A holder pauses past its lease; the stale write must be rejected.
```python
def test_stale_holder_is_fenced(lockserver, store):
    a = lockserver.acquire("job", ttl=1)          # token 1
    clock.advance(2)                               # lease expired
    b = lockserver.acquire("job", ttl=1)          # token 2
    store.write("x", "from-b", token=b.token)
    with pytest.raises(StaleToken):
        store.write("x", "from-a", token=a.token) # a wakes up late
    assert store.read("x") == "from-b"
```

## Do
- Prefer not needing a lock: use a DB unique constraint, an optimistic version check, or an idempotent operation.
- Always set a TTL; renew with a heartbeat while working, and abandon work if renewal fails.
- Issue a monotonically increasing fencing token per acquisition and have the resource reject lower tokens.
- Release only if you still own it: compare-and-delete on a random owner value (a Lua script in Redis).
- Within one Postgres, use `pg_advisory_xact_lock` which releases with the transaction.
- For correctness-critical use a consensus store (etcd, ZooKeeper or Consul sessions); a single Redis node is for efficiency locks only.
- Bound waiting with a timeout and a jittered retry.

## Avoid
- Lock with no TTL: a crashed holder blocks forever. Set a lease.
- Assuming the lock is still held after a GC pause or slow call: the lease may have expired. Use fencing tokens.
- Unconditional `DEL` on release: you may delete someone else's lock. Compare owner first.
- Using wall-clock agreement between machines as a safety argument: clocks drift. Rely on tokens.
- Holding a lock across network calls you could do outside it: shrink the critical section.

## Review
- [ ] Alternative (constraint, version, idempotency) considered first.
- [ ] TTL, renewal and owner-checked release present.
- [ ] Resource enforces fencing tokens.
- [ ] Acquire has a timeout and failure path.
