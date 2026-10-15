---
name: cassandra
title: Cassandra / ScyllaDB
area: data
tags: [nosql, cassandra, scylla, cql, partitions, wide-column]
detect: [dep:cassandra-driver, dep:scylla-driver, dep:gocql/gocql, dep:cassandra-driver-core, dep:java-driver-core, dep:CassandraCSharpDriver, dep:scylla, dep:cassandra-client]
related: [dynamodb, kafka, query-tuning]
---
Cassandra/Scylla: tables modeled per query, bounded partitions, prepared statements, explicit consistency.

## Verify
- `cqlsh -e "DESCRIBE KEYSPACE ks"`: schema, replication and table options as deployed.
- `cqlsh -e "TRACING ON; SELECT ... WHERE pk = ?"`: the query touches one partition and few SSTables.
- `nodetool tablestats ks.table`: partition sizes, tombstones per read, SSTable counts.
- `nodetool status`: all nodes UN (up and normal).

## Test first
Run a single-node container; create the keyspace from the same CQL as production.
```python
def test_orders_by_user_sorted(session):
    for i in (1, 3, 2):
        session.execute("insert into orders_by_user(user_id, ts, id) values (%s,%s,%s)", (U, i, i))
    rows = session.execute("select ts from orders_by_user where user_id=%s", (U,))
    assert [r.ts for r in rows] == [3, 2, 1]  # clustering order DESC
```

## Do
- Design one table per query: partition key for distribution and lookup, clustering columns for order within it.
- Keep partitions bounded (tens of MB); add a time bucket to the partition key for time series.
- Use prepared statements and bind values; reuse the session for the process lifetime.
- Pick consistency per query (`LOCAL_QUORUM` read and write for strong-ish reads); set `NetworkTopologyStrategy`.
- Make writes idempotent (inserts are upserts); use `IF NOT EXISTS` (LWT) only for rare uniqueness.
- Use TTLs and `TimeWindowCompactionStrategy` for time-series data.
- Page results with the driver's paging state.

## Avoid
- `ALLOW FILTERING` in production queries: full scans. Add a table shaped for the query.
- Secondary indexes on high-cardinality or frequently updated columns: slow and unscalable. Denormalize.
- Unbounded partitions (e.g. all events for one user): hot, huge partitions. Bucket by time.
- Heavy use of deletes or null writes: tombstones slow reads. Use TTL and avoid explicit nulls in inserts.
- Logged batches across partitions for speed: coordinator overload. Batch only within one partition.
- `SimpleStrategy` in production: ignores racks and datacenters. Use `NetworkTopologyStrategy`.
- Read-before-write counters or lists: races. Use counters or collections properly.

## Review
- [ ] Each query hits a single partition by full partition key.
- [ ] Partition size is bounded by design (bucketing).
- [ ] Statements are prepared; consistency level is explicit.
- [ ] No ALLOW FILTERING, no cross-partition batches.
- [ ] TTL and compaction match the data lifecycle.
