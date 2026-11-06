---
id: T-1138
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmbus.py, plugin/tests/test_claims.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-16T09:25:42Z
updated: 2026-10-16T09:28:31Z
base: bb34c2b5c1b6744f3be982bb4170fb5d52658bb1
base_tree: 0eef4c8767ff2c2bf13d2dfd4eec9d77a1de7919
plan0_at: 2026-10-16T09:25:42Z
plan0_scope: []
verified: strong
---
# Lane pre-claims are advisory: a builder's file-wide pre-claim (lane-<id>) never denies another worktree's edit
## Raw request
> Lane pre-claims are advisory: a builder's file-wide pre-claim (lane-<id>) never denies another worktree's edit
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an edit to a file another lane pre-claimed is allowed (the lease is named in a note); a session's own explicit fm lease take still denies others — verify with `python3 plugin/tests/run.py test_claims`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test then exempt lane- pre-claims from the deny in fmbus.conflict
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_claims` → ✗ exit 1 · Ran 15 tests in 8.8s (3 classes, 16 at a time; slowest: ClaimsReview 9s, Claims 8s, Stop 5s) / FAILED (1 classes) [ran] [tree 9bce5d4baae3] (2026-10-16T09:26:07Z)
- (step 1) `python3 plugin/tests/run.py test_claims test_bus test_builder` → exit 0 · Ran 52 tests in 19.9s (15 classes, 16 at a time; slowest: Contract 20s, Watch 16s, ClaimsReview 16s) / OK [ran] [tree 3e75b0082473] (2026-10-16T09:26:35Z)
- `python3 plugin/tests/run.py test_claims` → ✗ exit 1 · Ran 15 tests in 12.3s (3 classes, 16 at a time; slowest: ClaimsReview 11s, Claims 10s, Stop 8s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 83bcad738d72] (2026-10-16T09:27:11Z)
- `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 15 tests in 11.2s (3 classes, 16 at a time; slowest: ClaimsReview 11s, Claims 10s, Stop 8s) / OK [ran] [tree 83bcad738d72] (2026-10-16T09:27:11Z)
- (ac 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 15 tests in 11.0s (3 classes, 16 at a time; slowest: ClaimsReview 11s, Claims 10s, Stop 8s) / OK [ran] [tree 83bcad738d72] (2026-10-16T09:27:23Z)
- (audit self) `self: only lane- sessions (pre-claims written by fm lane brief) are dropped from the deny set; explicit leases from fm lease take still deny (tested elsewhere in test_claims); the edit hot path no longer loads briefs at all; seen live: lane-T-1135 blocked T-1137's builder on fmcli.py` → no findings [tree 83bcad738d72] (2026-10-16T09:27:23Z)
## Log
- 2026-10-16T09:25:42Z created
- 2026-10-16T09:25:42Z focused
- 2026-10-16T09:26:15Z set scope=['plugin/lib/fmbus.py', 'plugin/tests/test_claims.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-16T09:26:46Z scope: CHANGELOG.md, MASTER.md — docs
- 2026-10-16T09:28:30Z done
- 2026-10-16T09:28:31Z committed ece5a0f (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- research wave2-plan-a4b64956d53d543cc: === T-1058 [stale: plugin/lib/fmbacktest.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-16: Drafts (fm draft) run headless claude with --permission-mode acceptEdits
- the similar finished task took 2 steps
## Lessons
- Coordination between isolated worktrees should inform, not block: the merge is where overlaps are real
## Plan gaps
- failed first: step 1 Test then exempt lane- pre-claims from the deny in fmbus.conflict
## Files touched
- plugin/tests/test_claims.py
- plugin/lib/fmbus.py
- CHANGELOG.md
- MASTER.md
