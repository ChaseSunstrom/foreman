---
name: health-checks
title: Health checks
area: design
tags: [health, liveness, readiness, probes, kubernetes, observability]
detect: []
related: [graceful-shutdown, circuit-breaker, leader-election, timeouts, multi-region]
---
Separate liveness (restart me) from readiness (send me traffic), keep both cheap, and never let a dependency blip kill every pod.

## Verify
- `curl -fsS localhost:8080/healthz`: liveness answers 200 quickly.
- `curl -fsS localhost:8080/readyz`: readiness reflects dependencies and startup state.
- `kubectl describe pod POD`: probe configuration and recent probe failures (Kubernetes).
- `pytest -q -k health`: tests below.

## Test first
Liveness stays green when a dependency is down; readiness goes red; readiness is red until warm.
```python
def test_db_down_fails_readiness_not_liveness(app, db):
    db.stop()
    assert app.get("/healthz").status_code == 200
    assert app.get("/readyz").status_code == 503

def test_not_ready_until_startup_done(app_factory):
    app = app_factory(warmup=True)
    assert app.get("/readyz").status_code == 503
    app.finish_warmup()
    assert app.get("/readyz").status_code == 200

def test_health_is_fast_and_unauthenticated(app):
    assert app.get("/healthz", timeout=0.2).elapsed < 0.2
```

## Do
- Liveness: the process loop is responsive; it checks nothing external. Readiness: can serve now (config loaded, caches warm, critical dependencies reachable, not draining).
- Add a startup probe for slow boots so liveness does not kill the app during init.
- Cache dependency check results for a few seconds, give each check its own short timeout, and run them concurrently.
- Distinguish critical dependencies (fail readiness) from degraded optional ones (report in the body but stay ready).
- Return a small JSON body with per-check status for humans, without leaking versions or hostnames to the public.
- On shutdown, flip readiness to failing first, then drain (see graceful-shutdown).
- Keep the endpoints off authentication and outside rate limits but not exposed publicly.

## Avoid
- Liveness probing the database: a DB outage restarts every pod and prolongs the incident. Check only the process.
- Expensive checks on every probe: self-inflicted load. Cache and time-box.
- Probe timeout equal to its period with no failure threshold: flapping. Set thresholds and a sensible `timeoutSeconds`.
- Always-200 readiness: traffic reaches broken instances. Check real dependencies.
- Readiness depending on every downstream service: one outage removes the whole fleet. Only critical ones.

## Review
- [ ] Liveness and readiness are separate endpoints with different checks.
- [ ] Startup probe covers slow init.
- [ ] Checks time-boxed and cached.
- [ ] Optional dependencies degrade rather than fail readiness.
