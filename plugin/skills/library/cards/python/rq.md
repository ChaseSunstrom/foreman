---
name: rq
title: RQ (Redis Queue)
area: python
tags: [python, tasks, queue, redis, rq, workers]
detect: [dep:rq, dep:rq-scheduler]
related: [celery, pytest, django, flask]
---
RQ background jobs on Redis: queues, workers, job results, retries, scheduling.

## Verify
- `rq info`: queues, workers and job counts against the configured Redis.
- `rq worker --burst`: drains the queues and exits, so a run can finish in a script or test.
- `rq info --only-workers`: workers are registered and alive (flag availability varies; omit if `rq info` suffices).
- `pytest -q`: the suite, with a synchronous queue or a real local Redis.

## Test first
Use `is_async=False` so jobs run inline, or a `Worker` in burst mode against a test Redis.
```python
from fakeredis import FakeStrictRedis
from rq import Queue
from app.jobs import resize

def test_resize_job_returns_dims():
    q = Queue(connection=FakeStrictRedis(), is_async=False)
    job = q.enqueue(resize, "img1", 64)
    assert job.result == (64, 64)
```
`fakeredis` is a separate dependency; use a real Redis when unsure about parity.

## Do
- Enqueue importable top-level functions by reference: `q.enqueue(mod.func, arg)`.
- Pass IDs and primitives; re-load state inside the job.
- Give jobs `job_timeout=`, `result_ttl=` and `failure_ttl=` explicitly.
- Retry with `Retry(max=3, interval=[10, 30, 60])` passed to `enqueue(retry=...)`.
- Use separate queues (`high`, `default`, `low`) and start workers with queue order: `rq worker high default low`.
- Run workers under a supervisor (systemd, container restart policy).
- Handle failure with `on_failure=` callbacks or the failed-job registry.
- Make jobs idempotent; a worker kill can re-run a job.

## Avoid
- Enqueueing lambdas, bound methods of unimportable classes or `__main__` functions: the worker cannot import them. Use module-level functions.
- Passing large objects or open connections as arguments: pickled into Redis. Pass references.
- Unpickling jobs from an untrusted Redis: RQ serializes with pickle by default, so protect Redis with auth and a private network, or set a JSON serializer.
- Default `job_timeout` (180s) on long jobs: they are killed mid-run. Set it explicitly.
- Forgetting `result_ttl`: results accumulate in Redis forever with `-1`, and vanish after 500s by default. Choose a value.
- Using `fork`-based workers with libraries that are not fork-safe (DB connections opened pre-fork): open connections inside the job, or use `SimpleWorker` carefully.

## Review
- [ ] Job functions are importable and take IDs, not objects.
- [ ] Timeouts, TTLs and retries are set deliberately.
- [ ] Redis is authenticated and not exposed, since jobs are pickled.
- [ ] Workers are supervised and queue priority is stated.
- [ ] Jobs are safe to run twice.
