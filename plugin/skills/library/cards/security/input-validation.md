---
name: input-validation
title: Input validation
area: security
tags: [security, validation, allowlist, schema, sanitization, parsing]
detect: []
related: [sql-injection, xss, command-injection, path-traversal, authorization, upload-security]
---
Validate every untrusted input at the boundary against an allowlist schema for type, size, range and format, then use safe sinks downstream.

## Verify
- `pytest -q tests/security -k "validation or oversize or malformed"`: bad, huge and malformed inputs are rejected.
- `semgrep scan --config p/security-audit --error`: no input flows to a dangerous sink unhandled.
- `curl -s -o /dev/null -w "%{http_code}" -X POST localhost:8000/items -H "Content-Type: application/json" -d '{"name": 5}'`: a wrong type returns 4xx, not 500.

## Test first
Send hostile input to the boundary and expect a 4xx.
```python
import pytest
@pytest.mark.parametrize("body", [
    {"qty": -1}, {"qty": 10**12}, {"qty": "1; DROP TABLE x"},
    {"name": "a" * 100_000}, {"name": None}, {"unknown_field": 1},
])
def test_create_item_rejects_bad_input(client, body):
    r = client.post("/items", json={"name": "ok", "qty": 1, **body})
    assert 400 <= r.status_code < 500
```

## Do
- Define one schema per endpoint (Pydantic, Zod, JSON Schema, Bean Validation) with types, min and max, patterns, and enums. Reject unknown fields.
- Validate on the server for every request; client checks are for UX only.
- Cap body size, array length, string length, nesting depth, and number of fields at the framework or proxy.
- Parse into typed values once, then pass the typed value, not the raw string.
- Prefer allowlists to denylists: describe what is valid, not what is bad.
- Canonicalize before checking (decode, normalize Unicode with NFC, resolve paths), then validate, then use the same canonical value.
- Validate again where trust changes: queue consumers, webhooks, file contents, third-party API responses.
- Return a generic 400 or 422 with field names, never the raw input echoed unescaped.

## Avoid
- Validation as sanitization by regex stripping (`replace("<script>", "")`): trivially bypassed. Encode on output and parameterize on input.
- Checking before decoding: `%2e%2e` or double-encoded input passes the check and decodes later. Canonicalize first.
- Trusting `Content-Type`, file extension or hidden form fields: attacker-controlled. Verify content.
- Unbounded input (`limit=1000000`, no body cap): memory and CPU denial of service. Enforce maximums.
- Regexes with nested quantifiers on user input: ReDoS. Use linear-time engines or bound the length first.
- Using validation to replace output encoding or parameterized queries: they are separate defenses. Apply all.

## Review
- [ ] Every entry point has a schema with limits and rejects extras.
- [ ] Sizes, counts and depth are bounded.
- [ ] Input is canonicalized before validation.
- [ ] Failures return 4xx without echoing input.
- [ ] Safe sinks (parameters, encoders, allowlists) are used in addition.
