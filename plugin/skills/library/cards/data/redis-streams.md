---
name: redis-streams
title: Redis Streams
area: data
tags: [redis, streams, consumer-groups, queue, ack, messaging]
detect: []
related: [redis, kafka, nats, rabbitmq]
---
Redis Streams with consumer groups: at-least-once processing, pending entries, trimming and idempotent handlers.

## Verify
- `redis-cli XINFO STREAM orders`: length, last-generated-id, groups.
- `redis-cli XINFO GROUPS orders`: per-group pending count and lag.
- `redis-cli XPENDING orders workers - + 10`: stuck entries with idle time and delivery count.
- `redis-cli XLEN orders`: bounded by trimming, not growing forever.

## Test first
Test that an unacked message is redelivered and the handler is idempotent.
```python
def test_unacked_message_is_reclaimed(r):
    r.xgroup_create("s", "g", id="0", mkstream=True)
    r.xadd("s", {"k": "v"})
    r.xreadgroup("g", "c1", {"s": ">"}, count=1)          # c1 crashes, no ack
    _, claimed, _ = r.xautoclaim("s", "g", "c2", min_idle_time=0, start_id="0-0")
    assert len(claimed) == 1
```

## Do
- Create groups with `XGROUP CREATE s g $ MKSTREAM` (new entries only) or `0` (from the start).
- Read with `XREADGROUP GROUP g consumer COUNT n BLOCK ms STREAMS s >`; `XACK` only after the work succeeds.
- On start, drain your own pending list (read with id `0`) before reading `>`.
- Run a reclaimer: `XAUTOCLAIM s g consumer min-idle-time start` to take over entries from dead consumers.
- Make handlers idempotent (dedupe on entry id or a business key); delivery is at least once.
- Cap growth: `XADD s MAXLEN ~ 100000 * field value` or `XTRIM s MINID ~ <id>`.
- Send entries over a delivery-count limit (from XPENDING) to a dead-letter stream.
- Use a unique, stable consumer name per worker instance.

## Avoid
- Acking before processing: a crash loses the message. Ack after success.
- Never reading the pending list: failed messages sit forever. Reclaim with XAUTOCLAIM.
- Unbounded streams: memory exhaustion. Always trim, using the approximate `~` form for speed.
- Using `XREAD` (no group) for work distribution: every reader sees everything. Use groups.
- Trimming past entries a slow group has not read: silent data loss. Size MAXLEN from the slowest group lag.
- Random consumer names per restart: orphaned pending entries under dead names. Reuse names or reclaim.
- Assuming persistence equals Kafka durability: check AOF and replication settings.

## Review
- [ ] Ack follows successful handling; handlers idempotent.
- [ ] Reclaim and dead-letter paths exist and are tested.
- [ ] Trim policy sized to the slowest consumer.
- [ ] Group start id chosen deliberately.
- [ ] Persistence (AOF or replicas) matches the loss tolerance.
