---
name: kustomize
title: Kustomize
area: infra
tags: [kustomize, kubernetes, overlays, patches, manifests, gitops]
detect: [file:kustomization.yaml, file:kustomization.yml, file:Kustomization]
related: [kubernetes, helm, argo-cd, flux]
---
Kustomize: a base of plain manifests plus per-environment overlays using patches, generators and image transforms.

## Verify
- `kustomize build overlays/prod`: the overlay renders (or `kubectl kustomize overlays/prod`).
- `kubectl kustomize overlays/prod | kubectl apply --dry-run=server -f -`: rendered output is admitted by the API server.
- `kubectl diff -k overlays/prod`: the change against the live cluster.
- `diff <(kustomize build overlays/dev) <(kustomize build overlays/prod)`: overlays differ only where intended.

## Test first
Render and assert on the output before changing an overlay. Keep each overlay buildable in CI.
```sh
out=$(kustomize build overlays/prod)
echo "$out" | grep -q 'replicas: 3'                 # red until the patch exists
echo "$out" | grep -q 'image: ghcr.io/org/app:1.4.2'
echo "$out" | kubectl apply --dry-run=server -f -
```

## Do
- Keep `base/` environment-neutral and make overlays reference it under `resources: [../../base]`.
- Use `patches:` with a `target` selector (strategic merge or JSON 6902), not the deprecated `patchesStrategicMerge` and `patchesJson6902` fields.
- Set images with `images:` (`name`, `newName`, `newTag` or `digest`) instead of patching `containers`.
- Use `configMapGenerator` and `secretGenerator`: the content hash suffix rolls pods on change. Reference by the original name.
- Set `namespace:`, `namePrefix` and `labels:` (with `includeSelectors: false` unless intended) at the overlay level.
- Use `components:` for reusable optional features shared across overlays.
- Use `replacements:` to copy a value between fields, not the deprecated `vars`.

## Avoid
- `commonLabels`: it rewrites immutable selectors, so an existing Deployment cannot be applied. Use `labels:` with `includeSelectors: false`.
- `bases:`: deprecated. List the directory under `resources:`.
- Patches that match by array index: they break on reorder. Use strategic merge by `name` key.
- `generatorOptions: disableNameSuffixHash: true` on config consumed by pods: changes no longer roll them.
- Putting secrets in `secretGenerator` literals committed to git: use sealed or external secrets.
- Deep chains of overlays referencing overlays: hard to reason about. Keep one base plus one layer, and use components.
- Running `kustomize edit` in CI and forgetting to commit it: the cluster and git drift.

## Review
- [ ] Every overlay builds and passes server-side dry-run.
- [ ] No deprecated fields (`bases`, `patchesStrategicMerge`, `vars`, `commonLabels`).
- [ ] Image tags or digests are set in one place per overlay.
- [ ] Selectors stay unchanged across the diff.
