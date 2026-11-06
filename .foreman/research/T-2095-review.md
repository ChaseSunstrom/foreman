**Verdict:** approve with nits. It meets the criteria as written. One resumability gap and one silent-skip case are worth fixing. I did not run `plugin/tests/run.py test_genesis`; this is a read-only review of the code.

## lens: intent
- MEDIUM — `plugin/lib/fmgenesis.py:122-124` — "Resumable after any kill" is not true across `fm intake`. Intake creates the briefs, and the mission file's `Task:` line is the only record of them. After a kill between `fm intake` and the `put`, step still says "0 of N briefs intaken → fm intake". `cmd_intake` (`fmcli.py:186-199`) has no dedupe, so the rerun creates duplicate briefs. The test only proves `step()` is idempotent on a fixed tree. Fix: have the intake action say "put the Task: line first, then intake", or have step match the open briefs' `Mission:` or title against the intake block before saying "intake". Confidence: plausible. I traced the code path but did not run it.
- MEDIUM — `plugin/lib/fmgenesis.py:101-102,137` — An unparseable Missions table reads as a dry generation. `ROW` (line 81) needs a bare `mission-x.md` cell and 5 columns, so a backticked file name or a 4-column table gives `rows == []`. Step then skips every Mission and asks for select, drift and sweep. After two such generations it declares the final report, and `_next_for` goes quiet once `report.md` exists. Repro: put `| 1 | \`mission-a.md\` | #1 | g (3) | — |` in `gen-1/seed.md`, and step says `select`. Fix: if the seed text matches `mission-[a-z0-9-]+\.md` but `ROW` finds nothing, return `fatal` ("table rows don't parse"). Confidence: confirmed by reading the regex.

## lens: adversary
No findings. `put` and `SHAPE` still whitelist names, and `esc()` guards the new `genesis.js` line. `step` only reads files.

## lens: edge
- LOW — `plugin/lib/fmcore.py:3460-3465` — `step()` runs on the hot `fm next` path (every prompt and Stop) with no `try/except`. Any exception from `step()` would break `fm next` for a project that has a tower. Callers such as `fmhooks.py:1293` catch it, but `fm next` itself doesn't. Fix: wrap it as `fmfriction.due` is wrapped just above, and fall through to the old idle text.
- LOW — `plugin/lib/fmgenesis.py:121` — `INTAKE` counts every line starting with `FIX:` or `FEATURE:` in a mission doc. Mission docs are prompts, so a prose example line would raise `want` and stick the mission at "intake". Fix: count only inside the first fenced block.

## lens: operator
- LOW — `plugin/lib/fmcore.py:3460-3470` — An open tower now ranks above the forever loop's action and above "queue is empty: FINAL VERIFY and REFLECT". It stays there until `report.md` exists, so a dormant tower hides both. Nothing in the task recorded this as intended. Fix: put one line in the CHANGELOG, or sort Genesis after `fmloop`.
- LOW — `plugin/lib/fmgenesis.py:113` — Every empty-queue prompt does `load_briefs(include_archive=True)` once a mission has any `Task:` id. That is about 2100 briefs against the index. The brief recorded no timing. Fix: measure it, or use the already-loaded `briefs` and fall back to the archive only for ids not found.

## lens: maintainer
- LOW — `plugin/tests/test_genesis.py:312` — The comment says "a fifth level", but `gen-1/deeper/seed.md` is the third. The 4-level cap is the pre-existing `SHAPE`, and `step` doesn't enforce it. Fix: reword the comment, or use `gen-1/a/b/seed.md`.
- LOW — `plugin/tests/test_genesis.py:215` — No test covers a kill between steps with partial state, such as a mission doc written but its intake not yet recorded. See the first intent finding.

## Acceptance criteria
- Next action per stage from the files alone: met. `step` is read-only, and the tests walk every stage.
- A kill after every stage resumes to the same action: met for `step` called twice on the same files. Not met across the `fm intake` window (see above).
- Caps (8 rows, 4 levels) and the lock hold: met. `step` returns `fatal` over 8 rows, `SHAPE` stops deeper paths, and `put` still takes `c.lock`.
- `fm next` names it while a tower is open: met, at `fmcore.py:3460`.

## Implicit decisions
- The `Task:` line in a mission doc is the only link between a mission and its briefs.
- An unparseable table counts as "no rows".
- Genesis ranks above the loop and the idle text in `fm next`.
- `fm genesis step` exits 1 only for `fatal`, and `blocked` exits 0.
- `drift.md` and `sweep.md` are now tower doc names.

## Not checked
- The rendering of `site/genesis/genesis.js` (no screenshots listed).
- The MASTER.md hunk, which was left out of the diff.
- A test run.

**Noticed:** `fm genesis step`'s intake command doesn't say where the intake text comes from (stdin or file).
