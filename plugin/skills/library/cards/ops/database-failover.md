---
name: database-failover
title: Database failover
area: ops
tags: [database, failover, replication, postgres, promotion, drills]
detect: [file:patroni*.yml, file:pg_hba.conf]
related: [backups-restore, disaster-recovery, load-balancing, runbooks]
---
Prove failover with a drill: kill the primary, time promotion, check no acknowledged write is lost, and rejoin the old primary safely.

## Verify
- `psql -Atc "select pg_is_in_recovery()"`: `f` on the primary, `t` on a replica (PostgreSQL).
- `psql -Atc "select client_addr, state, sync_state, replay_lag from pg_stat_replication"`: replicas attached, streaming, and their lag (run on the primary).
- `psql -Atc "select now() - pg_last_xact_replay_timestamp()"`: replay delay on a replica.
- `psql -Atc "select pg_current_wal_lsn()"`: the primary's write position, to compare with replicas.
- `patronictl list`: cluster roles and timelines, when Patroni manages it.

## Test first
The drill fails first: write a marker row continuously, kill the primary, and count lost acknowledged writes.
```sh
i=0
while true; do
  i=$((i+1))
  psql "$WRITER_DSN" -qAtc "insert into drill(n) values ($i)" && echo $i >> acked.txt
  sleep 0.05
done &
sleep 10; ssh db1 'systemctl kill -s KILL postgresql'   # the primary
sleep 60; kill %1
last=$(tail -1 acked.txt)
psql "$WRITER_DSN" -Atc "select count(*) from drill where n <= $last"   # must equal $last for sync replication
```
Record time to promotion and the number of failed writes, then compare them with RTO and RPO.

## Do
- Decide the RPO: synchronous replication loses nothing but adds latency and can stall on replica loss; asynchronous is fast but can lose the tail. Write the choice down.
- Use a proven manager (Patroni, a managed service) with a consensus store to avoid split brain; do not script promotion by hand without fencing.
- Give clients one stable endpoint (a virtual IP, proxy, or DNS with low TTL) and make drivers retry and reconnect.
- Monitor replication lag, replica state, WAL archive health, and timeline changes, and alert on them.
- Fence the old primary (stop it or block it) before promoting, and rebuild it as a replica with `pg_rewind` or a fresh base backup.
- Keep WAL archiving and base backups separate from replication; a replica copies mistakes, including a bad `DROP`.
- Drill on a schedule in staging, and in production during a quiet window once confidence exists.
- Test planned switchover separately from crash failover.

## Avoid
- Promoting a replica while the old primary may still accept writes: split brain and divergent data. Fence first.
- Treating replication as backup: deleted data replicates. Keep point-in-time recovery backups.
- App connection strings pointing to a host name: failover needs a code change. Use a stable endpoint.
- Ignoring replica lag: promotion loses minutes of writes. Alert on lag and refuse promotion past a limit.
- Untested automatic failover: it first runs during the outage. Drill it and review the manager's timeouts.
- Bringing the old primary back with no rewind: its timeline diverged. Rewind or reseed it before it rejoins.

## Review
- [ ] RPO, RTO, and the sync or async choice are written down.
- [ ] A failover drill ran recently with measured promotion time and lost writes.
- [ ] Fencing and split-brain protection exist.
- [ ] Clients reconnect through a stable endpoint.
- [ ] Lag, WAL archive, and timeline alerts exist, with PITR backups separate from replication.
