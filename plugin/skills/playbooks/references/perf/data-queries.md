<!-- Foreman's own playbook (written for Foreman, not ported). -->
# A data query or warehouse job is slow

Use when a Postgres, ClickHouse, DuckDB or MySQL query, or a batch job built on them, is slow or costly.

Built on the cards `fm lib show query-tuning`, `fm lib show postgres-indexes`, `fm lib show n-plus-one`, `fm lib show clickhouse`, `fm lib show duckdb` and `fm lib show parquet-arrow`.

1. **Count calls before tuning one:** a loop issuing one query per row (N+1) beats any index. Log query count per request.
2. **Read the plan on real data volumes:** `EXPLAIN (ANALYZE, BUFFERS) <query>` in Postgres, `EXPLAIN` in DuckDB or ClickHouse. A sequential scan on a big table, rows estimated far from actual, or a sort spilling to disk names the fix.
3. **Query before index.** Select only needed columns, filter early, avoid functions on indexed columns. Then add an index:
   ```bash
   psql -c "CREATE INDEX CONCURRENTLY idx_orders_user ON orders (user_id)"   # dev or staging only; for prod follow fix/migration.md
   psql -c "SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid"
   ```
   The second line finds a failed concurrent build.
4. **Columnar stores:** prune partitions and columns; read parquet with a filter pushed down rather than loading it whole.
5. **Prove it:** the plan and the timing before and after, same data, several runs.

Pass: the plan changed as predicted, the time fell outside the noise band, and the query result is identical (compare counts and a checksum).

Never add an index to production without the migration playbook.
