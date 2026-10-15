---
name: crossplane
title: Crossplane
area: infra
tags: [crossplane, kubernetes, composition, xrd, providers, iac, gitops]
detect: [file:crossplane.yaml, file:composition*.yaml, file:xrd*.yaml]
related: [kubernetes-operators, terraform, argo-cd, flux]
---
Crossplane: compose cloud resources as Kubernetes APIs with XRDs, Compositions, provider packages and ProviderConfigs.

## Verify
- `kubectl get providers,functions`: packages are `INSTALLED` and `HEALTHY`.
- `kubectl get xrd,composition`: definitions are established.
- `kubectl get managed`: every managed resource is `SYNCED` and `READY`.
- `crossplane render xr.yaml composition.yaml functions.yaml`: render the composition locally without a cluster.
- `crossplane beta trace TYPE/NAME`: the resource tree and per-resource conditions (the command may be under `beta` in your CLI).

## Test first
Render and assert before applying to a cluster.
```bash
crossplane render xr.yaml composition.yaml functions.yaml > out.yaml
# expect exactly one bucket with private ACL
test "$(yq 'select(.kind=="Bucket") | .spec.forProvider.acl' out.yaml)" = "private"
```
Use `crossplane render` outputs as golden files in CI.

## Do
- Define the API with a `CompositeResourceDefinition` (`apiextensions.crossplane.io/v2` or the version your release serves); add an OpenAPI schema with required fields and enums.
- Write compositions in pipeline mode: `mode: Pipeline` with function steps such as `function-patch-and-transform` or `function-go-templating`, and finish with `function-auto-ready`.
- Pin provider and function packages by version in `Provider` and `Function` manifests.
- Authenticate providers through `ProviderConfig` with workload identity or IRSA rather than static keys in Secrets.
- Set `deletionPolicy` (`Delete` or `Orphan`) and `managementPolicies` deliberately on stateful resources.
- Use `EnvironmentConfig` or composition inputs for per-environment values.
- Control access with RBAC: who can create claims and XRs versus managed resources.

## Avoid
- Deprecated patch-and-transform `resources:` mode in new compositions: it is replaced by pipeline functions.
- Unpinned provider versions: upgrades change schemas under live resources. Pin.
- Deleting a claim without checking `deletionPolicy`: databases and buckets go with it. Set `Orphan` or `Delete` on purpose.
- Patching secrets in plain text through connection details: write them to `writeConnectionSecretToRef` and consume with RBAC limits.
- Giant compositions per cloud product: hard to test. Compose smaller XRs.
- Debugging only the XR: the cause is in a managed resource condition. Trace down the tree.

## Review
- [ ] XRD schema validates required inputs.
- [ ] Compositions render in CI with assertions.
- [ ] Packages are pinned; credentials use workload identity.
- [ ] Deletion and management policies are explicit.
- [ ] RBAC separates platform and tenant access.
