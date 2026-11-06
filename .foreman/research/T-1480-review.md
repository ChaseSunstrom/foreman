**Verdict: changes needed.** This was a read-only review: I could not run anything, so neither finding has been executed against the guard. Both come from tracing the code paths.

## lens: adversary
- HIGH — plugin/lib/fmguard.py:1045 — `_decode_ansi_c` returns the text unchanged if `<<` appears anywhere in the command, not only when a real heredoc starts. This includes `$((1<<3))`, `echo '<<'` and `1<<2`. An unrelated `<<` therefore turns the whole T-1480 fix off, and the original gap comes back. Example: `echo $((1<<3)); $'cat' ~/.ssh/id_ed25519`. Nothing is decoded, shlex still reads the word as `$cat`, and the credentials classifier never sees `cat`. A real heredoc earlier in the command does the same. Fix: decode only outside heredoc bodies. Use `_heredoc_starts` (which already ignores quoted markers) and `_ends_body`, as `_strip_heredocs` does, to find the body lines, and decode every other line. Add a test for `$((1<<3))` followed by `$'cat' ~/.ssh/id_ed25519`, and one for a command line after a closed heredoc. Confidence: high.
- MEDIUM — plugin/lib/fmguard.py:1054-1055 — The decoder tracks quotes with a flat scan, but bash opens a new quoting context inside each `$( )` and backtick. `_inner_quote` (line 625) exists for exactly this, and the heredoc code uses it. Nested quotes inside a double-quoted `$( )` make the scan think a later `$'…'` is quoted, so it is left undecoded. Shape: `echo "$(echo ")")" ; $'cat' ~/.ssh/id_ed25519`. Bash closes the string after `)")`, so the `cat` runs. The flat scan sees an unclosed `"`, skips the `$'cat'`, and the old gap applies. Fix: decide quoting at each `$'` candidate with `_inner_quote(text[:i]) is None`, which is quadratic but the input is short. Alternatively fail closed: if a `$'` outside heredoc bodies survives decoding while `_inner_quote` says it is unquoted, add a refusal. Confidence: medium, unrun.
- LOW — plugin/lib/fmguard.py:1030, 1033 — The decoded bytes are not bash's. `\xc3\xa9` becomes two Latin-1 characters instead of one UTF-8 character, and `\c?` gives 0x1f where bash gives 0x7f. Neither can hide an ASCII command name, so this is cosmetic. Fix: leave it, or add a comment.

## lens: edge
- No other defects found in the decoder. I checked these against the code, all consistent with bash:
  - Escapes: `\x` with one digit, octal above 377 (masked), NUL truncation, an unknown escape keeping its backslash, `\'` becoming `'\''`, and `$$'x'`.
  - Quoting: `$'…'` inside double quotes left alone, and the comment rule matching `_strip_comments`.
- In `check_bash`, `val` is reset every loop iteration at line 2825, so the `val` reassignment at line 2802 cannot leak into the chain.
- The chain now holds the resolved value, which only adds fetcher and `env` detections.

## Acceptance criteria
- Criterion 1 (the 8 variants refused and moved to the corpus; BASH_ENV dropped from the generator): not verifiable here. The code paths and the test inputs line up, and `gen_evasions.py:111` does skip BASH_ENV. The first finding shows these only hold when the command has no `<<`.
- Criterion 2 (decoding as bash does; same-line literal assignment resolves `$NAME`): met for the escapes listed above. It is not met for `<<` anywhere in the command or for nested `$( )` quoting, per the two findings. The `test_guard_pipes.py` row change is correct: `$'\''` is a `'` word, so `'IFS=m $IFS'` is plain data.

## Implicit decisions
- Decoding happens in `check_bash` once per recursion level, so nested bodies are decoded again.
- An unclosed `$'` leaves the rest of the text untouched.
- The `$NAME` resolution reads `{**lits, **known}`, so a name set once on the line to a literal counts.
- A command that has a heredoc gets no decoding at all.

## Not checked
- I ran no tests, so I did not confirm that the regenerated corpus and gap files are consistent.
- I did not review the remaining `gen_evasions.py` changes or the other fixtures.

**Noticed:** `_strip_comments` (fmguard.py:983) returns early on any `$'`. After this change that branch is reachable only through the heredoc skip, so the fail-closed comment only covers the case that finding 1 should remove. Revisit it once the heredoc handling is fixed.
