All three reviews are below. Only fmhooks, fmcore, fmcli, fmplugins and fmevolve were read. I did not run the tests or the PreToolUse hook.

## adversary + edge: changes needed

**MEDIUM** — `plugin/lib/fmcli.py:1621`, `plugin/lib/fmplugins.py:254-257`, `plugin/lib/fmevolve.py:61-72`
- `c.routing()` (`plugin/lib/fmcore.py:100`) only checks that the top level is an object. `check_revision` only compares top-level key sets. Neither checks the types of the values.
- Trigger: a revision like `{"stage_words":{},"ui_words":[],"builtin_skills":{},"review_groups":5}` passes `check_revision`. `tuple(g) for g in 5` then raises `TypeError` when `fmcli` is imported, so every `fm` command fails.
- A string such as `"FIX":"debug"` becomes `tuple("debug")`, which is single characters. Those match almost any skill text, so the hints become noise.
- This contradicts the docstring's "a bad file costs hints, never work". A hand edit hits the same path.
- Fix: validate shapes inside `routing()` (dict of lists of str, list of lists of str) and return `{}` otherwise. Make `check_revision` call the same validator.

**MEDIUM** — `plugin/lib/fmcore.py:113`
- `_VETO` uses `.search`, so only the first clause is kept, and it consumes the rest of the sentence.
- "I don't think so, never push without asking" records `think, never, push`. `git push` then never carries "think", so the note is missed.
- Fix: use `finditer`, or split the text into clauses first.

**MEDIUM** — `plugin/lib/fmcore.py:113`, with the gate at `plugin/lib/fmhooks.py:383`
- `don'?t` does not match the curly apostrophe in "don’t".
- "No, don’t push" passes `_CORRECTION` through `no\b,` but records no veto. Smart quotes are common from phone keyboards.
- Fix: `don['’]?t`, in both regexes.

**LOW** — `plugin/lib/fmcore.py:136`, `plugin/lib/fmcore.py:148`
- Matching on 3 key words with a prefix match is crude. "Don't forget to run tests" yields `forget run tests`, which matches only `run`+`tests` commands. "never commit without tests" matches `git commit -m "add tests"` or any heredoc body. It is a note, not a block, so the cost is small.
- Vetoes are project-wide and have no expiry or removal command (nothing outside fmcore, fmwatch and the tests references `vetoes`). A one-off "stop doing X" nags indefinitely, until it is among the newest 30.

**LOW** — `plugin/lib/fmhooks.py:760`
- `_veto_note` runs inside the same `try` as the scope and tripwire notes, so an exception in it drops all three notes. This is fail-safe, because nothing blocks.
- `veto_hits` scans every command word once per veto, up to 30 vetoes. A very large Bash heredoc could cost a few tenths of a second per call. That is an estimate, not measured.
- `vetoes()` accepts `words: []`, and `all([])` then matches every call. Only a hand-edited file produces this.
- Fix: filter empty `words` in `vetoes()`.

**LOW** — `plugin/lib/fmcore.py:139`
- `add_veto` does an unlocked read-modify-write. Two sessions at once can lose a veto.

## intent + operator: approve with nits

- T-0251 is met. `_CORRECTION` gates it (`plugin/lib/fmhooks.py:405`) and the note is built before the other notes (`plugin/lib/fmhooks.py:760`). The note quotes the user's saved words (`said`), which is the whole prompt up to 200 characters rather than the matched clause.
- **Prompt injection (LOW)**: `said` goes through `plain()` but not `defang()`, and the note does not escape `"`. The text is the user's own prompt, so the vector is only pasted content after a leading "never" or "don't". The risk is low.
- T-0252 is met, and I checked what reads each table:
  - `stage_words`, `ui_words` and `builtin_skills` are read only in `stage_skills` (`plugin/lib/fmplugins.py:305-315`). They affect hint text only, and the call is wrapped in try/except (`plugin/lib/fmcore.py:1836`).
  - `builtin_skills` strings are printed unsanitised into the injected "Next:" hint (LOW). A revision from evolve could carry text there, though merging stays the user's call.
  - `review_groups` is read in `plugin/lib/fmcli.py:1693`. A lens in no group goes to an extra reviewer, so no lens is dropped. An evolved file could still weaken review rigor by regrouping lenses, and that goes beyond hints.
- Operator: `check_frontmatter` skips non-directories, so `routing.json` does not trip doctor. Doctor does not validate `routing.json` itself. No install or setup change is needed.
- Docs: the CHANGELOG and MASTER edits to the `fm export agents` line (sensitive projects, symlinks) have no code in this diff. The code is already present in `plugin/lib/fmcost.py:375` and `:423`, so the docs match.

## maintainer: approve with nits

- The pre-audit items need no edit. `fmhooks.py` is covered through `hook()` in `test_steering.py`. `fmplugins.py` is covered by the equality test.
- The `Routing` test compares the readers to the file they read, so it only proves the wiring. No test covers `add_veto` dedupe or the cap of 30, the curly-quote case, or a wrong-typed `routing.json`. The wrong-typed case is the MEDIUM above. No test covers `--drop` writing `{}\n` for a `.json` target (`plugin/lib/fmevolve.py:123`).
- `_EDIT_VERBS` is a string constant, and `VETOES_KEEP` follows existing naming. No duplicated helper found.

## Not checked
Test execution, the TSX pane rendering, whether the guard blocks agent writes to `vetoes.json`, and the hook import paths at `plugin/lib/fmhooks.py:639` and `:873`.
