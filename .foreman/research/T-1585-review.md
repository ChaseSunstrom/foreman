**Verdict: changes needed.** I could not run anything, so every finding is traced by reading `~/.claude/foreman/plugin/lib/fmguard.py`. That file has moved on since `T-1585.diff`: `_ENV_DROPPERS`, the `unread` handling in `_check_awk` and the glob/`/home` branch in `_interpreter_reads` are not in the diff. I reviewed the current tree.

## lens: adversary

- HIGH — fmguard.py:2210 — `awk '{system($0)}' cmds.txt` returns `[]`. `$0` becomes `$AWKVAR`, `check_bash("$AWKVAR")` finds nothing, and `print | "sh"` has a `cat … | sh` rewrite that `system()` lacks. Same for `echo 'rm -rf ~' | awk '{system($0)}'`. — treat a computed `system()` argument like the `print | sh` case, as `cat DATA | sh`. — high
- HIGH — fmguard.py:2133,2146 — `gawk -i inplace '{gsub(/a/,"b")}1' ~/.claude/settings.json` (or `~/.bashrc`) edits the file in place. `-i inplace` is swallowed and `_write_targets` has no awk branch, so it passes. — in `_write_targets`, make awk with `-i inplace` (or `--include=inplace`) write its data operands. — high
- HIGH — fmguard.py:2076 — `perl -pe 1 ~/.ssh/id_rsa` and `python3 -c 'import sys;print(open(sys.argv[1]).read())' ~/.ssh/id_rsa` pass. Only quoted literals are scanned, and interpreters are not in `_READERS`. — classify bare operands of an interpreter command with `classify_read`. — high
- HIGH — fmguard.py:2078,2081 — `python3 -c 'print(open(os.path.join("~", ".ssh", "id_rsa")).read())'` passes. Absolute-home literals alone never fire `_CRED_PART`, because it needs a `~`/HOME token. `"~/"+".ssh/id_rsa"` passes too. — fire `_CRED_PART` when `ctx.home` appears anywhere in the code. — high
- MEDIUM — fmguard.py:2076 — ordinary credential-reading code gets through in four more ways: — high
  - `python3 -c 'import glob,os;print([open(f).read() for f in glob.glob(os.path.expanduser("~/.s*/id_*"))])'` passes: the under-home branch calls `classify_read` and never checks wildcards.
  - `cd ~/.aws && python3 -c 'print(open("credentials").read())'` passes: relative literals are never resolved against the tracked cwd.
  - `ln -s ~/.ssh /tmp/s` in an earlier call, then `open("/tmp/s/id_rsa")`, passes: only literals under home are judged, with no realpath.
  - A node heredoc using `` `${os.homedir()}/.ssh/id_rsa` `` passes, as does `print('"'); open("~/.ssh/id_rsa")`. Backtick strings aren't scanned, and a stray quote shifts the pairing.
  - Fix for all four: resolve every absolute literal and relative literal (against the tracked cwd) with `classify_read`. Also scan the tokenised code text for credential names.
- MEDIUM — fmguard.py:1445 (`_INTERP_NAMES`) — `lua -e`, `pypy3 -c`, `ipython -c`, `Rscript -e` and `julia -e` are not interpreters to this check, so none of the new code runs. — add them. — high
- MEDIUM — fmguard.py:2081 — false block, and an acceptance-criteria miss: `python3 -c 'import os;print(open(os.path.expanduser("~/.ssh/known_hosts")).read())'` is refused as credentials. The outer shell quotes make the whole program one "literal", which `_CRED_PART` matches because `~` is present. — skip literals containing whitespace, parentheses or quotes. — high
- MEDIUM — fmguard.py:2137 — awk programs the guard never reads: — high
  - `printf 'BEGIN{system("rm -rf ~")}' > /tmp/p.awk && awk -f /tmp/p.awk` passes. The unread-file fallback only scans heredocs and here-strings, and `awk -f <(printf …)` is also unread.
  - `gawk -E p.awk`, `--exec`, `-i lib`, `@include` and abbreviated options such as `--sou=…` are never read. `-E` and `--exec` are missing from `_AWK_TAKES`.
  - Fix: refuse awk with any option or `@include` that loads code the guard can't read.
- MEDIUM — fmguard.py:2178 — `awk 'BEGIN{system("\162\155 -rf ~")}'` passes. Only `\n` and `\t` are decoded, so the guard sees `162155 -rf ~`. — decode octal and `\x` escapes. — high
- MEDIUM — fmguard.py:2211,2224 — awk programs written with parenthesised operands pass: `awk 'BEGIN{print "rm -rf ~" | ("sh")}'`, `awk 'BEGIN{("rm -rf ~") | getline}'` and `print "x" > ("~/.bashrc")`. `_AWK_TERM` cannot match a leading `(`. — allow `\(` and `\)` around `_AWK_EXPR`. — high
- MEDIUM — fmguard.py:2132,2211 — possible exponential regex backtracking. `_AWK_EXPR` nests adjacent `[A-Za-z_]\w*` terms with `[ \t]*` between them, so a long identifier or word (30 or more characters) not followed by `| getline` has about 2^n splits. This runs in the hook on ordinary programs. Not timed. — make terms require a separator, or use atomic groups. — medium
- MEDIUM — fmguard.py:2100 — a path-spelled fm is never "bare", so these pass: `env -i plugin/bin/fm settings set motion off`, `exec -c ~/.local/bin/fm …`, and `sudo -u chase plugin/bin/fm …`. The lookbehind excludes `/`. — drop `/` from the lookbehind, or test `argv[0]`'s basename. — high
- MEDIUM — fmguard.py:2116,2123,2108 — three more ways to hide the variables from fm, all passing: — high
  - `env --ignore-env fm …`: only the exact long name is matched.
  - `exec -a x -c fm …`: the loop stops at `x` before it reaches `-c`.
  - `v=CLAUDECODE; unset $v; fm …` and `printf CLAUDECODE | xargs -I{} env -u {} fm …`: the name is never literal in the command.
  - Fix: match env long-option prefixes, step over the value of `-a`, and refuse `unset`/`env -u` with an expanded operand.
  - Impact is limited because `fmsettings.in_claude_code` also fails closed without a tty. It matters with a pty: `script -qc 'v=CLAUDECODE; unset $v; fm settings set motion off' /dev/null`.
- MEDIUM — fmguard.py:577 — false block, plausible: `echo x > /dev/stderr`, `awk '{print > "/dev/stderr"}'` and `> /dev/stdout` now return "system". `_variants` adds the realpath, `/proc/<pid>/fd/pipe:[n]`, which sits under `/proc` but not under the literal `/proc/self/fd` exemption. — exempt `^/proc/(self|thread-self|\d+)/fd/`. — medium
- MEDIUM — fmguard.py:2104 — false block: `sudo apt-get update && fm doctor` and `ssh host uptime; fm status` return self-authorize. `bare` is true for the whole line, not for the dropper's own command. — require fm/claude inside the dropper's own argv. — high
- LOW — fmguard.py:2108 — false block: `printf '%s\n' "$CLAUDECODE"` and `declare -p CLAUDECODE` are refused. `printf` and `declare` count as assigners whenever the name appears. — require `-v` for printf and ignore `declare -p`. — high
- LOW — fmguard.py:4213 (`_write_targets`) — these pass: `mv /etc/hosts /tmp/h` (the source is never judged), `touch /etc/nologin`, `mkdir -p /etc/x`, `install -d /opt/x`. `python3 -c "open('/etc/x','w')"` also passes, because `_interpreter_writes` filters `system` out. — add those verbs and keep `system` in the interpreter filter. — high

## Acceptance criteria

- **T-1460:** partly met. The listed spellings are refused, but the "still pass" criterion fails for `~/.ssh/known_hosts` inside quoted code.
- **T-1570:** met for the listed forms; the bypasses above are not covered.
- **T-1575:** met for the listed forms. Writes to `/etc` pass the tests, but the false block above hits `/dev/stderr`.

## Implicit decisions

- A shell-quoted program counts as one literal (accidentally protective).
- `/var` is a system folder except `/var/tmp` and `/var/folders`.
- Interpreter code sees only credentials and the CLAUDECODE variables, not system writes.
- `rm` of any `/var`, `/opt` or `/srv` path outside the project now returns "system".

## Not checked

Test files, CHANGELOG, runtime timing, the sudo/tmux behaviour of fm itself, and macOS paths (`/private/etc`).

Noticed: `perl -pi -e … /etc/hosts` is not in `_write_targets`; perl, ruby and node script files are never scanned by `_interpreter_reads`.
