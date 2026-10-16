---
name: eslint
title: ESLint
area: node
tags: [eslint, lint, flat-config, typescript, javascript, static-analysis]
detect: [dep:eslint, dep:@eslint/js, file:eslint.config.js, file:eslint.config.mjs, file:eslint.config.ts, file:.eslintrc*]
related: [prettier, biome, tsconfig, vitest, jest]
---
ESLint with flat config (`eslint.config.*`), typescript-eslint, and a lint step that fails CI.

## Verify
- `npx eslint .`: the whole tree passes with the repo config.
- `npx eslint . --max-warnings 0`: warnings fail too, so they cannot pile up.
- `npx eslint --print-config src/index.ts`: the effective rules and parser for one file (proves overrides apply).
- `npx eslint --inspect-config`: opens the config inspector, to see which config block sets a rule.

## Test first
Prove a rule by linting a bad snippet and expecting the error, using `--stdin`.
```sh
echo 'const x = await fetch("/a"); async function f(){ g() } async function g(){}' \
  | npx eslint --stdin --stdin-filename src/t.ts --rule '{"@typescript-eslint/no-floating-promises":"error"}' \
  ; test $? -ne 0
```
For a custom rule, use `RuleTester` from `eslint` with `valid` and `invalid` cases before writing the rule.

## Do
- Use flat config: export an array from `eslint.config.js` (use `defineConfig` or `tseslint.config(...)` helpers).
- Start from `js.configs.recommended` and `tseslint.configs.recommended` (or `recommendedTypeChecked` plus `parserOptions.projectService: true`).
- Scope blocks with `files: ['**/*.ts']`; set `languageOptions.globals` per environment.
- Put ignores in a standalone `{ ignores: ['dist/**', 'coverage/**'] }` object.
- Turn on `@typescript-eslint/no-floating-promises` and `no-misused-promises` for async server code (needs type info).
- Keep formatting out of ESLint; let Prettier or Biome format and use `eslint-config-prettier` if both run.
- Run `eslint --fix` locally, plain `eslint` in CI.
- Justify `eslint-disable` lines with a reason comment, and scope them to one rule.

## Avoid
- `.eslintrc.*` and `.eslintignore` in ESLint 9+: not read by default. Migrate to flat config (`npx @eslint/migrate-config .eslintrc.json`).
- `extends: [...]` strings in flat config: flat config uses imported config objects.
- `--ext` flag in flat config: removed. Match files with `files` globs.
- Global `ignores` inside a block that also has other keys: it then acts only as a per-block ignore. Use a standalone ignores object.
- Type-aware rules without `parserOptions.project` / `projectService`: they error or silently do nothing.
- Blanket `/* eslint-disable */` at the top of a file: hides new issues. Disable the specific rule on the specific line.
- Running ESLint on generated and build output: slow and noisy. Ignore it.

## Review
- [ ] Config is flat and ignores `dist`, `coverage` and generated files.
- [ ] CI runs `eslint . --max-warnings 0`.
- [ ] Type-aware async rules are enabled for server code.
- [ ] No formatting rules conflict with the formatter.
- [ ] Disable comments name one rule and a reason.
