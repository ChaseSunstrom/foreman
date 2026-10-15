---
name: celery
title: Celery
area: python
tags: [python, tasks, queue, celery, broker, workers]
detect: [dep:celery, file:celery.py]
related: [django, flask, pytest, rq]
---
Celery task queues: tasks, brokers (Redis, RabbitMQ), retries, beat schedules, result backends.

## Verify
- `celery -A proj inspect registered`: workers loaded the expected tasks (needs a running worker).
- `celery -A proj report`: the effective config and versions.
- `pytest -q`: tests calling tasks directly or with eager mode.
- `celery -A proj beat --loglevel=info` (briefly, locally): the schedule parses and dispatches.

## Test first
Call the task function directly for logic; use `.apply()` for the task machinery. No broker needed.
```python
from app.tasks import send_invoice

def test_send_invoice_is_idempotent(db, invoice):
    send_invoice.apply(args=[invoice.id]).get()
    send_invoice.apply(args=[invoice.id]).get()
    assert invoice.emails_sent == 1
```
Prefer `task_always_eager` only for smoke tests; it skips serialization and routing.

## Do
- Pass IDs and primitives as arguments, and re-load objects inside the task.
- Make tasks idempotent; delivery is at least once, and `acks_late=True` re-delivers on worker loss.
- Retry with `autoretry_for=(SomeError,)`, `retry_backoff=True`, `retry_jitter=True`, `max_retries=N`.
- Set `soft_time_limit` and `time_limit` on tasks that call external services.
- Keep the JSON serializer (default); set `task_serializer`/`accept_content` explicitly.
- Set `result_expires`, or `ignore_result=True` where the result is unused.
- Use named queues with `task_routes` so slow tasks do not starve fast ones.
- In Django, enqueue with `transaction.on_commit(lambda: task.delay(pk))`.

## Avoid
- Passing ORM objects or large payloads as arguments: stale data and serialization errors. Pass the primary key.
- `pickle` as the serializer: remote code execution if the broker is reachable. Use JSON.
- Blocking on `result.get()` inside a task: deadlocks the worker pool. Use `chain`, `chord` or callbacks.
- Enqueueing before the DB commit: the worker runs before the row exists. Use `on_commit`.
- Running `beat` on several hosts: every schedule fires N times. Run exactly one beat.
- Default visibility timeout shorter than an ETA/countdown task on Redis: the task is re-delivered repeatedly. Raise `broker_transport_options["visibility_timeout"]`.
- Unbounded retries with no backoff: retry storms. Cap `max_retries`.

## Review
- [ ] Task args are IDs or primitives, and the task is safe to run twice.
- [ ] Retries are bounded with backoff; time limits are set.
- [ ] Serializer is JSON; broker and result URLs come from env.
- [ ] Task enqueue happens after the commit, not before.
- [ ] A queue and concurrency plan exists for slow vs fast tasks.
