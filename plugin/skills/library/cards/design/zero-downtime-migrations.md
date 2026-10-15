---
name: zero-downtime-migrations
title: Zero-downtime migrations
area: design
tags: [migrations, database, expand-contract, deploys, locks, backfill]
detect: [file:migrations/*.sql, file:db/migrate/*.rb, file:alembic.ini, file:flyway.conf, dep:alembic, dep:django, dep:knex, dep:prisma, dep:liquibase]
related: [feature-flags, api-versioning, concurrency, caching, twelve-factor]
---
Schema changes shipped in compatible steps (expand, migrate, contract) so old and new code run together without long locks.

## Verify
- `psql -c "show lock_timeout; show statement_timeout"`: migrations run with a lock timeout (Postgres), so a blocked DDL fails fast instead of queueing everything behind it.
- `alembic upgrade head --sql` (or `python manage.py sqlmigrate APP N`): print the SQL to inspect locks and rewrites before running.
- `psql -c "select indexrelid::regclass, indisvalid from pg_index where not indisvalid"`: no invalid indexes left by a failed concurrent build (expect no rows).
- `alembic downgrade -1 && alembic upgrade head`: the step reverses and reapplies on a copy of the data.

## Test first
Run the previous release's tests against the migrated schema. This proves backward compatibility.
```python
def test_old_code_works_after_expand_migration(migrated_db, old_release_queries):
    # new column exists, nullable, old INSERT does not mention it
    migrated_db.execute(old_release_queries.insert_user, ("a@x.io",))
    assert migrated_db.fetchone("select email, display_name from users")[1] is None
```
Keep a CI job that checks out the previous tag and runs its suite against the new migrations.

## Do
- Follow expand, migrate, contract: add the new thing (nullable column, new table), deploy code that writes both and reads new, backfill, then remove the old one in a later release.
- Add columns as nullable or with a constant default (cheap in modern Postgres and MySQL 8). Add `NOT NULL` afterward through a validated `CHECK` constraint (`NOT VALID` then `VALIDATE CONSTRAINT`).
- Build indexes without blocking writes: `CREATE INDEX CONCURRENTLY` in Postgres, outside a transaction, or `ALGORITHM=INPLACE, LOCK=NONE` in MySQL.
- Backfill in small batches by primary-key range, with pauses, outside the DDL migration, and make it resumable and idempotent.
- Set `lock_timeout` and retry the DDL, so it doesn't queue behind a long transaction and block all traffic.
- Rename in steps: add the new column, dual-write, backfill, switch reads, then drop the old one.
- Deploy order: migrate first for expand steps, code first for contract steps.
- Take a backup or snapshot before destructive steps, and rehearse on production-sized data.

## Avoid
- `ALTER TABLE ... RENAME COLUMN` or changing a type in place while old code runs: running instances break instantly. Use the add-copy-switch pattern.
- `CREATE INDEX` without `CONCURRENTLY` on a big Postgres table: it blocks writes for the duration. Use concurrent builds.
- Adding a foreign key or `NOT NULL` with a full validation under an exclusive lock: add as `NOT VALID`, then validate separately.
- One huge `UPDATE` to backfill inside the migration transaction: long locks and replica lag. Batch it.
- Dropping a column in the same release that stops using it: rollback or a slow instance still reads it. Drop a release later.
- Migrations that import current application models: later model changes break old migrations. Use raw SQL or frozen model stubs.
- Editing a migration that already ran elsewhere: histories diverge. Add a new one.

## Review
- [ ] Every step is compatible with the code version before and after it.
- [ ] DDL has lock and statement timeouts, and indexes are built concurrently.
- [ ] Backfills are batched, resumable and separate from schema steps.
- [ ] Destructive steps come a release after the code stops using the object.
- [ ] The previous release's tests pass against the new schema.
