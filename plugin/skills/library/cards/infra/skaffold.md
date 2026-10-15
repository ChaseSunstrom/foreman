---
name: skaffold
title: Skaffold
area: infra
tags: [skaffold, kubernetes, ci, build, deploy, profiles, development]
detect: [file:skaffold.yaml]
related: [tilt, kubernetes, helm, kustomize, docker]
---
Skaffold: skaffold.yaml declares build, test and deploy pipelines with profiles for dev, CI and release.

## Verify
- `skaffold diagnose`: effective config and build details, including profile and file resolution.
- `skaffold fix`: reports and applies schema migrations when the config uses an old `apiVersion`.
- `skaffold build --dry-run`: what would be built, without building.
- `skaffold render`: the final manifests that would be deployed.
- `skaffold run --tail`: one-shot build and deploy with logs.

## Test first
Render and assert the manifests, then run the declared tests.
```bash
skaffold render -p ci > out.yaml
test "$(yq 'select(.kind=="Deployment") | .spec.template.spec.containers[0].image' out.yaml | grep -c ':latest')" = 0
skaffold test            # runs the configured structure and custom tests
```

## Do
- Keep `apiVersion` current for your installed Skaffold and run `skaffold fix` after upgrades.
- Define `build.artifacts` with `image`, `context` and a builder (`docker`, `jib`, `buildpacks`, `ko`); turn on `tagPolicy` such as `gitCommit` for traceable tags.
- Use `manifests.rawYaml`, `kustomize` or `helm` renderers, and the `deploy` section with `kubectl` or `helm`.
- Add `profiles` with `activation` for `kubeContext` or `env`, patching build or deploy per environment.
- Add `test` entries: `structureTests` with container-structure-test files and `custom` commands.
- Use `portForward` for dev and `skaffold dev` for the watch loop; `skaffold run` or `skaffold render` for CI.
- Use `build.local.useBuildkit` and a remote `cluster` or Cloud Build builder for CI speed.
- Set `deploy.kubeContext` or `activation.kubeContext` so contexts are explicit.

## Avoid
- Old `apiVersion: skaffold/v1alpha*` configs: unsupported. Run `skaffold fix`.
- `latest` tags in manifests with `tagPolicy` expecting replacement: Skaffold only rewrites images it builds. List each as an artifact.
- Running `skaffold dev` or `run` against whatever context is active: wrong cluster. Use `kubeContext` and activations.
- Secrets in `skaffold.yaml` env or build args: committed. Use secret mounts and CI-provided variables.
- Skipping `skaffold render` in review: reviewers cannot see the actual manifests. Output them in CI.
- Using it as the production deploy engine without pinned image digests: drift. Render with `--digest-source=remote` or record digests.

## Review
- [ ] `skaffold diagnose` passes and `apiVersion` is current.
- [ ] Every deployed image is a declared artifact.
- [ ] Profiles are explicit about context and environment.
- [ ] Rendered manifests are asserted in CI.
- [ ] No secrets in config.
