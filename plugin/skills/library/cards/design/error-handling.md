---
name: error-handling
title: Error handling
area: design
tags: [errors, exceptions, problem-details, logging, boundaries, failure-modes]
detect: []
related: [rest-api-design, retries-backoff, hexagonal-architecture, grpc, idempotency]
---
Typed errors at boundaries: expected failures are values or domain exceptions, unexpected ones are logged once and mapped to a safe response.

## Verify
- `curl -si localhost:8080/orders/nope`: 404 with the standard error body and no stack trace.
- `curl -si -X POST localhost:8080/orders -d 'not json'`: 400 or 422 with the same error shape, not 500.
- `grep -rnE "except( Exception)?:\s*(pass)?$|catch \(\w*\) \{\s*\}" src`: no swallowed exceptions (expect no output; adjust syntax for your language).
- `pytest -q tests/errors`: each domain error maps to its code and status.

## Test first
Assert the mapping and that internals never leak.
```python
def test_unexpected_error_hides_details_and_logs_once(client, caplog):
    with patch("app.orders.repo.get", side_effect=RuntimeError("db password=hunter2")):
        r = client.get("/orders/1")
    assert r.status_code == 500
    assert r.json() == {"error": {"code": "internal", "message": "Internal error", "request_id": ANY}}
    assert "hunter2" not in r.text
    assert sum("RuntimeError" in m for m in caplog.messages) == 1
```

## Do
- Define a small error taxonomy: validation, not found, conflict, unauthorized, forbidden, rate limited, unavailable, internal. Each has a stable machine code.
- Use one response shape (RFC 9457 `application/problem+json` is a good one), with `code`, `message`, field errors and a request ID.
- Throw or return domain errors from the core, and translate to HTTP or gRPC codes only at the edge in one handler.
- Log each failure once, at the boundary that handles it, with the request ID and cause chain. Rethrow with context (`raise X from e`, `fmt.Errorf("...: %w", err)`).
- Distinguish retryable from permanent errors in the type or code, so callers can decide.
- Validate input at the boundary and report all field errors together.
- Close resources with `finally`, `with`, `defer` or RAII, so failure paths release them.
- Fail fast on misconfiguration at startup.

## Avoid
- Bare `except:` or empty `catch`: failures vanish. Catch the specific type, and handle or rethrow.
- Returning raw exception messages to clients: they leak SQL, paths and secrets. Return a code, and log the detail server-side.
- Logging and rethrowing at every layer: the same error appears five times. Log once at the handling site.
- 200 responses carrying error payloads, or 500 for client mistakes: use accurate status codes.
- Using exceptions for normal control flow in hot paths (such as "not found" lookups): return an option or result.
- Error strings as the contract (`if "not found" in str(e)`): callers break on rewording. Match on type or code.
- Losing the original cause when wrapping: keep it chained.

## Review
- [ ] Every error maps to a stable code and the right status in one place.
- [ ] No internals (stack, SQL, hostnames) appear in responses.
- [ ] Each failure is logged once with a request ID.
- [ ] Retryable and permanent failures are distinguishable.
- [ ] Tests cover validation, not found, conflict and unexpected errors.
