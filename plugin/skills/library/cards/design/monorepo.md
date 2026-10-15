---
name: monorepo
title: Monorepo
area: design
tags: [monorepo, workspaces, build, ci, affected, dependencies]
detect: [file:pnpm-workspace.yaml, file:nx.json, file:turbo.json, file:lerna.json, file:WORKSPACE, file:MODULE.bazel, file:go.work, dep:turbo, dep:nx, dep:lerna]
related: [modular-monolith, semver, twelve-factor, configuration]
---
One repository with many packages: explicit boundaries, one lockfile, and CI that builds and tests only what changed.

## Verify
- `pnpm -r list --depth -1`: workspace packages are discovered (pnpm).
- `npx turbo run build test lint --filter='...[origin/main]'`: only affected packages and their dependents run (Turborepo).
- `npx nx affected -t build test lint --base=origin/main`: the same through Nx.
- `cargo check --workspace --all-targets`: every crate in a Cargo workspace compiles (Rust).
- `go work sync && go build ./...`: a Go workspace builds.

## Test first
Make boundaries testable: a failing check that a forbidden import is rejected.
```js
// tools/boundaries.test.js
import { execSync } from "node:child_process";
test("ui package must not import from api package", () => {
  const out = execSync("grep -rln \"@acme/api\" packages/ui/src || true").toString();
  expect(out.trim()).toBe("");
});
```
Prefer a real rule tool (an Nx `enforce-module-boundaries` lint rule, `dependency-cruiser`) once more than one rule exists.

## Do
- Declare every internal dependency in that package's manifest (`workspace:*` in pnpm) so the graph is real, not implied by relative paths.
- Keep one root lockfile and one version per third-party dependency where possible.
- Define task pipelines (`dependsOn: ["^build"]` in turbo) so builds run in graph order and cache.
- Include in cache keys every input that affects output: sources, config, env vars, lockfile.
- Run CI on affected projects, with a full run on main or on root config changes.
- Use CODEOWNERS per package path, and per-package READMEs listing public entry points.
- Export only through each package's entry point (`exports` field), keeping internals private.

## Avoid
- Relative imports across packages (`../../other/src`): they bypass the graph and caching. Import by package name.
- Undeclared dependencies that work through hoisting: they break in isolated installs. Declare them in the manifest that uses them.
- Cache keys missing env or config inputs: stale outputs get served. Declare `env` and `globalDependencies`.
- A shared `utils` package that everything depends on: any change rebuilds everything. Split by purpose.
- Running the full suite on every PR as the repo grows: use affected-only plus a nightly full run.
- Lockstep versioning of unrelated packages: release only what changed.
- Circular package dependencies: break the cycle by extracting the shared part.

## Review
- [ ] Every cross-package import goes through a declared dependency and a public entry point.
- [ ] No dependency cycles (checked by the tool or a script).
- [ ] Task pipelines list inputs and outputs so caching is correct.
- [ ] CI runs affected targets, with a full run on root changes.
- [ ] Ownership is defined for each package.
