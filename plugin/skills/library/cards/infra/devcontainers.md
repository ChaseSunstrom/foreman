---
name: devcontainers
title: Dev containers
area: infra
tags: [devcontainer, docker, vscode, codespaces, development, features]
detect: [file:.devcontainer/devcontainer.json, file:.devcontainer.json]
related: [docker, docker-compose, dockerfile-best-practices, github-actions]
---
Dev containers: a reproducible development environment defined in devcontainer.json with features, lifecycle commands and pinned images.

## Verify
- `devcontainer build --workspace-folder .`: the image and features build (needs the devcontainer CLI).
- `devcontainer up --workspace-folder .`: the container starts and lifecycle commands run.
- `devcontainer exec --workspace-folder . make test`: the project's tests pass inside the container.
- `python -c "import json,sys; json.load(open('.devcontainer/devcontainer.json'))"`: only valid when the file has no comments; devcontainer.json allows comments, so rely on the CLI otherwise.

## Test first
Make the environment prove itself with the project's own check.
```bash
devcontainer up --workspace-folder .
devcontainer exec --workspace-folder . bash -lc 'node --version && npm ci && npm test'
```
Run it in CI so a broken definition fails the build.

## Do
- Reference a pinned `image` (tag or digest) or a `build.dockerfile`; keep it close to CI and production images.
- Add tools with `features` (for example `ghcr.io/devcontainers/features/node`) instead of long install scripts, pinning feature versions.
- Use lifecycle hooks by purpose: `onCreateCommand` for one-time setup, `postCreateCommand` for dependency install, `postStartCommand` for each start.
- Set `remoteUser` to a non-root user and `containerEnv` for non-secret variables.
- Forward ports with `forwardPorts` and set `portsAttributes` labels.
- Put editor settings and extensions in `customizations.vscode`.
- For multiple services, use `dockerComposeFile` plus `service` and `workspaceFolder`.
- Use named volumes for caches (`node_modules`, package caches) via `mounts` for speed.

## Avoid
- Unpinned `latest` images and features: environments drift between developers. Pin.
- Secrets in `devcontainer.json` or `containerEnv`: committed to the repo. Use `secrets` support in the host service or a local `.env` that is ignored.
- Running as root with the host docker socket mounted: host takeover from the container. Avoid socket mounts or use docker-outside-of-docker deliberately.
- Heavy installs in `postStartCommand`: slow every start. Move to the image build or `onCreateCommand`.
- Editing files only inside the container image: lost on rebuild. Put changes in the repo or the definition.
- Bind mounting the repo on Windows and macOS for heavy IO: slow. Use a named volume or the container-native clone.

## Review
- [ ] Definition builds and tests pass through the CLI.
- [ ] Images and features are pinned.
- [ ] Non-root user; no secrets in the file.
- [ ] Lifecycle hooks are in the right phase.
- [ ] Ports and extensions are declared.
