---
name: airflow
title: Apache Airflow
area: data
tags: [airflow, orchestration, dags, scheduling, pipelines, python]
detect: [dep:apache-airflow, dep:apache-airflow-providers-*, file:airflow.cfg, file:dags/*.py]
related: [dagster, prefect, dbt, spark, etl-pipelines]
---
Airflow DAGs: light top-level code, idempotent tasks keyed to the data interval, retries, and work done outside the scheduler.

## Verify
- `airflow dags list-import-errors`: no DAG fails to import.
- `python dags/my_dag.py`: the file imports cleanly and builds the DAG object.
- `airflow tasks test my_dag my_task 2024-01-01`: one task runs for a date without recording state.
- `airflow dags test my_dag 2024-01-01`: the whole DAG runs locally for a date.

## Test first
Load all DAGs with `DagBag` and assert structure; then unit-test task callables as plain functions.
```python
from airflow.models import DagBag

def test_dags_load_and_have_retries():
    bag = DagBag(dag_folder="dags", include_examples=False)
    assert not bag.import_errors
    dag = bag.get_dag("daily_sales")
    assert dag.default_args["retries"] >= 2
```

## Do
- Use the TaskFlow API (`@dag`, `@task`) and set `schedule`, `start_date`, `catchup` explicitly.
- Make tasks idempotent and keyed to `data_interval_start`/`data_interval_end`, writing with overwrite or merge.
- Set `retries`, `retry_delay`, `execution_timeout` and `max_active_runs` in `default_args`/DAG.
- Pass small values by XCom and large data by object storage or tables with a path passed along.
- Read secrets from Connections and Variables via the secrets backend, using hooks and `conn_id`.
- Use pools and `max_active_tasks` to cap load on shared systems.
- Push heavy compute to Spark, dbt or a warehouse; keep Airflow as the coordinator.
- Use sensors in `mode="reschedule"` or deferrable operators to avoid hogging worker slots.

## Avoid
- Heavy imports, API calls or DB queries at module top level: parsed every few seconds by the scheduler. Do them inside tasks.
- `datetime.now()` or a dynamic `start_date`: runs never line up. Use a fixed date and the logical date/interval.
- Large payloads through XCom: bloats the metadata DB. Pass references.
- `catchup` left at default with an old start_date: floods of backfill runs. Set it deliberately.
- Non-idempotent appends: retries and backfills duplicate data. Overwrite the partition.
- Secrets hardcoded or in Variables as plain text: use Connections and a secrets backend.
- Old import paths (`airflow.operators.python_operator`): removed. Use `airflow.operators.python` or `airflow.decorators`.

## Review
- [ ] DAG imports fast and has no top-level side effects.
- [ ] Each task is safe to retry and re-run for a past interval.
- [ ] Schedule, start_date, catchup, retries and timeouts are explicit.
- [ ] Data moves via storage, not XCom; secrets via connections.
- [ ] Sensors and pools protect shared resources.
