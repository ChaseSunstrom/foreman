---
name: debezium
title: Debezium CDC
area: data
tags: [debezium, cdc, kafka-connect, postgres, mysql, outbox]
detect: [dep:debezium-core]
related: [kafka-connect, postgres-replication, kafka]
---
Debezium change data capture: connector config, snapshots, replication slot hygiene, outbox and tombstones.

## Verify
- `curl -s localhost:8083/connectors/NAME/status`: connector and task RUNNING.
- `psql -c "SELECT slot_name, active, restart_lsn FROM pg_replication_slots"`: the Debezium slot is active and advancing (Postgres source).
- `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic server.public.orders --from-beginning --max-messages 1`: a change event with before, after, op and source.
- `psql -c "SHOW wal_level"`: logical (Postgres). For MySQL, `SHOW VARIABLES LIKE 'binlog_format'` must be ROW.

## Test first
Fail on the event contract using a real source and a consumer.
```python
def test_update_event_carries_before_and_after(db, consume):
    db.execute("UPDATE orders SET status='paid' WHERE id=1")
    ev = consume("server.public.orders")
    assert ev["op"] == "u" and ev["after"]["status"] == "paid"
    assert ev["before"] is not None   # needs REPLICA IDENTITY FULL
```

## Do
- Postgres: use the `pgoutput` plugin, a dedicated `slot.name` and a `publication.name`; limit with `table.include.list`.
- Set `REPLICA IDENTITY FULL` on tables where consumers need the before image.
- Set `snapshot.mode` deliberately (`initial`, `schema_only`, `never`) and know that the initial snapshot of big tables takes time.
- Keep `topic.prefix` stable; changing it renames every topic.
- Use heartbeats (`heartbeat.interval.ms`) on low-traffic databases so the slot advances and WAL is released.
- Prefer the outbox pattern: write the event row in the same transaction, route it with the outbox event router SMT, instead of dual writes.
- Consumers must handle `op` values c, u, d, r and tombstones (null value after a delete) and be idempotent.
- Use signals or incremental snapshots to backfill without stopping the connector.

## Avoid
- Leaving a slot after removing the connector: WAL fills the disk. Drop the slot with `pg_drop_replication_slot`.
- Idle databases with no heartbeat: the slot's restart_lsn stalls and WAL piles up.
- Assuming exactly-once: delivery is at least once. Dedupe downstream.
- Unbounded `table.include.list` or regex: noise and cost. List the tables.
- Ignoring schema changes: a consumer breaks on a new column. Use a schema registry with compatibility rules.
- Primary-key-less tables: key-less events and no useful compaction. Add a key.
- Running against a read replica without checking support: logical slots need primary access on older versions.

## Review
- [ ] Slot and publication names are explicit; cleanup plan documented.
- [ ] Heartbeat configured; WAL retention monitored.
- [ ] Consumers idempotent and tombstone-aware.
- [ ] Snapshot mode matches the rollout.
- [ ] Schema evolution path tested.
