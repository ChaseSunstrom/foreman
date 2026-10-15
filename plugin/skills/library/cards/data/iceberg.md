---
name: iceberg
title: Apache Iceberg
area: data
tags: [iceberg, lakehouse, table-format, snapshots, parquet, catalog]
detect: [dep:pyiceberg, dep:iceberg-core]
related: [delta-lake, trino, spark, parquet-arrow]
---
Apache Iceberg tables: snapshots, hidden partitioning, schema evolution, and the maintenance that keeps them fast.

## Verify
- `SELECT * FROM db.t.snapshots` (Spark or Trino `"t$snapshots"`): commit history exists and operations are as expected.
- `SELECT file_path, record_count FROM db.t.files`: file count and sizes; many tiny files mean compaction is due.
- `SELECT * FROM db.t.history`: lineage of current-snapshot changes.
- `SELECT count(*) FROM db.t FOR VERSION AS OF <snapshot_id>`: time travel returns the older state.

## Test first
Test schema evolution and rollback on a throwaway local catalog.
```python
def test_added_column_reads_null_for_old_rows(catalog):
    t = catalog.create_table("db.t", schema=SCHEMA)
    t.append(pa.table({"id": [1]}))
    with t.update_schema() as u:
        u.add_column("note", StringType())
    assert catalog.load_table("db.t").scan().to_arrow()["note"][0].as_py() is None
```

## Do
- Use hidden partition transforms: `PARTITIONED BY (days(ts), bucket(16, id))`. Queries filter on the source column, no extra partition column.
- Evolve schema by ADD, DROP, RENAME and type promotion (int to long); columns are tracked by id, so renames are safe.
- Compact small files with `CALL system.rewrite_data_files(table => 'db.t')` and rewrite manifests with `rewrite_manifests`.
- Expire old snapshots with `CALL system.expire_snapshots(table => 'db.t', older_than => TIMESTAMP '...')` on a schedule.
- Remove orphans with `remove_orphan_files` using a safe age threshold.
- Use `MERGE INTO` for upserts; set `write.delete.mode` and `write.update.mode` knowing merge-on-read versus copy-on-write tradeoffs.
- Use one catalog (REST, Glue, Hive, Nessie) shared by all engines.

## Avoid
- Streaming small commits with no compaction: thousands of small files and metadata bloat. Schedule rewrite.
- Expiring snapshots then expecting time travel or rollback to those points: gone. Set retention to the recovery need.
- `remove_orphan_files` with a tiny `older_than`: deletes files from in-flight writes. Keep at least days.
- Two writers committing concurrently with no retry: commit conflicts. Retry (`commit.retry.num-retries`) and partition work.
- Treating the file system layout as the contract: engines must go through the catalog, not copy folders.
- Altering partition spec and expecting old data rewritten: it applies to new data only.

## Review
- [ ] Partitioning uses transforms matching the filter columns.
- [ ] Compaction, snapshot expiry and orphan cleanup scheduled.
- [ ] Retention matches rollback needs.
- [ ] Concurrent writers handle conflict retries.
- [ ] All engines use the same catalog.
