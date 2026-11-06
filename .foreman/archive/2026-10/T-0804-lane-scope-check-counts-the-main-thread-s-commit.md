---
id: T-0804
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/tests/test_lanes.py]
depends_on: []
source: discovered
created: 2026-10-14T16:29:14Z
updated: 2026-10-14T17:08:27Z
base: aaeb2f3b1a01e37e1e847ea77e20357f753eb769
base_tree: 8f08906305dcadfbd25b4d2bd5660abeb1c65e2f
verified: strong
---
# A merged lane's task is measured from the main checkout's commit before the merge
## Raw request
> Lane scope check counts the main thread's commits made while a lane ran (T-0803, T-0778 files) as the lane task's out-of-scope edits at finish (T-0779): measure a merged lane's diff from its branch's merge-base, not the old focus snapshot
## Interpretation
A lane task's start point is the snapshot from its focus in the worktree. After fm lane merge, fm lane rm and fm focus in the main checkout, finish measures the diff from that snapshot to the main tree, so every main-thread commit made while the lane ran counts as the lane task's out-of-scope edits (T-0779 listed 8 files of T-0803/T-0778). fm lane merge sets the task's base to the main checkout's HEAD just before the merge (and drops the old base_tree), so its diff is what the merge brought in plus later work.
## Assumptions (confidence)
## Acceptance criteria
- [x] after fm lane merge, a commit made in the main checkout while the lane ran isn't in the task's changed files; the lane's own files are — verify with `cd plugin/tests && python3 -m unittest test_lanes`
## Non-goals
## Approach (options → choice → why)
Options: subtract other tasks' touched files (already done for commits, not for scope); compare branch merge-base (needs the branch after lane rm); re-base at merge to the pre-merge HEAD (one meta update where the merge happens). Chose the re-base at merge.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing lanes test
2. [x] Re-base the task at merge
## Resume here
## Docs impact
## Verification evidence
- `cd plugin/tests && python3 -m unittest test_lanes.Lanes.test_a_merged_lanes_task_is_measured_from_the_main_commit_before_the_merge` → ✗ exit 1 · Ran 1 test in 0.433s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 5013984f2d49] (2026-10-14T17:06:06Z)
- `cd plugin/tests && python3 -m unittest test_lanes.Lanes.test_a_merged_lanes_task_is_measured_from_the_main_commit_before_the_merge` → exit 0 · Ran 1 test in 0.327s / OK [ran] [tree 5013984f2d49] (2026-10-14T17:06:06Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_lanes.Lanes.test_a_merged_lanes_task_is_measured_from_the_main_commit_before_the_merge` → exit 0 · Ran 1 test in 0.326s / OK [ran] [tree 5013984f2d49] (2026-10-14T17:06:10Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_lanes test_builder` → exit 0 · Ran 30 tests in 13.248s / OK [ran] [tree 5013984f2d49] (2026-10-14T17:06:24Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_lanes` → exit 0 · Ran 13 tests in 5.290s / OK [ran] [tree 5013984f2d49] (2026-10-14T17:06:29Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_lanes` → exit 0 · Ran 13 tests in 5.337s / OK [ran] [tree 5013984f2d49] (2026-10-14T17:08:17Z)
- (audit edge) `self: merged diff read; merge() reads the main HEAD before merging and, after a successful merge, sets the task's base to it and drops base_tree and paused_tree, so its diff is what the merge brought plus later work; the builder's test builds a lane commit and a main commit and checks only the lane's file is the task's` → a merge that fails leaves the old base (set only after success); a lane merged twice is re-based to the HEAD before the second merge, which still holds the first merge's files as committed [tree 5013984f2d49] (2026-10-14T17:08:17Z)
- (audit self) `self: merged diff read; merge() reads the main HEAD before merging and, after a successful merge, sets the task's base to it and drops base_tree and paused_tree, so its diff is what the merge brought plus later work; the builder's test builds a lane commit and a main commit and checks only the lane's file is the task's` → no findings [tree 5013984f2d49] (2026-10-14T17:08:17Z)
- (audit edge) `self: merged diff read; merge() reads the main HEAD before merging and, after a successful merge, sets the task's base to it and drops base_tree and paused_tree, so its diff is what the merge brought plus later work; the builder's test builds a lane commit and a main commit and checks only the lane's file is the task's` → a merge that fails leaves the old base (set only after success); a lane merged twice is re-based to the HEAD before the second merge [tree 5013984f2d49] (2026-10-14T17:08:26Z)
- (audit self) `self: merged diff read; merge() reads the main HEAD before merging and, after a successful merge, sets the task's base to it and drops base_tree and paused_tree, so its diff is what the merge brought plus later work; the builder's test builds a lane commit and a main commit and checks only the lane's file is the task's` → no findings [tree 5013984f2d49] (2026-10-14T17:08:26Z)
## Log
- 2026-10-14T16:29:14Z created
- 2026-10-14T17:04:47Z planned from capture
- 2026-10-14T17:04:48Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0804.builder.md
- 2026-10-14T17:04:53Z focused
- 2026-10-14T17:06:05Z merged worktree-agent-a7788e13617910d71 (2 file(s))
- 2026-10-14T17:06:05Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7788e13617910d71
- 2026-10-14T17:06:05Z focused
- 2026-10-14T17:08:26Z scope: the two paths are this task's own fmlanes.py and test_lanes.py as the builder edited them inside its worktree (.claude/worktrees/agent-…); same files, merged
- 2026-10-14T17:08:27Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- T-0767 [FIX S, done, 2 steps] Recreating a dropped task keeps its diff: fm task new --redo ID takes over the dropped task's start point and edited files — lesson: a recr…
- research T-0078-review: Verdict: changes needed (one MEDIUM, fail-open, plus a LOW).** `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0078.diff` is …
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- likely tests for the scope: plugin/tests/test_lanes.py
## Lessons
- a task's start point must move when its work lands somewhere else
## Files touched
- .claude/worktrees/agent-a7788e13617910d71/plugin/tests/test_lanes.py
- .claude/worktrees/agent-a7788e13617910d71/plugin/lib/fmlanes.py
- plugin/lib/fmlanes.py
- plugin/tests/test_lanes.py
