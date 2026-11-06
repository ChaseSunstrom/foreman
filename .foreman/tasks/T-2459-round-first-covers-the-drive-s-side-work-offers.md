---
id: T-2459
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T07:51:40Z
updated: 2026-11-01T08:08:19Z
base: ac25cc03fa8bca4295484dc46d2371c1ff91034d
base_tree: 886f37f5e7695167b0a0c22e07085326eabc5c2e
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-01T07:56:43Z
plan0_scope: []
verified: strong
---
# Round first covers the drive's side-work offers too: while background work runs, the Stop hook offered T-2365 (filed by Foreman) despite fm drive --round-first on
## Raw request
> Round first covers the drive's side-work offers too: while background work runs, the Stop hook offered T-2365 (filed by Foreman) despite fm drive --round-first on
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with fm drive --round-first on, the drive's side-work offer (fmhooks._side_work) skips the inbox items fmcore._round_held holds, as fm next does — verify with `python3 plugin/tests/run.py test_core`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the round filter in _side_work
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core -k test_the_drives_side_work_offer_holds_them_too` → ✗ exit 1 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: RoundFirst 0s) / FAILED (1 classes: test_core.RoundFirst) [ran] [tree dec43f3ad7be] (2026-11-01T07:56:58Z)
- (step 2) `python3 plugin/tests/run.py test_core test_hooks` → exit 0 · Ran 373 tests in 54.4s (57 classes, 16 at a time; slowest: Stop 54s, NoTaskGate 39s, PreToolUse 34s) / OK [ran] [tree 66cd60c3dc4b] (2026-11-01T07:58:02Z)
- (ac 1) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 132 tests in 6.2s (27 classes, 16 at a time; slowest: ConfidenceRoutes 6s, BriefIndex 2s, WritesAndLocks 2s) / OK [ran] [tree 66cd60c3dc4b] (2026-11-01T07:58:09Z)
- `python3 plugin/tests/run.py test_core -k test_the_drives_side_work_offer_holds_them_too` → ✗ exit 1 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: RoundFirst 0s) / FAILED (1 classes: test_core.RoundFirst) (start tree + this task's tests) [ran] [tree 66cd60c3dc4b] (2026-11-01T07:58:12Z)
- `python3 plugin/tests/run.py test_core -k test_the_drives_side_work_offer_holds_them_too` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: RoundFirst 0s) / OK [ran] [tree 66cd60c3dc4b] (2026-11-01T07:58:12Z)
- (ac 1) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 132 tests in 6.0s (27 classes, 16 at a time; slowest: ConfidenceRoutes 6s, BriefIndex 2s, WritesAndLocks 2s) / OK [ran] [tree 562cc897a25b] (2026-11-01T08:07:19Z)
- (audit self) `self: fm check exit 0 (5533 tests); red→green test (the drive's side-work offer named a held Foreman capture; with --round-first on it names none); fm task prove proved; the test_race.py insertion that ran under this task belongs to T-2403 (its scope log names it)` → no findings [tree 562cc897a25b] (2026-11-01T08:07:19Z)
## Log
- 2026-11-01T07:51:40Z created
- 2026-11-01T07:56:42Z focused
- 2026-11-01T07:56:43Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-01T07:58:12Z scope: plugin/lib/fmhooks.py (_side_work) and plugin/tests/test_core.py (the test)
- 2026-11-01T07:58:56Z paused: focus moved to T-2403
- 2026-11-01T08:07:11Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-01T08:07:11Z focused
- 2026-11-01T08:08:16Z done
- 2026-11-01T08:08:19Z committed a5bbf436 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1176 [FIX S, done, 2 steps] Stop drive: (1) offers 'fm lane brief … launch the builder' for RESEARCH and release tasks
- decision 2026-10-29: Keep the drive offering a new side task each Stop even when one was ignored
- T-1899 [FIX S, done, 3 steps] Drive side work skips a task that waits on any open task, not only on the active one: draf — lesson: A wait rule that checks only the activ…
- decision 2026-11-01: [revisited: T-2450 (the secrets finder reads a date as a credential)] [cites: user steer 2026-10-31: finish round 1 completely, in order; no new mai…
- similar finished tasks took 2–3 steps
## Lessons
- A rule enforced in one pick path isn't enforced: every place that chooses the next item needs the same filter
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmhooks.py
- plugin/tests/test_race.py
