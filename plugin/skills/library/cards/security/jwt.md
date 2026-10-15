---
name: jwt
title: JSON Web Tokens
area: security
tags: [security, jwt, tokens, auth, jws, api]
detect: [dep:jsonwebtoken, dep:PyJWT, dep:jose, dep:python-jose, dep:github.com/golang-jwt/jwt/v5, dep:jjwt-api, dep:java-jwt]
related: [oauth2-oidc, sessions, authorization, secrets-management, crypto-usage]
---
JWT verification: pin the algorithm, check every claim, keep tokens short-lived, and never trust an unverified payload.

## Verify
- `pytest -q tests/security/test_jwt.py`: tampered, expired, wrong-alg and wrong-audience tokens are refused.
- `grep -rnE "verify_signature.*False|algorithms=\[.none|ignoreExpiration" src/`: no verification switched off.
- `grep -rniE "jwt.*(secret|key)\s*=\s*['\"]" src/`: no hardcoded signing key.

## Test first
Forge the token and expect a refusal.
```python
import jwt, time, pytest
def test_rejects_alg_none(verify):
    forged = jwt.encode({"sub": "1", "exp": time.time() + 60}, key="", algorithm="none")
    with pytest.raises(Exception):
        verify(forged)

def test_rejects_expired(verify, make_token):
    with pytest.raises(Exception):
        verify(make_token(exp=int(time.time()) - 10))
```

## Do
- Pass an explicit algorithm allowlist to verify (`algorithms=["RS256"]`, `algorithms: ['ES256']`). Never read it from the token header.
- Require and check `exp`, `iss`, `aud`, and `nbf` when present. Set a small clock-skew leeway.
- Keep access tokens to minutes. Use rotating refresh tokens with server-side revocation.
- Prefer asymmetric signing (RS256, ES256, EdDSA) when others verify. For HS256 use a random key of at least 32 bytes.
- Select verification keys by `kid` from a trusted, cached JWKS you fetched from a configured issuer.
- Put identifiers and minimal claims in the payload: it is only encoded, not encrypted.
- Provide a revocation path: a denylist by `jti` or a per-user token version.

## Avoid
- `decode` without verification, or `verify=False`: any attacker can mint tokens. Always verify with keys and algorithms.
- Accepting `alg: none` or letting the header pick the algorithm: algorithm confusion (RS256 public key used as an HS256 secret). Pin it.
- Following a token-supplied `jku`, `x5u` or `jwk` header: attacker-chosen keys. Use configured keys only.
- Secrets or PII inside the payload: it is base64, readable by anyone holding the token.
- Tokens that never expire, or logout that only deletes them client-side: add expiry and revocation.
- Storing tokens in `localStorage`: XSS steals them. Use `HttpOnly` cookies where the architecture allows.
- Comparing a user by `email` claim: use `sub`.

## Review
- [ ] Algorithms are pinned; `none` is rejected.
- [ ] `exp`, `iss`, `aud` are enforced.
- [ ] Keys come from config or a trusted JWKS, never the token.
- [ ] Lifetime is short and revocation works.
- [ ] The payload holds no secrets.
