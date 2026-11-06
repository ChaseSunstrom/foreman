## Verdict
**Changes needed.** I had no shell tool, so I ran nothing and traced the code instead. Each finding below is a trace, not a measured result.

## lens: adversary
- HIGH — fmguard.py:2084 — The `cd DIR &&` handling only matches a leading `cd`. `cd ~/.aws; python3 - <<'EOF'\nprint(open("credentials").read())\nEOF` is not refused. The same holds for `(cd ~/.aws && python3 - <<…)` and a newline after `cd`. `python3 -` has no operands, and `.stdin` is only set by `<`. A bare `credentials` or `work_key` matches no name pattern. — Fix: resolve bare literals against every `cd` target in the command, or refuse relative literals when the command cds into a credential folder. — high
- HIGH — fmguard.py:2096 — The home-join fix only works when cwd is outside home. With cwd `/home/u/proj`, `python3 -c 'import os;print(open(os.path.join(os.environ["HOME"], ".aws", "credentials")).read())'` is not refused. The literal `.aws` resolves to `cwd/.aws`, which is under home, so `_CRED_PART` is skipped. The tests only pass because their home is a temp dir and the repo sits outside it. Non-standard key names under `.ssh` and `.kube` or `.gnupg` paths escape the same way. — Fix: apply the under-home exemption only to absolute, `~` and `$HOME` literals. — high
- MEDIUM — fmguard.py:2100 — The credential-name fallback scans the whole command, not just interpreter code. `ssh -i ~/.ssh/id_ed25519 host python3 -V` is refused, although the tests expect `ssh -i KEY` to pass. `git -C /home/u/p add .npmrc && git commit -m "bump node version"` is refused too. — Fix: look only in quoted literals or interpreter code. — high
- MEDIUM — fmguard.py:2149 — The `-l` option is ignored. `gawk -l readfile 'BEGIN{printf "%s", readfile("/home/u/.ssh/id_rsa")}'` reads the key and is not refused. — Fix: refuse `-l`, `@load` and `readfile(` when the argument names a credential. — medium
- MEDIUM — fmguard.py:2169 — In-place edit detection and program sources both have gaps. `gawk '@include "inplace"\n1' ~/.claude/settings.json` is not caught, and neither is `-i /usr/share/awk/inplace.awk`. `gawk -W source='BEGIN{system("rm -rf ~")}' /dev/null` and `mawk -W exec p.awk` leave the real program unread: the `-W` value is consumed and the first operand becomes the program. — Fix: match inplace by basename and by `@include` text, and parse `-W source=`, `file=` and `exec`. — medium
- MEDIUM — fmguard.py:585 — `project_root_for("/etc")` returns `/etc` when no `.git` exists. After `cd /etc` in one call, `touch /etc/cron.d/x` in the next call is exempt as "the project". — Fix: exempt a project root only if it has `.git`, or is strictly below a system root. — medium
- MEDIUM — fmguard.py:3272 — The touch/mkdir/mv check does not follow realpath or globs, and it skips unresolved `$D`. After `ln -s /etc e`, `touch e/x` and `mv e/hosts .` pass. `touch /et[c]/x` and `D=$(echo /etc); touch $D/x` pass too. Writes use `_variants` and `_expansions`. — Fix: use `classify_write`-style variants and globs. — high
- LOW — fmguard.py:2125 — `_hides_claude` misses several forms: `unset CLAUDE{,CODE}`, `env -uCLAUDE{CODE,} fm x`, `declare -n r=CLAUDECODE; unset r`, `let CLAUDECODE=`, and `for CLAUDECODE in x; do …`. — Fix: refuse brace words that expand to the names, plus `let`, `declare -n` and `for NAME`. — medium
- LOW — fmguard.py:4330 — The perl/ruby `-i` test looks for `i` anywhere in the cluster. `perl -MFile::Basename -ne 'print' ~/.claude/settings.json` (also `-Mstrict`, `-Ilib`, `ruby -rfileutils`) counts as an in-place edit and is refused as a core write. — Fix: parse the cluster up to the first switch that takes a value. — high
- LOW — fmguard.py:366 — `--key=/home/u/.ssh/work_key` is skipped by the `startswith("-")` filter. Standard `id_*` names still hit the name fallback. — Fix: also check the value after `=` in interpreter operands. — medium
- LOW — fmguard.py:2228 — An unread awk program makes the guard scan the whole command. `awk -f missing.awk d; grep -n 'system(' x` yields `cat d | sh`, which is refused. `touch -r /etc/hosts out` is a false block too. — Fix: scan only heredoc bodies and the `-f` argument, and skip `-r` values. — high

Performance was not measured. In theory `_AWK_EXPR` retries from every character, so a 100 KB unread-program command of space-separated words without punctuation costs O(n·k). `_balanced` rescans per unclosed `system(`. A normal heredoc is linear.

## Acceptance criteria
- Interpreter operands read as targets: met. `python3 script.py --out ~/.ssh/config` and `node x.js ~/.aws/config` pass, because those are public parts.
- Glob, backtick and `/proc/<pid>/fd` fixes: met (traced).
- `-i`/`--` forms of awk and `touch`/`mv` into system folders: not met (findings above).

## Implicit decisions
- The fallback name scan covers the whole command line.
- Interpreter operands that start with `-` are never read targets.
- Any system folder that is the cwd becomes a project root.

## Not checked
Whether fmhooks fails open on exceptions, such as a NUL byte in a literal reaching `os.path.realpath`. Whether the test suite passes.

**Noticed:** `_interpreter_reads` is called without the `fm --run` strip at depth > 0; no test covers the join-under-home case with a cwd inside home.
