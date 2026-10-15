---
name: oauth2-oidc
title: OAuth 2.0 and OpenID Connect
area: security
tags: [security, oauth2, oidc, auth, pkce, sso, login]
detect: [dep:authlib, dep:oauthlib, dep:openid-client, dep:oidc-client-ts, dep:passport-openidconnect, dep:github.com/coreos/go-oidc/v3]
related: [jwt, sessions, csrf, authorization, secrets-management]
---
Authorization code flow with PKCE, strict redirect URIs and state, and full ID token validation; never implicit flow.

## Verify
- `pytest -q tests/security/test_oauth.py`: state, nonce, PKCE and redirect tests pass.
- `curl -s https://ISSUER/.well-known/openid-configuration | jq '.code_challenge_methods_supported'`: the provider supports `S256`.
- `grep -rnE "response_type=token|implicit" src/`: no implicit flow.

## Test first
Prove the callback refuses forged input.
```python
def test_callback_rejects_wrong_state(client):
    client.get("/login/oidc")  # sets state in the session
    r = client.get("/callback?code=abc&state=attacker")
    assert r.status_code == 400

def test_id_token_wrong_audience_rejected(validate, token_for):
    with pytest.raises(Exception):
        validate(token_for(aud="some-other-client"))
```

## Do
- Use authorization code flow with PKCE (`S256`) for every client, public or confidential.
- Generate `state`, `nonce` and the PKCE verifier per request from a CSPRNG, store them server-side, and compare on callback.
- Register exact redirect URIs and compare them as whole strings. No wildcards, no open redirect on the app.
- Validate the ID token: signature via the issuer's JWKS, `iss`, `aud`, `exp`, `nonce`. Use the provider library for it.
- Request the minimum scopes. Treat access tokens as opaque unless you are the resource server.
- Keep client secrets and refresh tokens server-side. Rotate refresh tokens and revoke on logout.
- Map users by `iss` plus `sub`, not by email.

## Avoid
- Implicit flow or tokens in the URL fragment: tokens leak via history and Referer. Use code plus PKCE.
- Skipping `state`: login CSRF lets an attacker bind their account to the victim. Verify it.
- Matching users by unverified `email`: account takeover. Key on `sub` and require `email_verified` if linking.
- Decoding the ID token without verifying: `jwt.decode(..., verify=False)` trusts forged tokens. Verify signature and claims.
- Using an access token as proof of login: it is for an API, not for identity. Use the validated ID token.
- Storing tokens in `localStorage` for a web app: XSS reads them. Prefer a server session or a backend-for-frontend.

## Review
- [ ] Code flow with PKCE, and `state` and `nonce` are checked.
- [ ] Redirect URIs are exact and registered.
- [ ] ID token `iss`, `aud`, `exp`, signature are validated.
- [ ] Accounts link by `iss` and `sub`.
- [ ] Secrets and refresh tokens are server-side only.
