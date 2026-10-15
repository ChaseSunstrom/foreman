---
name: tilt
title: Tilt
area: infra
tags: [tilt, kubernetes, development, live-update, tiltfile, inner-loop]
detect: [file:Tiltfile]
related: [skaffold, kubernetes, helm, kustomize, docker]
---
Tilt: a Starlark Tiltfile that builds images, deploys to a dev cluster and live-updates containers for a fast inner loop.

## Verify
- `tilt ci`: runs the Tiltfile to completion in CI mode and exits non-zero if resources fail.
- `tilt alpha tiltfile-result`: evaluates the Tiltfile and prints the result, to catch Starlark errors (the subcommand lives under `alpha` in some releases).
- `tilt get uiresource`: resource status from a running Tilt.
- `kubectl config current-context`: you are pointed at the intended local cluster.

## Test first
Make the loop itself the test: a clean cluster must come up through the Tiltfile.
```bash
tilt ci --timeout 10m
kubectl wait --for=condition=Available deploy/api --timeout=120s
curl -fs localhost:8080/healthz
```
Add a `local_resource` for tests that depends on the service so a regression shows in the UI.

## Do
- Declare images with `docker_build('app', '.', live_update=[sync('./src', '/app/src'), run('pip install -r req.txt', trigger='req.txt')])`.
- Load manifests with `k8s_yaml`, `kustomize('.')` or `helm('chart', values=[...])`.
- Name resources and group with `k8s_resource('api', port_forwards=8080, labels=['backend'], resource_deps=['db'])`.
- Use `local_resource` for codegen, tests and linters with `deps` and `auto_init=False` for on-demand ones.
- Restrict contexts with `allow_k8s_contexts('kind-dev')` so Tilt never deploys to a real cluster by accident.
- Use `ignore` in `docker_build` or a `.dockerignore` so edits to docs do not trigger rebuilds.
- Read config with `config.parse()` and `tilt up -- --flag` for per-developer options.
- Break a large Tiltfile into `load('ext://...')` extensions and `include()`d files.

## Avoid
- Running Tilt against a shared or production context: it applies manifests. Set `allow_k8s_contexts` to the dev cluster only.
- `live_update` syncing into paths the image process does not watch: edits appear to do nothing. Sync where the app reloads from, or add a `restart_container()` step.
- Shelling out in the Tiltfile with `local()` for values that change: they only run on Tiltfile reload. Use `local_resource`.
- Secrets in Tiltfile literals: committed. Read from the environment or `read_file` of an ignored path.
- Rebuilding every image on each save through a broad `deps`: narrow paths and use `ignore`.
- Treating Tilt as a deploy tool: it is for development. Deploy with your CD system.

## Review
- [ ] Context is locked with `allow_k8s_contexts`.
- [ ] Live update paths match the running app's layout.
- [ ] `tilt ci` passes from a clean cluster.
- [ ] Resource dependencies and port forwards are declared.
- [ ] No secrets in the Tiltfile.
