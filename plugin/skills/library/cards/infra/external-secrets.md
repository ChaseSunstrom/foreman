---
name: external-secrets
title: External Secrets Operator
area: infra
tags: [kubernetes, secrets, external-secrets, eso, vault, aws, gitops]
detect: [file:externalsecret*.yaml, file:secretstore*.yaml]
related: [sealed-secrets, sops, vault, kubernetes-rbac, flux, argo-cd]
---
External Secrets Operator: sync secrets from a cloud store into Kubernetes Secrets through SecretStore and ExternalSecret resources.

## Verify
- `kubectl get externalsecret -A`: STATUS `SecretSynced` and READY True.
- `kubectl describe externalsecret NAME -n NS`: the sync error text when not ready.
- `kubectl get secretstore,clustersecretstore -A`: store is Valid and Ready.
- `kubectl get secret NAME -n NS -o jsonpath='{.data}' | jq 'keys'`: the expected keys exist (never print values).

## Test first
Assert the contract in a render test and a live check.
```python
def test_externalsecret_has_refresh_and_store(manifests):
    es = manifests.one("ExternalSecret", "db")
    assert es["spec"]["refreshInterval"]
    assert es["spec"]["secretStoreRef"]["name"]
    assert es["spec"]["target"]["name"] == "db-credentials"
```
In a cluster, apply the ExternalSecret and wait with `kubectl wait --for=condition=Ready externalsecret/db`.

## Do
- Use `apiVersion: external-secrets.io/v1` or the version your installed CRDs serve; confirm with `kubectl api-resources`.
- Set `refreshInterval`, `secretStoreRef` (name and kind), `target.name` and `data[].remoteRef.key` or `dataFrom`.
- Authenticate stores with workload identity (IRSA, Workload Identity, Vault Kubernetes auth) over static keys.
- Use `ClusterSecretStore` for shared stores and restrict who can reference it with namespace conditions.
- Set `target.creationPolicy` and `deletionPolicy` deliberately.
- Use `target.template` to shape keys (for example a connection string) instead of post-processing in app code.
- Restart consumers on rotation with a reloader, since mounted env vars do not update.

## Avoid
- Committing the store credentials Secret in plain YAML: bootstrap it out of band or with SOPS or sealed secrets.
- A ClusterSecretStore any namespace can use: a tenant reads other tenants' secrets. Add `conditions` namespace limits.
- `refreshInterval: 0` expecting continuous sync: it disables refresh. Choose a real interval.
- Granting the operator `*` on the cloud secret store: scope the IAM policy to a path prefix.
- Reading secret values in test or CI logs: assert on key names only.
- Relying on env-var consumption for rotation: pods keep the old value until restart.

## Review
- [ ] Stores authenticate without long-lived static keys where the platform allows.
- [ ] Store scope and IAM policy are least-privilege.
- [ ] Refresh and deletion policies are explicit.
- [ ] Consumers pick up rotated values.
- [ ] No secret values appear in repo, logs or events.
