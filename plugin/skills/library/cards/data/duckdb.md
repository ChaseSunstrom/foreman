---
name: duckdb
title: DuckDB
area: data
tags: [olap, duckdb, embedded, parquet, analytics, sql]
detect: [dep:duckdb, dep:duckdb-engine, dep:@duckdb/node-api, dep:duckdb-async, dep:go-duckdb, dep:duckdb_rs, dep:DuckDB.NET.Data.Full]
related: [parquet-arrow, sqlite, etl-pipelines, dbt]
---
DuckDB: embedded columnar SQL over Parquet/CSV and dataframes; one writer process, parameterized queries.

## Verify
- `duckdb app.duckdb "EXPLAIN ANALYZE <query>"`: operators, row counts and timings.
- `duckdb -c "DESCRIBE SELECT * FROM 'data/*.parquet'"`: inferred schema of the files.
- `duckdb app.duckdb "PRAGMA database_size;"`: file size and memory use.
- `duckdb -c "SELECT * FROM parquet_metadata('f.parquet') LIMIT 5"`: row groups and statistics enabling pruning.

## Test first
Use `duckdb.connect(":memory:")` per test; load fixtures from a tiny inline table.
```python
def test_daily_totals():
    con = duckdb.connect()
    con.execute("create table t as select * from (values ('2024-01-01', 5), ('2024-01-01', 7)) v(d, n)")
    assert con.execute("select sum(n) from t group by d").fetchone() == (12,)
```
Swap the real query in and run it against the fixture first.

## Do
- Query files in place (`read_parquet('p/*.parquet')`, `read_csv`) and push filters so row groups are skipped.
- Bind values: `con.execute("select * from t where id = ?", [x])`.
- Query pandas/Arrow/Polars objects directly by variable name, and return Arrow (`.arrow()`/`.fetch_arrow_table()`) to avoid copies.
- Write results with `COPY (select ...) TO 'out.parquet' (FORMAT PARQUET)` and partition with `PARTITION_BY`.
- Set `memory_limit` and `threads` explicitly in constrained environments, and set `temp_directory` for spilling.
- Keep one read-write connection per database file; use `read_only=True` for others.
- Specify CSV types (`columns=`, `types=`) for stability instead of auto-detect in pipelines.

## Avoid
- Multiple processes opening a database file read-write: lock errors. One writer, others read-only.
- Using it as a high-concurrency OLTP store: single-writer, row-at-a-time inserts are slow. Batch with `INSERT ... SELECT` or appenders.
- Row-by-row `INSERT` loops from Python: use `executemany` sparingly, prefer `INSERT INTO t SELECT * FROM df`.
- Relying on CSV auto-detect with drifting inputs: type changes between files. Declare the schema.
- `.fetchall()` on large results: pulls everything into Python. Stream with `fetch_record_batch`.
- Interpolating values or paths into SQL strings: injection. Bind parameters for values.

## Review
- [ ] Filters and column selection happen in SQL, not after fetching to Python.
- [ ] Concurrency model is single writer.
- [ ] File schemas are declared for pipeline inputs.
- [ ] Memory and temp-directory limits are set where it runs.
- [ ] Output files are written with a compression and partitioning plan.
