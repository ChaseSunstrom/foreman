---
name: postgres-replication
title: PostgreSQL replication
area: data
tags: [postgres, replication, wal, logical, standby, lag, slots]
detect: []
related: [postgres, debezium, pgbouncer, postgres-locking]
---
Streaming and logical replication: measure lag, protect WAL from slots, and handle read-your-writes.

## Verify
- `psql -c "SELECT client_addr, state, sent_lsn, replay_lsn, replay_lag FROM pg_stat_replication"`: on the primary, each standby and its lag.
- `psql -c "SELECT now() - pg_last_xact_replay_timestamp() AS lag, pg_is_in_recovery()"`: on a standby, replay delay.
- `psql -c "SELECT slot_name, active, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained FROM pg_replication_slots"`: inactive slots retaining WAL.
- `psql -c "SHOW wal_level"`: must be logical for logical replication or CDC.

## Test first
Fail on the guarantee you rely on: a read after write on a replica.
```python
def test_read_your_write_uses_primary(primary, replica, api):
    api.post("/orders", json={"sku": "a"})
    r = api.get("/orders/latest")   # must route to primary right after a write
    assert r.json()["sku"] == "a"
```
Alert checks (lag, slot retention) are separate monitors; assert their queries return rows.

## Do
- Use `hot_standby` replicas for reads; route writes and read-after-write to the primary.
- Logical replication: `CREATE PUBLICATION p FOR TABLE t`, `CREATE SUBSCRIPTION s CONNECTION '...' PUBLICATION p`. Tables need a primary key or `REPLICA IDENTITY` set.
- Set `max_slot_wal_keep_size` so an abandoned slot cannot fill the disk.
- Monitor lag in bytes (`pg_wal_lsn_diff`) and time; page on both.
- Sync replication: `synchronous_standby_names` plus `synchronous_commit`, knowing writes stall if the standby is down.
- Run schema changes on the subscriber first for additive logical changes; DDL is not replicated.
- Test failover (promotion with `pg_ctl promote` or your manager) regularly.

## Avoid
- Dropping a consumer but leaving its slot: WAL grows until the disk fills. Drop with `pg_drop_replication_slot`.
- Assuming logical replication copies DDL, sequences or large objects: it does not; sync them separately.
- Long queries on a standby with default settings: replay conflicts cancel them. Tune `max_standby_streaming_delay` or `hot_standby_feedback` knowingly (feedback bloats the primary).
- Tables without a key in a publication that does updates or deletes: the apply fails. Add a key or `REPLICA IDENTITY FULL`.
- Reading from a replica right after writing: stale. Pin to the primary or wait for an LSN.

## Review
- [ ] Slot retention capped and alerted.
- [ ] Lag measured and thresholds documented.
- [ ] Read-after-write paths do not hit replicas.
- [ ] Every published table has a replica identity.
- [ ] Failover procedure tested and written down.
