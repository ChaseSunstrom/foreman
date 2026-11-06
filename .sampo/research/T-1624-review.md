**Verdict:** approve with nits. I couldn't run anything (no Bash in this session), so every finding below comes from reading the code. No finding is a security hole. Fix the two MEDIUM ones before T-1625 builds on the resolved tokens.

## lens: edge / maintainer / adversary
- MEDIUM — plugin/lib/fmmotion.py:122-128 — `tokens_of` reads column positions from the first header row only. A hand-written Tokens section with a second table (`| Token | Value |` after the extract-style table) has every row skipped, because `len(cells) <= max(cols)`. A header with no Light/Value column silently defaults to column 2. The user then sees "DESIGN.md has no token '--dur-x'" for a token that is plainly there. Repro: an extract table followed by `| Token | Value |` / `|--|--|` / `| --dur-x | 200ms |`. Fix: treat a row followed by a separator row as a header and re-read the columns each time; say so when no Light/Value column is found. Also match `## Tokens` case-insensitively. Confidence: high.
- MEDIUM — plugin/lib/fmdesign.py:1098,1124 with plugin/lib/fmmotion.py:179 — `_cell` cuts a value at 60 characters and appends "…". A valid long easing, such as a `linear(...)` spring or a 9-decimal `cubic-bezier`, comes back as "easing token --x is 'linear(0, …' in DESIGN.md, not an easing". Nothing says it was truncated. Fix: use `_cell(v, 200)` for the Light/Dark columns, and make `_duration`/`_easing` say "truncated by fm design extract" when the value ends in "…". Confidence: high.
- MEDIUM — plugin/lib/fmmotion.py:150-166 — a bare number is milliseconds, so `duration = 0.3` passes as 0.3 ms with no warning. The string forms `"220"` and `"-5ms"` fall through to "DESIGN.md has no token" (or the no-DESIGN.md text), which points at the wrong cause. Fix: flag a bare number between 0 and 10 ms with "bare numbers are ms; write '0.3s'", and give unit-less or negative strings their own message. Confidence: high.
- LOW — fmmotion.py:158,179 — `{v}` is printed unquoted. A DESIGN.md token name containing ESC, with a score that names it, puts the escape sequence on the terminal. Fix: use `_show(v)`.
- LOW — fmmotion.py:85 — `PROP` rejects `-webkit-backdrop-filter`, a real animatable property. Fix: `(?:--|-[a-z]+-)?`.
- LOW — fmmotion.py:273-277 — only `ValueError` is caught. Any other exception (a `RecursionError` from `repr` on a deeply nested JSON value is plausible) exits 1 with a traceback, the same code as "problems". This is a lead; I didn't reproduce it. Fix: also catch `RecursionError` and exit 2.
- LOW — plugin/tests/test_motion_score.py — nothing covers a hand-written Value table, a second table, a truncated token, a FIFO, non-UTF-8 input, an oversize file or ESC in output.

## Your questions
- **Reduced meanings:** right and standard. They match motion.md:150-157 ("no travel, not no change"): fade means opacity only, instant means jump to the end state, and none means dropped. One gap: `none` and `instant` compile the same for a state change, and differ only for loops or decorative keyframes. The schema has no loop/trigger field. State at fmmotion.py:66 that `none` means "rest state, never plays" so T-1625 can't diverge.
- **Easing:** accept `steps(n[, jump-term])` and `linear(...)`. `step-start` and `step-end` are already accepted, so rejecting `steps()` is inconsistent, and WAAPI takes both. Use bounded regexes. Make keywords case-insensitive and strip whitespace, since `" ease"` and `EASE-IN` are rejected today. The three.js compiler must map or warn.
- **Hostile files:** handled well. `_read` caps at 1 MB, refuses non-regular files and non-UTF-8, and doesn't block on a FIFO. `RecursionError` is caught in `parse`, and `repr` escapes control characters. The one gap is the unquoted `{v}` above.
- **Exit codes:** 0, 1 and 2 match `fm design contrast`. The one caveat is the uncaught-exception case above.
- **Designer ergonomics, one improvement:** accept `[motion.menu-enter]` as well as `[[motion]]` with a `name` line. It's less typing and TOML itself rejects duplicate names. The test at line 398 already shows designers write it.

## Acceptance criteria
- A motion with no reduced form fails naming it: met by reading, not run. `test_a_motion_without_a_reduced_form_fails_naming_it` (line 364) asserts the motion's name appears. The exit code is covered only in `Cli`, which the verify command doesn't run.

## Implicit decisions
- The Light column of the Tokens table is the only one used; Dark is ignored.
- The first table row for a token name wins.
- A bare number is milliseconds.
- A missing default `motion.toml` exits 2.
- Names accept Unicode `\w`, though the message says "letters".
- The 2000 ms cap is hard-coded.

## Not checked
I didn't run the tests, the parser's `lazy`/tier wiring, or `--json` handling.

**Noticed:** none
