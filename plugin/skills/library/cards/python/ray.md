---
name: ray
title: Ray
area: python
tags: [python, ray, distributed, parallel, actors, serve]
detect: [dep:ray]
related: [dask, asyncio, celery, pytest]
---
Ray: distributed tasks and actors with an object store, for parallel Python, Ray Serve and Ray Data workloads.

## Verify
- `python -c "import ray; ray.init(num_cpus=2); print(ray.cluster_resources())"`: a local Ray runtime starts.
- `pytest -q`: tests against a shared local `ray.init(num_cpus=2)` fixture.
- `ray status`: nodes and resource usage on a running cluster.
- `ray stop`: cleans leftover local Ray processes when a test run hung.

## Test first
```python
import pytest
import ray

@pytest.fixture(scope="session", autouse=True)
def ray_local():
    ray.init(num_cpus=2, include_dashboard=False, ignore_reinit_error=True)
    yield
    ray.shutdown()

@ray.remote
def square(x):
    return x * x

def test_parallel_squares():
    assert ray.get([square.remote(i) for i in range(4)]) == [0, 1, 4, 9]
```
For pure logic, call the function directly: define the logic as a plain function and wrap with `ray.remote` at the edge.

## Do
- Launch many tasks first, then `ray.get(list_of_refs)` once. Use `ray.wait(refs, num_returns=1)` to process results as they finish.
- Put large inputs in the object store once with `ref = ray.put(big)` and pass `ref` to tasks.
- Declare resources: `@ray.remote(num_cpus=1, num_gpus=0.5, max_retries=3)`.
- Use actors (`@ray.remote class Worker`) for state or expensive init such as loading a model. Set `max_restarts` for fault tolerance.
- Use `ray.init(runtime_env={"pip": [...], "working_dir": "."})` or a container image so workers have the same code and dependencies.
- Bound in-flight work by waiting on a window of refs, to avoid memory blowups.
- Use Ray Serve (`@serve.deployment`) for online inference and Ray Data for batch pipelines.
- Make tasks idempotent, as retries re-run them.

## Avoid
- `ray.get` inside a loop right after each `.remote()`: serial execution. Collect refs, then get.
- Tiny tasks (microseconds): overhead dominates. Batch work into chunks.
- Capturing big arrays in a closure: serialized into every task. Use `ray.put`.
- Calling `ray.init()` in library code or at import: collides with a running cluster. Do it in the entry point, and use `address="auto"` to join a cluster.
- Mutating a global from tasks and expecting the driver to see it: processes are separate. Return values or use an actor.
- Blocking `ray.get` inside `async def`: use `await ref` instead.
- Unhandled `RayTaskError` and `ActorDiedError`: wrap `ray.get` and decide retry or fail.

## Review
- [ ] Tasks are coarse enough, with resources declared.
- [ ] Large data is shared by `ray.put` or loaded in actors once.
- [ ] Worker environment is declared (`runtime_env` or image).
- [ ] Failures and retries are handled and tasks are idempotent.
