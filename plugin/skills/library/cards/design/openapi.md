---
name: openapi
title: OpenAPI
area: design
tags: [openapi, spec, api, schema, contracts, codegen]
detect: [file:openapi.yaml, file:openapi.yml, file:openapi.json, file:swagger.yaml, dep:@redocly/cli, dep:@stoplight/spectral-cli]
related: [rest-api-design, api-versioning, error-handling, pagination]
---
OpenAPI 3.x documents as the contract: lint them, diff them for breaking changes, generate from or check against code.

## Verify
- `npx @redocly/cli lint openapi.yaml`: structure, refs and ruleset violations.
- `npx @stoplight/spectral-cli lint openapi.yaml`: style rules, if a `.spectral.yaml` exists.
- `npx @redocly/cli bundle openapi.yaml -o dist/openapi.yaml`: all `$ref`s resolve into one file.
- `git show main:openapi.yaml > /tmp/old.yaml && npx oasdiff breaking /tmp/old.yaml openapi.yaml`: no breaking changes against main (needs oasdiff installed).

## Test first
Validate real responses against the schema, so spec drift fails a test.
```python
from openapi_core import OpenAPI
from openapi_core.contrib.requests import RequestsOpenAPIRequest, RequestsOpenAPIResponse

spec = OpenAPI.from_file_path("openapi.yaml")

def test_get_order_matches_spec(live_server):
    r = requests.get(f"{live_server}/orders/1")
    spec.validate_response(RequestsOpenAPIRequest(r.request), RequestsOpenAPIResponse(r))
```
Alternatives: schemathesis (`schemathesis run openapi.yaml --url ...`) for property-based checks.

## Do
- Declare `openapi: 3.0.x` or `3.1.x` at the top. Pick one and keep the tooling consistent.
- Put shared objects in `components/schemas`, `components/parameters` and `components/responses`, and `$ref` them.
- Give each operation a unique `operationId`. Codegen uses it for method names.
- Mark `required` fields explicitly and set `additionalProperties: false` on request bodies you validate strictly.
- Document every response code the handler can return, including 4xx and the shared error schema.
- Use `securitySchemes` plus a top-level `security`, and override per operation (`security: []` for public).
- Add `example` values: they feed docs, mocks and contract tests.

## Avoid
- Hand-edited generated clients: regenerate from the spec and commit only the spec change.
- Using `nullable: true` in a 3.1 document: 3.1 uses JSON Schema, so write `type: [string, "null"]`.
- `type: object` with no properties: it accepts anything. Define fields or say `additionalProperties` deliberately.
- Documenting only the 200: clients can't handle errors they can't see.
- Inline-duplicating schemas: they drift. Use `$ref`.
- A spec that is never checked against the running service: add response validation to tests.

## Review
- [ ] Lint is clean and `oasdiff breaking` reports nothing without a version bump.
- [ ] Every operation has a unique `operationId`, tags, and documented error responses.
- [ ] Secured routes declare security, and public ones say so explicitly.
- [ ] Enums, formats, min/max and `required` match the actual validation code.
- [ ] Examples are valid against their own schemas.
