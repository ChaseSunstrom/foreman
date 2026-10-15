---
name: prefect
title: Prefect
area: data
tags: [prefect, orchestration, flows, tasks, python, deployments]
detect: [dep:prefect, dep:prefect-aws, dep:prefect-gcp, dep:prefect-dbt, dep:prefect-sqlalchemy, file:prefect.yaml]
related: [airflow, dagster, etl-pipelines, dbt]
---
Prefect flows and tasks: plain Python functions with retries, caching, deployments and typed parameters.

## Verify
- `python flow.py`: the flow runs locally end to end.
- `prefect config view`: which API URL and profile the run will use.
- `prefect deploy --all`: deployments in `prefect.yaml` build and register.
- `pytest -q`: flows and tasks pass under the test harness.

## Test first
Use `prefect_test_harness` and call tasks via `.fn` for pure logic.
```python
from prefect.testing.utilities import prefect_test_harness

def test_flow_retries_flaky_fetch():
    with prefect_test_harness():
        state = etl_flow(date="2024-01-01", return_state=True)
    assert state.is_completed()

def test_transform_pure():
    assert transform.fn([{"v": 1}]) == [{"v": 2}]
```

## Do
- Decorate with `@flow` and `@task`; give tasks `retries`, `retry_delay_seconds`, `timeout_seconds`.
- Type flow parameters; Prefect validates them with Pydantic and the UI renders a form.
- Cache expensive tasks with `cache_key_fn` and `cache_expiration`; use `task_input_hash` carefully.
- Fan out with `task.map(...)` or `.submit()` and gather futures with `.result()`.
- Define deployments in `prefect.yaml` or with `flow.serve()`/`flow.deploy()`, with schedules and work pools.
- Store credentials in Blocks or Secret blocks, variables for config; never in code.
- Use `get_run_logger()` rather than `print` so logs reach the run.
- Make each task idempotent so retries and reruns are safe.

## Avoid
- Calling `.result()` immediately after every `.submit()`: serializes work you meant to run concurrently. Submit all, then gather.
- Passing huge objects between tasks: serialization cost and state size. Pass references to storage.
- Cache keys that ignore a changed input: stale results. Include all inputs or set short expirations.
- Mutating global state inside tasks: tasks may run in other processes. Return values.
- Old Prefect 1.x idioms (`with Flow(...)`, `Parameter`, agents/`prefect register`): replaced by flows, parameters, work pools and `prefect deploy`.
- Secrets in deployment parameters: visible in the UI. Use Secret blocks.
- Unbounded retries on non-transient errors: retry only expected exceptions via `retry_condition_fn`.

## Review
- [ ] Tasks have retries and timeouts proportionate to the failure modes.
- [ ] Flow parameters are typed; deployments define schedule and work pool.
- [ ] Secrets are blocks or variables, not literals.
- [ ] Concurrency uses submit/map and gathers at the end.
- [ ] Each task is idempotent.
