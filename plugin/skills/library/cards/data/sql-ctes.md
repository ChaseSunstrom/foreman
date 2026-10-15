---
name: sql-ctes
title: SQL CTEs
area: data
tags: [sql, cte, recursive, with, readability, optimization]
detect: []
related: [sql-window-functions, query-tuning, postgres-indexes]
---
Common table expressions: readable query structure, recursive traversal with termination, and optimizer fences.

## Verify
- `psql -c "EXPLAIN ANALYZE <query>"`: whether each CTE is inlined or shows as a CTE Scan (materialized).
- `psql -c "SELECT version()"`: PostgreSQL 12 and later inlines non-recursive, side-effect-free CTEs used once; older versions always materialize.
- `psql -c "<recursive query> LIMIT 100"`: terminates and returns plausible depth.

## Test first
Test recursion with a cycle and the depth limit.
```python
def test_org_tree_terminates_on_cycle(db):
    db.execute("INSERT INTO emp VALUES (1,2),(2,1),(3,1)")   # id, manager_id with a cycle
    rows = db.execute("""
      WITH RECURSIVE t(id, depth, path) AS (
        SELECT id, 0, ARRAY[id] FROM emp WHERE id = 3
        UNION ALL
        SELECT e.manager_id, t.depth+1, t.path || e.manager_id
        FROM emp e JOIN t ON e.id = t.id WHERE NOT e.manager_id = ANY(t.path))
      SELECT count(*) FROM t""").fetchone()
    assert rows[0] == 3
```

## Do
- Name CTEs for steps (`active_users`, `monthly_totals`) so the final SELECT reads as a summary.
- Recursive form: anchor `UNION ALL` recursive term. Carry a `depth` column and a `path` array to stop cycles, and cap with `WHERE depth < N`.
- Force a choice in Postgres: `WITH x AS MATERIALIZED (...)` to compute once, or `NOT MATERIALIZED` to allow predicate pushdown.
- Use `UNION` (not `ALL`) in recursion only when you need deduplication and accept the cost.
- Use data-modifying CTEs (`WITH moved AS (DELETE ... RETURNING *) INSERT ...`) for atomic multi-step changes.
- Prefer a join or window over a CTE queried many times with different filters.
- Push filters into the CTE so it handles fewer rows.

## Avoid
- Assuming a CTE is a performance fence on modern Postgres: it is inlined by default. Say `MATERIALIZED` if you depend on one evaluation.
- Recursive CTE with no termination guard on cyclic data: infinite loop until memory or timeout. Track visited ids or depth.
- Referencing a materialized CTE many times where each use filters different rows: the whole set is computed anyway. Inline it.
- Deep CTE chains used to avoid thinking about a join: unreadable plans. Collapse where possible.
- Using a CTE where a view or temp table would let you index intermediate results.
- Relying on CTE ordering: order is not preserved unless the outer query sorts.

## Review
- [ ] Recursive CTEs have a cycle or depth guard.
- [ ] Materialization behavior is intentional and stated where it matters.
- [ ] EXPLAIN checked for repeated scans of a CTE.
- [ ] Filters are pushed down; row counts stay small.
- [ ] Data-modifying CTEs are wrapped in the intended transaction.
