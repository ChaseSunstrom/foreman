---
name: changesets
title: Changesets
area: node
tags: [changesets, versioning, release, monorepo, changelog, publishing]
detect: [dep:@changesets/cli, file:.changeset/config.json]
related: [npm-publishing, pnpm, turborepo, nx]
---
Changesets: one markdown file per change, versions and changelogs generated from them, release via CI.

## Verify
- `npx changeset status --since=origin/main`: fails when changed packages lack a changeset.
- `npx changeset version`: bumps versions and writes changelogs (inspect the diff; do not commit locally unless releasing).
- `npm publish --dry-run`: run inside a package to see exactly which files would ship.
- `cat .changeset/config.json`: `access`, `baseBranch`, `ignore` and `updateInternalDependencies` are intended.

## Test first
The check that must fail first is the status gate: make the change, then confirm the bot would block it.
```
$ git checkout -b feat/x
$ (edit packages/core/src/index.ts)
$ npx changeset status --since=main; echo $?
# non-zero: packages/core changed with no changeset
$ npx changeset add --empty   # for non-release changes
```
Add the changeset describing the user-visible change; the gate must then exit 0.

## Do
- Run `npx changeset` per PR: choose packages, bump type (patch, minor, major) and write a user-facing summary.
- Follow semver for bump type: breaking is major, features minor, fixes patch.
- Configure `.changeset/config.json`: `"access": "public"` for public scoped packages, `"baseBranch": "main"`, `"commit": false`.
- Automate with the changesets GitHub action: it opens a "Version Packages" PR, merging it publishes.
- Publish with `changeset publish` (it runs `npm publish` per package and tags); build before it in the same job.
- Use `linked` or `fixed` groups when packages must version together; `ignore` for private packages.
- Use `npx changeset pre enter next` and `pre exit` for prereleases.

## Avoid
- Editing versions or `CHANGELOG.md` by hand: the tool recomputes them. Add a changeset instead.
- Publishing without building: stale or empty `dist`. Run build in the release script.
- Forgetting `NPM_TOKEN` or provenance setup in CI: publish fails late. Check the workflow secrets.
- Marking private apps for release: set `"private": true` so they are skipped.
- Writing changeset summaries like "fix bug": they become the changelog. Describe the effect for users.
- Skipping `updateInternalDependencies`: dependents keep stale ranges.

## Review
- [ ] Every user-facing PR carries a changeset with the right bump and a clear summary.
- [ ] Config matches publish access and branch strategy.
- [ ] Release pipeline builds, versions via PR, then publishes.
- [ ] Private packages are excluded.
- [ ] Pre-release mode is exited before a stable release.
