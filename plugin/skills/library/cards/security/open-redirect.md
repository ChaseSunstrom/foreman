---
name: open-redirect
title: Open redirect
area: security
tags: [security, redirect, url, validation, oauth, web]
detect: []
related: [oauth2-oidc, ssrf, input-validation, xss]
---
Redirect targets from user input go through an allow-list of local paths or known hosts, parsed with a URL parser, never string checks.

## Verify
- `git grep -nE "redirect\(|Location|res\.redirect|HttpResponseRedirect" -- ':!*test*'`: list every redirect and check what feeds its target.
- `curl -si 'http://localhost:8000/login?next=//evil.example' | grep -i '^location'`: the Location stays on your host.
- `pytest -q -k redirect`: the table test below passes.

## Test first
One table of hostile targets.
```python
import pytest

@pytest.mark.parametrize("next_", [
    "https://evil.example", "//evil.example", "/\\evil.example",
    "javascript:alert(1)", "https:evil.example", "/ok@evil.example",
    "https://app.example.evil.example",
])
def test_next_param_never_leaves_site(client, next_):
    r = client.get("/login/done", params={"next": next_}, follow_redirects=False)
    assert r.headers["location"] == "/"
```

## Do
- Prefer an id or name mapped server-side (`next=dashboard`) over a URL.
- Otherwise accept only a relative path: starts with a single `/`, second character not `/` or `\`, no scheme, and no control characters.
- For cross-site targets, parse with a real URL parser and compare the scheme and exact hostname to an allow-list. Do not use `startswith` or `in`.
- Fall back to a safe default when validation fails. Do not echo the bad value.
- Validate OAuth `redirect_uri` by exact string match against registered values.
- Show an interstitial ("you are leaving") for any external link you must support.
- Reject backslashes, and decode once before checking so encoded slashes are caught.

## Avoid
- `startswith("/")` as the check: `//evil.example` passes. Also reject a leading `//` and `/\`.
- Substring or suffix host checks (`"example.com" in url`): `example.com.evil.example` passes. Compare exact parsed hostnames.
- Validating before decoding, then redirecting after: validate the exact string you send.
- Prefix matching for OAuth redirect URIs: use exact match.
- Allowing `javascript:` and `data:` schemes: accept only http and https, or relative.
- Using the `Referer` header as a return target: it is attacker-influenced.

## Review
- [ ] Every redirect target is traced to its source.
- [ ] Validation uses a URL parser and exact-host comparison.
- [ ] The table test covers protocol-relative, backslash, userinfo and lookalike hosts.
- [ ] Failure falls back to a fixed safe path.
- [ ] OAuth redirect URIs are exact-matched.
