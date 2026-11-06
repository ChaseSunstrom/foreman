**Verdict: changes needed.** `_track_vars` still has bypasses, and one of them is the same class T-0161 set out to close. I traced each through `_straight_line` → `_tokens` → `_split` → `_track_vars` → `_with_vars` by reading the code. I could not run bash or Python, so none are confirmed by execution. Paths are all `~/.claude/foreman/plugin/lib/fmguard.py`.

**Adversary findings**

1. **HIGH, line 62 (`_track_vars`, `command` and `builtin` stripping at 684-687).**
   - Command: `D=~; command D=/tmp/x/s; rm -rf "$D"`.
   - Bash: `command D=...` looks for a program named `D=...`. It is not an assignment, so `$D` stays `~`.
   - Guard: strips `command`, sees an assignment-only command, sets `env[D]=/tmp/x/s`, and `rm` passes. `builtin D=…` behaves the same way.
   - Trace: `_straight_line` is true (no branch characters), and `_split` yields 3 commands.
   - Fix: after stripping `command` or `builtin`, accept the assignment-only path only when the next word is `export`, `readonly` or `declare`. A bare `NAME=` after them must return None.

2. **HIGH, line 62 (`_tokens` drops quoting).**
   - Command: `D=~; "D=/tmp/x/s"; rm -rf "$D"`. `\D=/tmp/x/s` and `D"="/tmp/x/s` work too.
   - Bash: a quoted or escaped name or `=` is a command word, not an assignment. It gives "command not found" and `D` is unchanged.
   - Guard: posix `shlex` strips the quotes, so `_ASSIGN` matches and `env` is overwritten.
   - Related: `"time" D=…` and `\! D=…` hit the same blindness in line 684, because `time` and `!` are only keywords when unquoted.
   - Fix: have `_tokens` keep a marker for quoted words, or check the raw command segment. Resolve a variable only when the `NAME=` text appears unquoted in the original.

3. **HIGH, lines 63-70.**
   - Command: `readonly D=~; D=/tmp/x/s; rm -rf "$D"`.
   - Bash: the second assignment fails with "readonly variable". Non-POSIX bash continues, and `D` stays `~`.
   - Guard: `readonly` is treated as a plain assignment, then `D=` overwrites it in `env`.
   - Fix: after `readonly` or `export -r`, record the name as frozen. Drop it from `env` and refuse to re-assign it.
   - Related: bash's own read-only variables (`UID`, `EUID`, `PPID`, `SHELLOPTS`) fail the same way.

4. **MEDIUM, line 670 (`_SHELL_SET` is incomplete).**
   - Command: `RANDOM=/tmp/x/s; true; rm -rf "$RANDOM"`.
   - Bash: yields a number, so the `rm` target is a relative path in the cwd.
   - Guard: the resolver substitutes the safe absolute path.
   - Not covered: `SECONDS`, `LINENO`, `EPOCHSECONDS`, `EPOCHREALTIME`, `SRANDOM`, `UID`, `EUID`, `PPID`, `GROUPS`, `SHLVL`, `PIPESTATUS`, `FUNCNAME`, `HISTCMD`, `OPTIND`, `REPLY`, `HOSTNAME`.
   - Impact is limited to relative targets.
   - Fix: allowlist instead, so only names the script itself assigned from a `NAME=literal` are kept.
   - Related: `D=/tmp/x/s; [[ D=0 -eq 0 ]]; rm -rf "$D"`. Arithmetic inside `[[` assigns a number. `[[` is in `_INERT`, and its operands contain no brace or paren, so it passes `_straight_line`. Treat `[[` with `-eq`, `-ne`, `-lt` and similar as non-inert.

5. **MEDIUM, line 326 (`_tokens`, outside the focus but it hides commands).**
   - Command: `echo a#b; rm -rf ~`.
   - Bash: `#` mid-word is literal.
   - Guard: posix `shlex` with `commenters="#"` treats a mid-word `#` as a comment start and discards the rest of the line, as I remember CPython's `shlex.py`. That would hide the `rm`.
   - No test has `\w#\w` (grep found none). Confirm by running it.
   - Fix: set `commenters=""` and strip real comments yourself.

Not found: `${D:=…}`, `$((…))`, `{fd}>` and `+=` forms are all stopped by `_BRANCHY`, `_ASSIGNISH` or `_unresolvable`.

**Acceptance criteria**
- New EXTRA cases blocked: not verifiable here. The 18 listed cases look handled by the code, but findings 1 to 3 have no case.
- T-0151 safe forms still pass: not verifiable here. The new test lines at `test_guard.py:109-112` read consistently.
- `fm check`: not verifiable here.

**Intent:** changes needed. The request was "fails closed on every way bash changes a variable". Findings 1 to 3 contradict that, and the CHANGELOG and MASTER.md claim of "an allowlist, only builtins can change a variable" overstates it. `_SHELL_SET` is a denylist, and the differential test lacks `command D=`, quoted-name and `readonly` cases.

**adversary:** changes needed (3 HIGH, 2 MEDIUM)
**intent:** changes needed (the fail-closed claim is not met)

**Not checked:** I did not run bash or the test suites. I did not review the edge, operator or maintainer lenses.
