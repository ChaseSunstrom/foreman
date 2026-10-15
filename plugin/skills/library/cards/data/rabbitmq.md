---
name: rabbitmq
title: RabbitMQ
area: data
tags: [rabbitmq, amqp, messaging, queues, acks, dead-letter]
detect: [dep:pika, dep:aio-pika, dep:kombu, dep:amqplib, dep:amqp-connection-manager, dep:lapin, dep:amqp091-go, dep:RabbitMQ.Client, dep:spring-boot-starter-amqp, dep:bunny]
related: [kafka, nats, redis]
---
RabbitMQ: durable queues, publisher confirms, manual acks with prefetch, dead-letter exchanges, idempotent consumers.

## Verify
- `rabbitmqctl list_queues name messages_ready messages_unacknowledged consumers`: backlog, stuck unacked messages, consumer count.
- `rabbitmqctl list_bindings`: exchange to queue routing as declared.
- `rabbitmqctl list_connections name state`: connections are running, not blocked.
- `rabbitmq-diagnostics check_running`: node is up.

## Test first
Use a real broker (container); declare topology via the same function as production.
```python
def test_failed_message_dead_lettered(ch):
    publish(ch, b"bad")
    consume_once(ch, handler=lambda m: 1/0)   # nacks, requeue=False
    method, _, body = ch.basic_get("jobs.dlq", auto_ack=True)
    assert body == b"bad"
```
Fails until the queue has `x-dead-letter-exchange` and the consumer nacks without requeue.

## Do
- Declare exchanges and queues `durable=True` and publish with `delivery_mode=2` (persistent) for data that must survive restarts.
- Enable publisher confirms and wait for them before treating a publish as done.
- Consume with manual ack after the work succeeds; set `prefetch_count` (QoS) to bound in-flight messages.
- Set a dead-letter exchange and a message TTL or retry-delay queue for failures.
- Make handlers idempotent: redelivery happens after crashes and nacks.
- Use quorum queues for replicated durability; one connection per process, a channel per thread.
- Declare topology idempotently at startup with identical arguments.

## Avoid
- `auto_ack=True` on work you cannot lose: crash drops the message. Ack manually.
- `nack(requeue=True)` on a permanently failing message: infinite hot loop. Dead-letter it.
- No prefetch limit: one consumer hoards the backlog and memory. Set QoS.
- Sharing a channel across threads: not thread-safe in most clients. One channel per thread.
- Redeclaring a queue with different arguments: `PRECONDITION_FAILED`. Delete or version the queue name.
- Non-durable queue with persistent messages: queue disappears on restart. Make both durable.
- Ignoring connection blocked notices and heartbeats: silent stalls. Handle reconnect with backoff.

## Review
- [ ] Queues durable, messages persistent, confirms awaited where loss matters.
- [ ] Acks happen after the effect is committed; prefetch is set.
- [ ] Failure path leads to a DLQ with bounded retries.
- [ ] Handlers tolerate duplicates.
- [ ] Reconnect logic exists.
