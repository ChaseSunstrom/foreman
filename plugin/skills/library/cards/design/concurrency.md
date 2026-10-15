---
name: concurrency
title: Concurrency
area: design
tags: [concurrency, races, locks, atomicity, async, optimistic-locking]
detect: []
related: [idempotency, state-machines, caching, background-jobs, websockets]
---
Shared-state correctness: find the check-then-act races, make updates atomic, and test with real parallelism.

## Verify
- `go test -race ./...`: the Go race detector finds unsynchronized access during tests.
- `cargo test` with `RUSTFLAGS="-Zsanitizer=thread"` on nightly: a thread sanitizer run for unsafe or atomic code (Rust, nightly only).
- `pytest -q -k concurrent`: tests that run the operation from many threads or tasks and assert the invariant.
- `psql -c "select pid, wait_event_type, state, left(query,60) from pg_stat_activity where wait_event_type='Lock'"`: current lock waits in Postgres during a stress run.

## Test first
Hammer the operation in parallel and assert the invariant, not a count of calls.
```python
def test_withdraw_never_overdraws_under_contention(db):
    acct = db.create_account(balance=100)
    def w(_):
        try: withdraw(acct.id, 30)
        except InsufficientFunds: pass
    with ThreadPoolExecutor(16) as ex:
        list(ex.map(w, range(50)))
    assert db.balance(acct.id) == 10            # exactly 3 succeeded, never negative
```

## Do
- Treat every read-then-write on shared state as a race and make it one atomic operation, such as `UPDATE accounts SET balance = balance - 30 WHERE id=? AND balance >= 30`.
- Let the database enforce uniqueness and invariants (unique, `CHECK`, foreign keys), and handle the violation error.
- Use optimistic concurrency (a `version` column, `WHERE version = ?`) for low contention, and `SELECT ... FOR UPDATE` for high contention, with a consistent lock order.
- Keep critical sections small, never hold a lock across network calls, and set lock and statement timeouts.
- Prefer message passing or immutable data over shared mutable state. Confine state to one owner (an actor, a goroutine, a single writer).
- In async code, don't block the event loop, and bound parallelism with a semaphore or worker pool.
- Cancel and clean up properly: pass contexts or cancellation tokens, and wait for tasks on shutdown.
- Retry transaction serialization failures and deadlocks (Postgres `40001` and `40P01`) from the start of the transaction.

## Avoid
- Check-then-act in application code (`if not exists: insert`): two workers both pass. Use a unique constraint or an atomic upsert.
- In-process locks to protect shared data in a multi-instance service: they only guard one process. Use the database or a distributed lock with an expiry.
- Fire-and-forget tasks (`asyncio.create_task` with no reference, a bare `go func()`): errors vanish and they outlive shutdown. Track them and handle errors.
- Lock ordering that differs between code paths: deadlock. Always acquire in one global order, such as by ID.
- Python threads for CPU-bound speedup: the GIL serializes them. Use processes for CPU work.
- Sleeping in tests to wait for another thread: flaky. Use events, barriers and joins.
- Holding a transaction open while calling external services: it keeps row locks. Commit first, and do the call after.

## Review
- [ ] Each read-modify-write is atomic or guarded by a version or lock.
- [ ] The database enforces invariants, and violations are handled.
- [ ] Locks are held briefly, in a consistent order, with timeouts.
- [ ] A contention test and the race detector (where available) pass.
- [ ] Background tasks are tracked, cancelable and drained on shutdown.
