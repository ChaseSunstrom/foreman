---
name: aws-eventbridge
title: AWS EventBridge
area: cloud
tags: [aws, eventbridge, events, rules, scheduler, event-bus]
detect: [dep:@aws-sdk/client-eventbridge, dep:@aws-sdk/client-scheduler]
related: [aws-lambda, aws-sqs-sns, aws-step-functions, aws-iam, localstack]
---
EventBridge buses and rules: narrow event patterns, a DLQ and retry policy on every target, schema-versioned events, tested patterns.

## Verify
- `aws events test-event-pattern --event-pattern file://pattern.json --event file://event.json`: the pattern matches (or rejects) a sample event.
- `aws events list-rules --event-bus-name BUS`: rules exist and are ENABLED.
- `aws events list-targets-by-rule --rule R --event-bus-name BUS --query 'Targets[].[Id,DeadLetterConfig,RetryPolicy]'`: each target has a DLQ and retry policy.
- `aws events put-events --entries file://entries.json`: a smoke event publishes and `FailedEntryCount` is 0.

## Test first
Write the event pattern and a matching and a non-matching sample, then assert both.
```python
def test_pattern_matches_only_paid_orders(events):
    pat = json.dumps({"source": ["app.orders"], "detail-type": ["OrderPaid"]})
    ok = events.test_event_pattern(EventPattern=pat, Event=sample("OrderPaid"))
    no = events.test_event_pattern(EventPattern=pat, Event=sample("OrderCreated"))
    assert ok["Result"] is True and no["Result"] is False
```

## Do
- Use a custom bus per domain, not the default bus, and restrict `events:PutEvents` with a bus resource policy.
- Match on `source` and `detail-type` first, then on `detail` fields. Keep patterns as narrow as the consumer needs.
- Put a `version` in `detail` and keep changes additive.
- Attach an SQS dead-letter queue and a `RetryPolicy` (`MaximumEventAgeInSeconds`, `MaximumRetryAttempts`) to each target.
- Make consumers idempotent: delivery is at least once and unordered.
- Check `FailedEntryCount` in the PutEvents response and retry only the failed entries.
- Use EventBridge Scheduler for one-off and cron jobs with a flexible window and its own DLQ.
- Use an archive and replay for bus debugging on non-prod, and an input transformer to avoid glue Lambdas.

## Avoid
- Ignoring `FailedEntryCount`: PutEvents returns 200 with partial failures. Inspect `Entries` for `ErrorCode`.
- Patterns on `source` only: any publisher with that string triggers it. Add `detail-type` and detail filters.
- Targets without a DLQ: failed deliveries vanish after retries. Add one and alarm on its depth.
- Assuming ordering or exactly-once: add sequence ids and dedupe keys.
- Events over the 256 KB entry limit: send a pointer to S3 instead.
- Wildcard `events:*` on `*` in roles: scope to the bus ARN.

## Review
- [ ] Each rule has a tested pattern with a negative case.
- [ ] Each target has a DLQ and retry policy, and the target role is least privilege.
- [ ] Producers check partial failure.
- [ ] Consumers are idempotent.
- [ ] Event schema carries a version.
