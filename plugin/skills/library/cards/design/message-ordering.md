---
name: message-ordering
title: Message ordering
area: design
tags: [ordering, messaging, partitions, kafka, sequence, deduplication]
detect: []
related: [outbox-pattern, idempotency, event-driven, event-schemas, backpressure]
---
Ordering is guaranteed only within a partition key; design consumers to tolerate reordering, duplicates and redelivery outside it.

## Verify
- `pytest -q -k ordering`: out-of-order and duplicate delivery tests.
- `kafka-topics.sh --describe --topic TOPIC --bootstrap-server HOST:9092`: partition count and replication (Kafka stacks).
- `git grep -nE "key=|partition_key|MessageGroupId" -- src`: producers set an explicit key.

## Test first
Deliver a stream shuffled and duplicated; final state must equal the in-order result.
```python
def test_consumer_converges_under_reorder_and_duplicates():
    events = [Evt("o1", v=1, status="created"), Evt("o1", v=2, status="paid"),
              Evt("o1", v=3, status="shipped")]
    for delivery in ([2, 0, 1], [2, 2, 1, 0, 0], [0, 1, 2]):
        db = FakeDb()
        for i in delivery:
            handle(db, events[i])
        assert db.get("o1") == {"status": "shipped", "version": 3}
```

## Do
- Choose the key so everything needing relative order shares it (aggregate id, account id). One partition (or message group, FIFO queue group) per key.
- Put a per-key monotonic `version` or sequence on each event; the consumer applies only if `version > stored` (drop stale) and parks or waits on gaps.
- Make handlers idempotent: dedupe by event id or version.
- Keep a single in-flight message per key in a consumer; parallelise across keys.
- For retries, use per-key blocking or a retry topic that preserves the key; do not let a failed message be overtaken silently unless versions guard it.
- Size partitions for peak parallelism up front; changing the count remaps keys.
- Do not depend on cross-key ordering; use causal ids or timestamps from a trusted source only for tie-breaks.

## Avoid
- Assuming global order across partitions: it does not exist. Use per-key order or a single partition.
- Wall-clock ordering from different producers: skew reorders. Use version or sequence per aggregate.
- Concurrent consumers on the same key: race. Route by key to one worker.
- Retry queue that re-enqueues at the tail: it reorders. Keep the key and check versions.
- Increasing partitions on a live keyed topic without a plan: ordering breaks during the remap.

## Review
- [ ] Ordering scope (the key) is explicit and justified.
- [ ] Consumers apply versions and drop stale or duplicate events.
- [ ] Per-key serialisation in workers.
- [ ] Retry path preserves order guarantees or is guarded.
