---
name: dbt
title: dbt
area: data
tags: [dbt, analytics-engineering, sql, warehouse, models, tests]
detect: [file:dbt_project.yml, dep:dbt-core, dep:dbt-postgres, dep:dbt-snowflake, dep:dbt-bigquery, dep:dbt-duckdb, dep:dbt-redshift, dep:dbt-databricks]
related: [snowflake, bigquery, duckdb, airflow, etl-pipelines, sql-migrations]
---
dbt projects: layered models (staging, intermediate, marts), schema tests on every key, incremental models that are safe to re-run.

## Verify
- `dbt parse`: project, refs and YAML are valid without touching the warehouse.
- `dbt build --select state:modified+`: changed models and their dependents run with their tests and seeds.
- `dbt test --select model_name`: unique, not_null, relationships and custom tests pass.
- `dbt compile --select model_name`: rendered SQL is what you intend.
- `dbt docs generate`: docs and lineage build.

## Test first
Write the schema test before the model. Add data tests in YAML, and unit tests (dbt 1.8+) for logic.
```yaml
models:
  - name: dim_customers
    columns:
      - name: customer_id
        tests: [unique, not_null]
      - name: region_id
        tests:
          - relationships: {to: ref('dim_regions'), field: region_id}
```
`dbt test --select dim_customers` fails until the model exists and is correct.

## Do
- Layer models: `stg_` (rename, cast, one source each), `int_` (joins), marts (`dim_`, `fct_`).
- Use `{{ ref() }}` and `{{ source() }}` only; never hardcode schema or table names.
- Declare `unique` and `not_null` on every primary key and `relationships` on foreign keys.
- Set incremental models with `unique_key`, an `is_incremental()` filter and an `on_schema_change` policy.
- Add source freshness (`freshness`, `loaded_at_field`) and run `dbt source freshness`.
- Put config in `dbt_project.yml` by folder (materialization, schema) rather than per model.
- Use `--target` for dev/prod separation and CI with `--defer --state` to build only what changed.
- Document models and columns in YAML; use `contract: {enforced: true}` on public marts.

## Avoid
- Hardcoded `database.schema.table` references: breaks environments and lineage. Use `ref`/`source`.
- Incremental models without a `unique_key` or with a filter on a non-monotonic column: duplicates and gaps. Key and filter on a reliable timestamp, with a lookback.
- Business logic in staging models: staging only cleans. Move logic to intermediate or marts.
- `select *` from sources: upstream column adds break models silently. List columns.
- Tests only on marts: failures surface late. Test at staging boundaries.
- Running `dbt run` then `dbt test` separately in CI: bad data is already built. Use `dbt build`.
- Committing `target/` and `dbt_packages/`: gitignore them.

## Review
- [ ] Every model has key tests; foreign keys have relationships tests.
- [ ] No hardcoded relations; refs resolve in all targets.
- [ ] Incremental models are re-runnable and tested with a full refresh.
- [ ] Layering is respected and marts have docs and contracts.
- [ ] CI runs `dbt build` on changed models.
