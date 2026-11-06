---
id: T-1275
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T14:56:40Z
updated: 2026-10-20T17:02:30Z
base: 45b4388c5385e1ac06715e0eb43f8130956908e4
base_tree: 878bb31325673445a6fdd3a610f5c463385e60a4
plan0_at: 2026-10-20T16:55:53Z
plan0_scope: []
verified: strong
---
# Ambient test note: the failing tests' names instead of the runner's timing line, under 220 characters
## Raw request
> Ambient test lines ('Ambient tests: ✗ the affected tests now fail … Ran 44 tests in 1.6s (12 classes …)') were 23 KB over 92 edits: drop the runner's timing and class list, and say a still-failing state once until it changes
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a failing ambient run's note names up to three failing tests and the command in at most 220 characters, without the runner's timing or class counts; a pass note fits 200 — verify with `python3 plugin/tests/run.py test_ambient`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: the note for a run with two FAIL lines names both and fits 220 characters
2. [x] Build the note from the FAIL/ERROR lines in fmambient._record, measurements, changelog
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_ambient 2>&1 | tail -12` → exit 0 · Ran 4 tests in 11.1s (1 classes, 16 at a time; slowest: Ambient 11s) / OK [ran] [tree c96b5dcbf8bf] (2026-10-20T16:56:40Z)
- (step 1) `python3 plugin/tests/run.py test_ambient 2>&1 | tail -12` → exit 0 · Ran 4 tests in 11.1s (1 classes, 16 at a time; slowest: Ambient 11s) / OK [ran] [tree c96b5dcbf8bf] (2026-10-20T16:56:40Z)
- (step 1) `python3 plugin/tests/run.py test_ambient` → exit 0 · Ran 4 tests in 4.5s (1 classes, 16 at a time; slowest: Ambient 4s) / OK [ran] [tree c96b5dcbf8bf] (2026-10-20T16:56:47Z)
- (ac 1) `python3 plugin/tests/run.py test_ambient` → exit 0 · Ran 4 tests in 6.7s (1 classes, 16 at a time; slowest: Ambient 7s) / OK [ran] [tree 7632e5583371] (2026-10-20T17:01:28Z)
- (step 2) `python3 plugin/tests/run.py test_ambient` → exit 0 · Ran 4 tests in 6.7s (1 classes, 16 at a time; slowest: Ambient 7s) / OK [ran] [tree 7632e5583371] (2026-10-20T17:01:28Z)
- (audit intent) `main session read the builder's diff; restored the 'When step N is done' wording (T-0994: a pass is no proof the step is done), fixed spacing, added the pytest-pattern check; criteria re-run after the merge` → the note now tells the model which tests broke, the one thing it acts on, in half the space [tree 7632e5583371] (2026-10-20T17:01:28Z)
- (audit edge) `main session read the builder's diff; restored the 'When step N is done' wording (T-0994: a pass is no proof the step is done), fixed spacing, added the pytest-pattern check; criteria re-run after the merge` → no FAIL or FAILED lines (jest, go) gives the exit code; names are de-duplicated, three at most, 50 characters each; output is redacted before it's read; the pass hint keeps T-0994's caution [tree 7632e5583371] (2026-10-20T17:01:28Z)
- (audit self) `main session read the builder's diff; restored the 'When step N is done' wording (T-0994: a pass is no proof the step is done), fixed spacing, added the pytest-pattern check; criteria re-run after the merge` → no findings [tree 7632e5583371] (2026-10-20T17:01:28Z)
## Log
- 2026-10-20T14:56:40Z created
- 2026-10-20T16:53:51Z planned from capture
- 2026-10-20T16:55:37Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1275.builder.md
- 2026-10-20T16:55:53Z focused
- 2026-10-20T16:58:31Z merged worktree-agent-a063fa55c1889d4e6 (2 file(s))
- 2026-10-20T16:58:32Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a063fa55c1889d4e6
- 2026-10-20T17:01:06Z focused
- 2026-10-20T17:02:29Z done
- 2026-10-20T17:02:30Z committed a127187d (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0978-small-models: Measured, not guessed. Sources: two recorded Sonnet demo sessions (T-0979; T-0983/T-0984 were written by them), one [stale: plugin/tests/ru…
- T-0994 [FIX M, done, 3 steps] Ambient runs close only the step whose own verify ran; unmappable files get no ambient evidence (T-0994) — lesson: Automatic evidence must …
- T-0705 [FEATURE M, done, 4 steps] Frontier 05 — Ambient verification and test intelligence — lesson: Background verification has to answer the revert case: selection by …
- decision 2026-10-04: Drop T-0305 (edit a criterion in place)
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–4 steps
## Measurements
Failing ambient note: up to ~460 characters (names, command up to 160, the runner's result line up to 300) → at most 220, from the code and test_ambient; pass note: names plus a hint with the command up to 160 → at most 200. In the measured long session these notes came to 23 KB over 92 edits (about 250 each).
## Lessons
- When cutting a note, check that the shorter wording keeps the caveat an earlier fix put there: 'Step N done' read as a claim the old 'When step N is done' avoided
## Files touched
- plugin/tests/test_ambient.py
- plugin/lib/fmambient.py
- CHANGELOG.md
