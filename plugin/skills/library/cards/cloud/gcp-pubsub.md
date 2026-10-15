---
name: gcp-pubsub
title: GCP Pub/Sub
area: cloud
tags: [gcp, pubsub, messaging, subscriptions, dead-letter, ack]
detect: [dep:@google-cloud/pubsub, dep:google-cloud-pubsub, dep:cloud.google.com/go/pubsub]
related: [gcp-iam, gcp-cloud-run, aws-sqs-sns]
---
Pub/Sub topics and subscriptions: at-least-once delivery, ack deadlines, idempotent subscribers, dead-letter topics.

## Verify
- `gcloud pubsub subscriptions describe SUB`: ack deadline, retry policy, dead-letter policy, push or pull.
- `gcloud pubsub subscriptions pull SUB --limit=1 --auto-ack=false`: a message arrives and is shaped as expected (it stays unacked).
- `gcloud pubsub topics publish T --message='{"id":1}' --attribute=type=test`: publishing works for this identity.

## Test first
Use the emulator (`PUBSUB_EMULATOR_HOST`) and assert idempotence.
```python
def test_redelivery_does_not_double_apply(store):
    msg = FakeMessage(id="m1", data=b'{"order": 7}')
    handle(msg, store)
    handle(msg, store)
    assert store.applied("order", 7) == 1
    assert msg.ack_count >= 1
```

## Do
- Make subscribers idempotent; delivery is at least once and unordered by default.
- Ack only after the work is durable; nack or let the deadline lapse on failure.
- Set a dead-letter topic with `max-delivery-attempts` and grant the Pub/Sub service agent publisher and subscriber roles for it.
- Set an exponential backoff retry policy rather than immediate redelivery.
- Use flow control (`max_messages`, `max_bytes`) on streaming pull clients to bound memory.
- Use ordering keys only when needed (`enable_message_ordering` on both publisher and subscription).
- Use subscription filters on attributes to cut traffic.
- For push to Cloud Run, enable OIDC auth with a service account and verify the token audience.
- Use a schema on the topic when producers vary.

## Avoid
- Acking at receipt, then processing: a crash loses the message.
- Ack deadline shorter than processing time: duplicate redelivery storms. Extend with lease management or raise it.
- Creating a publisher client per message: build once and reuse; call `future.result()` or handle the callback to catch errors.
- Push endpoint without auth: anyone can post forged messages.
- Assuming ordering across keys, or without ordering enabled.
- A subscription with no dead-letter and no expiry: poison messages loop and unconsumed ones pile up (default retention is 7 days).

## Review
- [ ] Handler is idempotent; ack follows durable work.
- [ ] Dead-letter topic, permissions and backoff configured.
- [ ] Flow control bounds memory.
- [ ] Push subscriptions authenticate with OIDC.
- [ ] Publisher is a shared client and errors are observed.
