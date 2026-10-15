---
name: bigquery
title: BigQuery
area: data
tags: [bigquery, gcp, warehouse, sql, partitioning, cost]
detect: [dep:google-cloud-bigquery, dep:@google-cloud/bigquery, dep:cloud.google.com/go/bigquery, dep:google-cloud-bigquery-storage, dep:pandas-gbq, dep:dbt-bigquery, dep:Google.Cloud.BigQuery.V2, dep:google-cloud-bigquery]
related: [dbt, snowflake, parquet-arrow, etl-pipelines, query-tuning]
---
BigQuery: partitioned and clustered tables, dry-run cost checks, parameterized queries, batch loads.

## Verify
- `bq query --use_legacy_sql=false --dry_run '<sql>'`: bytes the query would process, with no cost.
- `bq show --format=prettyjson project:dataset.table`: schema, partitioning, clustering and expiration.
- `bq query --use_legacy_sql=false 'select count(*) from `p.d.t` where _PARTITIONTIME >= ...'`: partition filter works on a real table.
- `bq ls -j -n 5`: recent jobs and their state.

## Test first
Assert cost and correctness: a dry run must stay under a byte budget and a dev dataset gives results.
```python
def test_query_prunes_partitions(client):
    cfg = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    job = client.query(SQL, job_config=cfg)
    assert job.total_bytes_processed < 50 * 1024**2
```
Fails until the query filters on the partition column.

## Do
- Partition large tables by a date/timestamp column (or integer range) and cluster by common filter columns.
- Use `require_partition_filter` on big partitioned tables to block full scans.
- Select only needed columns; billing is by bytes read, not rows returned.
- Pass parameters with `QueryJobConfig(query_parameters=[ScalarQueryParameter(...)])`.
- Load bulk data with load jobs (`load_table_from_uri`/`from_dataframe`) or the Storage Write API, not row-by-row.
- Set `maximum_bytes_billed` on job configs as a guardrail.
- Use `MERGE` for upserts and `INSERT ... SELECT` for transforms; set table and partition expiration.
- Grant access via IAM on datasets, and use service accounts with minimal roles.

## Avoid
- `SELECT *`: bills every column. Name columns.
- `LIMIT` believing it cuts cost: the scan still happens. Filter on partitions.
- Filtering a partition column through a function or subquery (`DATE(ts)` on a non-partition column): no pruning. Filter the partition column directly.
- Streaming inserts (`insert_rows_json`) for bulk loads: costly and has a streaming buffer that blocks DML. Use load jobs or the Storage Write API.
- String-formatting values into SQL: injection. Use query parameters.
- Legacy SQL (`#legacySQL`) or `[project:dataset.table]`: use standard SQL with backticked names.
- Cross joins and unbounded `ARRAY_AGG`: exploding rows and memory limits.
- Sharded `table_YYYYMMDD` tables: use one partitioned table.

## Review
- [ ] Dry run bytes are within budget; partition filters are present.
- [ ] No `SELECT *`; `maximum_bytes_billed` is set on automated jobs.
- [ ] Values bind as parameters; standard SQL only.
- [ ] Bulk writes use load jobs or Storage Write API.
- [ ] Table partitioning, clustering and expiration are set.
