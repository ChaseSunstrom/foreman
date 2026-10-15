---
name: nx
title: Nx
area: node
tags: [nx, monorepo, workspace, caching, affected, generators]
detect: [dep:nx, dep:@nx/workspace, file:nx.json]
related: [turborepo, pnpm, tsconfig, jest, vitest]
---
Nx workspaces: project graph, `nx.json` target defaults, affected commands, generators, module boundaries.

## Verify
- `npx nx graph --file=graph.json`: the project graph builds without cycles or errors.
- `npx nx affected -t lint test build`: changed projects and dependents pass (needs a git base).
- `npx nx run-many -t build`: builds every project that has a build target.
- `npx nx show project <name>`: resolved targets, inputs and outputs for one project.
- `npx nx reset`: clears the cache and daemon when results look stale.

## Test first
The failing check is a module-boundary lint rule, since boundaries guard the graph.
```json
{
  "rules": {
    "@nx/enforce-module-boundaries": ["error", {
      "depConstraints": [
        { "sourceTag": "type:ui", "onlyDependOnLibsWithTags": ["type:ui", "type:util"] }
      ]
    }]
  }
}
```
Add an import from a `type:ui` lib to a feature lib, run `npx nx lint <ui-lib>`, and expect the violation before wiring tags.

## Do
- Tag projects in `project.json` (`"tags": ["type:ui", "scope:shop"]`) and enforce with `@nx/enforce-module-boundaries`.
- Set `targetDefaults` in `nx.json`: `dependsOn: ["^build"]`, `cache: true`, and `inputs`/`outputs`.
- Use named inputs (`production`, `default`) so test files do not invalidate builds.
- Use generators (`nx g`) and keep custom ones in a local plugin.
- Run `nx affected` in CI with `NX_BASE` and `NX_HEAD` set (or `nx-set-shas`).
- Run `nx migrate latest` then `nx migrate --run-migrations` to upgrade, and commit `migrations.json` changes.
- Declare `implicitDependencies` only where the graph cannot infer them.
- Enable Nx Cloud or a remote cache for CI.

## Avoid
- Deep imports across libs (`@org/ui/src/lib/x`): bypass the public API. Import the lib's index barrel alias.
- Circular dependencies between libs: break the graph and affected logic. Extract shared code.
- Missing `outputs` on cached targets: restored cache contains nothing. Declare them.
- Shallow clones in CI: `affected` cannot find a base and runs everything. Fetch full history or use `nx-set-shas`.
- Hand-editing `tsconfig.base.json` paths and leaving them stale: use generators to keep aliases correct.
- Mixing package-manager lockfiles: the graph reads one. Keep a single lockfile.
- Upgrading `nx` and plugin packages to different versions: mismatched executors. Move them together with `nx migrate`.

## Review
- [ ] Module boundary lint is on with tags.
- [ ] `targetDefaults` define caching, `dependsOn` and outputs.
- [ ] CI computes affected from a real base commit.
- [ ] Imports go through each lib's public entry.
- [ ] All `@nx/*` packages share a version.
