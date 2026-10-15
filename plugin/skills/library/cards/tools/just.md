---
name: just
title: just
area: tools
tags: [just, justfile, task-runner, recipes, automation, make]
detect: [file:justfile, file:Justfile, file:.justfile]
related: [make, shell-scripting, pre-commit]
---
`just`: a command runner with a `justfile` of recipes, arguments and settings, without make's dependency model.

## Verify
- `just --list`: the recipes and their doc comments.
- `just --fmt --check --unstable`: the justfile is formatted (the formatter is flagged unstable in some versions).
- `just --dry-run RECIPE`: prints the commands without running them.
- `just --evaluate`: resolved variable values.

## Test first
Practice check: a recipe fails loudly on bad input and succeeds on good input.
```just
test:
    pytest -q

check-env:
    @test -n "$API_URL" || { echo "API_URL unset" >&2; exit 1; }
```
```sh
env -u API_URL just check-env; echo $?   # expect 1
```

## Do
- Put the default recipe first or name one `default`; make it `@just --list`.
- Add a `# comment` line above a recipe for its `--list` description.
- Use parameters with defaults: `build target="debug":`; variadic `+args` and `*args`.
- Load env with `set dotenv-load`; use `set shell := ["bash", "-euo", "pipefail", "-c"]` for strict recipes.
- Prefix a recipe line with `@` to hide echo; list dependencies after the colon: `deploy: test build`.
- Use backticks for command output: `sha := `git rev-parse --short HEAD``.
- Use `[private]` or an underscore prefix for helper recipes.
- Use a shebang recipe (`#!/usr/bin/env bash`) for multi-line logic; the whole body runs in one process.

## Avoid
- Assuming recipe lines share state: each line runs in a new shell, so `cd` and variables do not persist. Use a shebang recipe or `&&`.
- Writing make-style `$@` or `$(VAR)`: just uses `{{var}}`. Shell variables need `$VAR` or `$$` in some contexts; check with `--dry-run`.
- Expecting file-timestamp rebuilds: just always runs recipes. Use make when you need incremental builds.
- Spaces and tabs mixed in a recipe: indentation must be consistent.
- Depending on tools installed only on your machine without a check recipe: fail with a clear message.
- Quoting arguments carelessly: `{{arg}}` is substituted textually. Quote it: `rm -- "{{arg}}"`.

## Review
- [ ] `just --list` is clean, with descriptions and no stray private helpers.
- [ ] Multi-line logic uses shebang recipes or a script file.
- [ ] Interpolated arguments are quoted.
- [ ] CI calls the same recipes developers run locally.
