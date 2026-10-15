---
name: security-tests
title: Security tests
area: testing
tags: [testing, security, authz, injection, sast, dependencies, secrets]
detect: []
related: [fuzzing, api-testing, integration-testing, regression-tests]
---
Turn security rules into tests: authorization matrices, hostile inputs, secret and dependency scans, each failing before the fix.

## Verify
- `semgrep --config auto --error .`: static rules flag injection, unsafe deserialization and similar patterns (fails on findings).
- `gitleaks detect --no-banner`: no secrets in the repository history.
- `pip-audit` (or `npm audit --audit-level=high`, `cargo audit`, `govulncheck ./...`): no known-vulnerable dependencies.
- `pytest -q tests/security`: authorization, injection and input-validation tests pass.

## Test first
Write the abuse case as a request that must be refused, and watch it fail.
```python
@pytest.mark.parametrize("path", ["/orders/{id}", "/orders/{id}/invoice"])
def test_user_cannot_read_another_users_order(client, alice, bob_order, path):
    r = client.get(path.format(id=bob_order.id), headers=auth(alice))
    assert r.status_code in (403, 404)
    assert bob_order.number not in r.text
```

## Do
- Test authorization as a matrix: each endpoint against anonymous, user, other-user, admin; the cross-tenant case is the one that matters.
- Test authentication edges: missing, expired, tampered and wrong-audience tokens; session fixation and logout invalidation.
- Feed hostile inputs to every parser and query: SQL metacharacters, path traversal (`../`), oversized bodies, null bytes, unicode tricks, XML entities, template syntax.
- Assert output encoding and headers: no secrets in errors or logs, `Content-Type` and CSP set, cookies `HttpOnly` and `Secure`.
- Verify rate limits and lockouts trigger, and that error messages do not reveal whether an account exists.
- Check that SQL uses bound parameters by testing a quote-bearing input end to end.
- Run SAST, secret scanning and dependency audits in CI as blocking checks.
- Add a regression test for every vulnerability fixed, named for the issue.

## Avoid
- Testing only that the happy path is allowed: access control gaps stay. Test the denied cases.
- Checking authorization in the UI test only: the API stays open. Test the endpoint directly.
- Hard-coded real secrets in tests or fixtures: leak risk. Use obviously fake values and generate them.
- Asserting only the status code on denial: data may still leak in the body. Assert the body is clean.
- Disabling the scanner on noisy findings with a blanket ignore: real issues hide. Suppress per finding with a reason.
- Mocking the auth layer in every test: auth bugs go untested. Keep a suite that uses real auth.

## Review
- [ ] Authorization matrix includes cross-user and cross-tenant access.
- [ ] Hostile inputs reach every parser, query and file path.
- [ ] Denial responses leak no data or account existence.
- [ ] Secret, SAST and dependency scans run and block in CI.
- [ ] Every fixed vulnerability has a regression test.
