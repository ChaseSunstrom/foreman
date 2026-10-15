---
name: integration-testing
title: Integration testing
area: testing
tags: [integration, database, testcontainers, boundaries, fixtures, isolation]
detect: [dep:testcontainers, dep:github.com/testcontainers/testcontainers-go, dep:org.testcontainers, dep:pytest-docker, file:docker-compose.test.yml]
related: [test-pyramid, test-doubles, e2e-strategy, flaky-tests, test-data-factories]
---
Integration tests run real components together (your code plus a real database, queue or HTTP server) to prove the wiring that unit tests fake.

## Verify
- `docker compose -f docker-compose.test.yml up -d --wait`: test dependencies start healthy (needs a compose file with healthchecks).
- `pytest -q -m integration`: only the integration-marked tests run against the real service.
- `go test -tags=integration ./...`: build-tagged suite runs; the default `go test ./...` skips it.
- `npx jest --selectProjects integration`: a separate Jest project runs the suite when configured.

## Test first
Hit the real dependency through your own code and assert persisted state.
```python
@pytest.mark.integration
def test_repo_roundtrip(pg_conn):
    repo = OrderRepo(pg_conn)
    oid = repo.add(Order(sku="A1", qty=2))
    assert repo.get(oid).qty == 2
```
Keep these in `tests/integration/` (or tagged), apart from unit tests, so each tier runs on its own.

## Do
- Use real instances in containers (Testcontainers) with the production engine and major version, not SQLite as a stand-in.
- Run schema migrations against the test database, so migrations are tested too.
- Isolate each test: transaction rollback, truncate tables, or a schema or database per worker.
- Wait on readiness (healthcheck, port poll with timeout), never a fixed sleep.
- Fake only what you cannot run: third-party SaaS, payment, email.
- Cover boundaries: serialization, constraints, timeouts, retries, connection loss.
- Assert through the public interface and the stored state, not internals.

## Avoid
- Sharing one mutable database across tests and workers: order-dependent failures. Isolate per test or per worker.
- `sleep(5)` to wait for startup: slow and flaky. Poll health.
- Pointing tests at a shared dev or staging service: data collisions, non-reproducible. Spin up your own.
- Hard-coded host ports: clashes in CI. Use mapped random ports from the container API.
- Skipping teardown: leaked containers and data. Use fixtures or context managers.
- Too many integration tests for logic: slow feedback. Test logic in unit tests, wiring here.

## Review
- [ ] Dependencies match production engine and version.
- [ ] Migrations run in the test setup.
- [ ] Tests are isolated and parallel-safe.
- [ ] Readiness uses polling with a timeout.
- [ ] Suite is separable from unit tests by marker, tag or directory.
