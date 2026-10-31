<!-- Foreman's own playbook (written for Foreman, not ported). -->
# A data pipeline run fails or writes wrong rows

Use when an Airflow, Dagster, dbt, Kafka or ETL job fails, hangs, duplicates rows or loads the wrong ones.

Built on the cards `fm lib show airflow`, `fm lib show dagster`, `fm lib show dbt`, `fm lib show kafka` and `fm lib show etl-pipelines`.

1. **Pin the run:** which partition or data interval, which code version, which input snapshot. Without it you are guessing.
2. **Does it load?** `airflow dags list-import-errors`, `dagster definitions validate`, `dbt parse`. An import error looks like a scheduler outage.
3. **Reproduce one partition locally** with a dry run and a tiny fixture:
   ```bash
   dbt build --select state:modified+ --state path/to/prod-artifacts --target dev
   python pipeline.py --date 2024-01-01 --dry-run
   kafka-consumer-groups.sh --bootstrap-server $BS --describe --group G
   ```
4. **Idempotence test first:** run the same partition twice and compare output. If the second run differs, the bug is the write (append instead of replace), not the read.
5. **Fix at the boundary** the bad data crossed (the schema check or the key), not by patching rows downstream.
6. **Backfill deliberately:** one partition, verify counts and a checksum, then the range, capped.

Pass: the failing partition reruns twice with identical output, the new test fails before the fix and passes after, and the DAG, asset or model loads clean.

Stop before touching production tables; a backfill needs the owner's yes.
