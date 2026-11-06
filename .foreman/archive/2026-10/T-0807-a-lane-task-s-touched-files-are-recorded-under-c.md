---
id: T-0807
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_core.py]
depends_on: []
source: discovered
created: 2026-10-14T17:08:26Z
updated: 2026-10-14T17:21:19Z
base: 810abac1be2f3be8390cae172bf830065da5d281
base_tree: d37dbce4f0ec6f214567ef30fd5e437cb2112544
verified: strong
---
# A lane's edits recorded under .claude/worktrees/<lane>/ count as the repo files they are
## Raw request
> A lane task's touched files are recorded under .claude/worktrees/<lane>/… and the close's scope check counts them as out of scope (T-0804): map a worktree path to its repo-relative path before the scope check
## Interpretation
Builders edit inside .claude/worktrees/<lane>/ (Claude Code's worktree folder inside the main checkout), so the hooks record touched files at those paths; after the merge the close's scope check (and the commit's 'only other tasks edited' filter) see .claude/worktrees/agent-…/plugin/lib/x.py, not plugin/lib/x.py, and T-0779/T-0786/T-0804 each needed a logged scope reason. task_touches maps a path under .claude/worktrees/<name>/ to the repo-relative path it stands for.
## Assumptions (confidence)
## Acceptance criteria
- [x] a touched event at .claude/worktrees/agent-x/plugin/lib/a.py counts as plugin/lib/a.py in task_touches — verify with `python3 plugin/tests/run.py -k test_lane_worktree_paths_map_to_repo_paths`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing core test
2. [x] Map worktree paths in task_touches
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_lane_worktree_paths_map_to_repo_paths` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Ledger 0s) / FAILED (1 classes) [ran] [tree efffe6e257f1] (2026-10-14T17:18:48Z)
- (step 2) `python3 plugin/tests/run.py test_core test_lanes test_cli` → exit 0 · Ran 164 tests in 17.6s (40 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 7s, Lanes 6s) / OK [ran] [tree 6e0aa6fd3f8c] (2026-10-14T17:19:11Z)
- (ac 1) `python3 plugin/tests/run.py -k test_lane_worktree_paths_map_to_repo_paths` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Ledger 0s) / OK [ran] [tree 6e0aa6fd3f8c] (2026-10-14T17:19:12Z)
- `python3 plugin/tests/run.py -k test_lane_worktree_paths_map_to_repo_paths` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Ledger 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6e0aa6fd3f8c] (2026-10-14T17:19:12Z)
- `python3 plugin/tests/run.py -k test_lane_worktree_paths_map_to_repo_paths` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Ledger 0s) / OK [ran] [tree 6e0aa6fd3f8c] (2026-10-14T17:19:12Z)
- (ac 1) `python3 plugin/tests/run.py -k test_lane_worktree_paths_map_to_repo_paths` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Ledger 0s) / OK [ran] [tree 6e0aa6fd3f8c] (2026-10-14T17:21:17Z)
- (audit edge) `self: diff read; task_touches strips a leading .claude/worktrees/<name>/ from a project-relative touched path, so the scope check, the commit filter and fm tour see the repo file a lane edited; nothing else in the ledger changes` → a repo that really keeps files under .claude/worktrees/ (not Claude Code's lanes) would see them mapped too; Claude Code reserves that folder for its worktrees [tree 6e0aa6fd3f8c] (2026-10-14T17:21:17Z)
- (audit self) `self: diff read; task_touches strips a leading .claude/worktrees/<name>/ from a project-relative touched path, so the scope check, the commit filter and fm tour see the repo file a lane edited; nothing else in the ledger changes` → no findings [tree 6e0aa6fd3f8c] (2026-10-14T17:21:17Z)
## Log
- 2026-10-14T17:08:26Z created
- 2026-10-14T17:18:40Z planned from capture
- 2026-10-14T17:18:40Z focused
- 2026-10-14T17:21:18Z done
- 2026-10-14T17:21:19Z committed 14c5cd8 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- research t0071-abc-review: MEDIUM** — `plugin/lib/fmcli.py:551-568` (`cmd_focus`/`_moved_since_planned`). `target.set_section("Related", related)` is only called inside …
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_core.py
## Lessons
- record a lane's edits as the repo files they stand for, or every close after a merge needs a hand-written reason
## Plan gaps
- failed first: step 1 Failing core test
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
