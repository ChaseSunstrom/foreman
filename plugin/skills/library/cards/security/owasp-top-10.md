---
name: owasp-top-10
title: OWASP Top 10
area: security
tags: [security, owasp, web, appsec, review, testing]
detect: []
related: [threat-modeling, authorization, sql-injection, security-headers, dependency-audit, semgrep]
---
Use the OWASP Top 10 as a review checklist: each category becomes one failing test or one scanner rule before the fix.

## Verify
- `semgrep scan --config p/owasp-top-ten --error`: the OWASP ruleset finds nothing new.
- `grep -rnE "(password|secret|api_key)\s*=\s*['\"][^'\"]+['\"]" --include=* src/`: no hardcoded credentials in source.
- `pytest -q tests/security` (or the stack's runner on the security folder): every category test passes.

## Test first
Keep one test per category you touch, in `tests/security/`, named by category. Write the exploit as the test and watch it fail.
```python
def test_user_cannot_read_other_users_invoice(client, alice, bob_invoice):
    r = client.get(f"/invoices/{bob_invoice.id}", headers=alice.auth)
    assert r.status_code in (403, 404)

def test_login_error_does_not_reveal_which_field_was_wrong(client):
    a = client.post("/login", json={"email": "nobody@x.io", "password": "x"})
    b = client.post("/login", json={"email": "real@x.io", "password": "bad"})
    assert a.json() == b.json() and a.status_code == b.status_code
```

## Do
- Map each Top 10 category to the code that owns it: access control in the authorization layer, injection in query builders, cryptographic failures in storage and transport, and so on.
- Deny by default: a route or object without an explicit rule is refused.
- Enforce checks on the server for every request, including the ones the UI hides.
- Pin and audit dependencies, and fail CI on known-vulnerable ones.
- Log security events (login failure, access denied, validation reject) with no secrets or PII in them.
- Make config secure by default: debug off, verbose errors off, default accounts removed, headers set.
- Treat every outbound fetch of a user-supplied URL as SSRF until proven otherwise.

## Avoid
- Checking access only at the UI or on list endpoints: direct object requests bypass it. Check ownership on every read, write and delete.
- Rolling your own crypto or token format: use a vetted library with its default algorithms.
- Returning stack traces or SQL errors to clients: log them server-side, return a generic message and a request id.
- Disabling TLS verification "just for dev" (`verify=False`, `rejectUnauthorized: false`): it ships. Use a local CA instead.
- Treating a passing scanner as proof of safety: scanners miss logic flaws. Keep the threat-model-driven tests.
- Trusting client-supplied roles, prices or ids in a body: re-derive them from the session or the database.

## Review
- [ ] Each changed endpoint has an authorization check tested with a second, unprivileged user.
- [ ] No user input reaches a query, shell, path, template or URL fetch unparameterized or unvalidated.
- [ ] Secrets come from the environment or a secret store, never the repo.
- [ ] New dependencies were audited and pinned.
- [ ] Failures are logged without sensitive data, and responses leak no internals.
