---
name: mysql-indexes
title: MySQL indexes
area: data
tags: [mysql, innodb, index, explain, performance, mariadb]
detect: []
related: [mysql, query-tuning, n-plus-one, sql-migrations]
---
InnoDB index design and proof with EXPLAIN: composite order, covering indexes, collation and online DDL.

## Verify
- `mysql -e "EXPLAIN FORMAT=TREE SELECT ..."`: the chosen access path (index lookup versus table scan).
- `mysql -e "EXPLAIN ANALYZE SELECT ..."`: actual rows and timing per step (MySQL 8.0.18 and later).
- `mysql -e "SHOW INDEX FROM orders"`: columns, order, cardinality and visibility.
- `mysql -e "SELECT * FROM sys.schema_unused_indexes"`: indexes never used since restart.

## Test first
Fail on the plan with realistic data and fresh statistics.
```python
def test_orders_lookup_uses_index(db):
    db.execute("ANALYZE TABLE orders")
    plan = "\n".join(str(r) for r in db.execute(
        "EXPLAIN SELECT id FROM orders WHERE customer_id = 7 ORDER BY created_at DESC LIMIT 20"))
    assert "idx_customer_created" in plan and "filesort" not in plan.lower()
```

## Do
- Composite order: equality columns, then the range or ORDER BY column. A range stops later columns from being used for lookup.
- Every secondary index silently carries the primary key; keep the PK short (an integer, not a UUID string) or all indexes bloat.
- Use covering indexes (all selected columns in the index) to show `Using index` and skip the clustered lookup.
- Use prefix indexes (`name(20)`) for long strings, accepting no covering and no ORDER BY use.
- Descending indexes (`created_at DESC`) are real in MySQL 8; use them for mixed-direction sorts.
- Test removals safely with `ALTER TABLE t ALTER INDEX i INVISIBLE`, then drop after a quiet period.
- Use `ALGORITHM=INPLACE, LOCK=NONE` explicitly on DDL so it fails instead of locking.
- Match types and collations across joined columns.

## Avoid
- Wrapping an indexed column in a function (`WHERE DATE(created_at) = ...`): no index use. Compare to a range.
- Comparing a string column to a number: implicit cast disables the index. Quote the literal.
- Joining columns with different collation or charset: the index is skipped. Align them.
- Many single-column indexes hoping for combination: the optimizer uses one. Build the composite.
- `SELECT *` with a covering index plan in mind: it forces row lookups. Select only needed columns.
- Leading wildcard `LIKE '%x'`: full scan. Use FULLTEXT or a different design.
- Adding an index in a migration without checking lock level on big tables.

## Review
- [ ] EXPLAIN attached for each new or changed query pattern.
- [ ] Composite order matches equality, range, sort.
- [ ] Short primary key; no redundant prefix indexes.
- [ ] DDL declares ALGORITHM and LOCK.
- [ ] Join columns have matching type and collation.
