---
name: locust
title: Locust load testing
area: testing
tags: [locust, load, python, performance, users, headless]
detect: [dep:locust, file:locustfile.py, file:locustfile*.py]
related: [k6, benchmarking, api-testing, pytest]
---
Locust defines user behavior in Python classes and swarms them against a target, reporting latency percentiles and failures.

## Verify
- `locust -f locustfile.py --headless -u 1 -r 1 -t 10s --host http://localhost:8000`: a short smoke run completes without exceptions.
- `locust -f locustfile.py --headless -u 100 -r 10 -t 2m --host $TARGET --csv results`: a sized run writes CSV stats.
- `locust -f locustfile.py --headless -u 50 -r 5 -t 1m --only-summary`: summary only for CI logs.
- `python -c "import locustfile"`: the file imports cleanly.

## Test first
Encode the pass condition as a failure in the task so a regression is visible.
```python
from locust import HttpUser, task, between

class Reader(HttpUser):
    wait_time = between(1, 3)

    @task
    def list_items(self):
        with self.client.get("/items", catch_response=True) as r:
            if r.status_code != 200 or r.elapsed.total_seconds() > 0.3:
                r.failure(f"bad: {r.status_code} {r.elapsed}")
```
Keep `locustfile.py` at the load-test directory root, with helpers beside it.

## Do
- Model real user mixes with several `HttpUser` classes and `@task(weight)`.
- Set `wait_time` (`between`, `constant_throughput`) to represent think time.
- Use `catch_response=True` to mark wrong bodies or slow responses as failures.
- Group dynamic URLs with the `name=` argument so stats do not explode into thousands of rows.
- Log in once in `on_start`, and keep per-user data on `self`.
- Fail the run in CI by setting `environment.process_exit_code` in a `quitting` listener.
- Scale with `--master` and `--worker` processes when one CPU saturates.

## Avoid
- Missing `name=` on URLs with ids: one stats row per id, unreadable. Pass `name="/items/[id]"`.
- Treating HTTP 200 as success without checking content: errors with 200 pass. Validate the body.
- Blocking calls like `requests` or `time.sleep` in tasks: they stall the gevent loop. Use `self.client` and `wait_time`.
- Judging results from one generator process near 100% CPU: the generator is the bottleneck. Add workers.
- Running against production data stores: destructive. Use a test environment.
- No exit-code gate: the run is green regardless. Set failure thresholds.

## Review
- [ ] User classes and weights mirror real traffic.
- [ ] Dynamic endpoints are grouped by name.
- [ ] Responses are validated, not just status-checked.
- [ ] CI fails when thresholds break.
- [ ] Generator capacity is checked before trusting numbers.
