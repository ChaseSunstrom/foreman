---
name: mass-assignment
title: Mass assignment
area: security
tags: [security, mass-assignment, validation, orm, api, authorization]
detect: []
related: [idor, input-validation, authorization, prototype-pollution]
---
Bind requests to explicit input schemas with only writable fields; never splat a body into a model.

## Verify
- `git grep -nE "\*\*(request|req|body|data|payload)|Object\.assign\(.*body|\.update\(req\.body|create\(req\.body|params\.permit!" -- ':!*test*'`: unfiltered binding sites.
- `pytest -q -k mass_assign`: the privilege-field tests pass.
- `git grep -nE "is_admin|role|owner_id|tenant_id|balance|verified" -- '*schema*' '*serializer*' '*dto*'`: sensitive fields are absent from input schemas.

## Test first
Send privileged fields on create and update and require that they are ignored or refused.
```python
def test_user_cannot_set_role_on_signup(client):
    r = client.post("/users", json={"email": "a@x.io", "password": "pw-long-enough",  # pragma: allowlist secret
                                    "role": "admin", "is_verified": True})
    assert r.status_code in (201, 422)
    u = client.get("/me", headers=login(r)).json()
    assert u["role"] == "user" and u["is_verified"] is False

def test_user_cannot_reassign_owner(client, alice, alice_doc, bob):
    client.patch(f"/docs/{alice_doc.id}", json={"owner_id": bob.id}, headers=alice.auth)
    assert alice_doc.refresh().owner_id == alice.id
```

## Do
- Define separate input and output types per operation (`UserCreate`, `UserUpdate`, `UserOut`) listing only writable fields.
- Forbid unknown fields (Pydantic `extra="forbid"`, zod `.strict()`, Rails strong parameters with explicit `permit`, DTO whitelisting in NestJS `whitelist: true, forbidNonWhitelisted: true`).
- Set server-controlled fields (owner, tenant, role, status, price, timestamps) in code from the session or logic.
- Use a different schema for admin edits, behind an admin check.
- Mark sensitive model attributes as read-only or protected where the ORM supports it.
- Return 422 on unknown fields in internal APIs, so mistakes surface in tests.
- Apply the same rules to PATCH, bulk and nested writes.

## Avoid
- `Model(**request.json())` or `Model.objects.create(**data)`: callers choose any column. Parse into an input schema, then map named fields.
- One schema for read and write: the output fields (`role`, `id`) become writable. Split them.
- Blocklisting `is_admin`: new sensitive fields slip through. Allow-list instead.
- Rails `permit!` or Mongoose `new Model(req.body)`: list fields explicitly.
- Trusting hidden form fields or client-sent prices and totals: recompute on the server.
- Treating PATCH differently from POST: validate both with explicit schemas.

## Review
- [ ] No request body is splatted into a model or query.
- [ ] Input schemas forbid extras and exclude privileged fields.
- [ ] Ownership, role, tenant and money fields are set server-side only.
- [ ] Tests post privileged fields on create, update and bulk routes.
- [ ] Admin schemas are separate and role-gated.
