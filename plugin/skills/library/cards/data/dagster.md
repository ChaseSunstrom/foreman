---
name: dagster
title: Dagster
area: data
tags: [dagster, orchestration, assets, pipelines, python, partitions]
detect: [dep:dagster, dep:dagster-webserver, dep:dagster-dbt, dep:dagster-aws, dep:dagster-postgres, dep:dagster-pandas, file:dagster.yaml, file:workspace.yaml]
related: [airflow, prefect, dbt, etl-pipelines, pandera]
---
Dagster: software-defined assets with resources, partitions and asset checks, tested by materializing in process.

## Verify
- `dagster definitions validate`: code location loads and definitions resolve.
- `dagster asset materialize --select my_asset -m my_package`: the asset materializes locally.
- `pytest -q`: asset functions and `materialize([...])` runs pass in process.
- `dagster dev -m my_package`: UI and daemon start so you can inspect the asset graph.

## Test first
Call assets as plain functions for logic; use `materialize` with test resources for wiring.
```python
from dagster import materialize

def test_clean_orders_drops_nulls():
    out = materialize([raw_orders, clean_orders], resources={"warehouse": FakeWarehouse()})
    assert out.success
    assert out.output_for_node("clean_orders").null_count().sum() == 0
```

## Do
- Model data as `@asset` with dependencies by parameter name or `deps=[...]`; return the value or write via an IO manager.
- Put external systems behind `ConfigurableResource` subclasses so tests inject fakes.
- Use `StaticPartitionsDefinition`/`DailyPartitionsDefinition` with `context.partition_key` to make runs idempotent per partition.
- Attach `@asset_check` for quality rules and `freshness` policies for staleness.
- Add schedules and sensors with `define_asset_job`; keep them in `Definitions`.
- Return `MaterializeResult(metadata={...})` to record row counts and sample data.
- Load config through `Config` classes (typed run config), secrets through `EnvVar`.
- Register everything in a single `Definitions(assets=..., resources=..., schedules=...)`.

## Avoid
- Reading `os.environ` or building clients inside asset bodies: untestable. Use resources and `EnvVar`.
- Op/graph/`@job` style for new data work: asset-based modelling gives lineage. Reach for assets first.
- Unpartitioned assets that rebuild everything daily: slow, no backfill. Partition by time.
- Side effects outside the asset's declared outputs: lineage lies. Declare outputs or `deps`.
- Heavy top-level code at import: slows code-location loading. Defer into the asset.
- Passing large objects through the default IO manager (pickle on local disk) in production: use a Parquet/warehouse IO manager.
- Skipping checks: bad data propagates downstream silently.

## Review
- [ ] All definitions load via `dagster definitions validate`.
- [ ] External systems are resources with test doubles.
- [ ] Partitions and idempotent writes cover reruns and backfills.
- [ ] Asset checks exist for key quality rules.
- [ ] Config and secrets come from typed config and `EnvVar`.
