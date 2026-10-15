---
name: sql
title: SQL
area: lang
tags: [sql, queries, migrations, sqlfluff, indexes, transactions]
detect: [ext:.sql, file:.sqlfluff]
related: [bash]
---
SQL queries and schema scripts: dialect-aware linting, null and join semantics, safe migrations, plans before indexes.

## Verify
- `sqlfluff lint --dialect postgres .`: style and parse errors (set the dialect, or put it in `.sqlfluff`; `sqlfluff fix` applies safe fixes).
- `psql -v ON_ERROR_STOP=1 -f migration.sql "$DATABASE_URL"`: the script runs against a scratch database and stops at the first error.
- `sqlite3 :memory: < schema.sql`: SQLite schemas load cleanly.
- `psql -c "EXPLAIN (ANALYZE, BUFFERS) <query>"`: the plan on realistic data uses the expected index (run on a copy, since ANALYZE executes the query).

## Test first
Check the behavior before writing the query: seed a scratch database and assert on the result so the check fails first.
```sql
-- test_active_users.sql  (psql -v ON_ERROR_STOP=1 -f)
BEGIN;
INSERT INTO users (id, email, deleted_at) VALUES
  (1, 'a@x.io', NULL), (2, 'b@x.io', now());
DO $$
BEGIN
  IF (SELECT count(*) FROM active_users) <> 1 THEN
    RAISE EXCEPTION 'active_users must hide deleted rows';
  END IF;
END $$;
ROLLBACK;
```
pgTAP or the project's migration test tool are fine if already present.

## Do
- List columns explicitly and qualify them with table aliases in joins.
- Use explicit `JOIN ... ON`; filter outer-joined tables in the `ON` clause, not `WHERE`, to keep the outer semantics.
- Parameterize values (`$1`, `:name`, `?`); never build SQL by string concatenation from input.
- Add `ORDER BY` with a unique tiebreaker for any pagination, and prefer keyset pagination over large `OFFSET`.
- Wrap multi-statement changes in a transaction; constrain data in the schema (`NOT NULL`, `CHECK`, `UNIQUE`, foreign keys).
- Store time as `timestamptz` (Postgres) or UTC, and money as integers or `numeric`.
- Make migrations additive and reversible: add nullable column, backfill in batches, then add the constraint.

## Avoid
- `NOT IN (subquery)` where the subquery can return NULL: returns no rows. Use `NOT EXISTS`.
- `= NULL` or `<> NULL`: always unknown. Use `IS NULL`, `IS DISTINCT FROM`.
- `SELECT *` in views, inserts or app queries: breaks when columns change. Name the columns.
- `UPDATE` or `DELETE` without `WHERE` run in a console: run it as a `SELECT` first, inside a transaction, and check the row count.
- Functions on indexed columns in `WHERE` (`lower(email) = ...`, `date(created_at) = ...`): skips the index. Use an expression index or range predicate.
- `float` for money and `varchar(255)` by habit: rounding errors and arbitrary limits. Use `numeric`/integer cents, and `text` where the dialect allows.
- Long `ALTER TABLE` locks on a hot table: add the index with `CREATE INDEX CONCURRENTLY` (Postgres) outside a transaction.
- `COUNT(*)` of a joined one-to-many as if it were the parent count: use `COUNT(DISTINCT parent.id)`.

## Review
- [ ] Dialect is named and the lint passes with that dialect.
- [ ] No string-built SQL from input, and no `SELECT *` in committed queries.
- [ ] NULL behavior is considered for joins, `NOT IN`, aggregates and comparisons.
- [ ] Migrations are re-runnable or reversible, and lock impact is considered.
- [ ] A plan or test shows the query uses its index.
