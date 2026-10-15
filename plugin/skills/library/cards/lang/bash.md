---
name: bash
title: Bash and shell scripts
area: lang
tags: [bash, shell, shellcheck, shfmt, bats, scripting]
detect: [ext:.sh, ext:.bash, ext:.bats, file:.shellcheckrc]
related: [powershell]
---
Bash scripts: ShellCheck-clean, shfmt-formatted, strict mode, bats tests.

## Verify
- `shellcheck -x script.sh`: static analysis, following `source`d files (`-x`).
- `shfmt -d .`: prints a diff for unformatted scripts and exits non-zero (use `-w` to write).
- `bash -n script.sh`: syntax check, no execution.
- `bats test/`: runs `*.bats` tests, when bats-core is installed.

## Test first
Put tests in `test/*.bats`; run the script as a subprocess with `run`.
```bash
#!/usr/bin/env bats

@test "refuses to run without an argument" {
  run ./bin/deploy.sh
  [ "$status" -eq 2 ]
  [[ "$output" == *"usage:"* ]]
}

@test "dry run prints the plan and changes nothing" {
  run ./bin/deploy.sh --dry-run prod
  [ "$status" -eq 0 ]
  [ ! -e "$BATS_TEST_TMPDIR/deployed" ]
}
```
No bats available: a failing `assert` script that calls the function and `exit 1` on mismatch is enough.

## Do
- Start with `#!/usr/bin/env bash` and `set -euo pipefail`; add `IFS=$'\n\t'` only if the script splits words on purpose.
- Quote every expansion: `"$var"`, `"${arr[@]}"`, `"$(cmd)"`.
- Use `[[ ... ]]` for tests, `$(...)` for substitution, `local` for function variables, and `readonly` for constants.
- Create temp files with `mktemp` and clean up with `trap 'rm -rf "$tmp"' EXIT`.
- Parse options with `getopts` or a `case` loop, and print `usage` to stderr with exit status 2.
- Pass `--` before user-supplied paths (`rm -- "$f"`), and use `printf '%s\n'` over `echo` for arbitrary data.
- Read lines with `while IFS= read -r line; do ...; done < file`, and use `mapfile -t arr < <(cmd)` for arrays.

## Avoid
- Unquoted `$var`: word splitting and globbing; the classic `rm -rf $dir/` disaster. Quote, and use `${dir:?}` to abort on empty.
- Parsing `ls` output or `for f in $(ls)`: breaks on spaces and newlines. Use a glob or `find -print0 | xargs -0`.
- Relying on `set -e` inside `if`, `&&`/`||` lists, or pipelines: errors are ignored there. Check `$?` explicitly or use `|| exit`.
- `cd dir; rm *` with no guard: if `cd` fails you delete elsewhere. Use `cd dir || exit 1`.
- `eval` and `bash -c "$user_input"`: injection. Use arrays: `cmd=(prog "$arg"); "${cmd[@]}"`.
- `cat file | while read ...` assigning variables: the pipe runs a subshell, so values are lost. Use redirection or `< <(...)`.
- Bashisms under `#!/bin/sh`: arrays and `[[` fail on dash. Use bash in the shebang or stay POSIX.

## Review
- [ ] ShellCheck passes with no new `# shellcheck disable`, and each disable has a reason.
- [ ] All expansions are quoted; destructive commands guard against empty variables.
- [ ] Temp files and background jobs are cleaned up via `trap`.
- [ ] Exit codes are meaningful, and errors go to stderr.
- [ ] Shebang matches the syntax used (bash vs POSIX sh).
