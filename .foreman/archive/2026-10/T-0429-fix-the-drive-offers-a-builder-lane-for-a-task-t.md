---
id: T-0429
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-09T14:06:15Z
updated: 2026-10-09T14:12:54Z
base: 9983d66f76a8901c5c981c89354282008a95f649
base_tree: e6df513f8b7539a083abaa29aa5198959cba6201
verified: strong
---
# Drive: no builder lane offered for a task already under way
## Raw request
> FIX: the drive offers a builder lane for a task that is already done in this checkout and only waits on a gate (T-0414, T-0421 offered while their gate ran): _side_work should skip a task with recorded evidence or ticked steps (it's started; a lane would redo it)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a queued task with recorded evidence or a ticked step is not offered as side work — verify with `python3 plugin/tests/run.py -k test_drive_skips_work_already_under_way`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then the skip in _side_work
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_drive_skips_work_already_under_way` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes) [ran] [tree 98640d76270b] (2026-10-09T14:12:17Z)
- (step 1) `python3 plugin/tests/run.py -k test_drive_skips_work_already_under_way` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 4838eaf00fdd] (2026-10-09T14:12:25Z)
- (ac 1) `python3 plugin/tests/run.py -k test_drive_skips_work_already_under_way` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree f4f08a2637e0] (2026-10-09T14:12:54Z)
- (audit edge) `self: one condition in _side_work; red→green; hooks suite OK` → a task blocked mid-way also has evidence and is now skipped too, which is right: it isn't fresh work for a lane [tree f4f08a2637e0] (2026-10-09T14:12:54Z)
- (audit self) `self: one condition in _side_work; red→green; hooks suite OK` → no findings [tree f4f08a2637e0] (2026-10-09T14:12:54Z)
## Log
- 2026-10-09T14:06:15Z created
- 2026-10-09T14:06:40Z planned from capture
- 2026-10-09T14:11:32Z focused
- 2026-10-09T14:11:53Z paused: focus moved to T-0423
- 2026-10-09T14:12:07Z focused
- 2026-10-09T14:12:54Z done
- 2026-10-09T14:12:54Z committed 6092fd5 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0401 [FIX M, done, 3 steps] Drive: while background work runs, name a concrete queued task to start (builder lane / plan / block), offer up to 3 in turn, then wait — J…
- research T-0167-review: Verdict:** changes needed. One HIGH finding (a hang) and two MEDIUM ones. I traced each finding below by reading the code. I did not run any of t…
- T-0174 [FIX M, done, 4 steps] Parallel runs clean up after a failure, re-check main before merging; task commits take paths literally — lesson: A cleanup that covers onl…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar past tasks were M: consider --tier M
## Lessons
- An offer list needs the same 'already started' test as the queue: work in progress is never side work.
## Files touched
- CHANGELOG.md
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/tests/test_builder.py
