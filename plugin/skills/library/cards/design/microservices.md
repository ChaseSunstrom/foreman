---
name: microservices
title: Microservices
area: design
tags: [microservices, distributed, boundaries, contracts, resilience, observability]
detect: [file:docker-compose.yml, file:docker-compose.yaml, file:skaffold.yaml, file:Tiltfile]
related: [event-driven, sagas, retries-backoff, api-versioning, modular-monolith, idempotency]
---
Independently deployable services with owned data, versioned contracts, bounded timeouts and traceable calls.

## Verify
- `docker compose config -q`: the compose file is valid.
- `docker compose up -d --wait && docker compose ps`: every service starts and reports healthy.
- `curl -fsS localhost:8080/healthz && curl -fsS localhost:8080/readyz`: liveness and readiness are separate and answer.
- `pytest -q tests/contract`: consumer-driven contract tests (Pact or similar) pass for each pair.

## Test first
Test the consumer against a stubbed provider that enforces the contract, and prove it survives failure.
```python
def test_checkout_degrades_when_inventory_times_out(respx_mock, client):
    respx_mock.get("http://inventory/stock/A1").mock(side_effect=httpx.ReadTimeout)
    r = client.post("/checkout", json={"sku": "A1"})
    assert r.status_code == 503 and r.json()["error"]["code"] == "inventory_unavailable"
```

## Do
- Split by business capability and data ownership. Each service has its own datastore, and no one reads another's tables.
- Set a timeout on every outbound call, shorter than the caller's own deadline, and propagate the deadline.
- Retry only idempotent calls, with backoff and jitter, behind a circuit breaker or concurrency limit.
- Version contracts and evolve additively. Run both versions until all consumers move.
- Propagate a correlation ID (`traceparent`) through HTTP and messages, and log it in every line.
- Prefer async events for cross-service state propagation, and sync calls only where an answer is needed now.
- Expose separate `/healthz` (process alive) and `/readyz` (dependencies usable) endpoints.
- Put each service's config in the environment, and deploy each one independently.

## Avoid
- A shared database or shared library holding domain models: it recouples deployments. Share contracts only.
- Chains of synchronous calls (A to B to C to D): latency and availability multiply. Aggregate, cache or go async.
- Distributed transactions across services: use sagas with compensations.
- Default HTTP client timeouts (often none): a slow dependency exhausts your threads. Set connect and read timeouts.
- Splitting before there are clear boundaries and team need: begin with a modular monolith and extract later.
- Readiness probes that check every downstream: one blip removes all your pods. Check only what you can't serve without.
- Integration tests that need the whole fleet running: use contract tests per pair plus a few end-to-end smoke tests.

## Review
- [ ] Each service owns its data, and no cross-service table access exists.
- [ ] All outbound calls have timeouts, bounded retries and a failure-path test.
- [ ] Contracts are versioned and checked in CI.
- [ ] Trace and correlation IDs pass through every hop.
- [ ] Health and readiness endpoints are distinct, and deploys don't need lockstep.
