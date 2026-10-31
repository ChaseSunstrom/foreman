<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Verify a data transform or table change

Use when a dbt model, SQL transform, parquet export or dataframe step changed and you must show the data is still right, not just that the job exits 0.

Built on the cards `fm lib show dbt`, `fm lib show pandera`, `fm lib show parquet-arrow`, `fm lib show duckdb` and `fm lib show etl-pipelines`.

1. **Contract first:** keys unique, not null, foreign keys present. `dbt test --select model_name`, or a `pandera` schema on the dataframe at the boundary.
2. **Parse and build only what changed:** `dbt parse`, then `dbt build --select state:modified+ --state path/to/prod-artifacts --target dev` (never the prod target).
3. **Diff old against new on the same input.** Row count, distinct keys, sums of money columns, min and max dates:
   ```bash
   duckdb -c "SELECT count(*), count(DISTINCT id), sum(amount) FROM read_parquet('old/*.parquet')"
   duckdb -c "SELECT count(*), count(DISTINCT id), sum(amount) FROM read_parquet('new/*.parquet')"
   ```
   An unexplained difference is a finding; an explained one goes in the report.
4. **Idempotence:** run the job twice for one partition and compare the outputs.
5. **Schema drift:** compare column names and types of the parquet files, since a silent type widening breaks readers.

Pass: tests exit 0, the diff is zero or each difference is named and intended, and the second run matches the first.

Never validate with the same query that built the table.
