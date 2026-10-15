---
name: mise
title: mise
area: tools
tags: [versions, toolchain, tasks, env, dev-setup]
detect: [file:mise.toml, file:.mise.toml, file:.tool-versions]
related: [direnv, just, make, homebrew]
---
mise: pins tool versions, environment variables and tasks for a project in mise.toml (or .tool-versions), installed per directory.

## Verify
- `mise ls`: tools, versions and where each is pinned from (and whether it is installed).
- `mise install`: installs everything the config requires.
- `mise doctor`: shell activation, shims and config problems.
- `mise exec -- node --version`: the command runs with the pinned tool, even without shell activation.
- `mise tasks ls`: the tasks defined in the config, and `mise run <task>` runs one.

## Test first
Prove the pinned version wins inside the project.
```
cd project
cat mise.toml        # [tools] node = "20"
mise install
mise exec -- node --version     # 20.x
node --version                  # same, if the shell is activated
```
In a fresh clone, `mise install` must succeed with no manual steps.

## Do
- Write tools in `[tools]` in `mise.toml`, with the narrowest version that gives reproducibility (`"20"`, or exact for CI-critical tools).
- Commit `mise.toml`, and use `mise.local.toml` (ignored) for personal overrides.
- Put project variables in `[env]`, and tasks in `[tasks.name]` with `run` and `description`.
- Activate in the shell rc (`eval "$(mise activate bash)"`) for interactive use, and use `mise exec` or `mise run` in scripts.
- In CI, install mise, then run `mise install` and the tasks, so CI and laptops match.
- Run `mise trust` after reading a new config file, since configs can run commands.

## Avoid
- Trusting an unreviewed mise.toml from a cloned repo: tasks and env templates can execute code. Read it, then `mise trust`.
- Unpinned `latest`: the toolchain changes under you. Pin a major or exact version.
- Having both `.tool-versions` and `mise.toml` disagree: pick one source of truth and delete the other, or keep them identical.
- Relying on shims in non-interactive scripts: PATH is not set. Use `mise exec --` or `mise run`.
- Mixing mise with another version manager for the same tool: PATH order decides silently. Remove one from the PATH.
- Putting secrets in `[env]` in a committed file: use an ignored local file, or a secret manager.

## Review
- [ ] A fresh clone can run `mise install` and the main task with no manual steps.
- [ ] Versions are pinned and agree across config files and CI.
- [ ] No secrets in committed config.
- [ ] Tasks have descriptions and fail with nonzero exit codes.
