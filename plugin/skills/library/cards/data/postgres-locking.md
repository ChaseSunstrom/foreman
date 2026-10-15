---
name: postgres-locking
title: PostgreSQL locking
area: data
tags: [postgres, locks, deadlock, migrations, skip-locked, concurrency]
detect: []
related: [postgres, sql-migrations, postgres-indexes, pgbouncer]
---
Find, avoid and survive PostgreSQL lock waits, deadlocks and risky DDL on live tables.

## Verify
- `psql -c "SELECT pid, pg_blocking_pids(pid), state, wait_event_type, left(query,80) FROM pg_stat_activity WHERE cardinality(pg_blocking_pids(pid)) > 0"`: who is blocked and by whom.
- `psql -c "SELECT locktype, relation::regclass, mode, granted, pid FROM pg_locks WHERE NOT granted"`: ungranted lock requests.
- `psql -c "SELECT pid, now()-xact_start AS age, state, left(query,80) FROM pg_stat_activity WHERE state = 'idle in transaction'"`: idle-in-transaction sessions that hold locks.
- `psql -c "SHOW lock_timeout"`: migrations run with a bounded wait.

## Test first
Reproduce the contention with two connections; the failing test is a lock wait that exceeds a timeout.
```python
def test_claim_does_not_block_other_workers(conn_a, conn_b):
    conn_a.execute("BEGIN"); conn_a.execute("SELECT id FROM jobs WHERE status='queued' LIMIT 1 FOR UPDATE")
    conn_b.execute("SET lock_timeout = '200ms'")
    row = conn_b.execute("SELECT id FROM jobs WHERE status='queued' ORDER BY id LIMIT 1 FOR UPDATE SKIP LOCKED").fetchone()
    assert row is not None  # a different job, no wait
```

## Do
- Set `SET lock_timeout = '3s'` (and a statement_timeout) at the top of every DDL migration; retry on failure.
- Queue claims: `SELECT ... FOR UPDATE SKIP LOCKED LIMIT n`.
- Take row locks in a consistent order (`ORDER BY id`) to prevent deadlocks.
- Keep transactions short; no network calls inside them.
- Add constraints safely: `ADD CONSTRAINT ... NOT VALID`, then `VALIDATE CONSTRAINT` (weaker lock).
- Use `pg_advisory_xact_lock(key)` for app-level mutexes; it releases at commit.
- Set `idle_in_transaction_session_timeout`.
- Use `CREATE INDEX CONCURRENTLY` and `ALTER TABLE ... ADD COLUMN` without volatile defaults.

## Avoid
- `ALTER TABLE` without `lock_timeout`: it queues behind a long query, and then every later query queues behind it. Set the timeout and retry.
- Session-level `pg_advisory_lock` behind a transaction pooler: the lock leaks to another client. Use the xact variant.
- `SELECT ... FOR UPDATE` on wide ranges: use a narrower predicate or `FOR NO KEY UPDATE`.
- Assuming `SERIALIZABLE` never fails: catch SQLSTATE 40001 and 40P01 and retry the whole transaction.
- Rewriting a big table in one UPDATE: batch by key range with commits.

## Review
- [ ] Every migration sets `lock_timeout` and has a retry.
- [ ] Lock order is consistent across code paths touching several rows.
- [ ] Deadlock and serialization failures are retried.
- [ ] No transaction spans an external call.
- [ ] Constraints and indexes added with the low-lock variants.
