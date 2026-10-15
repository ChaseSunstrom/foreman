---
name: pii-logging
title: PII and secrets in logs
area: security
tags: [security, logging, pii, privacy, redaction, observability]
detect: []
related: [secrets-management, password-hashing, input-validation, owasp-top-10]
---
Logging without leaks: never write credentials, tokens or personal data to logs, redact centrally, and test that the redaction holds.

## Verify
- `pytest -q tests/security/test_log_redaction.py`: logged records contain no planted secret or PII values.
- `grep -rnE "log(ger)?\.(debug|info|warn|error).*(password|token|secret|authorization|ssn|card)" src/`: no log line names a sensitive field.
- `gitleaks detect --no-git --source logs/ --no-banner`: sample log output has no secrets.

## Test first
Plant canary values and assert they never reach the log.
```python
import logging
def test_request_logging_redacts_sensitive_fields(client, caplog):
    caplog.set_level(logging.DEBUG)
    client.post("/login", json={"email": "ann@example.com", "password": "S3cretCanary!"},  # pragma: allowlist secret
                headers={"Authorization": "Bearer tok_canary_123"})
    out = caplog.text
    assert "S3cretCanary!" not in out
    assert "tok_canary_123" not in out
    assert "ann@example.com" not in out
```

## Do
- Add a logging filter or formatter that redacts known keys (`password`, `token`, `authorization`, `cookie`, `set-cookie`, `api_key`, `secret`, `ssn`, `card`) in dicts and headers.
- Log identifiers (internal user id, request id) rather than email, name, phone or address.
- Allowlist the fields that may be logged from request and response bodies, instead of dumping the whole object.
- Mask partially when needed (last four digits), and hash with a keyed hash if correlation is required.
- Keep debug logging off in production, and treat access to logs as access to data: restrict, retain briefly and encrypt.
- Strip secrets from URLs and query strings before logging (`?token=...`), and from exception messages and stack-trace local variables.
- Configure error trackers (Sentry and similar) with `send_default_pii` off and a `before_send` scrubber.
- Define retention and deletion for logs that contain personal data.

## Avoid
- `logger.info("request: %s", request.__dict__)` or logging full bodies and headers: it captures tokens and passwords. Log an allowlist.
- Printing the config object at startup: it includes secrets. Log only non-sensitive keys.
- Logging ORM objects or `repr` of models that include hashes, tokens or personal fields: define a safe `__repr__`.
- Redaction by regex on the final string only: formats vary and it misses structured fields. Redact at the structured-field level too.
- Verbose exception output with local variables enabled in production: secrets in frames end up in logs. Disable it.
- Shipping logs to third parties without scrubbing: personal data leaves your control. Scrub before export.
- `?password=` or API keys in URLs: they land in access logs and proxies. Use headers or bodies.

## Review
- [ ] A canary test proves secrets and PII are not logged.
- [ ] Redaction is centralized, not per call site.
- [ ] Request and response logging uses allowlists.
- [ ] Error reporting has PII collection off.
- [ ] Log access and retention are defined.
