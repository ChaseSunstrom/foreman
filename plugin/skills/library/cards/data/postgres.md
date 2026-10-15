---
name: postgres
title: PostgreSQL
area: data
tags: [sql, postgres, database, transactions, indexes, migrations]
detect: [dep:psycopg, dep:psycopg2, dep:psycopg2-binary, dep:asyncpg, dep:pg, dep:postgres, dep:pgx, dep:lib/pq, dep:tokio-postgres, dep:Npgsql, file:*.sql]
related: [sql-migrations, query-tuning, n-plus-one, pgvector, timescaledb]
---
PostgreSQL access: parameterized queries, explicit transactions, constraints in the schema, indexes proven by EXPLAIN.

## Verify
- `psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f migration.sql`: the migration applies and stops at the first error.
- `psql "$DATABASE_URL" -c "EXPLAIN (ANALYZE, BUFFERS) <query>"`: the real plan, row counts and index use.
- `psql "$DATABASE_URL" -c "\d+ table"`: columns, constraints, indexes and FKs as the database sees them.
- `pg_dump --schema-only "$DATABASE_URL" | diff - schema.sql`: committed schema matches the live one.

## Test first
Run tests against a real Postgres (a throwaway container or schema per run), not SQLite. Write the constraint test before the migration.
```python
def test_email_unique_case_insensitive(db):
    db.execute("insert into users(email) values ('A@x.io')")
    with pytest.raises(psycopg.errors.UniqueViolation):
        db.execute("insert into users(email) values ('a@x.io')")
```
Fails until the `unique index on lower(email)` exists.

## Do
- Use `timestamptz`, `text`, `bigint`/`uuid` keys and `numeric` for money. Add `NOT NULL`, `CHECK` and FKs in the schema, not only in app code.
- Pass values as bind parameters (`$1`, `%s`), never string-formatted.
- Index every FK column and each hot `WHERE`/`ORDER BY`. Use partial and covering (`INCLUDE`) indexes where they fit.
- Keep transactions short. Lock rows with `SELECT ... FOR UPDATE SKIP LOCKED` for queue-like work.
- Upsert with `INSERT ... ON CONFLICT (cols) DO UPDATE`, naming the unique columns.
- Pool connections (pgbouncer or the driver's pool) and set `statement_timeout` and `lock_timeout`.
- Use `CREATE INDEX CONCURRENTLY` on live tables; it cannot run inside a transaction block.

## Avoid
- `timestamp` without time zone: silent shifts across zones. Use `timestamptz`.
- `NOT IN (subquery)` with NULLs returns nothing: use `NOT EXISTS`.
- `OFFSET` pagination on large tables: it scans skipped rows. Use keyset (`WHERE id > $last ORDER BY id LIMIT n`).
- `ALTER TABLE ... ADD COLUMN ... DEFAULT` plus rewrites or `SET NOT NULL` on huge tables in one step: add nullable, backfill in batches, then add a validated constraint (`NOT VALID` then `VALIDATE CONSTRAINT`).
- `SELECT *` in application code: schema changes break it and it blocks index-only scans. List columns.
- A connection per request without a pool: exhausts `max_connections`. Pool it.
- Serial/identity gaps treated as bugs: sequences are not gapless. Don't rely on them.

## Review
- [ ] Every query is parameterized and every new FK has an index.
- [ ] Migration is safe on a live table (no long exclusive lock, concurrent index builds).
- [ ] Constraints enforce what the code assumes (unique, not null, check).
- [ ] Transactions are short, with explicit isolation or locking where races matter.
- [ ] EXPLAIN evidence for any new hot query.
