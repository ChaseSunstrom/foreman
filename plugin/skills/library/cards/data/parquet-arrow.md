---
name: parquet-arrow
title: Parquet and Arrow
area: data
tags: [parquet, arrow, columnar, pyarrow, datasets, compression]
detect: [dep:pyarrow, dep:fastparquet, dep:polars, dep:parquet, dep:apache-arrow, dep:parquetjs, dep:parquet-wasm, dep:arrow2, ext:.parquet, ext:.arrow]
related: [duckdb, spark, pandera, etl-pipelines, clickhouse]
---
Parquet on disk and Arrow in memory: explicit schemas, sensible row groups, partitioned datasets, projection and filter pushdown.

## Verify
- `python -c "import pyarrow.parquet as pq; print(pq.read_schema('f.parquet'))"`: the file's schema and types.
- `python -c "import pyarrow.parquet as pq; m=pq.ParquetFile('f.parquet').metadata; print(m.num_rows, m.num_row_groups)"`: row and row-group counts.
- `duckdb -c "SELECT * FROM parquet_metadata('f.parquet') LIMIT 5"`: column statistics and compression per row group.
- `pytest -q`: round-trip tests (write, read, compare) pass.

## Test first
Round-trip a frame with the awkward types and compare schemas, not just values.
```python
def test_roundtrip_preserves_types(tmp_path):
    t = pa.table({"id": pa.array([1, None], pa.int64()),
                  "ts": pa.array([datetime(2024,1,1,tzinfo=timezone.utc)] * 2, pa.timestamp("us", "UTC"))})
    pq.write_table(t, tmp_path / "f.parquet")
    assert pq.read_table(tmp_path / "f.parquet").schema == t.schema
```

## Do
- Pass an explicit `pa.schema` when writing; do not rely on inference from the first batch.
- Use `pyarrow.dataset` (`ds.dataset(path, partitioning="hive")`) to scan large data with `columns=` and `filter=` pushdown.
- Write with `zstd` (or `snappy`) compression and row groups of roughly 100k to 1M rows; keep files in the 100 MB to 1 GB range.
- Partition directories by low-cardinality columns used in filters (`year=2024/month=01`).
- Write large outputs incrementally with `pq.ParquetWriter` or `ds.write_dataset`, batch by batch.
- Store timestamps as UTC with an explicit unit; store money as `decimal128`.
- Write to a temp path and rename for atomic publish.

## Avoid
- `pd.read_parquet` of a whole dataset when you need two columns: read with `columns=[...]` and a filter.
- Thousands of tiny files (over-partitioning, per-record writes): slow listing and reads. Compact.
- Partitioning by a high-cardinality column (user id): file explosion. Bucket or cluster instead.
- Float for money and loose timestamp units: rounding and unit mismatch across engines. Use decimal and explicit units.
- Pandas index written implicitly (`__index_level_0__`): stray column. Pass `index=False`.
- Schema drift between files in one dataset: read errors or silent nulls. Unify schemas on write.
- Converting Arrow to pandas early: copies and loses types such as nullable ints. Stay in Arrow or Polars as long as possible.

## Review
- [ ] Schema is explicit and types (UTC timestamps, decimals) are deliberate.
- [ ] Reads project columns and push filters.
- [ ] File size, row group size and partitions are sane.
- [ ] Writes are atomic and incremental for big outputs.
- [ ] A round-trip test covers nulls and timestamps.
