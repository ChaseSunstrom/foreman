---
name: etl-pipelines
title: ETL / ELT pipelines
area: data
tags: [etl, elt, pipelines, idempotency, backfill, data-quality]
detect: []
related: [airflow, dagster, prefect, dbt, spark, parquet-arrow, pandera, kafka]
---
Data pipelines that are idempotent per partition, validated at each boundary, safe to retry and backfill.

## Verify
- `pytest -q`: transform functions pass on small fixtures and a run-twice test.
- `python pipeline.py --date 2024-01-01 --dry-run`: the run plans its work and writes nothing (build a dry-run flag into every job).
- `python pipeline.py --date 2024-01-01 && python pipeline.py --date 2024-01-01`: the second run leaves identical output.
- `python -m pipeline.checks --date 2024-01-01`: row counts, null rates and key uniqueness for the output partition.

## Test first
Prove idempotency and bad-input handling before writing the load.
```python
def test_rerun_same_partition_is_idempotent(db, source):
    run(date="2024-01-01"); run(date="2024-01-01")
    assert db.scalar("select count(*) from fct_sales where ds='2024-01-01'") == len(source)

def test_bad_row_goes_to_quarantine(db):
    run(date="2024-01-02", rows=[{"id": None}])
    assert db.scalar("select count(*) from quarantine") == 1
```

## Do
- Parameterize every run by a logical date or interval; never read "now" inside a transform.
- Write by replacing a partition or merging on a key, so a retry produces the same state.
- Land raw data unchanged first, then transform; keep raw for replays.
- Validate schema, nulls, uniqueness and row counts at ingest and before publish; fail loudly or quarantine bad rows.
- Stage output in a temp location and swap or rename to publish atomically.
- Track watermarks or offsets in durable storage and advance them only after the load commits.
- Log row counts in and out, source versions and run ids; alert on freshness and volume anomalies.
- Support backfills by running the same code over a date range with bounded concurrency.

## Avoid
- Append-only loads on retry: duplicates. Replace the partition or merge by key.
- Using wall-clock time or the latest-state of a source to derive a historical partition: backfills diverge. Use the interval and event time.
- Advancing the watermark before the write commits: data gaps on failure. Commit first, then advance.
- Swallowing row errors silently: bad data flows downstream. Quarantine and count them.
- Loading everything into memory: out-of-memory on growth. Stream or process by chunk or partition.
- Transform logic coupled to the orchestrator: untestable. Keep pure functions with thin task wrappers.
- Full reloads every run when incremental is possible: cost and time. Use a reliable change column with a lookback window for late data.
- Hardcoded credentials and paths: use secrets managers and config.

## Review
- [ ] Re-running any partition gives identical output.
- [ ] Validation exists at ingest and publish, with a quarantine path.
- [ ] Watermarks advance only after commit.
- [ ] Late-arriving data and backfills are handled.
- [ ] Row counts, freshness and failures are observable.
