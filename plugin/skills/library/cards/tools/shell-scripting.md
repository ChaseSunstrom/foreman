---
name: shell-scripting
title: Shell scripting
area: tools
tags: [bash, sh, shell, shellcheck, scripts, posix]
detect: [ext:.sh, ext:.bash, file:.shellcheckrc, file:*.bats]
related: [make, just, jq, sed-awk, ripgrep]
---
Robust bash and POSIX sh: quoting, strict mode, traps and linted scripts.

## Verify
- `shellcheck script.sh`: quoting, portability and common bugs.
- `shfmt -d script.sh`: formatting diff (if shfmt is used by the repo).
- `bash -n script.sh`: syntax parses without running.
- `bats test/`: if Bats tests exist, the behavior suite.

## Test first
Run the script in a temp dir with bad input and check the exit status.
```bash
# test/cleanup.bats
@test "refuses empty target" {
  run ./cleanup.sh ""
  [ "$status" -ne 0 ]
  [[ "$output" == *"usage"* ]]
}
```
Without Bats, a plain `./script.sh bad; test $? -ne 0` in CI.

## Do
- Start with `#!/usr/bin/env bash` and `set -euo pipefail`; add `IFS=$'\n\t'` if splitting matters.
- Quote every expansion: `"$var"`, `"${arr[@]}"`, `"$(cmd)"`.
- Use `[[ ... ]]` in bash, `[ ... ]` in POSIX sh; use `printf` over `echo` for arbitrary data.
- Create temp files with `mktemp` and clean up with `trap 'rm -rf "$tmp"' EXIT`.
- Validate arguments early and print usage to stderr with a non-zero exit.
- Use `local` in functions; use `readonly` for constants.
- Use `--` to end options before user-supplied paths: `rm -- "$f"`.
- Iterate files with globs or `find -print0 | while IFS= read -r -d '' f`, not `ls`.

## Avoid
- Unquoted variables: word splitting and globbing break on spaces. Quote them.
- `for f in $(ls)` or parsing `ls`: use a glob. Quote results.
- `cd dir; rm -rf *` without checking: if `cd` fails, it deletes the wrong place. Use `cd dir || exit 1` or `set -e`.
- Assuming `set -e` catches everything: it is ignored in `if`, `&&` and `||` contexts, and `pipefail` is needed for pipes. Check returns explicitly where it matters.
- `eval` or building commands as strings from input: injection. Use arrays.
- `echo -e` or bashisms under `#!/bin/sh`: not portable. Use `printf`, or declare bash.
- `[ $x = y ]` with empty `$x`: syntax error. Quote it.
- `curl | sh` installers without verification.

## Review
- [ ] shellcheck is clean without blanket disables.
- [ ] All expansions quoted, temp files trapped, args validated.
- [ ] Failure paths exit non-zero with a message on stderr.
- [ ] The shebang matches the syntax used.
