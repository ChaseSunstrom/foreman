**Verdict: changes needed.** The adversary lens found three plausible regressions, each by code reading only. I could not run anything, so check each with `fm replay --cmd '…'` before acting.

## lens: adversary: changes needed

- HIGH — fmguard.py:2252-2256 — A bytes path is no longer a write candidate. Reproducer: `python3 - <<'EOF'\nopen(b'~/.claude/settings.json','wb').write(b'x')\nEOF`. The old `_QUOTED` scan matched `b'…'`. The new AST branch takes only `str` constants, and `_open_targets` cannot prove bytes, so the coarse rule gets no candidates and the command passes. Fix: also accept `bytes` constants, decoded with `os.fsdecode`, and add a test. Confidence: medium-high.
- HIGH — fmguard.py:2244 (`_python_units` starters, comment at 1756) — The quoted argv on the `python3 - 'PATH' <<'EOF'` line is no longer scanned. The starter line is excluded from `rest`. Reproducer: `python3 - '~/.claude/settings.json' <<'EOF'\nimport sys\nopen(sys.argv[1],'w').write('x')\nEOF`. This was refused before and now passes. The new test's own `$S/a.py` case relies on this path. Fix: add each starter's quoted words to `_quoted_paths`. Confidence: medium-high.
- HIGH — fmguard.py:1278-1281 with `_split` at 1441 — The fd drop turns `;2>f` into `;>f`, and shlex merges `;>` into one token that `_split` does not treat as a redirect. Reproducer: `echo a;2>~/.claude/settings.json`. The target then lands in argv, so the write goes unrecorded. Before the change, `2` stayed a separate word and `>` stayed a redirect. The same applies to `&&2>f`, `|2>f` and `(2>f`. Fix: replace the dropped digits with a space instead of deleting them, and add a test. Confidence: medium.
- LOW — fmguard.py:2247-2250 — `ast.parse` can raise RecursionError or MemoryError on deeply nested code. `fmhooks.py:1992` catches Exception and blocks with exit 2, so this fails closed and is not a bypass. Fix: broaden the except, as `_open_targets` does at line 1814. Confidence: high.
- LOW — fmguard.py:1278-1279 — `isdigit` and `\d` accept Unicode digits, which bash does not read as an fd. The boundary check also ignores `\ ` and `\<newline>`. Fix: use `[0-9]` and `ch in "0123456789"`. Confidence: low.

Candidates that do not regress:
- Concatenation and f-strings were already unprovable, and the old regex missed split literals too.
- A path in a comment is not run, and `exec('...')` string constants are still scanned.
- `{fd}>f`, `&>`, `>&` and here-strings are untouched, because the drop needs digits.
- `>&2>f` is still caught through `>&>`.
- A redirect glued to a quoted word is unchanged.

## Acceptance criteria
- (a) `FdAndLiterals`: met as written, but its negative coverage misses the three HIGH cases above. I could not run it.
- (b) The eight guard suites: not verifiable here.

## Implicit decisions
- Only `str` constants count as paths.
- Starter-line argv words are treated as not holding paths.
- The fd digits are dropped, not replaced by a space.
- The fd drop is judged on the previous character alone.
- An unparsable unit falls back to the old regex scan.

## Not checked
Nothing was executed. I did not trace `test_guard_*` for tests asserting the old behaviour.

Noticed: the comment at fmguard.py:1756 wrongly says `sys.argv` is covered. An unquoted or `$S` argv path used by `open(sys.argv[n])` was already unscanned, a pre-existing hole. Glued `;>f`, `&&>f` and `|>f` redirects have no tests.
