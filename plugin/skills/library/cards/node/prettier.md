---
name: prettier
title: Prettier
area: node
tags: [prettier, formatter, code-style, javascript, typescript, ci]
detect: [dep:prettier, file:.prettierrc*, file:prettier.config.*, file:.prettierignore]
related: [eslint, biome, tsconfig]
---
Prettier as the single formatter: config file, ignore file, CI check, and editor and ESLint boundaries.

## Verify
- `npx prettier --check .`: no file differs from its formatted form (CI step).
- `npx prettier --write .`: formats the tree.
- `npx prettier --check . --log-level warn`: quieter output for CI logs.
- `npx prettier --find-config-path src/index.ts`: which config file applies to a path.
- `npx prettier --file-info src/index.ts`: whether the file is ignored and which parser is inferred.

## Test first
The failing check is `--check` on a deliberately misformatted file.
```sh
d=$(mktemp -d)
printf 'const a   = {b:1,\n c:2}\n' > "$d/t.js"
npx prettier --check "$d/t.js"; test $? -ne 0
npx prettier --write "$d/t.js" && npx prettier --check "$d/t.js"
```
For a config change, run `--check .` and expect a diff list before writing.

## Do
- Keep options in one config file (`.prettierrc`, `prettier.config.js`); set few options (`singleQuote`, `printWidth`, `trailingComma`).
- Exclude generated files in `.prettierignore` (lockfiles, `dist`, `coverage`, build output).
- Pin the exact Prettier version in `devDependencies`; formatting output changes between releases.
- Run `prettier --check` in CI and `prettier --write` through lint-staged or an editor on save.
- Use `overrides` for per-glob options (for example Markdown `proseWrap`).
- Add `.editorconfig`; Prettier reads indent and line-ending settings from it.
- Commit a bulk reformat in its own commit and list it in `.git-blame-ignore-revs`.
- Add `eslint-config-prettier` last in the ESLint config to switch off conflicting rules.

## Avoid
- `eslint-plugin-prettier` for new setups: runs Prettier inside ESLint, slow and noisy. Run both tools separately.
- Two formatters (Prettier plus Biome, or editor "format" extensions with other settings) over the same files: they undo each other. Choose one.
- A caret range on Prettier: a minor release reformats files and fails CI. Pin.
- Formatting lockfiles, minified or generated code: huge diffs. Ignore them.
- Long config of many options: defeats the point. Keep defaults.
- Different line endings across OSes: set `endOfLine: "lf"` and `.gitattributes`.
- Running `--write` in CI and not committing: the check passes with local-only changes. Use `--check` in CI.

## Review
- [ ] One config, one ignore file, one formatter.
- [ ] Version pinned; CI runs `--check`.
- [ ] Generated files are ignored.
- [ ] ESLint formatting rules are disabled via `eslint-config-prettier`.
- [ ] Bulk reformat commits are isolated.
