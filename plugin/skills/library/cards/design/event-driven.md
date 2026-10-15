---
name: event-driven
title: Event-driven architecture
area: design
tags: [events, messaging, broker, outbox, consumers, at-least-once]
detect: [dep:kafkajs, dep:confluent-kafka, dep:aiokafka, dep:amqplib, dep:pika, dep:celery, dep:nats, dep:sarama]
related: [idempotency, sagas, event-sourcing, retries-backoff, background-jobs]
---
Services that communicate by publishing immutable facts, with at-least-once delivery, idempotent consumers and a transactional outbox.

## Verify
- `pytest -q tests/contract`: event schemas match what consumers expect (a contract suite you maintain).
- `kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders`: partitions and replication match the design (Kafka only).
- `rabbitmqctl list_queues name messages consumers`: no growing backlog or missing consumer (RabbitMQ only).
- `npm test` (or `go test -race ./...`): consumers tolerate duplicates and reordering.

## Test first
Deliver the same event twice and out of order, and assert the end state is correct once.
```python
def test_payment_captured_twice_credits_once(handler, db):
    ev = {"id": "e1", "type": "payment.captured", "order_id": "o1", "amount": 500}
    handler.handle(ev); handler.handle(ev)
    assert db.balance("o1") == 500
```

## Do
- Name events in the past tense as facts (`OrderPlaced`). Commands (`PlaceOrder`) are different and have one handler.
- Give every event an `id`, `type`, `occurred_at`, `schema_version` and a stable key for ordering (such as the aggregate ID).
- Write state and the outgoing event in the same DB transaction (outbox table), and publish from a relay.
- Deduplicate in consumers with a processed-ID table or natural idempotency, since delivery is at least once.
- Keep payloads self-sufficient or reference stable IDs. Do not make consumers call back for every event.
- Route poison messages to a dead-letter queue after bounded retries with alerts.
- Version schemas additively, and validate on both publish and consume (schema registry or JSON Schema).
- Partition by the ordering key. Order is only guaranteed within a partition or queue.

## Avoid
- Publishing after the DB commit in a separate step: a crash loses the event. Use an outbox.
- Assuming exactly-once: consumers must be idempotent, or duplicates double-charge.
- Global ordering assumptions across keys or partitions: design for per-key order only.
- Infinite retry of a failing message: it blocks the partition. Retry with backoff, then dead-letter.
- Events that mirror table rows (CRUD events): they leak internals. Publish business facts.
- Breaking a field type in an event: old messages in the log still exist. Add a field or new type version.

## Review
- [ ] State change and event emission are atomic (outbox or equivalent).
- [ ] Every consumer is idempotent, with a test delivering duplicates.
- [ ] Events carry id, type, version and ordering key, and schemas are checked in CI.
- [ ] There is a dead-letter path with an alert and a replay procedure.
- [ ] Ordering assumptions are limited to a single key.
