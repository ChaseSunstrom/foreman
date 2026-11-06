---
id: T-1136
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T09:05:45Z
updated: 2026-10-16T09:25:25Z
base: ca85d4d20d0086d6aad7fb9a42c2a2dd47c424d7
base_tree: c6c48ab54c1fe7d3efb50b7baad8c181e06a46da
plan0_at: 2026-10-16T09:23:14Z
plan0_scope: [plugin/lib/fmlanes.py, plugin/tests/test_lanes.py, CHANGELOG.md]
verified: strong
---
# Fm lane rm right after a conflicted fm lane merge removes the worktree and the builder rec
## Raw request
> fm lane rm right after a conflicted fm lane merge removes the worktree and the builder record (branch kept), so fm lane resume can't reopen it and a new builder must re-merge the kept branch (T-1059, T-1062 on 2026-10-16): refuse rm while a conflict brief is open, or keep enough for resume to rebuild the worktree from the kept branch
## Interpretation
fm lane rm after a conflicted fm lane merge removed the worktree and the builder record. The branch was kept, but the lane couldn't be resumed and needed a new builder to re-merge it.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane rm is refused while a conflict brief is open and the branch is unmerged; allowed once merged or the task is dropped — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
Refuse fm lane rm while the lane's task has an open conflict brief (audits/ID.conflict.md) and its branch isn't merged, unless the task was dropped or done. The message says to resolve on the branch and fm lane merge, or drop the task to abandon it (the branch is kept either way).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test then the refusal in fmlanes.remove
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_rm_waits test_lanes` → ✗ exit 1 · Ran 28 tests in 14.3s (4 classes, 16 at a time; slowest: Lanes 14s, BoardLanes 1s, SafeGitFailsClosed 0s) / FAILED (1 classes) [ran] [tree b79a13b926c2] (2026-10-16T09:23:36Z)
- (step 1) `python3 plugin/tests/run.py test_lanes test_tidy test_builder` → exit 0 · Ran 80 tests in 15.8s (22 classes, 16 at a time; slowest: Lanes 16s, Contract 11s, Brief 7s) / OK [ran] [tree 847a09a593c1] (2026-10-16T09:24:01Z)
- `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 28 tests in 12.7s (4 classes, 16 at a time; slowest: Lanes 12s, BoardLanes 1s, SafeGitFailsClosed 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 0eef4c8767ff] (2026-10-16T09:24:34Z)
- `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 28 tests in 12.8s (4 classes, 16 at a time; slowest: Lanes 13s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree 0eef4c8767ff] (2026-10-16T09:24:34Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 28 tests in 10.8s (4 classes, 16 at a time; slowest: Lanes 11s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree 0eef4c8767ff] (2026-10-16T09:24:45Z)
- (audit self) `self: refuses only when all three hold (a conflict brief exists, the task isn't closed, the lane's tip isn't in HEAD), so tidy's removal of closed tasks' lanes and a normal rm after a clean merge are unchanged (test_lanes, test_tidy pass); the message names both ways out` → no findings [tree 0eef4c8767ff] (2026-10-16T09:24:45Z)
## Log
- 2026-10-16T09:05:45Z created
- 2026-10-16T09:23:13Z set scope=['plugin/lib/fmlanes.py', 'plugin/tests/test_lanes.py', 'CHANGELOG.md']
- 2026-10-16T09:23:14Z focused
- 2026-10-16T09:24:08Z scope: CHANGELOG.md — release note
- 2026-10-16T09:25:24Z done
- 2026-10-16T09:25:25Z committed bb34c2b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- T-1028 [FEATURE M, done, 8 steps] Worktree agents resume easily after a session stops: find a stopped builder's worktree and — lesson: A resume that frees a worktree mus…
- T-0808 [FIX S, done, 2 steps] fm check --affected works in Foreman's own project; lane briefs steer verify commands away from cd chains — lesson: an instruction to a bui…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- likely tests for the scope: plugin/tests/test_lanes.py
## Lessons
- A cleanup verb must refuse while the thing it cleans up still holds unfinished work, not just uncommitted files
## Plan gaps
- failed first: step 1 Test then the refusal in fmlanes.remove
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
