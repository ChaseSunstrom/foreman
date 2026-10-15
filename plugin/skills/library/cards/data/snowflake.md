---
name: snowflake
title: Snowflake
area: data
tags: [snowflake, warehouse, sql, cloud, cost, stages]
detect: [dep:snowflake-connector-python, dep:snowflake-sqlalchemy, dep:snowflake-snowpark-python, dep:snowflake-sdk, dep:snowflake-jdbc, dep:gosnowflake, dep:snowflake-connector-nodejs, dep:Snowflake.Data, dep:dbt-snowflake]
related: [dbt, bigquery, parquet-arrow, etl-pipelines, query-tuning]
---
Snowflake: parameterized queries, right-sized and auto-suspending warehouses, bulk loads via stages, role-based access.

## Verify
- `snow sql -q "select current_role(), current_warehouse(), current_database()"`: session context is the intended one (Snowflake CLI).
- `snow sql -q "select * from table(information_schema.query_history()) order by start_time desc limit 5"`: recent queries, bytes scanned and time.
- `snow sql -q "show warehouses"`: size, auto_suspend and state of warehouses.
- `snow sql -q "explain using text <query>"`: plan and partitions scanned versus total.

## Test first
Use a dedicated dev database/schema per run (clone or temp schema), never prod.
```python
def test_load_is_idempotent(cur):
    load_batch(cur, "b1"); load_batch(cur, "b1")
    cur.execute("select count(*) from stg.orders where batch_id='b1'")
    assert cur.fetchone()[0] == 100   # same as one load
```

## Do
- Bind parameters (`%s` with paramstyle, or `:1`) instead of formatting SQL strings.
- Load files with `PUT` plus `COPY INTO` or Snowpipe, never row-by-row `INSERT`s.
- Use `MERGE INTO` for upserts and `COPY INTO ... ON_ERROR` with a load history check.
- Set `AUTO_SUSPEND` low (60-300s), `AUTO_RESUME`, and size warehouses by workload; separate ETL and BI warehouses.
- Add resource monitors with credit quotas.
- Authenticate with key-pair or OAuth for services, not passwords; use least-privilege roles.
- Filter on columns that align with clustering/micro-partition pruning and select only needed columns.
- Use `QUERY_TAG` to attribute cost.

## Avoid
- Single-row `INSERT` loops: slow and costly. Stage files and `COPY INTO`.
- A warehouse left running or `AUTO_SUSPEND` disabled: burns credits. Set suspend.
- `SELECT *` on wide tables: reads every column. List columns.
- Putting passwords or account secrets in code or connection strings: use key-pair auth and a secrets manager.
- Using `ACCOUNTADMIN` for applications: over-privileged. Create a scoped role.
- Assuming constraints enforce: PRIMARY KEY and UNIQUE are informational, not enforced. Check with queries or dbt tests.
- Case-sensitivity surprises: unquoted identifiers fold to uppercase. Quote consistently or stay unquoted.
- Large `ORDER BY` without `LIMIT`: costly sort spill.

## Review
- [ ] Queries are parameterized and read only the needed columns.
- [ ] Bulk loads use stages and are idempotent.
- [ ] Warehouse size, suspend and resource monitors are set.
- [ ] Service auth is key-pair/OAuth with a least-privilege role.
- [ ] Uniqueness is tested, since constraints are not enforced.
