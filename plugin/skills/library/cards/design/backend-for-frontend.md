---
name: backend-for-frontend
title: Backend for frontend
area: design
tags: [bff, api, aggregation, frontend, mobile, composition]
detect: []
related: [api-gateway-pattern, graphql-schema, microservices, timeouts, caching]
---
Give each client type its own thin backend that aggregates downstream calls into the shapes that client needs.

## Verify
- `pytest -q -k bff`: aggregation, partial failure and shape tests.
- `curl -s localhost:8080/bff/home | python -m json.tool`: the response is one payload shaped for the screen.
- `git grep -nE "import .*(domain|repositories)" -- bff`: the BFF calls services over APIs, not their databases.

## Test first
One downstream failing must degrade the screen, not break it.
```python
def test_home_degrades_when_recommendations_fail(bff, downstream):
    downstream.profile.returns({"name": "Ada"})
    downstream.recs.raises(Timeout)
    r = bff.get("/home")
    assert r.status_code == 200
    body = r.json()
    assert body["profile"]["name"] == "Ada"
    assert body["recommendations"] == [] and body["partial"] == ["recommendations"]
    assert downstream.calls_started_together("profile", "recs")   # fanned out in parallel
```

## Do
- One BFF per distinct client experience (web, mobile, partner), owned by the team that owns that client.
- Fan out downstream calls in parallel with per-call timeouts and a total deadline.
- Define which parts are essential and which are optional, and return partial results with a marker.
- Shape, trim and rename for the UI here; keep domain rules in the services.
- Authenticate the user once and forward identity; handle tokens (session cookie to token exchange) server side.
- Cache per-screen composites carefully, keyed by user and locale.
- Version the BFF with its client; breaking changes ship together.

## Avoid
- Business rules in the BFF: logic duplicates across clients. Keep them in services.
- Sequential downstream calls: latency adds up. Parallelise independent ones.
- One BFF for every client: it grows into a lowest-common-denominator API. Split per client.
- Passing downstream error bodies through: leaks internals. Map to stable errors.
- A BFF that talks to the database directly: it bypasses service ownership. Call the service.

## Review
- [ ] Each BFF serves one client type and has one owner.
- [ ] Parallel fan-out with per-call timeouts.
- [ ] Partial failure behaviour tested.
- [ ] No domain logic or direct data access.
