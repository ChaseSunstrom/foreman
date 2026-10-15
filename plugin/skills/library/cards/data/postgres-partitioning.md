---
name: postgres-partitioning
title: PostgreSQL partitioning
area: data
tags: [postgres, partitioning, retention, range, pruning, pg-partman]
detect: []
related: [postgres, postgres-indexes, timescaledb, sql-migrations]
---
Declarative partitioning for large time or tenant tables: pruning, retention by DROP, and safe attach.

## Verify
- `psql -c "EXPLAIN SELECT * FROM events WHERE created_at >= '2026-01-01' AND created_at < '2026-02-01'"`: only the matching partitions appear (pruning works).
- `psql -c "SELECT inhrelid::regclass FROM pg_inherits WHERE inhparent = 'events'::regclass"`: the partition list, including a default partition if any.
- `psql -c "SHOW enable_partition_pruning"`: must be on.
- `psql -c "SELECT count(*) FROM ONLY events_default"`: rows that missed every range.

## Test first
Test that out-of-range inserts are routed, and that pruning happens.
```python
def test_prunes_to_one_partition(db):
    db.execute("INSERT INTO events(created_at) VALUES ('2026-01-15')")
    plan = "\n".join(r[0] for r in db.execute(
        "EXPLAIN SELECT * FROM events WHERE created_at >= '2026-01-01' AND created_at < '2026-02-01'"))
    assert "events_2026_01" in plan and "events_2026_02" not in plan
```

## Do
- `CREATE TABLE events (...) PARTITION BY RANGE (created_at)`, then `CREATE TABLE events_2026_01 PARTITION OF events FOR VALUES FROM ('2026-01-01') TO ('2026-02-01')`. Upper bound is exclusive.
- Include the partition key in every primary key and unique constraint; Postgres requires it.
- Always filter on the partition key with constants or parameters so the planner prunes.
- Create future partitions ahead of time with a scheduled job (or pg_partman).
- Retire data with `ALTER TABLE events DETACH PARTITION events_2025_01 CONCURRENTLY`, then drop or archive; never mass DELETE.
- Load offline, then attach: build a table with a matching CHECK constraint, then `ATTACH PARTITION`, so no full scan is needed under heavy lock.
- Keep partitions in the tens to low hundreds, not thousands.

## Avoid
- Partitioning a table that fits comfortably in memory: planning cost with no gain. Measure first.
- Wrapping the key in a function or cast in WHERE (`date(created_at) = ...`): no pruning. Compare the raw column to a range.
- A missing partition for new data: the insert fails. Add a default partition and alert if it receives rows, or create ahead.
- Foreign keys pointing at a partitioned table's non-key column or unique indexes lacking the key: not allowed; model around it.
- `DETACH ... CONCURRENTLY` inside a transaction block: it errors. Run it standalone.
- Per-partition indexes created by hand: create the index on the parent so new partitions inherit it.

## Review
- [ ] Hot queries show pruning in EXPLAIN.
- [ ] Partition creation is automated with lead time and monitored.
- [ ] Retention uses detach and drop.
- [ ] Unique keys include the partition key.
- [ ] Default partition is empty in steady state.
