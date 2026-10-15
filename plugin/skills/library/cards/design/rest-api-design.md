---
name: rest-api-design
title: REST API design
area: design
tags: [rest, http, api, resources, status-codes, contracts]
detect: [file:openapi.yaml, file:openapi.json, file:swagger.yaml]
related: [openapi, pagination, idempotency, api-versioning, error-handling]
---
Resource-oriented HTTP APIs with correct verbs, status codes, caching headers and one error shape.

## Verify
- `npx @redocly/cli lint openapi.yaml`: the spec is valid and follows the lint ruleset.
- `curl -si -X POST localhost:8080/orders -H 'content-type: application/json' -d '{}'`: a bad body returns 4xx with the documented error shape, not 500.
- `curl -si -X OPTIONS localhost:8080/orders`: the `Allow` header lists exactly the verbs the route supports.
- `curl -si localhost:8080/orders/unknown-id`: 404 with the standard error body.

## Test first
Contract tests hit the running app (or its in-process test client) and assert status, headers and body shape together.
```python
def test_create_order_returns_201_with_location(client):
    r = client.post("/orders", json={"sku": "A1", "qty": 2})
    assert r.status_code == 201
    assert r.headers["Location"] == f"/orders/{r.json()['id']}"

def test_create_order_rejects_negative_qty(client):
    r = client.post("/orders", json={"sku": "A1", "qty": -1})
    assert r.status_code == 422 and r.json()["error"]["code"] == "validation_failed"
```

## Do
- Model nouns, not actions: `POST /orders`, `GET /orders/{id}`, `POST /orders/{id}/cancel` only when a state change has no resource form.
- Return 201 plus `Location` on create, 204 on empty success, 202 for accepted async work with a status resource.
- Make GET and HEAD safe, PUT and DELETE idempotent. Use PATCH with a documented merge format.
- Give every collection pagination, a stable sort and a filter whitelist from day one.
- Send `ETag` and honor `If-None-Match` (304) and `If-Match` (412) for optimistic concurrency.
- Use one error envelope everywhere, with a machine code, a message and field paths.
- Use plural, lowercase, hyphenated path segments and opaque string IDs.

## Avoid
- 200 with `{"success": false}`: clients and proxies read the status. Use a real 4xx or 5xx.
- Verbs in paths (`/getUser`, `/createOrder`): model the resource and use the HTTP method.
- Sequential integer IDs exposed publicly: they enable enumeration. Use UUIDs or ULIDs, plus authorization checks on every read.
- Returning 500 for validation or missing rows: map domain errors to 400, 404, 409 or 422 explicitly.
- Unbounded list endpoints: add a default and maximum `limit`.
- Breaking changes inside a version, such as renaming a field or tightening an enum: add a field, deprecate the old one, version for removals.
- Leaking DB columns by serializing the ORM row: use explicit response schemas.

## Review
- [ ] Each route's verb, status codes and idempotency match HTTP semantics.
- [ ] One error envelope is used across all routes, including 404 and 405.
- [ ] Collections are paginated, sorted deterministically and filtered through a whitelist.
- [ ] Authorization is checked per resource, not just per route.
- [ ] The OpenAPI document is updated in the same change and lint passes.
