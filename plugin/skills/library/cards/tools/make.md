---
name: make
title: GNU Make
area: tools
tags: [make, makefile, build, automation, phony, targets]
detect: [file:Makefile, file:makefile, file:GNUmakefile, file:*.mk]
related: [just, shell-scripting, pre-commit]
---
GNU Make: file-based dependency builds and a task entry point, with correct prerequisites and recipes.

## Verify
- `make -n TARGET`: dry run prints the recipe without executing it.
- `make -q TARGET; echo $?`: 0 when the target is up to date, so incremental builds work.
- `make --warn-undefined-variables -n`: typos in variable names.
- `make -p -n | less`: the resolved rules and variables when expansion confuses you.

## Test first
Practice check: a second run must do nothing, and a touched input must rebuild.
```sh
make build && make -q build && echo "up to date"
touch src/main.c && ! make -q build && echo "rebuilds on change"
```
A target that always rebuilds is missing its output file name or lists a phony as a prerequisite.

## Do
- Declare task targets `.PHONY: test lint clean`.
- Name the real output as the target and list every input as prerequisites; add `-MMD -MP` for header dependencies in C.
- Put `SHELL := bash` and `.SHELLFLAGS := -eu -o pipefail -c` at the top when recipes use bash features.
- Add `.DELETE_ON_ERROR:` so a failed recipe does not leave a half-written target.
- Use `$@`, `$<`, `$^`; use `$(shell ...)` sparingly and with `:=` so it runs once.
- Use `$$` to pass a dollar sign to the shell; `$(VAR)` for make variables.
- Make a `help` target that greps `##` comments, and give `.DEFAULT_GOAL`.
- Use `make -j` only when dependencies are complete; `-O` groups output.

## Avoid
- Spaces instead of a tab before recipe lines: "missing separator". Use a tab or set `.RECIPEPREFIX`.
- Recipes with `cd dir` on one line and commands on the next: each line is a separate shell. Join with `&&` or use `.ONESHELL:`.
- Phony targets that produce files, or file targets without prerequisites: stale or endless rebuilds.
- `$(shell ...)` with `=` in a hot variable: it re-runs at every use. Use `:=`.
- Hiding errors with a leading `-` or `|| true`: failures vanish. Be explicit about which ones are allowed.
- Parallel make with undeclared dependencies: flaky builds. Declare the ordering as prerequisites.
- Relying on bash-only syntax with the default `/bin/sh`: set `SHELL`.

## Review
- [ ] Every non-file target is `.PHONY`.
- [ ] `make -n` shows the right recipe; a second `make` is a no-op.
- [ ] Inputs are fully listed so `make -j` is safe.
- [ ] `help` and the default goal are sane.
- [ ] Variables use `:=` where evaluated once.
