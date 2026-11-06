---
id: T-1024
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T01:52:32Z
updated: 2026-10-16T02:00:52Z
base: 5dd2e84b232c55ee537a815d1f4bc589286ba318
base_tree: 5784ae3e4edbce5d5b2094e59f1aac2f4d6072e5
verified: strong
---
# Remove the merged leftover worktree t0971 and its branch
## Raw request
> Remove the leftover worktree .claude/worktrees/t0971 (branch worktree-agent-a714812d19c0f3e45): clean and fully merged into foreman/build; the Agents graph shows it as 'nothing to merge'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] git worktree list shows no t0971 and the branch worktree-agent-a714812d19c0f3e45 is gone — verify with `! git worktree list | grep -q t0971 && ! git rev-parse -q --verify worktree-agent-a714812d19c0f3e45`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] git worktree remove .claude/worktrees/t0971; git branch -d worktree-agent-a714812d19c0f3e45 (merged, so -d is safe)
## Resume here
## Docs impact
none: repo housekeeping
## Verification evidence
- (step 1) `! git worktree list | grep -q t0971 && ! git rev-parse -q --verify worktree-agent-a714812d19c0f3e45` → exit 0 · (no output) [ran] [tree 5784ae3e4edb] (2026-10-16T02:00:51Z)
- (ac 1) `! git worktree list | grep -q t0971 && ! git rev-parse -q --verify worktree-agent-a714812d19c0f3e45` → exit 0 · (no output) [ran] [tree 5784ae3e4edb] (2026-10-16T02:00:52Z)
- (audit operator) `self` → worktree was clean and its HEAD merged into foreman/build (checked before removal); branch deleted with -d (refuses unmerged) [tree 5784ae3e4edb] (2026-10-16T02:00:52Z)
- (ac 1) `! git worktree list | grep -q t0971 && ! git rev-parse -q --verify worktree-agent-a714812d19c0f3e45` → exit 0 · (no output) [ran] [tree 5784ae3e4edb] (2026-10-16T02:00:52Z)
- (audit operator) `pre-checked clean and merged; removed` → nothing unmerged lost [tree 5784ae3e4edb] (2026-10-16T02:00:52Z)
- (audit self) `pre-checked clean and merged; removed` → no findings [tree 5784ae3e4edb] (2026-10-16T02:00:52Z)
## Log
- 2026-10-16T01:52:32Z created
- 2026-10-16T01:52:37Z planned from capture
- 2026-10-16T02:00:21Z focused
- 2026-10-16T02:00:47Z focused
- 2026-10-16T02:00:52Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- T-0948 [FEATURE M, done, 4 steps] Enforce: fm lane merge re-runs the lane task's criteria in the worktree and refuses red — lesson: Gate merges on the work's own criteri…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
