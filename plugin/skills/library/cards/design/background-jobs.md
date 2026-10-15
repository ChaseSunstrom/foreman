---
name: background-jobs
title: Background jobs
area: design
tags: [jobs, queues, workers, retries, scheduling, idempotent]
detect: [dep:celery, dep:rq, dep:bullmq, dep:bull, dep:sidekiq, dep:arq, dep:river, dep:asynq, dep:oban, dep:hangfire, dep:Hangfire]
related: [idempotency, retries-backoff, event-driven, concurrency, sagas]
---
Work moved off the request path: durable queues, idempotent handlers, bounded retries, visible failures.

## Verify
- `celery -A app inspect active` (or `npx bullmq-cli`, `sidekiq` web UI): workers are alive and consuming.
- `pytest -q tests/jobs`: handlers run synchronously in tests, including the duplicate and failure cases.
- `redis-cli llen queue:default` (Redis-backed queues, adjust the key): backlog is not growing without bound.

## Test first
Call the handler directly, twice, and with a failing dependency.
```python
def test_send_receipt_is_idempotent(db, mailer):
    send_receipt(order_id="o1"); send_receipt(order_id="o1")
    assert mailer.sent == 1

def test_send_receipt_retries_on_smtp_error(db, mailer):
    mailer.fail_next(TimeoutError)
    with pytest.raises(TimeoutError):   # the framework retries, not the handler
        send_receipt(order_id="o1")
    assert db.receipt("o1").status == "pending"
```

## Do
- Enqueue IDs and small arguments, not objects or large payloads. The handler loads fresh state.
- Enqueue after the DB transaction commits (or via an outbox), so the worker finds the row.
- Make handlers idempotent: check a status column or dedupe key before the side effect.
- Configure retries with exponential backoff and jitter, a maximum attempts count, and a dead-letter or failed set that alerts.
- Set a per-job timeout, shorter than the queue's visibility or lock timeout.
- Use separate queues for latency-sensitive and bulk work, and size concurrency per queue.
- Shut down gracefully: finish or return in-flight jobs on SIGTERM.
- Schedule periodic jobs from one scheduler (beat, cron, or the library's own), and make them safe to run twice.

## Avoid
- Enqueuing inside the transaction before commit: the worker runs first and sees no row. Enqueue on commit.
- Passing ORM objects or datetimes through pickle: stale or unsafe. Pass primitives and reload.
- Retrying forever with no backoff: it hammers a failing dependency. Cap attempts and back off.
- A job timeout longer than the visibility timeout: the queue redelivers while it still runs, so it runs twice. Keep visibility greater than the timeout.
- Swallowing exceptions in the handler: the job is marked success and the failure vanishes. Let it raise.
- Running scheduled jobs on every web instance: duplicates. Use one scheduler or a lock.
- Non-idempotent side effects (charges, emails) with at-least-once delivery: add dedupe keys.

## Review
- [ ] Jobs take IDs, load fresh data, and are tested twice in a row.
- [ ] Enqueue happens after commit or through an outbox.
- [ ] Retries, backoff, max attempts and dead-letter handling are configured and alerting.
- [ ] Timeouts are shorter than the visibility lock, and SIGTERM is handled.
- [ ] Scheduled jobs run from one scheduler and tolerate overlap.
