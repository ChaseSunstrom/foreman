---
name: azure-blob-storage
title: Azure Blob Storage
area: cloud
tags: [azure, blob-storage, storage-account, sas, lifecycle, rbac]
detect: [dep:@azure/storage-blob, dep:azure-storage-blob, dep:Azure.Storage.Blobs]
related: [azure-entra-id, azure-key-vault, aws-s3, gcp-cloud-storage]
---
Blob Storage: Entra RBAC instead of account keys, no anonymous access, user delegation SAS for sharing, soft delete, lifecycle management and TLS only.

## Verify
- `az storage account show -n ACCOUNT -g RG --query '{pub:allowBlobPublicAccess,keys:allowSharedKeyAccess,tls:minimumTlsVersion,https:enableHttpsTrafficOnly}'`: public access off, shared key off, TLS settings.
- `az storage account blob-service-properties show --account-name ACCOUNT -g RG --query '{softDelete:deleteRetentionPolicy,versioning:isVersioningEnabled}'`: soft delete and versioning.
- `az role assignment list --scope ACCOUNT_ID --query '[].{p:principalName,r:roleDefinitionName}'`: data roles like Storage Blob Data Reader per identity.
- `az storage blob list --account-name ACCOUNT -c C --auth-mode login --num-results 5`: access works with Entra login, not a key.
- `az storage account management-policy show --account-name ACCOUNT -g RG`: lifecycle rules.

## Test first
Test the SAS generator and the access boundary against the Azurite emulator.
```python
def test_sas_is_read_only_and_short_lived(make_sas):
    sas = make_sas("c", "a.pdf", minutes=10)
    q = parse_qs(sas)
    assert q["sp"] == ["r"] and q["se"][0] <= iso_in(minutes=15)
```

## Do
- Authenticate with `DefaultAzureCredential` and managed identity. Assign `Storage Blob Data Contributor` or `Reader` at container scope.
- Set `allowBlobPublicAccess=false` and `allowSharedKeyAccess=false` on accounts where all clients support Entra auth.
- Share with user delegation SAS (signed by Entra, not the account key) with read-only permission, a short expiry and an `https` protocol.
- Use stored access policies or short expiry so SAS can be revoked.
- Enable blob soft delete, container soft delete and versioning, plus point-in-time restore for block blobs where needed.
- Add lifecycle management rules to tier to cool or archive and to delete old data.
- Upload large blobs in blocks and set `Content-Type`. Use `If-None-Match: *` conditions to avoid overwrites.
- Restrict network access with private endpoints or firewall rules and require TLS 1.2 or higher.
- Use Azurite for local tests.

## Avoid
- Account keys or connection strings in code and CI: full control of the account. Use managed identity.
- Account-level SAS with write and delete and year-long expiry: effectively a permanent key. Use user delegation SAS with minutes.
- Containers set to blob or container anonymous access: public data. Keep private and serve with SAS or a CDN with private origin.
- Assuming a hierarchical namespace for plain blob accounts: "folders" are name prefixes, and renames copy. Enable ADLS Gen2 when you need real directories.
- Skipping soft delete: a mistaken delete is permanent. Turn it on.
- Hot tier for everything: cost. Use lifecycle rules.
- Reading whole blobs to check existence: use `get_blob_properties`.

## Review
- [ ] Shared key and anonymous access disabled, or the exception is documented.
- [ ] SAS are user delegation, read-minimal and short.
- [ ] Soft delete, versioning and lifecycle configured.
- [ ] Network access restricted and TLS enforced.
- [ ] Code uses managed identity credentials.
