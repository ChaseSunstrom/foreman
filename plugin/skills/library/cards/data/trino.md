---
name: trino
title: Trino
area: data
tags: [trino, presto, sql, federation, iceberg, query-performance]
detect: [dep:trino]
related: [iceberg, delta-lake, query-tuning, parquet-arrow]
---
Trino queries over lakes and federated sources: partition pruning, statistics, EXPLAIN and memory limits.

## Verify
- `trino --execute "EXPLAIN ANALYZE <query>"`: per-stage rows, CPU and input size; scan volume tells you if pruning worked.
- `trino --execute "EXPLAIN (TYPE DISTRIBUTED) <query>"`: join distribution (partitioned versus broadcast) and pushdown.
- `trino --execute "SHOW STATS FOR schema.table"`: row counts and distinct values exist; nulls mean ANALYZE is missing.
- `trino --execute "SELECT * FROM system.runtime.queries ORDER BY created DESC LIMIT 10"`: state and error of recent queries.

## Test first
Run the SQL against a small fixture table and assert on both result and scan size.
```python
def test_daily_report_prunes_partitions(trino):
    plan = trino.execute("EXPLAIN SELECT count(*) FROM events WHERE ds = DATE '2026-01-01'")
    assert "ds = DATE '2026-01-01'" in str(plan)     # predicate pushed to the scan
    assert trino.execute("SELECT count(*) FROM events WHERE ds = DATE '2026-01-01'")[0][0] == 3
```

## Do
- Filter directly on partition columns with literals so connectors prune.
- Run `ANALYZE schema.table` after large loads so the optimizer picks join order and distribution.
- Select only needed columns; columnar formats read only those.
- Put the smaller table on the right side of a join; override with the `join_distribution_type` session property when stats are missing.
- Use `approx_distinct` and `approx_percentile` when exact is not required.
- Use `LIMIT` with `ORDER BY` (top-N) rather than a full sort; avoid `ORDER BY` in subqueries.
- For lake tables use Iceberg or Delta tables with file compaction maintained.
- Set `query_max_memory` and per-query limits and use resource groups to isolate workloads.

## Avoid
- Wrapping partition columns in functions (`WHERE year(ds) = 2026`): no pruning. Compare the raw column.
- `SELECT *` over wide Parquet tables: reads everything.
- Casting join keys with mismatched types: no pushdown and slow hash joins. Align types in the schema.
- Huge `IN (...)` lists or cross joins by accident: memory blowups. Join against a table.
- Federating a large join across two remote databases: all data moves through Trino. Pre-aggregate at the source.
- Small-file lakes with no compaction: split planning dominates runtime.

## Review
- [ ] EXPLAIN ANALYZE shows pruned scans for date filters.
- [ ] Table stats collected after loads.
- [ ] No functions on partition columns in predicates.
- [ ] Memory limits and resource groups set for shared clusters.
- [ ] Federated joins reduce data at the source first.
