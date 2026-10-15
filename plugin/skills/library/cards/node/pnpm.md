---
name: pnpm
title: pnpm
area: node
tags: [pnpm, package-manager, workspaces, lockfile, monorepo, node]
detect: [file:pnpm-lock.yaml, file:pnpm-workspace.yaml, file:.npmrc]
related: [turborepo, nx, npm-publishing, node]
---
pnpm installs: strict `node_modules`, `pnpm-workspace.yaml`, the `workspace:` protocol, catalogs, frozen lockfile in CI.

## Verify
- `pnpm install --frozen-lockfile`: the lockfile matches every `package.json`; fails otherwise.
- `pnpm -r build`: every workspace package builds in dependency order.
- `pnpm -r --filter "...[origin/main]" test`: tests only for changed packages and dependents.
- `pnpm why <pkg>`: which dependents pull a package in, and which versions.
- `pnpm audit --prod`: advisories in production dependencies.

## Test first
The failing check for a dependency change is the frozen install itself: edit `package.json`, run `pnpm install --frozen-lockfile`, and expect it to fail until you run `pnpm install` and commit the lockfile.
```sh
pnpm add -D vitest --filter @acme/api
git diff --stat pnpm-lock.yaml packages/api/package.json
pnpm install --frozen-lockfile
```
For phantom-dependency bugs, the check is `pnpm -r build` after removing the undeclared import's source: it fails under pnpm's strict layout.

## Do
- Declare workspaces in `pnpm-workspace.yaml` (`packages: ['apps/*', 'packages/*']`).
- Reference sibling packages with `"@acme/ui": "workspace:*"`; pnpm rewrites it on publish.
- Share versions via `catalog:` entries in `pnpm-workspace.yaml` (current pnpm versions).
- Pin the manager with `"packageManager": "pnpm@x.y.z"` and enable it through Corepack.
- Install in CI with `--frozen-lockfile`; cache the pnpm store, not `node_modules`.
- Add every import to the package that uses it; use `pnpm add <pkg> --filter <name>`.
- Use `pnpm.overrides` (or the workspace yaml `overrides`) to force a patched transitive version, and comment why.
- Use `pnpm dlx` for one-off tools, not a global install.

## Avoid
- Relying on hoisted packages that are not in your `package.json`: works under npm, fails in pnpm's strict tree. Declare the dependency.
- `shamefully-hoist=true` or `node-linker=hoisted` as a first fix: hides missing declarations. Fix the manifest unless a tool truly needs it.
- Committing both `pnpm-lock.yaml` and `package-lock.json`: installs diverge. Keep one lockfile.
- `pnpm install` (not frozen) in CI: silently rewrites the lockfile. Use `--frozen-lockfile`.
- `workspace:*` in packages you publish with `npm publish`: leaks the protocol. Publish with `pnpm publish` which rewrites it.
- Running `npm` or `yarn` commands in a pnpm repo: creates stray lockfiles.
- Ignoring `onlyBuiltDependencies`/build-script prompts: native modules fail to build. Allow vetted packages explicitly.

## Review
- [ ] One lockfile, installed frozen in CI.
- [ ] `packageManager` field is set.
- [ ] Internal deps use `workspace:`; each import is declared where used.
- [ ] Overrides are commented and temporary.
- [ ] Only vetted packages may run build scripts.
