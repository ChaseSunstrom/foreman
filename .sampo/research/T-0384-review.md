## Verdict
**Changes needed.** I found four concrete bypasses by reading the code. I could not run bash or the tests, because I only had read tools. For each one I traced the guard's code path and compared it with what bash does from its documented behavior.

## Findings

**1. HIGH — `plugin/lib/fmguard.py:1184`, `:1441`, `:1389-1404`.** `_mask_quotes` pairs apostrophes inside `#` comments.
- `check_bash` passes `_top` and `_prefix_vars` the comment-bearing text (`shell = _strip_heredocs(cmd)`, line 1644). `_tokens` strips comments, but `_mask_quotes` does not.
- Input, run with cwd set to a guarded folder such as `<fhome>/plugin/lib`:
  ```
  echo # a'
  true || cd /tmp
  echo x > fmguard.py # b'
  ```
- The mask runs from the apostrophe in `# a'` to the one in `# b'` and hides the `||` and both newlines. `_top` then returns straight=True.
- At line 1697, `cd /tmp` is treated as certain (a straight line and it can't fail), so cwds becomes `[/tmp]`.
- In bash, `true ||` skips the cd, so the write lands in `fmguard.py` in the original cwd.
- Before this diff the visible `||` made `certain` false.
- Fix: make `_mask_quotes` mask a word-start `#` to end of line, as `_strip_comments` does, and keep the length unchanged. Add the case above to `test_guard_diff.py`.
- Confidence: high.

**2. HIGH — `plugin/lib/fmguard.py:1419-1430`.** `source` and `.` open whatever path the command names while the guard runs.
- `source /dev/stdin <<< 'cd ~'` has "/" in `args[0]`. `open("/dev/stdin")` reads the hook's own stdin, which is already consumed and empty. `_MOVERS` finds nothing, so moves=False. Bash then runs the `cd ~`.
- `/dev/fd/0` and `/proc/self/fd/0` behave the same way.
- A FIFO path makes `open` block, which hangs the hook.
- A file that exists but is edited earlier in the same command is read stale. Example: `echo 'cd ~' > ok.sh; . ./ok.sh` where `ok.sh` already exists and is harmless.
- Fix: read only `os.path.isfile` paths outside `/dev` and `/proc`, and return True for anything else.
- Confidence: high on `/dev/stdin`; medium on the stale-file case.

**3. HIGH — `plugin/lib/fmguard.py:1462-1470`.** A pipeline that continues after a newline is only half dropped.
- The code splits the prefix on `;|\n|&&` and drops only the elements that contain a `|`.
- Input: `true |` newline `S=/tmp/x; echo hi > $S/../etc/guarded`.
- The first element `true |` is dropped, but `S=/tmp/x` is the last stage of the same pipeline and is kept. `counts[S]` is 1, so `pre` gets `S=/tmp/x`, and line 1661 passes it on as fixed.
- The guard resolves the target to `/tmp/etc/guarded`. In bash `S` is unset in the main shell, so the path is `/../etc/guarded`, which is `/etc/guarded`.
- Before this diff the cut at `|` stopped tracking there.
- Fix: if an element ends in `|` or `|&`, drop the next element too. Alternatively, skip the whole prefix when any pipe is followed by a newline.
- Confidence: medium-high.

**4. HIGH — `plugin/lib/fmguard.py:1416`.** `trap -- 'cd ~' DEBUG` slips through.
- `args[0]` is `--`, which starts with "-", so `text` is empty and moves is False. The same applies to `trap -p`.
- A DEBUG or ERR trap runs `cd ~` before the next command, so `echo x > f` writes in `~`.
- Fix: skip a leading `--` and read the next word as the code. Treat any option other than `-p` as moving the shell.
- Confidence: high.

**5. MEDIUM — `plugin/lib/fmguard.py:1416-1418`.** Brace expansion happens before `eval` sees its text.
- `eval {c,#}d` expands to `eval cd '#d'`, which is a bare `cd` to HOME.
- The guard sees the literal `{c,#}d`: no `$`, backtick, or backslash, and no match in `_MOVERS`.
- Fix: add `{` to the `[$`\\]` check.
- Confidence: medium (the mechanism is documented bash behavior; I did not run it).

**6. MEDIUM — `plugin/lib/fmguard.py:1428`.** The file path of `_moves_shell` never applies the `[$`\\]` check that the eval path applies.
- A script containing only `"$@"` or `$1`, sourced as `. ./run.sh cd /x`, moves the shell.
- A script containing `c\d ~` or `c""d ~` also moves it and matches no pattern.
- Fix: for a sourced file, treat `$`, a backslash, or a quote adjacent to a mover word as moving the shell. Alternatively, treat `source` with extra arguments as moving it.
- Confidence: medium.

**7. LOW — `plugin/lib/fmguard.py:1691`, `:1695`.** `cd /tmp extra` uses only `dirs[0]`.
- I recall bash 5 failing with "too many arguments". I did not run it.
- The cd is then treated as one that cannot fail.
- This is pre-existing in the straight case. The diff extends it to the `base` replacement at line 1699.
- Fix: set `can_fail` when `len(dirs) > 1`.

**8. LOW, unverified — `plugin/lib/fmguard.py:1703`.** The mover list is missing `mapfile -C 'cd ~ #'`, which runs its callback in the current shell.

## Acceptance criteria
- **Three JARVIS commands pass, conservative rows still block:** not verifiable here, because I could not run the tests. By reading, the test rows do not exercise a comment containing an apostrophe, the `/dev/stdin` source, `trap --`, or a pipe followed by a newline.
- **Real bash agrees (`test_guard_diff.py`):** not verifiable, same reason. The new `EXTRA` rows match the mechanisms I read, but none of findings 1 to 6 are in them.

## Not checked
- Whether I verified the claim that `_outside` voids tracking for any setter that sits in a pipeline. I confirmed it only for `eval`, `read`, and `printf -v` (line 1288).
- Whether `$S/tool` in `_track_vars` is safe. I found no break. `_setter` matches only the exact builtin name, and the value filters at line 1614 hold.
- Other lenses, and unquoted-substitution parity effects on `_mask_quotes`. I could not build a bypass from the substitution step, because the quote count goes odd and the function fails closed.
