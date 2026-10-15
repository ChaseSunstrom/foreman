---
name: auth-providers
title: Auth Providers and OAuth
area: domains
tags: [auth, oauth, oidc, sessions, jwt, sso]
detect: [dep:next-auth, dep:@auth/core, dep:passport, dep:@clerk/nextjs, dep:@auth0/nextjs-auth0, dep:firebase-admin, dep:@supabase/supabase-js, dep:authlib, dep:oauthlib, dep:openid-client, dep:jose, dep:lucia, dep:better-auth, dep:keycloak-js]
related: [browser-storage, stripe, chat-bots, gdpr, webhooks]
---
Delegated login with OAuth 2.0 and OpenID Connect: authorization code with PKCE, validated tokens, server-side sessions.

## Verify
- `curl -s https://issuer.example.com/.well-known/openid-configuration | jq '.issuer,.jwks_uri,.token_endpoint'`: discovery document matches what the app is configured with.
- `grep -rnE "client_secret|CLIENT_SECRET" . --exclude-dir=node_modules --exclude=.env.example`: secrets are not in tracked source.
- `curl -sI https://app.example.com/dashboard`: unauthenticated request redirects to login (302) or gives 401.
- `curl -s -X POST localhost:3000/api/admin -H "authorization: Bearer $USER_TOKEN" -w "%{http_code}"`: a valid but unprivileged token gets 403.

## Test first
Test token validation and authorization, not the provider.
```python
import jwt, time, pytest
from app.auth import verify_token, AuthError

def make(claims, key="k", alg="HS256"):
    return jwt.encode({"iss": "https://idp", "aud": "app", "exp": time.time()+60, **claims}, key, alg)

@pytest.mark.parametrize("claims", [
    {"exp": time.time()-1},          # expired
    {"aud": "other-app"},            # wrong audience
    {"iss": "https://evil"},         # wrong issuer
])
def test_rejects_invalid_claims(claims):
    with pytest.raises(AuthError):
        verify_token(make(claims))

def test_rejects_alg_none():
    with pytest.raises(AuthError):
        verify_token(jwt.encode({"iss": "https://idp", "aud": "app"}, None, algorithm="none"))
```

## Do
- Use authorization code flow with PKCE for web, SPA and mobile; skip implicit and password grants (removed in OAuth 2.1).
- Generate and check `state` (CSRF) and `nonce` (ID token replay); require exact registered redirect URIs.
- Validate ID and access tokens: signature via JWKS (cache with rotation), `iss`, `aud`, `exp`, `nbf`, and an allow-listed `alg`.
- Keep tokens server-side: session cookie `HttpOnly; Secure; SameSite=Lax`; rotate the session id at login; short access tokens with refresh rotation.
- Authorize on your own data and roles per request; the identity from the provider is not permission.
- Key users by the stable `sub` plus issuer, not by email; treat unverified email as unverified when linking accounts.
- Request minimal scopes; handle consent denial and revoked access.
- Implement logout including provider logout and token revocation.
- Prefer a maintained library or hosted provider over hand-written flows.

## Avoid
- Accepting `alg: none` or letting the token pick the algorithm: forgery. Pin the expected algorithms.
- Decoding a JWT without verifying (`jwt.decode(..., verify=False)`, `decode` instead of `verify` in jsonwebtoken): trusts attacker data. Verify.
- Tokens in localStorage: stolen by XSS. Use HttpOnly cookies or the backend-for-frontend pattern.
- Wildcard or prefix-matched redirect URIs: open redirect and code theft. Register exact URIs.
- Linking accounts by email automatically: account takeover. Require verified email and confirmation.
- Skipping `state` or PKCE: CSRF and code interception. Always send both.
- Long-lived JWTs with no revocation: no logout. Use short expiry plus a server-side session.
- Client secrets in SPAs or mobile apps: public clients cannot keep secrets. Use PKCE only.

## Review
- [ ] Flow is code plus PKCE with `state` and `nonce` verified.
- [ ] Token validation checks signature, issuer, audience, expiry and algorithm.
- [ ] Tokens never reach script-readable storage; sessions rotate on login.
- [ ] Authorization is enforced server-side per request, with identity keyed on `sub`.
- [ ] Logout, revocation and secret rotation are implemented.
