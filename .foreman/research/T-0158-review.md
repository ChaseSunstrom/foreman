**Verdict: changes needed.** I found four verified bypasses and one regression. I could not run code here (read-only), so every trace is by hand against `fmguard.py`, `_tokens` (299-306) and `_split` (309-340).

**Findings**

1. **HIGH (regression)** — `fmguard.py:445-446` — the `$'` fallback anchors on the first `$(`, even one inside single quotes.
   - Input: `echo '$(' $'x' "$(rm -rf ~)"`
   - New code: `"$'" in text` takes the fallback. The greedy match starts at the `$(` inside `'$('` and returns the body `' $'x' "$(rm -rf ~`.
   - `check_bash` on that body hits the fallback again and finds no `)`. `shlex` raises on the unbalanced quote, so the whitespace-split fallback gives tokens `'`, `$'x'`, `"$(rm`, `-rf`, `~`. No token is named `rm`.
   - Top level: `_tokens` yields `echo`, `$(`, `$x`, and `$(rm -rf ~)` as a single token, so the command name is `echo`.
   - Old code: the removed per-token loop matched `\$\(([^()]*)\)` on that `$(rm -rf ~)` token and checked `rm -rf ~`. It is now caught by nothing.
   - Fix: in the fallback, return a body for every `$(` occurrence (`text[m.end():]` or up to the last `)`). That also covers the `$'` case with stray `$(`.

2. **HIGH** — `fmguard.py:609`, `_heredocs` at 280-292 — unquoted heredoc bodies run `$(…)` and backticks but are dropped.
   - Input: `cat <<EOF\n$(rm -rf ~)\nEOF`
   - `check_bash` uses `_strip_heredocs`, so `_subst_bodies` never sees the body. `_interpreter_writes` returns `[]` because there is no interpreter.
   - Fix: have `_heredocs` also report whether the delimiter was unquoted (group 1 of `_HEREDOC_START` is empty). Pass those bodies through the fail-closed backtick and `$(` extraction.
   - Same behaviour before the change, but heredocs were named in the brief.

3. **HIGH** — `fmguard.py:466-478` — a `)` in a `case` pattern ends the body early inside double quotes.
   - Input: `echo "$(case a in a) rm -rf ~;; esac)"`
   - The scanner closes the body at `a)` and returns only `case a in a`. The remainder is in `ctx[0]` with the `"` quote open, so `shlex` treats it as one string and `rm` is never a command.
   - The same early close happens with a `)` inside a `#` comment: `"$(true # )\nrm -rf ~\n)"`.
   - The unquoted form is still caught, because the tail is tokenized at top level.
   - Same behaviour before the change.
   - Fix: after any pop, fail closed. For example, also return `text[start:]` to the end for every `$(`, or reject a body whose text contains `esac`, `case` or `#`.

4. **HIGH** — `fmguard.py:479` — `$((` followed by a subshell is skipped as arithmetic.
   - Input: `echo "$((rm -rf ~); echo)"`
   - Bash falls back from arithmetic to command substitution when there is no matching `))`. Line 462 skips every `$((`, so nothing is extracted. The quoted text is one token to `shlex`.
   - The old regex `[^()]*` missed it too.
   - Fix: treat `$((` as a substitution when its `))` does not close, or just add the text after each `$((` to the returned bodies.

5. **MEDIUM** — `fmguard.py:450-452, 456-459` — nested backticks written as `` \` `` are never unescaped.
   - Input: ``echo `echo \`rm -rf ~\` ` ``
   - The body is `` echo \`rm -rf ~\` ``. In the recursive call the escaped backticks are not substitutions, and `_tokens` yields `` `rm ``, so `rm` is never the command.
   - Same behaviour before the change.
   - Fix: when extracting a backtick body, replace `` \` ``, `\$` and `\\` with their unescaped characters, as bash does.

Checked and fine: `${v:-$(cmd)}`, `$[$(cmd)]`, `<(…)` and `>(…)`, here-strings, a `$(` inside double quotes with a `'` in it, and the unterminated-body tail (all fail closed or are caught).

**Acceptance criteria:** no explicit list in the brief. Reading it as "one reader for substitutions (nested, quoted, backticks) with no cases dropped", the first part is met for the new tests, and the no-drop part is not met (finding 1).

**Not checked:** I ran no tests. I did not review `_check_rm` or the other `check_bash` callers, or `fmhooks`.
