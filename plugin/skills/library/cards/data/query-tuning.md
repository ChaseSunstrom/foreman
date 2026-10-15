---
name: query-tuning
title: Query tuning
area: data
tags: [sql, performance, indexes, explain, query-plans, databases]
detect: []
related: [postgres, mysql, n-plus-one, sql-migrations, clickhouse]
---
Tune a slow query by measuring the plan first, changing one thing, and proving the new plan on realistic data.

## Verify
- `psql "$DATABASE_URL" -c "EXPLAIN (ANALYZE, BUFFERS) <query>"`: actual rows, loops, buffers and time per node (Postgres).
- `mysql -e "EXPLAIN ANALYZE <query>"`: actual timings per iterator (MySQL 8).
- `sqlite3 app.db "EXPLAIN QUERY PLAN <query>"`: SEARCH versus SCAN (SQLite).
- `psql "$DATABASE_URL" -c "SELECT query, calls, mean_exec_time FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;"`: which statements cost the most overall.

## Test first
Capture the baseline, then make a test that fails on the slow shape.
```python
def test_orders_by_user_uses_index(db):
    seed(db, rows=200_000)
    plan = "\n".join(r[0] for r in db.execute("explain select * from orders where user_id = 7"))
    assert "Seq Scan" not in plan
```
Seed enough rows: the planner picks seq scans on tiny tables.

## Do
- Read the plan top-down for the biggest actual time and the biggest gap between estimated and actual rows.
- Add an index that matches the filter columns then sort columns; use partial or covering indexes where the shape fits.
- Select only needed columns so index-only scans become possible.
- Refresh statistics (`ANALYZE`) when estimates are far off, and test on production-sized data.
- Replace correlated subqueries or per-row lookups with a join or a window function; batch with `WHERE id = ANY($1)`.
- Use keyset pagination instead of `OFFSET` for deep pages.
- Record before and after plan, row counts and timings as evidence.

## Avoid
- Adding indexes by guesswork: write cost and bloat with no gain. Prove with EXPLAIN ANALYZE.
- Plain `EXPLAIN` as proof: it shows estimates only. Use `ANALYZE` (and know it executes the statement, so wrap writes in a rolled-back transaction).
- Wrapping an indexed column in a function (`lower(email)`, `date(ts)`): no index use. Create an expression index or rewrite as a range.
- Leading-wildcard `LIKE '%x'`: cannot use a B-tree. Use trigram or full-text indexes.
- Implicit type casts in comparisons (`varchar` to `int`): index skipped. Match the types.
- Tuning against a tiny dev database: plans differ at scale. Test on realistic volume.
- `SELECT DISTINCT` to hide a bad join: fix the join.

## Review
- [ ] Before and after plans are attached with actual timings.
- [ ] New indexes serve a measured query and their write cost is acknowledged.
- [ ] No function or cast on indexed columns in predicates.
- [ ] Pagination is keyset on large tables.
- [ ] Verified on production-scale data volumes.
