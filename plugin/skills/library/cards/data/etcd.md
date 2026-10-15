---
name: etcd
title: etcd
area: data
tags: [etcd, consensus, kv, leases, watch, raft]
detect: [dep:etcd3, dep:go.etcd.io/etcd/client/v3, dep:jetcd-core]
related: [redis-locks, kafka, postgres-locking]
---
etcd as a coordination store: transactions, leases, watches with revisions, compaction and quota limits.

## Verify
- `etcdctl endpoint health --cluster`: all members healthy.
- `etcdctl endpoint status --cluster -w table`: leader, DB size and raft index per member.
- `etcdctl alarm list`: no NOSPACE alarm.
- `etcdctl get /app/ --prefix --keys-only`: the key layout under your prefix.

## Test first
Test lease expiry and compare-and-swap against an embedded or containerized etcd.
```python
def test_cas_and_lease_expiry(etcd):
    lease = etcd.lease(2)
    ok, _ = etcd.transaction(
        compare=[etcd.transactions.version("/lock") == 0],
        success=[etcd.transactions.put("/lock", "me", lease=lease)], failure=[])
    assert ok
    time.sleep(3)
    assert etcd.get("/lock")[0] is None
```

## Do
- Use transactions (`Txn` with compare, then, else) for compare-and-swap rather than read then write.
- Attach ephemeral keys to a lease and keep it alive with `KeepAlive`; handle the keep-alive channel closing.
- Watch from a known revision (`WithRev(lastSeen+1)`) and handle compaction errors by re-listing then re-watching.
- Use the client's lock or election recipe (`concurrency.NewMutex`, `NewElection`) tied to a session lease.
- Keep values small (a few KB at most); etcd is for metadata, not blobs. The default request limit is about 1.5 MiB.
- Run an odd number of members (3 or 5) on fast disks; monitor fsync latency.
- Enable auto-compaction (`--auto-compaction-retention`) and defragment members with `etcdctl defrag` one at a time.
- Use TLS and role-based auth; scope clients to key prefixes.
- Set client dial and request timeouts with context deadlines.

## Avoid
- Writing large or high-churn data: DB size hits the quota (`--quota-backend-bytes`), then the cluster goes read-only with a NOSPACE alarm. Compact, defrag, then `etcdctl alarm disarm`.
- Watching without handling compaction and disconnects: missed events. Resume from the revision and re-sync on error.
- A lock without a lease TTL: a crashed holder blocks forever.
- Even-sized clusters (2 or 4): no more fault tolerance than the next lower odd size.
- Using wall-clock for ordering: use revisions.
- Running on slow or shared disks: leader elections flap.

## Review
- [ ] Mutations that depend on state use transactions.
- [ ] Leases and keep-alives handled, with failure paths.
- [ ] Watch resumes from revision and handles compaction.
- [ ] Compaction, defrag and quota alarms monitored.
- [ ] Auth and TLS enabled.
