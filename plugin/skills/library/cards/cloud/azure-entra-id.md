---
name: azure-entra-id
title: Azure Entra ID
area: cloud
tags: [azure, entra-id, oauth, oidc, msal, managed-identity, rbac]
detect: [dep:@azure/identity, dep:@azure/msal-node, dep:@azure/msal-browser, dep:msal, dep:azure-identity, dep:Microsoft.Identity.Web]
related: [azure-key-vault, azure-aks, azure-functions, aws-cognito]
---
Entra ID for app sign-in and workload identity: MSAL with PKCE, server-side token validation, managed identities over secrets, least-privilege roles and scopes.

## Verify
- `az ad app show --id APP_ID --query '{redirects:web.redirectUriSettings,spa:spa.redirectUris,aud:signInAudience}'`: exact redirect URIs and sign-in audience.
- `az ad app credential list --id APP_ID`: no unexpected client secrets, with expiry dates.
- `az role assignment list --assignee PRINCIPAL_ID --all --query '[].{r:roleDefinitionName,s:scope}'`: roles and scopes held by the identity.
- `az account get-access-token --resource https://vault.azure.net --query expiresOn`: the signed-in identity can obtain a token for the resource.
- `az identity list -o table`: user-assigned managed identities.

## Test first
Test token validation with the wrong audience, wrong tenant and expired tokens.
```python
@pytest.mark.parametrize("claims", [{"aud": "other"}, {"tid": "other-tenant"}, {"exp": 1}])
def test_validator_rejects_bad_claims(validator, make_token, claims):
    with pytest.raises(InvalidToken):
        validator.validate(make_token(**claims))
```

## Do
- Use managed identity and `DefaultAzureCredential` for Azure-to-Azure calls, so there are no stored secrets. Prefer federated credentials (workload identity or GitHub OIDC) for CI and clusters.
- For user sign-in use MSAL with the authorization code flow and PKCE. SPAs register as `spa` redirects.
- Validate access tokens on the API: signature from the tenant's JWKS, `iss`, `aud` (your API's application id URI), `exp` and the `scp` (delegated) or `roles` (application) claim.
- Define app roles and scopes for your API and check them per endpoint. Check `tid` for single-tenant apps.
- Request the minimum Microsoft Graph permissions and prefer delegated over application permissions. Get admin consent deliberately.
- Assign Azure RBAC at the narrowest scope (resource, not subscription), and group assignments through Entra groups.
- Protect with Conditional Access and MFA, and use Privileged Identity Management for admin roles.
- Use certificates or federated credentials over client secrets when a secret is unavoidable, with short expiry and rotation.

## Avoid
- Decoding a token without verifying it: claims are forgeable. Validate with a library.
- Accepting tokens whose `aud` is not your API or from any tenant (`common` authority) on single-tenant services: restrict issuer and tenant.
- Client secrets in repos or app settings: use managed identity or Key Vault.
- Implicit flow and ROPC (username and password): deprecated and unsafe. Use code with PKCE.
- `Owner` or `Contributor` at subscription scope for an app identity: assign a data role at resource scope.
- Wildcard or `http` redirect URIs: token interception. Register exact HTTPS URIs.
- Using the id token to call APIs: use the access token.
- ADAL for new code: use MSAL.

## Review
- [ ] Workloads use managed or federated identity.
- [ ] APIs validate issuer, audience, expiry and scope or role.
- [ ] Redirect URIs exact and HTTPS, flows are code plus PKCE.
- [ ] Role assignments narrow, Graph permissions minimal.
- [ ] Secrets, if any, expire and are rotated.
