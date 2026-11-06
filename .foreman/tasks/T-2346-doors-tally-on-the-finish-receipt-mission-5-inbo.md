---
id: T-2346
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T13:59:18Z
updated: 2026-11-01T07:41:53Z
group: Mission 5 inbox items
base: 1fe52aa93d711fc1302b730e2dd4d2f4a02e0ce6
base_tree: a10d2530d2ac4b4ab687375e7f75efdc37033e40
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-01T07:29:17Z
plan0_scope: []
verified: strong
---
# Doors tally on the finish receipt: one line naming each one-way step and how it was undone or parked
## Raw request
> Doors tally on the finish receipt (Mission 5 inbox, tier 2): fm task finish prints one line, one-way steps passed and how each was undone or parked
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task finish prints 'Doors: N one-way step(s): step K undone (its restore) | parked' when the plan had a local one-way step, and nothing when it had none — verify with `python3 plugin/tests/run.py test_judgment`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] fmdoors.tally and the receipt line
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_judgment -k test_the_finish_receipt_tallies` → ✗ exit 1 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: DoorPark 1s) / FAILED (1 classes: test_judgment.DoorPark) [ran] [tree e92a2ca8e8de] (2026-11-01T07:29:35Z)
- (step 2) `python3 plugin/tests/run.py test_judgment` → exit 0 · Ran 55 tests in 14.5s (15 classes, 16 at a time; slowest: DoorPark 14s, DoorGate 7s, Followups 5s) / OK [ran] [tree f1b75f9b6eff] (2026-11-01T07:30:11Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment` → exit 0 · Ran 55 tests in 14.5s (15 classes, 16 at a time; slowest: DoorPark 14s, DoorGate 7s, Followups 5s) / OK [ran] [tree 4f048e37fae8] (2026-11-01T07:30:54Z)
- `python3 plugin/tests/run.py test_judgment -k test_the_finish_receipt_tallies` → ✗ exit 1 · Ran 1 tests in 3.1s (1 classes, 16 at a time; slowest: DoorPark 1s) / FAILED (1 classes: test_judgment.DoorPark) (start tree + this task's tests) [ran] [tree 4f048e37fae8] (2026-11-01T07:33:38Z)
- `python3 plugin/tests/run.py test_judgment -k test_the_finish_receipt_tallies` → exit 0 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: DoorPark 1s) / OK [ran] [tree 4f048e37fae8] (2026-11-01T07:33:38Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment` → exit 0 · Ran 55 tests in 8.0s (15 classes, 16 at a time; slowest: DoorPark 8s, DoorGate 4s, Followups 3s) / OK [ran] [tree 4f048e37fae8] (2026-11-01T07:40:28Z)
- (audit self) `self: fm check exit 0 (5529 tests); red→green test (a snapshotted step reads 'undone (cp -a …)', a plan without one-way steps prints nothing, a marked step with no way back reads 'parked'); fm task prove proved` → no findings [tree 4f048e37fae8] (2026-11-01T07:40:28Z)
## Log
- 2026-10-31T13:59:18Z created
- 2026-11-01T07:29:15Z planned from capture
- 2026-11-01T07:29:16Z focused
- 2026-11-01T07:29:17Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-01T07:30:54Z scope: plugin/lib/fmdoors.py (tally) and plugin/lib/fmcli.py (the receipt line), plugin/tests/test_judgment.py (the test), MASTER.md and CHANGELOG.md (docs)
- 2026-11-01T07:41:50Z done
- 2026-11-01T07:41:53Z committed 7eeb4b35 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2342 [FEATURE M, done, 4 steps] Stop only at an irreversible, ambiguous step (Mission 5, #8): plan steps are classified one-way or two-way by the guard's own command p…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- T-0854 [FIX M, done, 5 steps] A newcomer's first fm commands make sense: short --help, task new shows its values and an example, init/status say what… — lesson: The firs…
- decision 2026-10-31: [costly] Parked T-2357 at a one-way, ambiguous step: red tests: staging writes nothing outside state; guard category; install after the yes; uninsta…
## Lessons
- A receipt line that only prints when there's something to say keeps the receipt short for the common case
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_judgment.py
- plugin/lib/fmdoors.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
