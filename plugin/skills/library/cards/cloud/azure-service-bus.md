---
name: azure-service-bus
title: Azure Service Bus
area: cloud
tags: [azure, service-bus, queues, topics, dead-letter, messaging]
detect: [dep:@azure/service-bus, dep:azure-servicebus, dep:Azure.Messaging.ServiceBus]
related: [azure-functions, azure-entra-id, aws-sqs-sns, gcp-pubsub]
---
Service Bus queues and topics: peek-lock with explicit settle, dead-letter handling, idempotent consumers, sessions only when ordering is needed, Entra auth.

## Verify
- `az servicebus queue show -g RG --namespace-name NS -n Q --query '{lock:lockDuration,max:maxDeliveryCount,dlq:deadLetteringOnMessageExpiration,ttl:defaultMessageTimeToLive,dup:requiresDuplicateDetection}'`: lock, delivery count, dead-lettering, TTL and duplicate detection.
- `az servicebus queue show -g RG --namespace-name NS -n Q --query 'countDetails'`: active and dead-letter message counts.
- `az servicebus namespace show -g RG -n NS --query '{local:disableLocalAuth,sku:sku.name}'`: SAS keys disabled and tier.
- `az role assignment list --scope NS_ID --query '[].{p:principalName,r:roleDefinitionName}'`: Data Sender and Data Receiver roles per identity.

## Test first
Test the handler with a duplicate delivery and a poison message before wiring the receiver.
```python
def test_poison_message_is_dead_lettered_after_failure(receiver, handler):
    msg = FakeMessage(body=b"not-json", delivery_count=1)
    process(handler, receiver, msg)
    assert receiver.dead_lettered == [(msg, "InvalidPayload")]
    assert receiver.completed == []
```

## Do
- Use peek-lock receive mode. Complete after the work is durable, abandon on transient errors, dead-letter on permanent ones with a reason and description.
- Set `lockDuration` longer than the processing time, or renew the lock. Set `maxDeliveryCount` so poison messages reach the dead-letter queue.
- Make handlers idempotent: delivery is at least once. Use the `MessageId` and enable duplicate detection on the entity where producers retry.
- Use topics with subscription filters for fan-out. Keep filters simple and on application properties.
- Use sessions only for per-key ordering. A session consumer then handles one session at a time.
- Authenticate with managed identity and the `Azure Service Bus Data Sender` and `Data Receiver` roles, and disable local auth.
- Send in batches (`create_message_batch`) and reuse one client per process.
- Monitor the dead-letter queue depth and age, and have a replay procedure.
- Set TTL on messages that go stale. Premium tier for private endpoints and isolation.

## Avoid
- Receive-and-delete mode for work that matters: a crash loses the message. Use peek-lock.
- Completing before the work finishes: a failure afterwards loses data. Complete last.
- Ignoring the dead-letter queue: failures pile up unseen. Alarm on its count.
- Long processing with a short lock: the message reappears and runs twice. Renew or extend.
- Connection strings with the root manage key in apps: use Entra roles.
- Opening a new client per message: connection churn and throttling. Reuse clients and senders.
- Sessions on queues where order is not needed: they limit parallelism.

## Review
- [ ] Peek-lock with explicit complete, abandon and dead-letter.
- [ ] Handlers idempotent, with tests for duplicates and poison messages.
- [ ] Lock duration and max delivery count set.
- [ ] Dead-letter queue monitored with a replay path.
- [ ] Managed identity roles replace connection strings.
