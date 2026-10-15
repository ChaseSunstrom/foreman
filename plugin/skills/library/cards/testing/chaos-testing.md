---
name: chaos-testing
title: Chaos testing
area: testing
tags: [chaos, resilience, fault-injection, toxiproxy, steady-state, game-day]
detect: [dep:toxiproxy, dep:chaostoolkit, dep:pumba, file:chaos/*, file:chaos-mesh*.yaml, file:litmus*.yaml]
related: [integration-testing, e2e-strategy, k6, test-pyramid]
---
Chaos testing injects failures (latency, dropped connections, killed processes) in a controlled way to check the system keeps its steady state.

## Verify
- `toxiproxy-cli list`: proxies and toxics are as the experiment expects (needs the Toxiproxy server).
- `chaos run experiment.json`: a Chaos Toolkit experiment checks the steady state before, during and after.
- `kubectl get podchaos,networkchaos -A`: Chaos Mesh experiments are active only when intended.
- `curl -sS -w "%{http_code} %{time_total}\n" -o /dev/null $URL/health`: the steady-state probe during the fault.

## Test first
Define the steady-state check and the abort condition first; a fault that breaks it is the failing result.
```python
def test_checkout_survives_slow_payment(toxiproxy):
    toxiproxy.add_latency("payment", ms=3000)
    r = client.post("/checkout", json=cart)
    assert r.status_code in (202, 503)     # degraded, never a hang
    assert r.elapsed.total_seconds() < 5   # timeout honored
```
Experiments live in `chaos/` with the steady-state probe and a rollback.

## Do
- State a hypothesis: "with 3 s latency on the payment call, checkout returns within 5 s".
- Start in a test or staging environment with small blast radius; expand deliberately.
- Define metrics for steady state (error rate, p95 latency, queue depth) and an automatic abort threshold.
- Inject one fault at a time: latency, errors, packet loss, process kill, dependency down, clock skew, disk full.
- Verify timeouts, retries with backoff and jitter, circuit breakers, idempotency and graceful degradation.
- Always remove the fault and confirm recovery in the same run, even on failure.
- Turn each finding into a permanent automated test or alert and fix.

## Avoid
- Starting in production without observability and an abort switch: outages. Prove it in staging first.
- Injecting several faults at once: causes unclear. One variable at a time.
- Experiments with no steady-state definition: nothing to pass or fail. Write the check first.
- Retries without backoff, or on non-idempotent writes: faults multiply load or duplicate effects. Add backoff, jitter and idempotency keys.
- Forgetting rollback of the injected fault: lingering damage. Use teardown that always runs.
- One-time game days only: resilience decays. Automate the key experiments in CI or on a schedule.

## Review
- [ ] Hypothesis, steady-state metric and abort condition are written.
- [ ] Blast radius is limited and the environment is not production by default.
- [ ] Fault removal and recovery are verified.
- [ ] Timeouts, retries and breakers have explicit limits.
- [ ] Each finding became a test, alert or fix.
