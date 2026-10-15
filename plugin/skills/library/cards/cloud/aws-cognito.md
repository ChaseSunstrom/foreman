---
name: aws-cognito
title: AWS Cognito
area: cloud
tags: [aws, cognito, auth, user-pool, jwt, oauth, identity]
detect: [dep:@aws-sdk/client-cognito-identity-provider, dep:amazon-cognito-identity-js, dep:aws-jwt-verify, dep:@aws-sdk/client-cognito-identity]
related: [aws-api-gateway, aws-iam, aws-lambda, aws-secrets-manager]
---
Cognito user pools for sign-in and JWTs: authorization code with PKCE, server-side token validation, MFA, and scoped app clients.

## Verify
- `aws cognito-idp describe-user-pool --user-pool-id POOL --query 'UserPool.[MfaConfiguration,Policies.PasswordPolicy,DeletionProtection]'`: MFA, password policy and deletion protection.
- `aws cognito-idp describe-user-pool-client --user-pool-id POOL --client-id CID --query 'UserPoolClient.[AllowedOAuthFlows,CallbackURLs,ExplicitAuthFlows,GenerateSecret]'`: code flow only, exact callback URLs, no unwanted auth flows.
- `aws cognito-idp admin-initiate-auth --user-pool-id POOL --client-id CID --auth-flow ADMIN_USER_PASSWORD_AUTH --auth-parameters USERNAME=u,PASSWORD=p`: a test user signs in on a non-prod pool (the flow must be enabled on the client).
- `curl -s https://cognito-idp.REGION.amazonaws.com/POOL/.well-known/jwks.json`: the public keys the verifier uses.

## Test first
Write the token validation test with a bad audience, expired token and wrong issuer first.
```python
def test_rejects_token_from_other_client(verifier, other_client_token):
    with pytest.raises(Exception):
        verifier.verify(other_client_token)   # checks iss, aud or client_id, exp, token_use
```

## Do
- Use the authorization code flow with PKCE for browsers and mobile. Public clients have no secret. Server clients keep the secret in Secrets Manager.
- Validate JWTs on the server: signature against the JWKS, `iss`, `exp`, `token_use` and `aud` (id token) or `client_id` (access token). A maintained verifier such as `aws-jwt-verify` does this.
- Send the access token to APIs and use the id token only to read profile claims.
- Register exact callback and sign-out URLs. Keep dev and prod pools separate.
- Require MFA (TOTP) for privileged groups, and use groups or custom claims for roles, checked server side.
- Set token lifetimes short for access tokens and use refresh token rotation settings that fit the app.
- Use a pre-token-generation Lambda trigger only for claims you must add, and keep it fast.
- Turn on advanced security or threat protection where available, and set `PreventUserExistenceErrors` to enabled.

## Avoid
- Trusting a decoded JWT without verifying the signature: anyone can forge claims. Verify against JWKS.
- The implicit grant or `ALLOW_USER_PASSWORD_AUTH` in production clients: use code with PKCE and disable unused `ExplicitAuthFlows`.
- Wildcard callback URLs: open redirect and token theft. List exact URLs.
- Storing tokens in `localStorage` for web apps: XSS steals them. Prefer httpOnly cookies set by a backend.
- Changing user pool attributes or the sign-in alias later: they are immutable after creation, so plan them first.
- Using the id token as an API credential: it is for the client. Use the access token.
- Identity pool roles with `*` actions: scope the authenticated role to the caller's own resources.

## Review
- [ ] Servers verify iss, aud or client_id, exp and token_use.
- [ ] Code flow with PKCE, exact redirect URIs, no client secret in front-end code.
- [ ] MFA and password policy match the risk of the app.
- [ ] Roles come from verified claims, not client input.
- [ ] Separate pools per environment, deletion protection on prod.
