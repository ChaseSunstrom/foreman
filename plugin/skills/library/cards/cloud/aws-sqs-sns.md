---
name: aws-sqs-sns
title: AWS SQS and SNS
area: cloud
tags: [aws, sqs, sns, queues, messaging, dlq]
detect: [dep:@aws-sdk/client-sqs, dep:@aws-sdk/client-sns, dep:boto3, dep:aws-sdk-sqs, dep:aws-sdk-sns]
related: [aws-lambda, aws-iam, localstack, aws-cloudformation]
---
SQS queues and SNS topics: at-least-once delivery, idempotent consumers, visibility timeouts, dead-letter queues.

## Verify
- `aws sqs get-queue-attributes --queue-url U --attribute-names All`: visibility timeout, redrive policy, FIFO flags.
- `aws sqs get-queue-attributes --queue-url U --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible`: backlog and in-flight counts.
- `aws sqs receive-message --queue-url DLQ_URL --max-number-of-messages 1`: what is landing in the dead-letter queue.
- `aws sns list-subscriptions-by-topic --topic-arn T`: subscriptions are confirmed and filtered as intended.

## Test first
Test the consumer with a duplicate message; use `moto` or LocalStack for wiring.
```python
def test_duplicate_message_processed_once(db):
    msg = {"messageId": "m1", "body": '{"order": 7}'}
    handle(msg, db)
    handle(msg, db)
    assert db.count_payments(order=7) == 1
```

## Do
- Attach a DLQ with a redrive policy (`maxReceiveCount` 3 to 5) to every queue; alarm on DLQ depth.
- Set visibility timeout above the consumer's max processing time (at least 6x the Lambda timeout).
- Use long polling (`WaitTimeSeconds=20`) and batch receives and sends (up to 10).
- Make consumers idempotent with a dedupe key (business id or `MessageId`); delete only after success.
- Fan out with SNS to SQS (raw message delivery on, filter policies on subscriptions).
- Use FIFO (`.fifo` name) only when order matters; set `MessageGroupId` for parallelism and a `MessageDeduplicationId` or content-based dedup.
- Encrypt with SSE and keep messages small; put big payloads in S3 and send a pointer.
- Allow SNS to send with a queue policy conditioned on `aws:SourceArn`.

## Avoid
- Deleting before the work succeeds: a crash loses the message.
- Short polling in a tight loop: empty responses and cost. Use long polling.
- Assuming order or exactly-once on standard queues: handle reordering and duplicates.
- Publishing to SNS without a queue policy permitting it: messages vanish silently. Check the subscription.
- A single `MessageGroupId` on FIFO: throughput of one consumer. Use a key like customer id.
- Poison messages with no DLQ: they retry forever and block throughput.
- Message body over 256 KB: the send fails. Use S3 pointers.

## Review
- [ ] Every queue has a DLQ, redrive and an alarm.
- [ ] Visibility timeout exceeds processing time.
- [ ] Consumer is idempotent and deletes after success.
- [ ] Queue policy scopes SNS senders by source ARN.
- [ ] Payload size and FIFO group choices are justified.
