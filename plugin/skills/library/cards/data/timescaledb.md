---
name: timescaledb
title: TimescaleDB
area: data
tags: [timescaledb, postgres, timeseries, hypertables, compression, continuous-aggregates]
detect: [dep:timescaledb, dep:timescale]
related: [postgres, query-tuning, sql-migrations, clickhouse]
---
TimescaleDB: hypertables on Postgres with chunk sizing, compression, retention and continuous aggregates.

## Verify
- `psql "$DATABASE_URL" -c "SELECT * FROM timescaledb_information.hypertables;"`: tables are hypertables with the expected dimensions.
- `psql "$DATABASE_URL" -c "SELECT * FROM timescaledb_information.jobs;"`: policies (compression, retention, aggregate refresh) are scheduled.
- `psql "$DATABASE_URL" -c "SELECT * FROM chunks_detailed_size('metrics');"`: chunk sizes versus memory and compression effect.
- `psql "$DATABASE_URL" -c "EXPLAIN (ANALYZE) <query>"`: chunk exclusion, so only relevant chunks are scanned.

## Test first
Run the `timescale/timescaledb` image; apply the migration then assert the policy exists.
```python
def test_metrics_is_hypertable_with_retention(db):
    assert db.scalar("select count(*) from timescaledb_information.hypertables where hypertable_name='metrics'") == 1
    assert db.scalar("select count(*) from timescaledb_information.jobs where proc_name='policy_retention'") == 1
```

## Do
- Create the extension, then `SELECT create_hypertable('metrics', by_range('time'))` on an empty or migrated table (older releases: `create_hypertable('metrics', 'time')`).
- Size chunks so recent chunks and indexes fit in memory; set `chunk_time_interval` for your ingest rate.
- Add compression: `ALTER TABLE ... SET (timescaledb.compress, timescaledb.compress_segmentby = 'device_id')` plus `add_compression_policy`.
- Add `add_retention_policy` for expiry; drop old data by chunk, not `DELETE`.
- Build rollups as continuous aggregates (`CREATE MATERIALIZED VIEW ... WITH (timescaledb.continuous)`) with `add_continuous_aggregate_policy`.
- Always filter queries by a time range so chunk exclusion works; use `time_bucket()` for grouping.
- Batch inserts (multi-row or `COPY`).

## Avoid
- A regular Postgres table for large time series: no chunking, bloated indexes. Make a hypertable.
- Queries without a time predicate: scans every chunk. Always bound time.
- `DELETE` of old rows: slow and bloats. Use retention policies or `drop_chunks`.
- Too-small chunks (thousands): planner overhead. Increase the interval.
- Segmenting compression by a high-cardinality column: poor ratio. Segment by a low-cardinality key, order by time.
- Updating compressed chunks routinely: expensive decompress. Keep recent data uncompressed with a compress-after delay.
- Unique indexes that omit the time column: not allowed on hypertables. Include it in the key.

## Review
- [ ] Table is a hypertable with an intentional chunk interval.
- [ ] Compression and retention policies exist and show in `jobs`.
- [ ] Hot queries have a time range and show chunk exclusion in EXPLAIN.
- [ ] Rollups use continuous aggregates, not ad hoc heavy queries.
- [ ] Inserts are batched.
