---
name: shellcheck
title: ShellCheck
area: tools
tags: [shell, bash, lint, static-analysis, quoting]
detect: [file:.shellcheckrc]
related: [shell-scripting, pre-commit, hadolint]
---
ShellCheck: static analysis for sh and bash scripts that catches quoting, word-splitting and portability bugs.

## Verify
- `shellcheck script.sh`: findings with SC codes and line numbers.
- `shellcheck -x script.sh`: follows `source` directives to check sourced files.
- `shellcheck -s bash script.sh`: forces the dialect when there is no shebang.
- `shellcheck -f gcc script.sh`: compact one-line findings, easy for CI and editors.
- `bash -n script.sh`: the syntax parses, which shellcheck does not replace.

## Test first
Reproduce the finding on the smallest script.
```
cat > /tmp/t.sh <<'EOF'
#!/usr/bin/env bash
rm -rf $dir/*
EOF
shellcheck /tmp/t.sh    # expect SC2086: double quote to prevent globbing and word splitting
```
Fix and rerun until it exits 0. Also run the script on an input with spaces in a path.

## Do
- Start scripts with a shebang so the dialect is known, and `set -euo pipefail` for bash.
- Quote every expansion: `"$var"`, `"${arr[@]}"`, `"$(cmd)"`.
- Put project-wide options in `.shellcheckrc` (`shell=bash`, `enable=...`, `source-path=SCRIPTDIR`).
- Add `# shellcheck source=path/lib.sh` above a `source` line when the path is dynamic.
- Use `[[ ]]` in bash and `[ ]` in sh, and arrays instead of space-joined strings.
- Run it in CI over all shell files, including those without an extension, found via a git file list.

## Avoid
- Silencing with `# shellcheck disable=SC2086` as a reflex: fix the quoting. If a split is intended, use an array or `read -ra`, and say so in a comment.
- `for f in $(ls)` or `for f in $(find ...)`: breaks on spaces. Use globs or `find -print0 | while IFS= read -r -d '' f`.
- `cd dir` without a guard: use `cd dir || exit 1`, or `set -e`.
- `[ $a == $b ]` in sh: `==` is a bashism. Use `=` and quotes.
- `echo $var | cmd` on data that may start with a dash: use `printf '%s\n' "$var"`.
- `local x=$(cmd)` hides the exit code (SC2155). Declare, then assign.

## Review
- [ ] shellcheck exits 0 on every changed shell file, with `-x` where scripts source others.
- [ ] Each `disable` is single-code and explained.
- [ ] Shebang matches the syntax used (no bashisms under `#!/bin/sh`).
- [ ] The script was tried with spaces and an empty argument in the inputs.
