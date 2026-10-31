<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Incident: a data pipeline is late, stuck or wrong

Use when a stream or batch pipeline stops, lags, or feeds wrong data to people who depend on it: Kafka consumers behind, a Debezium connector failed, a replica far behind.

Built on the cards `fm lib show kafka`, `fm lib show debezium`, `fm lib show postgres-replication` and `fm lib show airflow`. Declare it first with the incident playbook; this one is the data-side triage.

1. **Stop the spread:** pause the downstream consumers or the publishing job if bad data is flowing; stale data is better than wrong data.
2. **Where does the flow stop?** Check each hop in order:
   ```bash
   kafka-consumer-groups.sh --bootstrap-server $BS --describe --group G
   curl -s localhost:8083/connectors/NAME/status
   psql -c "SELECT client_addr, state, replay_lag FROM pg_stat_replication"
   ```
   Consumer lag growing means a slow or dead consumer; a FAILED connector task needs its trace; an inactive replication slot is retaining WAL and can fill the disk.
3. **Disk first:** `pg_replication_slots` retained WAL is the one that turns lag into an outage. Mitigate before diagnosing.
4. **Recover in order:** restart the failed hop, confirm lag falls, then replay or backfill only the affected range.
5. **Check the data, not the dashboard:** sample rows and counts at the sink for the incident window.
6. **Follow-ups with owners:** an alert on lag and on slot size, and a dead-letter path.

Pass: lag is back inside its threshold and counts at the sink match the source for the window.
