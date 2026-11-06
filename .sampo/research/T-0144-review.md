**Verdict:** changes needed. This is one MEDIUM finding in the guard, plus LOW cosmetic gaps in `clean()`. I had no execution tool, so every case below comes from tracing the code. None was run.

## Findings

**1. MEDIUM — `~/.claude/foreman/plugin/lib/fmguard.py:436-448` (`_top_level`). `$'...'` quoting desyncs the quote scan, so a `--run` span inside a real shell string is treated as top level and dropped.** Confidence: medium-high.

- **Why it breaks:** `_top_level` treats every `'` string as raw, with no escapes. In bash `$'\''` is one quoted quote, so the scan closes the string at the `\'` while the shell is still inside it.
- **Input** (the command contains a real newline inside the `$'...'`):

```
ruby -e $'#\'
fm --run "#{system(\"claude plugin install x\")}"'
```

- **What the shell does:** Ruby receives `#'` as a comment, then the line `fm --run "#{system("claude plugin install x")}"`. Ruby evaluates the interpolation before `fm` raises NoMethodError, so claude runs.
- **What `_top_level` does:** the `\'` closes the quote in the scan, so `before` looks top level. The last segment after the newline is `fm `, so `name == "fm"`. `_interp_code` (line 466) removes the span, and `_CLAUDE_IN_CODE` cannot match the remainder.
- **Why nothing else catches it:** `check_bash` line 524 turns the newline into ` ; ` and tokenises with shlex, which also stops at `\'`. The trailing `'` is then unterminated, so `_tokens` falls back to a whitespace split. The `--run` value becomes the fragment `"#{system(\"claude`, which cannot match a claude plugin command.
- **Fix:** in `_top_level`, handle `$'`. When a `'` follows `$`, scan that string as a quote where backslash escapes the next character. Alternatively, make `_interp_code` keep any span if `"$'"` appears in `before`, since the guard is meant to fail closed.
- **Test:** add `test_guard.py` cases for this command and for the `$"..."` variant.

**2. LOW — `~/.claude/foreman/mods/foreman-ui/hooks/kit.ts:274-278` (`clean`). Escape payloads can survive as visible text.** None of these are executable, because every ESC and C1 character is removed.

- `"\u009d0;title\u0007"` leaves `0;title`. `\u009b31m` leaves `31m`. `ESC_SEQ` only matches the 7-bit `ESC [` and `ESC ]` forms, and the control-character strip then removes just the C1 byte.
- `ESC P…ESC \` (DCS), `ESC _…` (APC), `ESC ^` (PM) and `ESC X` (SOS): only the two-byte introducer is removed, so the payload stays.
- `ESC ( B` leaves `(B`.
- Unremoved bidi and invisible marks: U+200E, U+200F, U+061C, U+200B-U+200D. The acceptance criterion says only "bidi overrides", and those are covered. LRM, RLM and ALM can still reorder neighbouring text.
- **Fix:** add `\u009b[0-?]*[ -/]*[@-~]` and `\u009d[^\u0007\u009c]*(?:\u0007|\u009c)?` to `ESC_SEQ`. Make the 7-bit string form `\u001b[PX^_][^\u001b]*(?:\u001b\\)?`. Add `\u200b-\u200f\u061c` to the final strip.

## Acceptance criteria

- **Fake `--run` in a heredoc, in a `-c` body, or as a non-fm argument:** met for the cases covered. Heredoc bodies are read whole, and an argv[0] that is not fm is kept. Finding 1 is a remaining bypass that was not tested for.
- **Heredoc plus `fm task evidence --run "claude plugin test …"` still passes:** not verified. I did not run the tests, but the code path keeps the span out of the interpreter check.
- **Output, command and diff lines drop OSC/CSI/C1 escape sequences and bidi overrides:** mostly met. The escape characters and U+202A-202E and U+2066-2069 are gone. Finding 2 covers the payload residue.

## Not checked

I ran no tests. I did not read the diff file or `test_guard.py`. I did not review the intent, edge, operator or maintainer lenses.
