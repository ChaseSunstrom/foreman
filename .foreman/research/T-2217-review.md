Verdict: changes needed (3 MEDIUM, 6 LOW, no HIGH); fixed or accepted with reason. Reviewer: one foreman:fm-reviewer, six lenses, read-only.

## lens: intent
- MEDIUM — the oracle turned each regex into a note by splitting on | and stripping backslashes, so `\bcache\b`, a class or a group made a note that misses its own regex; fm exam check doesn't grade the oracle, so the scenario passed check while the oracle couldn't close it. FIXED: the child writes an example answer that must match every regex; the oracle says it. Test: the stub's readings now use \b and a group.
- MEDIUM (plausible) — a child vague request was decoupled from the template's slow plant it must close. FIXED: the vague prompt tells the child one helper is slow on big inputs and asks for what a user who felt that would say.
- LOW — 2-3 readings asked, all required by the grade. FIXED: exactly 2.
- LOW — `says` required but unused for ASKS. FIXED: not asked, not required.

## lens: adversary
- MEDIUM — `_guard` accepted broad regexes (`e`, `\.`, a function name) that any answer would match. FIXED: a regex that matches the module, its tests, its README or a filler answer is refused. Tests: a broad reading and a broad missing regex are dropped.
- LOW — OverflowError at compile escaped. FIXED: caught with re.error and RecursionError.
- LOW — `?` not counted among repeats. FIXED: counted (group syntax excluded).

## lens: edge
- LOW — stale scorecard docstring. FIXED.

## lens: maintainer
- LOW — in-process scorecard calls run with CHILD_KINDS patched, the CLI half unpatched. FIXED (said): comments name why (a kind T-2216 adds reads so before its child shape) and the CLI assertions check the real table.
- LOW — no tests for the guard branches. FIXED: table-driven drops for empty-match, repeated group, wrong count, duplicates, broad, missing example.

Noticed: one scenario of a kind is enough for it to count as graded (a per-kind minimum would be stricter); earlier nits on newest() and the dep check stay open.
