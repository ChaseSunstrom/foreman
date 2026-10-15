---
name: nats
title: NATS / JetStream
area: data
tags: [nats, jetstream, messaging, pubsub, streams, consumers]
detect: [dep:nats-py, dep:nats, dep:nats.js, dep:nats.go, dep:async-nats, dep:nats.net, dep:NATS.Client, dep:nats.rs, dep:jnats, dep:nats-server]
related: [kafka, rabbitmq, redis]
---
NATS core for fast fire-and-forget, JetStream for durable streams and acked consumers.

## Verify
- `nats server check connection --server $NATS_URL`: server reachable (nats CLI).
- `nats stream info STREAM`: subjects, retention, replicas and limits.
- `nats consumer info STREAM CONSUMER`: ack policy, pending and redelivered counts.
- `nats sub 'app.>' --count 5`: messages are published on the expected subjects.

## Test first
Run `nats-server -js` in a container or subprocess; create the stream from production code.
```python
async def test_redelivers_unacked(js):
    await js.publish("jobs.a", b"x")
    sub = await js.pull_subscribe("jobs.a", "w", config=ConsumerConfig(ack_wait=1))
    (m,) = await sub.fetch(1)      # no ack
    await asyncio.sleep(1.2)
    (m2,) = await sub.fetch(1)
    assert m2.metadata.num_delivered == 2
```

## Do
- Use core pub/sub only for data you can lose; use JetStream when delivery must survive restarts.
- Define streams with explicit `subjects`, `retention` (`limits`, `workqueue`, `interest`), `max_age`/`max_bytes` and replicas.
- Use durable pull consumers with explicit ack, `ack_wait`, `max_deliver` and backoff.
- Ack after the effect succeeds; use `nak`/`term` to retry or drop poison messages.
- Dedupe publishes with the `Nats-Msg-Id` header inside the stream's duplicate window.
- Design subject hierarchies (`orders.created.eu`) and subscribe with `*` and `>` wildcards.
- Use request/reply with a timeout; use queue groups to load-balance core subscribers.
- Drain connections on shutdown (`drain()`), and use the KV or object store for small state.

## Avoid
- Expecting core NATS messages to be stored: a subscriber that is down misses them. Use JetStream.
- Publishing to a stream subject with core `publish` and assuming it persisted: no ack received. Use the JetStream publish and check the ack.
- Unlimited `max_deliver` on poison messages: endless redelivery. Set a limit and an advisory/DLQ stream.
- Ephemeral consumers for durable work: state is lost on disconnect. Use a durable name.
- Ignoring slow-consumer drops: pending limits discard messages. Prefer pull consumers with bounded batches.
- Credentials in URLs: use creds files or NKeys/JWT.

## Review
- [ ] Each flow is explicitly core (lossy) or JetStream (durable).
- [ ] Stream limits and retention are set and sized.
- [ ] Consumers are durable with ack policy and max_deliver.
- [ ] Publishers dedupe with msg id and check acks.
- [ ] Connection drains on shutdown and reconnects on failure.
