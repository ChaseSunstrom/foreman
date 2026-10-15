---
name: delta-lake
title: Delta Lake
area: data
tags: [delta, lakehouse, spark, merge, optimize, vacuum]
detect: [dep:delta-spark, dep:deltalake]
related: [iceberg, spark, parquet-arrow, trino]
---
Delta Lake tables: transaction log, MERGE upserts, OPTIMIZE and VACUUM, schema enforcement and time travel.

## Verify
- `DESCRIBE HISTORY tbl`: operations, versions and user metrics per commit.
- `DESCRIBE DETAIL tbl`: numFiles, sizeInBytes and partition columns.
- `SELECT count(*) FROM tbl VERSION AS OF 5`: time travel works for the version.
- `python -c "from deltalake import DeltaTable; print(DeltaTable('p').version())"`: the table opens from the Python reader.

## Test first
Test upsert idempotency against a temp-dir table.
```python
def test_merge_is_idempotent(spark, tmp_path):
    path = str(tmp_path)
    spark.createDataFrame([(1, "a")], "id int, v string").write.format("delta").save(path)
    for _ in range(2):
        dt = DeltaTable.forPath(spark, path)
        dt.alias("t").merge(src.alias("s"), "t.id = s.id") \
          .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    assert spark.read.format("delta").load(path).count() == 1
```

## Do
- Upsert with `MERGE INTO` using a unique key in the source; deduplicate the source first, or the merge fails on multiple matches.
- Put partition columns in the merge condition to prune files.
- Compact with `OPTIMIZE tbl` (and `ZORDER BY (col)` or liquid clustering where available) on a schedule.
- Run `VACUUM tbl RETAIN 168 HOURS` on a schedule, with retention longer than your longest reader or job.
- Rely on schema enforcement; evolve deliberately with `mergeSchema` or `ALTER TABLE ADD COLUMNS`.
- Partition only low-cardinality columns on big tables (date), not user ids.
- Use `CREATE TABLE ... USING DELTA` with explicit properties (`delta.autoOptimize.*` where supported).
- For streaming, set a checkpoint location and write with `foreachBatch` plus MERGE for upserts.

## Avoid
- Lowering the vacuum retention check to zero hours: running readers and time travel break. Keep the default window.
- Over-partitioning: millions of tiny files. Partition coarsely and use clustering.
- MERGE with duplicate source keys: error or wrong results. Dedupe with a window function.
- Overwriting a path with plain parquet writes: the log desyncs. Always write through the delta format.
- Concurrent writers touching the same files: conflict exceptions. Isolate by partition and retry.
- Assuming other engines see features instantly: reader and writer protocol versions must be supported.

## Review
- [ ] Merge source deduplicated; merge condition prunes partitions.
- [ ] OPTIMIZE and VACUUM scheduled with safe retention.
- [ ] Partitioning is coarse.
- [ ] Schema changes explicit.
- [ ] Concurrent write conflicts handled.
