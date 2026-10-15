---
name: biome
title: Biome
area: node
tags: [biome, lint, format, javascript, typescript, tooling]
detect: [dep:@biomejs/biome, file:biome.json, file:biome.jsonc]
related: [eslint, prettier, tsconfig, vitest]
---
Biome as one fast formatter and linter for JS/TS/JSON/CSS, configured in `biome.json`.

## Verify
- `npx biome ci .`: format, lint and import-order checks in CI mode (read-only, non-zero on any problem).
- `npx biome check .`: the same checks locally; add `--write` to apply safe fixes.
- `npx biome format --write .`: formats files.
- `npx biome lint --max-diagnostics=100 .`: lint only, with the diagnostic cap raised.
- `npx tsc --noEmit`: types, which Biome does not check.

## Test first
Prove a rule by running `biome lint` on a bad snippet and expecting a failure.
```sh
d=$(mktemp -d)
printf 'var a = 1;\nconsole.log(a == 1);\n' > "$d/t.js"
npx biome lint "$d/t.js"; test $? -ne 0
```
Then enable or tune the rule in `biome.json` and rerun to see it pass on fixed code.

## Do
- Create config with `npx biome init`; keep it at the repo root (`biome.json`).
- Pin the exact Biome version in `devDependencies`; formatting and rules change between releases.
- Set `$schema` in `biome.json` to the installed version's schema for editor validation.
- Use `files.includes` (current schema) or `files.ignore` (older) to exclude `dist` and generated code; match the installed version.
- Turn on `linter.rules.recommended` and add specific rules per group (`correctness`, `suspicious`, `style`).
- Use `biome migrate` after upgrading to update config, and `biome migrate eslint --write` / `biome migrate prettier --write` when switching.
- Use `overrides` for per-glob rule changes (tests, scripts).
- Run `biome ci` in CI and `biome check --write` in a pre-commit hook.

## Avoid
- Running Biome alongside Prettier on the same files with different options: they fight. Pick one formatter.
- Copying config keys from older docs: option names changed between majors. Run `biome migrate` and read its output.
- Expecting every ESLint plugin rule: type-aware and plugin rules may be missing. Keep ESLint for those.
- Using `--write` with `--unsafe` blindly: applies risky fixes. Review the diff.
- Treating Biome as a type checker: it is not. Keep `tsc --noEmit`.
- Unpinned `@biomejs/biome` with `^`: formatting diffs appear on a minor update. Pin.
- Ignoring the VCS integration: set `vcs.enabled` and `useIgnoreFile` so `.gitignore` is respected.

## Review
- [ ] One formatter owns formatting.
- [ ] CI runs `biome ci`.
- [ ] Biome version is pinned and `biome.json` matches it.
- [ ] Generated and build paths are excluded.
- [ ] Type-check is a separate step.
