---
name: npm-publishing
title: npm publishing
area: node
tags: [npm, publishing, package, exports, provenance, semver]
detect: [file:.npmignore, file:.changeset/config.json, file:.npmrc]
related: [pnpm, tsconfig, rollup, esbuild, turborepo]
---
Publishing packages to npm: `files`, `exports`, types, provenance, dry-run checks and versioning.

## Verify
- `npm pack --dry-run`: the exact file list that would ship; no tests, secrets or source maps you did not intend.
- `npm publish --dry-run`: the publish passes validation without uploading.
- `npx publint`: lints `exports`, `main`, `module` and `types` against the files present.
- `npx @arethetypeswrong/cli --pack .`: types resolve for ESM and CJS consumers.
- `npm view <name> version`: current published version, to confirm the bump is new.

## Test first
Install the packed tarball into a scratch project and import it as a consumer would.
```sh
npm pack
d=$(mktemp -d) && cd "$d" && npm init -y >/dev/null
npm i /path/to/pkg-1.2.3.tgz
node --input-type=module -e "import('pkg').then(m => { if (!m.parse) process.exit(1) })"
node -e "if (!require('pkg').parse) process.exit(1)"
```
Fails before `exports` and the build output are correct.

## Do
- Whitelist shipped files with `files` (`["dist"]`); README, LICENSE and `package.json` always ship.
- Define `exports` with `types` first: `{ ".": { "types": "./dist/index.d.ts", "import": "./dist/index.js", "require": "./dist/index.cjs" } }`.
- Set `"type"`, `"sideEffects": false` where true, and `engines.node`.
- Add `prepublishOnly` (or `prepack`) to build and test: `"prepublishOnly": "npm run build && npm test"`.
- Publish from CI with provenance: `npm publish --provenance --access public` using a trusted-publishing or granular token, with `id-token: write` permission.
- Use semver honestly; automate with Changesets (`changeset version`, `changeset publish`).
- Scoped packages are private by default to publish; pass `--access public` the first time.
- Tag prereleases: `npm publish --tag next`.

## Avoid
- No `files` field and no `.npmignore`: publishes everything not git-ignored, including `.env`. Whitelist with `files`.
- `exports` omitting `./package.json` or listing paths that do not exist: consumers break. Check with `publint`.
- `types` placed after `import`/`require` in `exports`: TypeScript never reaches it. Put `types` first.
- Long-lived classic automation tokens in CI: leak risk. Use trusted publishing or granular, expiring tokens.
- Republishing a version: npm forbids it, and unpublishing breaks dependents. Bump instead and `npm deprecate` the bad one.
- Committing `.npmrc` with `_authToken` literals: use `${NPM_TOKEN}` interpolation or CI-provided auth.
- Breaking changes in a minor: bump major and note it.

## Review
- [ ] `npm pack --dry-run` lists only intended files.
- [ ] `exports` verified by `publint` and a consumer install test.
- [ ] Provenance and scoped auth in CI; no secrets in `.npmrc`.
- [ ] Version bump and changelog match the change's semver impact.
- [ ] `prepublishOnly` builds fresh output.
