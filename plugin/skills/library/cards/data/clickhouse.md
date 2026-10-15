---
name: clickhouse
title: ClickHouse
area: data
tags: [olap, clickhouse, columnar, analytics, mergetree, sql]
detect: [dep:clickhouse-connect, dep:clickhouse-driver, dep:@clickhouse/client, dep:clickhouse, dep:clickhouse-rs, dep:ClickHouse.Client, dep:clickhouse-jdbc, dep:ClickHouse/clickhouse-go]
related: [parquet-arrow, kafka, query-tuning, etl-pipelines]
---
ClickHouse: MergeTree tables with a sorting key built for the queries, batched inserts, no row-level updates.

## Verify
- `clickhouse-client --query "EXPLAIN indexes = 1 <select>"`: which parts and granules the primary key prunes.
- `clickhouse-client --query "SELECT query_duration_ms, read_rows, read_bytes FROM system.query_log WHERE type='QueryFinish' ORDER BY event_time DESC LIMIT 5"`: rows and bytes read by recent queries.
- `clickhouse-client --query "SELECT table, count() FROM system.parts WHERE active GROUP BY table"`: active part counts stay small.
- `clickhouse-client --query "SHOW CREATE TABLE t"`: engine, ORDER BY, PARTITION BY as deployed.

## Test first
Test against a real server; assert the query reads few rows.
```python
def test_filter_uses_primary_key(ch):
    ch.command("insert into events select number, now() from numbers(100000)")
    r = ch.query("select count() from events where id = 5")
    assert int(r.summary["read_rows"]) < 10000  # fails if ORDER BY lacks id
```

## Do
- Choose `ORDER BY` from the common filters, low-cardinality columns first; it is the primary index.
- Use `MergeTree` family engines; pick `ReplacingMergeTree`/`SummingMergeTree` only with their merge semantics in mind.
- Insert in large batches (thousands to hundreds of thousands of rows) or use async inserts.
- Use `LowCardinality(String)`, narrow integer types and `Date`/`DateTime` instead of strings.
- Partition coarsely (by month) only for retention; avoid high-cardinality partition keys.
- Use materialized views and projections for repeated aggregations.
- Read with `FINAL` only when required; prefer `argMax` patterns for latest-row queries.

## Avoid
- Row-by-row inserts: too many small parts and "too many parts" errors. Batch.
- `UPDATE`/`DELETE` as a normal workflow: mutations rewrite parts. Use Replacing engines, TTL or lightweight deletes sparingly.
- Over-partitioning (by day-and-user): part explosion. Partition by month or not at all.
- `SELECT *` on wide tables: reads every column. Name columns.
- Assuming `ReplacingMergeTree` dedupes immediately: merges are eventual. Use `FINAL` or aggregate.
- Joining huge right-hand tables: loads into memory. Put the small table on the right or pre-aggregate.
- Nullable everywhere: extra storage and slower scans. Use defaults.

## Review
- [ ] ORDER BY matches the dominant filters; EXPLAIN shows pruning.
- [ ] Inserts are batched and idempotent where retried.
- [ ] Types are narrow (LowCardinality, Date) and Nullable is justified.
- [ ] Dedup semantics of the chosen engine are handled in queries.
- [ ] Retention is set by TTL or partition drops.
