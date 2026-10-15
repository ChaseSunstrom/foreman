---
name: kafka
title: Apache Kafka
area: data
tags: [kafka, streaming, messaging, consumers, producers, exactly-once]
detect: [dep:kafkajs, dep:confluent-kafka, dep:kafka-python, dep:aiokafka, dep:kafka-clients, dep:spring-kafka, dep:rdkafka, dep:segmentio/kafka-go, dep:IBM/sarama, dep:Confluent.Kafka]
related: [rabbitmq, nats, spark, etl-pipelines, elasticsearch]
---
Kafka producers and consumers: idempotent sends, keyed ordering, commit-after-process, idempotent handlers.

## Verify
- `kafka-topics.sh --bootstrap-server $BS --describe --topic T`: partitions, replication factor and ISR.
- `kafka-consumer-groups.sh --bootstrap-server $BS --describe --group G`: committed offsets and lag per partition.
- `kafka-console-consumer.sh --bootstrap-server $BS --topic T --from-beginning --max-messages 5`: what is actually on the topic.
- `kafka-configs.sh --bootstrap-server $BS --describe --entity-type topics --entity-name T`: retention and cleanup policy.

## Test first
Test against a real broker (container) or the client's mock; assert on redelivery.
```python
def test_handler_idempotent(db):
    msg = {"id": "e1", "amount": 5}
    handle(msg, db); handle(msg, db)   # redelivery
    assert db.balance() == 5
```
Fails until the handler dedupes on the event id.

## Do
- Set producer `acks=all` and `enable.idempotence=true`; handle delivery callbacks or await sends.
- Key messages by the entity whose order matters; ordering holds only within a partition.
- Disable auto-commit; commit offsets after processing succeeds.
- Make consumers idempotent (dedupe key or upsert), because delivery is at-least-once.
- Define a schema (Avro/Protobuf/JSON Schema) and evolve it compatibly.
- Send failures after bounded retries to a dead-letter topic with the error and original offset.
- Size partitions for the target parallelism; consumers in a group cannot exceed partition count.
- Handle rebalances: finish or abandon in-flight work and commit in the revoke callback.

## Avoid
- Auto-commit with slow processing: offsets commit before work finishes and messages are lost on crash. Commit manually after success.
- Fire-and-forget produce without `flush()` before exit: buffered messages vanish. Flush on shutdown.
- Assuming global ordering across partitions: use a key or one partition.
- Long processing between polls: exceeds `max.poll.interval.ms` and triggers rebalance loops. Offload and pause, or raise the limit.
- Poison messages retried forever, blocking a partition: route to a DLQ.
- Changing partition count of a keyed topic casually: remaps keys and breaks ordering.
- Unbounded consumer retries without backoff: hot loop on a failing dependency.

## Review
- [ ] Producer durability settings (`acks`, idempotence) are explicit.
- [ ] Offsets are committed only after the effect is durable.
- [ ] Handlers tolerate duplicate delivery.
- [ ] Message key matches the ordering requirement.
- [ ] A DLQ and lag alerting exist.
