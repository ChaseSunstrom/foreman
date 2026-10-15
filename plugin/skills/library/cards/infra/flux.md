---
name: flux
title: Flux
area: infra
tags: [flux, fluxcd, gitops, kubernetes, kustomization, helmrelease]
detect: [file:flux-system/gotk-components.yaml, file:flux-system/gotk-sync.yaml, file:clusters/*/flux-system/*.yaml, file:gotk-sync.yaml]
related: [argo-cd, kubernetes, helm, kustomize, vault]
---
Flux: GitOps controllers reconciling `GitRepository`, `Kustomization` and `HelmRelease` objects from git or OCI.

## Verify
- `flux check`: controllers are installed, healthy, and version-compatible.
- `flux build kustomization apps --path ./apps/prod`: renders what Flux would apply.
- `flux diff kustomization apps --path ./apps/prod`: drift against the live cluster.
- `flux get all -A`: ready status of every source and release.
- `flux reconcile kustomization apps --with-source`: forces a fetch and apply, then shows the result.

## Test first
Render and server-validate before pushing, then watch reconciliation.
```sh
flux build kustomization apps --path ./apps/prod --dry-run
kustomize build apps/prod | kubectl apply --dry-run=server -f -
flux reconcile kustomization apps --with-source && flux get kustomization apps --no-header | grep -q True
```
Red first: reconciliation reports False with a message until the manifest is valid.

## Do
- Bootstrap with `flux bootstrap github` (or git) so Flux manages its own manifests in `flux-system/`.
- Use `Kustomization` with `path`, `prune: true`, `sourceRef`, `interval`, and `dependsOn` for ordering (CRDs and infra before apps).
- Set `healthChecks` or `wait: true` and a `timeout` so dependents wait for readiness.
- Use `HelmRelease` with a pinned chart `version` range, `install.remediation` and `upgrade.remediation` with `retries`.
- Decrypt secrets with SOPS: `decryption: { provider: sops, secretRef: { name: sops-age } }` on the Kustomization.
- Use `postBuild.substituteFrom` for per-cluster values, and escape a literal `$` as `$${`.
- Split `clusters/<name>/` per cluster over shared `base` and `overlays` directories.
- Use `suspend: true` to pause one object during incidents, not by deleting controllers.

## Avoid
- `v1beta1` or `v2beta1` API versions on newer Flux: they were removed. Use the stable `v1` and `v2` versions your controllers serve (`flux migrate` helps).
- Plaintext `Secret` manifests in git: use SOPS or an external secrets operator.
- A `Kustomization` with no `dependsOn` for CRDs and their resources: first reconcile fails. Order them.
- Unpinned chart versions (`*`): a chart release upgrades prod. Pin a range or exact version.
- `kubectl apply` on Flux-owned objects: reverted at the next interval, or conflicting. Commit to git.
- `prune: true` on a path overlapping another Kustomization: objects get deleted by the other owner. Keep paths disjoint.
- Very short `interval` on many objects: API load. Use a few minutes and webhook `Receiver` for instant sync.
- Committing the SOPS private key or age secret: use only the public recipient in `.sops.yaml`.

## Review
- [ ] `flux check` and `flux diff` are clean and objects show Ready.
- [ ] Ordering via `dependsOn` and health checks covers CRDs and infra.
- [ ] Secrets are encrypted and keys stay out of git.
- [ ] Charts and sources are pinned, with remediation set.
