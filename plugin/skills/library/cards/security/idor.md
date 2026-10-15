---
name: idor
title: IDOR and BOLA
area: security
tags: [security, idor, bola, authorization, api, multi-tenant]
detect: []
related: [authorization, mass-assignment, api-security, input-validation]
---
Every object lookup is scoped to the caller: owner or tenant in the query itself, 404 for foreign ids, tested with two users.

## Verify
- `pytest -q -k "idor or cross_tenant"`: two-user tests pass for every resource route.
- `git grep -nE "get_object_or_404|findById|find_by_id|\.get\(id|WHERE id *=" -- ':!*test*'`: each lookup by raw id is checked for an owner or tenant filter.
- `git grep -nE "uuid|gen_random_uuid" -- ':!*test*'`: ids are unguessable, which helps but is never the control.

## Test first
User B must not reach user A's object by any verb.
```python
import pytest

@pytest.mark.parametrize("method,path", [
    ("get", "/orders/{id}"), ("put", "/orders/{id}"),
    ("delete", "/orders/{id}"), ("get", "/orders/{id}/invoice"),
])
def test_other_user_gets_404(client, alice_order, bob, method, path):
    r = getattr(client, method)(path.format(id=alice_order.id), headers=bob)
    assert r.status_code == 404
```

## Do
- Put the scope in the query: `WHERE id = :id AND owner_id = :uid` (or tenant id). Do not fetch and then compare in handler code.
- Centralise it in one repository, manager or policy layer so a new route cannot forget.
- Return 404 for objects the caller cannot see, so existence does not leak.
- Derive the owner from the session, never from a body or query field.
- Check child resources against the parent's ownership (`/orders/1/items/9`).
- Cover bulk, export, search, file download, websocket and GraphQL paths as well as CRUD.
- Use database row-level security for multi-tenant stores as a second layer.
- Use random UUIDs for ids as defence in depth only.

## Avoid
- Trusting a `user_id` field in the JSON body or URL: read it from the authenticated principal.
- Authorising the parent but not the child id: verify the relation in the query.
- Auth checks only on the UI route: apply them in the API and the data layer.
- "Hidden" admin endpoints with no role check: enforce the role server-side.
- Sequential ids with no scope check: scoping fixes it, and UUIDs alone do not.
- Separate, unscoped code for exports or downloads: use the same scoped lookup.

## Review
- [ ] Every object route loads through a scoped query or policy.
- [ ] Tests exist with two users and two tenants for read, write and delete.
- [ ] Foreign ids return 404, not 403 or 200.
- [ ] Owner comes from the session, not the request.
- [ ] Nested, bulk, export and file routes are covered.
