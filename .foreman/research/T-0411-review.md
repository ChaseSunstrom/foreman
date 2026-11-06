**Verdict: changes needed.** I found three bypasses in `_expand_literal_loops`. I could not run bash (read-only), so each one is traced from the code and not executed.

**Findings**

1. **HIGH** — `plugin/lib/fmguard.py:1453` (`_LOOP`) and `:1488-1500` — **an unquoted `done` inside the body ends the match early.**
   - `(.*?)(?<![\w-])done\b` stops at `echo done`, because `done` is a plain argument there.
   - The matched body is only `echo`, which passes the `_LOOP_SETTERS` check. The real remainder of the loop stays in the text after `; w=b`.
   - Input: `for w in /etc ok; do echo done; rm -rf $w/passwd; done`.
   - The guard reads `echo; echo; w=b; rm -rf $w/passwd; done`, so it sees only `rm -rf b/passwd`. Bash runs `rm -rf /etc/passwd` too.
   - Fix: require `done` in command position, `(?:^|[;\n&|])\s*done\b`. Alternatively, skip the loop whenever another `done` token follows in the masked text.
   - Confidence: high.

2. **HIGH** — `:1492` and `:1499` — **`V=last` is appended even when bash does not run the loop in this shell.**
   - `before[-1]` may be `&` or `|`, so the loop can sit after `&&`, `||` or a pipe. `keeps` looks only at what follows `done`.
   - Input 1: `[ -f /nonexistent ] && for w in a; do :; done; rm -rf $w/etc`. The loop is skipped, so `w` is unset and bash runs `rm -rf /etc`. The guard sees `w=a` and `rm -rf a/etc`, a relative path.
   - Input 2: `echo | for w in a; do :; done; rm -rf $w/etc`. The loop runs in a pipeline subshell, so `w` is unset in the parent. The guard still assigns it.
   - The unset-name check at `:1629` no longer applies, because `w` now looks set.
   - Fix: set `keeps` only when `before` is empty or ends in `;`, a newline or `(`. If `before` ends in `&&`, `||` or `|`, still expand the body but do not append `V=`.
   - Confidence: medium-high.

3. **MEDIUM** — `:1454` and `:1739` — **IFS is not checked.**
   - The literal word set includes `,`, `.`, `/`, `:`, `=`, `@`, `+` and `%`. An earlier `IFS=,` makes bash split the unquoted `$w`, but the guard substitutes it as a single word.
   - Input: `IFS=,; for w in x,/etc/foo; do tee $w </dev/null; done`. Bash writes `/etc/foo`; the guard sees `tee x,/etc/foo`, a relative file.
   - The `IFS` guard in `_track_vars` only covers tracked variables, not loop expansion. Before this change `$w` was unknown and failed closed.
   - Fix: return `cmd` unchanged if `IFS` appears anywhere in it.
   - Confidence: medium.

**Forms I checked that hold**
- A pipe or redirect after `done`: the targets are still seen.
- Nested loops, `case`, heredocs and C-style loops: skipped.
- `in` omitted: not matched.
- Quoted `done`: masked.
- Reassignment of `w` through `${w:-}`, `$((w))`, `read`, `declare -n` or `printf -v`: skipped.
- Words containing `=` or `-`: the expanded text is sequential and equivalent.
- `\$w`: only a false-positive difference.
- Aliases and function bodies: no new gap.
- The `V=` append for special variables (`HOME`, `CDPATH`, `PATH`): no worse than writing `V=…` literally.

**Acceptance criteria**
- JARVIS's literal loops pass: not verified; I did not run `python3 plugin/tests/run.py -k test_literal_for_loops_expand`.
- Loops over `~`, globs, braces, a reassigned variable or a write outside still refuse: partly met. Findings 1 to 3 are loop forms that no longer refuse.
- Real bash agrees: not met for findings 1 and 2. The differential rows evidently don't cover `echo done`, a loop after `&&` or `|`, or IFS.

**Not checked**
- The T-0412 hunks.
- The test files.
- The impact of `_join_continued`.
- Anything outside the loop expansion.
