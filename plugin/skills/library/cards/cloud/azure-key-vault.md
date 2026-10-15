---
name: azure-key-vault
title: Azure Key Vault
area: cloud
tags: [azure, key-vault, secrets, keys, rbac, managed-identity]
detect: [dep:@azure/keyvault-secrets, dep:@azure/keyvault-keys, dep:azure-keyvault-secrets, dep:azure-keyvault-keys, dep:Azure.Security.KeyVault.Secrets]
related: [azure-entra-id, azure-aks, azure-functions, aws-secrets-manager]
---
Key Vault for secrets, keys and certificates: RBAC authorization, managed identity access, soft delete and purge protection, cached reads, and network limits.

## Verify
- `az keyvault show -n V --query '{rbac:properties.enableRbacAuthorization,soft:properties.enableSoftDelete,purge:properties.enablePurgeProtection,net:properties.networkAcls.defaultAction}'`: RBAC mode, soft delete, purge protection and firewall default.
- `az role assignment list --scope VAULT_ID --query '[].{p:principalName,r:roleDefinitionName}'`: who holds Key Vault Secrets User or Officer.
- `az keyvault secret list --vault-name V --query '[].{n:name,exp:attributes.expires}'`: secrets and their expiry.
- `az keyvault secret show --vault-name V -n NAME --query 'attributes'`: enabled state and dates, without printing the value.

## Test first
Test the loader's cache, failure and missing-secret handling with a fake client.
```python
def test_secret_cached_and_missing_fails_closed(fake_client):
    s = SecretSource(fake_client, ttl=60)
    assert s.get("db") == s.get("db") and fake_client.calls == 1
    with pytest.raises(SecretUnavailable):
        s.get("nope")
```

## Do
- Use Azure RBAC authorization (not access policies) and give workloads `Key Vault Secrets User` at the vault or secret scope. Reserve Officer roles for automation.
- Authenticate with `DefaultAzureCredential` using a managed identity. No client secrets in config.
- Enable soft delete and purge protection on production vaults.
- Set expiry dates and use rotation policies or Event Grid near-expiry events for rotation.
- Use App Service and Functions Key Vault references, or the CSI secrets store driver on AKS, to inject values without code.
- Cache secret values in memory for minutes and refetch on authentication failure, since vault request limits are per vault.
- Use a vault per environment and per trust boundary, and Managed HSM only when compliance demands it.
- Restrict network with a private endpoint or firewall rules, and send diagnostic logs to Log Analytics.
- Perform cryptography with key operations (`wrapKey`, `sign`) so private keys never leave the vault.

## Avoid
- Legacy access policies granting get, list and delete to everyone: broad and unreviewable. Use RBAC with narrow roles.
- Reading the secret on every request: throttling (429) and latency. Cache.
- `list` permission for apps that only need `get`: Secrets User allows reads only. Do not hand out Officer.
- Secrets in app settings plain text, pipelines or repos: put them in the vault.
- Purge protection off with soft delete retention at the minimum: deleted secrets can be purged by mistake. Turn protection on.
- Logging secret values or showing them in CI output: mask and avoid `--query value` in logs.
- A single shared vault for all teams: blast radius. Split by boundary.

## Review
- [ ] RBAC mode with narrow roles and managed identities.
- [ ] Soft delete and purge protection enabled.
- [ ] Secrets carry expiry and a rotation path.
- [ ] Reads are cached and the vault network is restricted.
- [ ] No secret values appear in code, logs or pipeline output.
