---
name: authorization
title: Authorization and access control
area: security
tags: [security, authorization, rbac, idor, access-control, multitenancy]
detect: [dep:casbin, dep:django-guardian, dep:@casl/ability, dep:cancancan, dep:pundit, dep:github.com/casbin/casbin/v2, dep:open-policy-agent]
related: [owasp-top-10, sessions, jwt, input-validation, threat-modeling]
---
Authorization: a central, deny-by-default check on every request that binds the caller to the specific object, tested with a second user.

## Verify
- `pytest -q tests/security -k "authz or idor or forbidden"`: cross-user and cross-tenant access is refused.
- `grep -rnE "@(public|no_auth|allow_any)|skip_authorization|permit_all" src/`: every bypass is listed and justified.
- `semgrep scan --config p/owasp-top-ten --error`: no missing-authorization patterns flagged.

## Test first
Write the IDOR test with two users before the endpoint exists.
```python
def test_alice_cannot_read_or_delete_bobs_document(client, alice, bob_doc):
    assert client.get(f"/docs/{bob_doc.id}", headers=alice.auth).status_code in (403, 404)
    assert client.delete(f"/docs/{bob_doc.id}", headers=alice.auth).status_code in (403, 404)
    assert Document.exists(bob_doc.id)

def test_unauthenticated_is_401(client, bob_doc):
    assert client.get(f"/docs/{bob_doc.id}").status_code == 401
```

## Do
- Enforce in one layer (middleware, policy object, or query scope) that handlers cannot skip. Default is deny.
- Scope queries by owner or tenant (`WHERE id = ? AND tenant_id = ?`) so a foreign id returns nothing.
- Check the action on the object (read, update, delete) rather than only a role.
- Derive identity and tenant from the verified session or token, never from a body or header the client sets.
- Return 404 for objects the caller may not know exist and 403 for known ones, consistently.
- Re-check authorization when a job, webhook, or background task acts on a user's behalf.
- Test every role against every write endpoint, including mass-assignment of `role`, `owner_id` and `is_admin`.

## Avoid
- Hiding the button and calling it done: direct requests bypass the UI. Enforce on the server.
- Sequential ids with no ownership check (IDOR): add the scope to the query, and use unguessable ids as defense in depth only.
- Authorizing at the controller but not in the service or job that also exposes the data: put the check where data is loaded.
- Binding the whole request body to a model: mass assignment sets `is_admin`. Use an allowlist schema.
- Trusting a role claim from an unverified or stale token: re-read permissions from the source of truth for sensitive actions.
- Role checks scattered as `if user.is_admin` strings: centralize them as named permissions.

## Review
- [ ] Every route is authenticated or listed as public on purpose.
- [ ] Every object access is scoped to the caller or tenant.
- [ ] A second-user test exists for each read and write.
- [ ] Input schemas whitelist writable fields.
- [ ] Background jobs and webhooks re-check access.
