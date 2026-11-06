---
id: T-2345
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T13:59:18Z
updated: 2026-11-01T07:56:37Z
group: Mission 5 inbox items
base: 01de3ebc0fbba93e42a07fc1bfa39cf646cb0089
base_tree: 4f048e37fae8800a6a589bd89e40cd81bab8894a
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-01T07:44:26Z
plan0_scope: []
verified: strong
---
# Finish receipt groups assumptions by how they were checked: ran, read, typed or never
## Raw request
> Plan lint (Mission 5 inbox, tier 1): certainty words in a plan (certainly, obviously, guaranteed) with no command or file beside them are listed by fm task check as advisory
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task finish prints 'Assumptions: N ran, N read, N typed, N never checked' when the brief has assumptions (ran: verified with --run; read: --from a source; typed: --evidence; never: still [assumed]), and nothing when it has none — verify with `python3 plugin/tests/run.py test_judgment`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the grouping in the receipt
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_judgment -k test_the_finish_receipt_groups_assumptions` → ✗ exit 1 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: AssumptionReceipt 1s) / FAILED (1 classes: test_judgment.AssumptionReceipt) [ran] [tree 8d01bd4a7216] (2026-11-01T07:44:31Z)
- (step 2) `python3 plugin/tests/run.py test_judgment` → exit 0 · Ran 56 tests in 12.5s (16 classes, 16 at a time; slowest: DoorPark 12s, DoorGate 7s, Followups 5s) / OK [ran] [tree ccd1264b78a0] (2026-11-01T07:44:59Z)
- (step 2) `python3 plugin/tests/run.py test_judgment test_docs` → exit 0 · Ran 158 tests in 8.9s (39 classes, 16 at a time; slowest: DoorPark 9s, Fences 8s, DoorGate 4s) / OK [ran] [tree 0dacdea25ef4] (2026-11-01T07:45:42Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment` → exit 0 · Ran 56 tests in 9.8s (16 classes, 16 at a time; slowest: DoorPark 10s, DoorGate 4s, Followups 3s) / OK [ran] [tree 0dacdea25ef4] (2026-11-01T07:45:52Z)
- `python3 plugin/tests/run.py test_judgment -k test_the_finish_receipt_groups_assumptions` → ✗ exit 1 · Ran 1 tests in 3.6s (1 classes, 16 at a time; slowest: AssumptionReceipt 2s) / FAILED (1 classes: test_judgment.AssumptionReceipt) (start tree + this task's tests) [ran] [tree 0dacdea25ef4] (2026-11-01T07:45:59Z)
- `python3 plugin/tests/run.py test_judgment -k test_the_finish_receipt_groups_assumptions` → exit 0 · Ran 1 tests in 2.3s (1 classes, 16 at a time; slowest: AssumptionReceipt 2s) / OK [ran] [tree 0dacdea25ef4] (2026-11-01T07:45:59Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment` → exit 0 · Ran 56 tests in 8.1s (16 classes, 16 at a time; slowest: DoorPark 8s, DoorGate 4s, Followups 3s) / OK [ran] [tree 224e20c13dfe] (2026-11-01T07:55:58Z)
- (audit self) `self: fm check exit 0 (5531 tests); red→green test (1 ran, 1 typed, 1 proved false, 2 never checked; none when the brief has no assumptions); fm task prove proved; the JSON carries assumptions apart from doors` → no findings [tree 224e20c13dfe] (2026-11-01T07:55:58Z)
## Log
- 2026-10-31T13:59:18Z created
- 2026-10-31T14:07:15Z set title=Finish receipt groups assumptions by how they were checked (Mission 5 inbox, tier 2): ran, typed or never, so an unchecked one shows at close
- 2026-11-01T07:31:38Z planned from capture
- 2026-11-01T07:44:25Z focused
- 2026-11-01T07:44:26Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-01T07:45:59Z scope: plugin/lib/fmcli.py (_assumption_tally and the receipt line), plugin/tests/test_judgment.py (the test), MASTER.md and CHANGELOG.md (docs)
- 2026-11-01T07:46:57Z paused: focus moved to T-2348
- 2026-11-01T07:55:48Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-01T07:55:48Z focused
- 2026-11-01T07:56:35Z done
- 2026-11-01T07:56:37Z committed ac25cc03 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
- T-2346 [FEATURE S, done, 2 steps] Doors tally on the finish receipt: one line naming each one-way step and how it was undone or parked — lesson: A receipt line that only…
- T-2113 [FEATURE M, done, 3 steps] fm genesis charter seal + privilege diff (mission-genesis brief 8, tier 3): init seals… — lesson: A seal file beside the file it seals …
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fifth): moonshot Mission from gen 2] [check: pending T-2187] Standing rule from gen 2 on: one Mission per gener…
## Lessons
- Classify a recorded check by what wrote it (a run's backticked command, a source's 'from', else typed) rather than adding a field
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_judgment.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
