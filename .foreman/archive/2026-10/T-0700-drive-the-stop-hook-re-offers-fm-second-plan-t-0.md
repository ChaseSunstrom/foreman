---
id: T-0700
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-09T16:09:08Z
updated: 2026-10-09T16:12:02Z
base: 2b54b056329cea088ec58791d6248b2bbebf7fba
base_tree: ec51c94c64a9bff123cb9e16a222cb99491c58fc
verified: strong
---
# Drive: the Stop hook re-offers 'fm second plan T-0672' after the plan review is saved, and
## Raw request
> Drive: the Stop hook re-offers 'fm second plan T-0672' after the plan review is saved, and doesn't know a backgrounded release gate holds the tree (each repeat costs a turn)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the drive never offers a lane while the builder slots are full, nor a plan review a task already has — verify with `python3 plugin/tests/run.py -k side_work_respects`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first + _side_work/_start_how read lane capacity and the Plan review section
2. [x] test-first + _side_work/_start_how read lane capacity and the Plan review section
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k side_work_respects` → ✗ exit 1 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: Stop 2s) / FAILED (1 classes) [ran] [tree d102d07ae7c8] (2026-10-09T16:11:21Z)
- (step 1) `python3 plugin/tests/run.py -k side_work_respects -k test_drive_offers_queued_work` → exit 0 · Ran 2 tests in 5.1s (1 classes, 16 at a time; slowest: Stop 5s) / OK [ran] [tree 2b8533ecd210] (2026-10-09T16:11:51Z)
- (step 2) `python3 plugin/tests/run.py -k side_work_respects` → exit 0 · Ran 1 tests in 2.8s (1 classes, 16 at a time; slowest: Stop 3s) / OK [ran] [tree cd21fddebf7a] (2026-10-09T16:11:58Z)
- (ac 1) `python3 plugin/tests/run.py -k side_work_respects` → exit 0 · Ran 1 tests in 2.8s (1 classes, 16 at a time; slowest: Stop 3s) / OK [ran] [tree cd21fddebf7a] (2026-10-09T16:12:01Z)
- (audit self) `self: red then green; the existing offer test still passes; lanes_free reads the same BUILDERS limit fm lane brief enforces` → no findings [tree cd21fddebf7a] (2026-10-09T16:12:01Z)
## Log
- 2026-10-09T16:09:08Z created
- 2026-10-09T16:10:21Z also: the drive offered 'fm lane brief T-0671' while two builders were out, which fm lane brief refuses; the drive should check the builder limit before offering a lane
- 2026-10-09T16:10:52Z set tier=S
- 2026-10-09T16:10:56Z focused
- 2026-10-09T16:12:01Z done
- 2026-10-09T16:12:02Z committed 92034cd (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0401 [FIX M, done, 3 steps] Drive: while background work runs, name a concrete queued task to start (builder lane / plan / block), offer up to 3 in turn, then wait — J…
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- research mission-20261009-091631.pack: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just sim…
- decision 2026-09-26: Work T-0019 (drive vs background work) before T-0016: T-0016's five-lens audit runs background agents, where drive currently pushes the turn on ever…
## Lessons
- a suggestion engine must ask the command it suggests whether it would accept; mirror its refusal conditions
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
