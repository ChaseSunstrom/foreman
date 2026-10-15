---
name: api-testing
title: API testing
area: testing
tags: [api, http, rest, status-codes, schema, auth]
detect: [dep:supertest, dep:httpx, dep:rest-assured, dep:schemathesis, dep:dredd, file:openapi.yaml, file:openapi.json, file:*.http]
related: [contract-testing, integration-testing, e2e-strategy, test-data-factories]
---
Test HTTP APIs at the boundary: status, headers, body schema, auth and error shapes, against a real app instance with a real or contained database.

## Verify
- `pytest -q tests/api`: in-process client tests (httpx with the ASGI or WSGI app) pass.
- `npx jest --testPathPattern api`: Supertest-style tests pass without binding a fixed port.
- `schemathesis run openapi.yaml --url http://localhost:8000`: generated requests find responses violating the schema.
- `curl -sS -o /dev/null -w "%{http_code}\n" http://localhost:8000/health`: a manual smoke check of status.

## Test first
Write the request and the full expected response contract, including the error case.
```ts
import request from "supertest";
import { app } from "../src/app";

test("POST /users rejects a duplicate email with 409", async () => {
  await request(app).post("/users").send({ email: "a@b.co" }).expect(201);
  const res = await request(app).post("/users").send({ email: "a@b.co" }).expect(409);
  expect(res.body).toEqual({ error: "email_taken" });
});
```
Tests live in `tests/api/` or beside routes.

## Do
- Assert status code, `Content-Type`, body shape and key values for every route, on success and each failure class (400, 401, 403, 404, 409, 422).
- Test authentication and authorization separately: no token, bad token, wrong role, another tenant's resource.
- Validate responses against the OpenAPI schema in a shared helper.
- Test pagination, filtering, sorting and idempotency of retried writes (`Idempotency-Key` where used).
- Check that errors never leak stack traces or internals.
- Use an in-process client for speed, and a few tests through the real network stack.
- Create data per test via factories; reset the database between tests.

## Avoid
- Asserting only `200`: wrong bodies pass. Check the payload.
- Exact equality on generated ids and timestamps: brittle. Match types or capture and reuse them.
- Testing only the happy path and a logged-in admin: authorization bugs slip through. Add forbidden and cross-tenant cases.
- Tests that depend on execution order or leftover rows: shard-unsafe. Isolate data.
- Calling a shared staging API from CI: flaky and destructive. Use a local or ephemeral instance.
- Hand-maintained expected JSON drifting from the spec: validate against the schema instead.

## Review
- [ ] Each route has success and error tests with full status and body checks.
- [ ] Auth cases cover missing, invalid, insufficient and cross-tenant access.
- [ ] Responses are schema-validated.
- [ ] Error bodies do not leak internals.
- [ ] Tests own their data and run in any order.
