---
name: influxdb
title: InfluxDB
area: data
tags: [influxdb, time-series, tags, fields, retention, line-protocol]
detect: [dep:influxdb-client, dep:influxdb3-python, dep:influxdb]
related: [timescaledb, data-modeling, clickhouse]
---
InfluxDB time series: tag versus field design, series cardinality, retention, batched line-protocol writes.

## Verify
- `influx bucket list`: buckets and their retention periods (InfluxDB 2.x CLI).
- `influx query 'from(bucket:"b") |> range(start:-5m) |> limit(n:5)'`: recent points arrive with expected tags and fields.
- `influx query 'import "influxdata/influxdb" influxdb.cardinality(bucket:"b", start:-30d)'`: series cardinality is bounded.
- `influx ping`: server reachable and healthy.

## Test first
Test the mapping from domain object to point, including tag cardinality choices.
```python
def test_point_uses_low_cardinality_tags():
    p = to_point(Reading(host="h1", region="eu", request_id="r-9", temp=21.5))
    line = p.to_line_protocol()
    assert "request_id" not in line.split(" ")[0]      # not a tag
    assert "temp=21.5" in line and "region=eu" in line
```

## Do
- Tags: indexed, low-cardinality strings you filter and group by (host, region). Fields: the measured values, unindexed.
- Keep measurement and tag names stable and short; schema is implicit in the first write.
- Write in batches (the client's batching write API, hundreds to thousands of points) with a flush on shutdown and error callbacks.
- Set bucket retention to the real need; downsample with tasks into a longer-retention bucket.
- Use explicit nanosecond or consistent precision timestamps.
- Query with a tight `range()` first, then `filter()` on tags, then aggregate (`aggregateWindow`).
- Use API tokens scoped to a bucket, with read and write separated.
- Keep field types consistent per field; a conflicting type write is rejected.

## Avoid
- Unique ids (request id, user id, UUID) as tags: series cardinality explodes, memory and query time with it. Make them fields or drop them.
- Synchronous per-point writes: huge overhead. Batch.
- A query with no `range()` or a huge window: full scan. Always bound time.
- Writing a field as int then float: type conflict errors. Pick one, write floats consistently.
- All-powerful operator tokens in applications: scope them per bucket.
- Infinite retention by default for high-rate data: disk fills. Set retention and downsample.
- Ignoring write errors from the async client: silent data loss. Register an error callback.

## Review
- [ ] Tag cardinality estimated and bounded.
- [ ] Writes batched with flush on shutdown and error handling.
- [ ] Retention and downsampling defined.
- [ ] Queries always bound by time and tags.
- [ ] Tokens scoped.
