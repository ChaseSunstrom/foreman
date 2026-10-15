---
name: turborepo
title: Turborepo
area: node
tags: [turborepo, monorepo, caching, pipeline, workspaces, build]
detect: [dep:turbo, file:turbo.json]
related: [pnpm, nx, npm-publishing, tsconfig, vitest]
---
Turborepo task graphs over workspaces: `turbo.json` tasks, cache inputs and outputs, filters, remote cache.

## Verify
- `npx turbo run build --dry=json`: the resolved task graph and cache status without running anything.
- `npx turbo run build lint test`: every task passes across the workspace.
- `npx turbo run build --filter=...[origin/main]`: only changed packages and their dependents build.
- `npx turbo run build --summarize`: writes a run summary showing hashes, inputs and cache hits.

## Test first
The check that fails first is a cache correctness test: make a change that must invalidate and prove it does.
```sh
npx turbo run build            # warm cache
echo "// x" >> packages/ui/src/index.ts
npx turbo run build --dry=json | jq -e '.tasks[] | select(.package=="ui" and .task=="build") | .cache.status == "MISS"'
```
Revert the edit afterwards. For new tasks, add the task to `turbo.json`, run `--dry=json`, and expect it in the graph.

## Do
- Define tasks in `turbo.json` under `tasks` (v2 key; older versions used `pipeline`).
- Express dependencies with `dependsOn`: `"^build"` means the dependencies' build first, `"build"` means same package.
- List `outputs` for cacheable tasks (`["dist/**", ".next/**", "!.next/cache/**"]`); a task with no outputs caches only logs.
- Narrow `inputs` when the default (all tracked files) over-invalidates; include config files that affect output.
- Declare every env var a task reads in `env` (or `globalEnv`) so the hash changes with it.
- Set `cache: false` and `persistent: true` for `dev` tasks.
- Put scripts in each package's `package.json` with the same names (`build`, `test`, `lint`).
- Use `--filter` in CI with the base ref for affected-only runs, and a remote cache for CI speed.

## Avoid
- Missing `outputs`: cache hits restore nothing and downstream tasks fail. List every artifact directory.
- Undeclared env vars: a build for staging is replayed as production from cache. Declare them, or use `passThroughEnv` only for non-output-affecting vars.
- `dependsOn: ["build"]` where `["^build"]` is meant: skips building dependencies first.
- Root `package.json` scripts that call `turbo` recursively through workspaces: loops. Call tasks once from the root.
- Using `pipeline` with `turbo` v2 or `tasks` with v1: ignored or rejected. Match the installed major.
- Caching tasks with side effects (deploys, publishes): replayed from cache without running. Set `cache: false`.
- Relying on global tools not in the hash: different versions give stale hits. Pin via `globalDependencies` or the lockfile.

## Review
- [ ] Every cacheable task lists `outputs`.
- [ ] Env vars that change output are declared.
- [ ] `dependsOn` uses `^` where upstream builds are needed.
- [ ] Deploy and dev tasks are uncached.
- [ ] CI uses `--filter` for affected work.
