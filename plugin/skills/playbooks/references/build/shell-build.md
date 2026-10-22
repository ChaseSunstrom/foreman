<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Shell script errors (bash -n, ShellCheck, bats)

Use when a shell script fails to parse, fails ShellCheck, dies under strict mode, or fails its bats tests. Shell has
no compiler, so "the build" here is three checks: the parser (`bash -n`), the linter (`shellcheck`) and the tests
(`bats`). The goal is all three green with the smallest diff. Built on the library cards `fm lib show bash`
(strict mode, bats), `fm lib show shellcheck` (the SC codes, directives), `fm lib show shell-scripting`
(quoting, traps, POSIX sh) and `fm lib show cli-tests` (testing a script through its real entry point).

## Diagnostic commands

```bash
head -1 script.sh                          # the shebang decides the dialect: bash, sh, dash, zsh
bash -n script.sh                          # parse only, runs nothing (sh -n for #!/bin/sh scripts)
shellcheck -f gcc script.sh                # one line per finding: file:line:col: severity: message [SCnnnn]
shellcheck -S warning script.sh            # errors and warnings only
file script.sh                             # "with CRLF line terminators" means Windows line endings
bash -x script.sh 2>&1 | tail -20          # trace each command as it runs (only on a script that is safe to run)
bats --print-output-on-failure test/       # tests, with the failing test's output
```

## First error

1. **Parse errors first.** Nothing else is meaningful while `bash -n` fails. Its message,
   ``script.sh: line 6: syntax error near unexpected token `done'``, names the line where the parser gave up, not
   where the mistake is: checked here, a missing `fi` on line 5 was reported at the `done` on line 6. Look upward
   for the unclosed `if`/`case`/`do`/`{`/quote. `syntax error: unexpected end of file` means the opener is
   never closed anywhere; the last one opened is the usual suspect. Pass: you name the opening line you fixed.
2. **Then ShellCheck, by severity.** Severities are `error`, `warning`, `info`, `style`. Fix every `error` and
   `warning` before any `info` or `style`, and read the SC code: each has a wiki page
   (`https://www.shellcheck.net/wiki/SC2086`). A file that sources others needs `-x` to follow them.
3. **A silent exit is strict mode.** Under `set -e` a failing command ends the script with no message. Find it with
   `bash -x`, or add `trap 'echo "line $LINENO: $BASH_COMMAND exited $?" >&2' ERR` with `set -E` (without `-E`,
   functions don't inherit the trap). Under `set -u`, the message `VAR: unbound variable` names the variable.
4. **bats failures name the line.** `not ok 3 parses flags` is followed by `# (in test file test/cli.bats, line 12)`
   and the failed command. `run` captures a failure instead of stopping the test, so the assertion after it
   (`[ "$status" -eq 0 ]`) is what fails: print `$output` to see why.

## Common causes

| Message | Usual cause | Fix |
|---|---|---|
| `syntax error near unexpected token` | Unclosed block above the reported line, or `[ ]` without spaces | Close the block; `[ "$a" = b ]` needs a space after `[` and before `]` |
| `$'\r': command not found` / `/usr/bin/env: 'bash\r'` | CRLF line endings | Convert to LF (`dos2unix FILE`) and add `*.sh text eol=lf` to .gitattributes |
| SC2086 `Double quote to prevent globbing and word splitting` | Unquoted `$var` | `"$var"`; for a list of arguments use an array: `"${args[@]}"` |
| SC2046 `Quote this to prevent word splitting` | Unquoted `$(cmd)` | Quote it, or read lines into an array with `mapfile -t` |
| SC2045 `Iterating over ls output is fragile` | `for f in $(ls …)` | Glob directly: `for f in ./*.txt; do [ -e "$f" ] \|\| continue; …` |
| SC2164 `Use 'cd … \|\| exit' in case cd fails` | `cd` without a failure branch | `cd "$dir" \|\| exit 1` |
| SC2155 `Declare and assign separately to avoid masking return values` | `local x=$(cmd)` hides `cmd`'s status | `local x; x=$(cmd)` |
| SC1090 / SC1091 `Not following` a sourced file | Non-constant or unreachable `source` path | Add `# shellcheck source=lib/common.sh` above it and run with `-x` |
| SC3010 and other SC3xxx `In POSIX sh, … is undefined` | Bash features in a `#!/bin/sh` script | Use the POSIX form (`[ ]`, no arrays), or change the shebang to bash if bash is guaranteed |
| SC2148 `Tips depend on target shell` | No shebang | Add `#!/usr/bin/env bash` (or `#!/bin/sh`) on line 1 |
| `VAR: unbound variable` | `set -u` and an unset variable or missing positional | `${VAR:-default}`, or check `$#` before using `$1` |
| `pipefail` exit from `grep -q` or `head` in a pipe | Producer killed by SIGPIPE, or `grep` found nothing (status 1) | Handle the "no match" status explicitly (`\|\| true` on that one command, with a comment) |

## Verify

```bash
git ls-files -z '*.sh' '*.bash' | xargs -0 -r -n1 bash -n \
  && git ls-files -z '*.sh' '*.bash' | xargs -0 -r shellcheck -x -S warning \
  && bats test/
```

Pass: exit 0. Add extensionless scripts (find them with `grep -rlE '^#!.*\b(ba)?sh\b' bin/`) to both lists by
name; use `sh -n` for `#!/bin/sh` files. A repo without bats tests skips the last line and says so in the
evidence.

## Rules

- No new `# shellcheck disable=` line without a comment on the same or previous line saying why the finding is
  wrong for this code.
- No `set +e`, `set +u` or removal of `pipefail` to get past a failure; handle the one command that may fail.
- No `eval` added to fix quoting.
- Every changed script passes `bash -n` (or `sh -n`) and `shellcheck -S warning` on its own.

## Stop conditions

Stop and report when the same error survives three fixes, when a fix needs bash 4+ features on a target that ships
bash 3.2 (macOS's `/bin/bash`), or when making a script POSIX would mean rewriting it.

## Report

```text
[FIXED] bin/deploy.sh:5  missing fi (bash -n reported line 6, token 'done')
Fix: closed the if block
Check: bash -n OK | shellcheck -S warning clean | bats 12/12 | files: bin/deploy.sh
```
