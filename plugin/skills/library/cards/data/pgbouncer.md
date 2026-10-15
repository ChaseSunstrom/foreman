---
name: pgbouncer
title: PgBouncer
area: data
tags: [pgbouncer, postgres, pooling, connections, transaction-mode]
detect: [file:pgbouncer.ini]
related: [postgres, postgres-locking, postgres-rls]
---
PgBouncer connection pooling for PostgreSQL: pool modes, sizing, and what breaks in transaction mode.

## Verify
- `psql -p 6432 pgbouncer -c "SHOW POOLS"`: cl_active, cl_waiting and sv_active per pool; waiting clients mean the pool is too small.
- `psql -p 6432 pgbouncer -c "SHOW STATS"`: per-database request and wait times.
- `psql -p 6432 pgbouncer -c "SHOW CONFIG"`: effective pool_mode, default_pool_size, max_client_conn.
- `psql -c "SELECT count(*) FROM pg_stat_activity WHERE backend_type = 'client backend'"`: server connections stay under max_connections.

## Test first
Run the app test suite against the pooler port in transaction mode; fail on session-state leaks.
```python
def test_no_session_state_leaks_between_transactions(pooled):
    with pooled() as c: c.execute("SET statement_timeout = '1s'")
    with pooled() as c:
        assert c.execute("SHOW statement_timeout").fetchone()[0] != "1s"  # use SET LOCAL instead
```

## Do
- Use `pool_mode = transaction` for web apps; a server connection is held only for the transaction.
- Size `default_pool_size` near the DB's useful concurrency (cores times a small factor), and `max_client_conn` for all app instances.
- Keep PgBouncer authentication in `auth_type` with `auth_file` or `auth_query`; prefer `scram-sha-256` matching the server.
- Use `SET LOCAL` and `set_config(..., true)` inside transactions for per-request settings.
- Reload config with `RELOAD;` on the admin console; use `PAUSE` and `RESUME` for maintenance.
- Run migrations and `LISTEN` consumers over a direct connection or a session-mode pool.
- Put `server_reset_query` only on session mode; transaction mode uses `server_reset_query_always` only if needed.

## Avoid
- Session features in transaction mode: plain `SET`, `LISTEN/NOTIFY`, session advisory locks, `WITH HOLD` cursors, temp tables. They break or leak across clients. Use direct connections or session pooling.
- Protocol-level prepared statements in older setups: failures such as "prepared statement does not exist". Disable client-side server prepares (for example `prepare_threshold=0` in psycopg) or use a PgBouncer version with `max_prepared_statements` set.
- A client-side pool of 100 behind PgBouncer per instance: client waits hide in the app. Keep app pools small.
- Setting pool size equal to max_connections: leaves nothing for admin, replication, migrations.
- Using the pooler for `pg_dump` or logical replication: connect directly.

## Review
- [ ] Pool mode matches the features the app uses.
- [ ] Per-request settings use SET LOCAL.
- [ ] Sum of pools across databases and users is under max_connections with headroom.
- [ ] Prepared-statement behavior tested through the pooler.
- [ ] Migrations and listeners bypass transaction pooling.
