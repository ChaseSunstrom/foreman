---
name: migration-tests
title: Migration tests
area: testing
tags: [testing, migrations, database, schema, rollback, data, upgrade]
detect: []
related: [database-tests, integration-testing, regression-tests, characterization-tests]
---
Prove schema migrations apply cleanly to a fresh and to a populated database, preserve data, and roll back or stay compatible mid-deploy.

## Verify
- `alembic upgrade head && alembic downgrade base && alembic upgrade head`: the full chain applies, reverses and reapplies (Alembic).
- `python manage.py migrate && python manage.py makemigrations --check --dry-run`: migrations apply and models have no missing migration (Django).
- `npx prisma migrate deploy` (or `rails db:migrate && rails db:rollback`): the migration runs against a real database in CI.
- `psql "$TEST_DATABASE_URL" -f schema_dump.sql`: a production-like dump loads before the migration runs.

## Test first
Seed old-shape data, run the migration, assert the new shape and preserved values.
```python
def test_split_name_migration_preserves_rows(migrator):
    migrator.upgrade("0041_before")
    migrator.exec("INSERT INTO users (id, name) VALUES (1, 'Ada Lovelace')")
    migrator.upgrade("0042_split_name")
    row = migrator.query_one("SELECT first_name, last_name FROM users WHERE id=1")
    assert row == ("Ada", "Lovelace")
```
Write it before the migration so it fails at "no such column".

## Do
- Run all migrations from empty in CI against the same engine and version as production.
- Test data migrations with representative rows: NULLs, empty strings, unicode, max lengths, duplicates, orphans.
- Test against a production-sized or anonymized dump for lock time and duration on large tables.
- Check backward compatibility during rollout: the old code must work with the new schema (expand, then contract in a later release).
- Provide and test a downgrade, or document and test the forward fix when a downgrade is impossible.
- Assert idempotency where required, and that a failed migration leaves the schema consistent (transactional DDL or a clean retry).
- Fail CI if models and migrations disagree (autogenerate diff is non-empty).
- Add indexes concurrently on large tables, and test that path.

## Avoid
- Testing only on an empty database: data-dependent failures reach production. Seed old-shape rows.
- Using SQLite in tests while production is another engine: dialect-specific DDL passes falsely. Use the real engine.
- Dropping or renaming a column in the same release the code stops using it: old instances break mid-deploy. Expand first, contract later.
- Editing a migration already applied elsewhere: histories diverge. Add a new migration.
- Data migrations that import current application models: later model changes break old migrations. Use frozen or raw SQL.
- Skipping the downgrade test: rollback fails when it is needed. Run it in CI.

## Review
- [ ] Migrations apply from empty and on seeded old-shape data.
- [ ] Data preservation and edge rows are asserted.
- [ ] Old code works with the new schema during rollout.
- [ ] Rollback or forward-fix is tested.
- [ ] Models and migrations are checked for drift in CI.
