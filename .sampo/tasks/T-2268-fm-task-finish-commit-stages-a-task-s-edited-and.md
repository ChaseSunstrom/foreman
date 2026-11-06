---
id: T-2268
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T04:38:56Z
updated: 2026-10-31T05:03:05Z
base: ea94b84a3d36b79c6210eca853a6f8d4546a6455
base_tree: 258575a781d0f4befe3b092fc4224579922b0b4b
plan0_at: 2026-10-31T04:42:42Z
plan0_scope: []
verified: strong
---
# fm task finish --commit stages a task's edited and created files but not a tracked file…
## Raw request
> fm task finish --commit stages a task's edited and created files but not a tracked file it deleted with rm (T-2266's commit missed plugin/skills/docs and security-review, so ship64's scratch tree held both names): stage deletions of scoped paths, or name the unstaged deletion in the Landed line
## Interpretation
T-2266 (focused by fm task new --focus; base_tree 4839ace7 holds plugin/skills/docs/SKILL.md and plugin/skills/security-review/SKILL.md) deleted both with a Bash rm after focus; its fm task finish --commit printed 'left out 2 uncommitted file(s) it didn't change' for them, so _commit_task's files = fmmap.changed(root, base) didn't list the deletions, and ship64's scratch tree held both old and new skill names. worktree_tree runs git add -A -- . on a copy of the index, which should stage removals, so the cause is somewhere between task_base, task_diff and _commit_task's filters: find it with a red test first.
## Assumptions (confidence)
## Acceptance criteria
- [x] a tracked file a task deletes after its focus (by rm, not Edit) is committed as a deletion by fm task finish --commit, and a deletion made before the focus still stays out — verify with `python3 plugin/tests/run.py test_dirty_at_focus test_execution`
## Non-goals
## Approach (options → choice → why)
1) red test in test_commit (or wherever _commit_task's tests live): fm task new --focus, commit-tracked file deleted with os.remove after focus, fm task finish --commit: the commit must hold the deletion; then fix the root cause (not a special case in finish). 2) just stage every deletion in the repo at finish — rejected: sweeps other tasks' work. Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test reproducing T-2266's missed deletion
2. [x] root-cause fix in the diff or the commit's file filter
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_dirty_at_focus` → ✗ exit 1 · Ran 9 tests in 24.4s (2 classes, 16 at a time; slowest: DirtyAtFocus 19s, EditedUnderAnotherTask 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 760285ac5446] (2026-10-31T04:58:54Z)
- `python3 plugin/tests/run.py test_dirty_at_focus` → exit 0 · Ran 9 tests in 29.0s (2 classes, 16 at a time; slowest: DirtyAtFocus 27s, EditedUnderAnotherTask 7s) / OK [ran] [tree 760285ac5446] (2026-10-31T04:58:54Z)
- (step 1) `python3 plugin/tests/run.py test_dirty_at_focus test_execution test_close_gates test_map` → exit 0 · Ran 57 tests in 119.9s (14 classes, 16 at a time; slowest: CloseGates 119s, BoardClose 55s, DirtyAtFocus 43s) / OK [ran] [tree 760285ac5446] (2026-10-31T05:00:57Z)
- (step 2) `python3 plugin/tests/run.py test_dirty_at_focus` → exit 0 · Ran 9 tests in 25.0s (2 classes, 16 at a time; slowest: DirtyAtFocus 24s, EditedUnderAnotherTask 5s) / OK [ran] [tree 760285ac5446] (2026-10-31T05:01:23Z)
- (step 3) `python3 plugin/tests/run.py test_dirty_at_focus` → exit 0 · Ran 9 tests in 18.8s (2 classes, 16 at a time; slowest: DirtyAtFocus 18s, EditedUnderAnotherTask 5s) / OK [ran] [tree 760285ac5446] (2026-10-31T05:01:43Z)
- (ac 1) `python3 plugin/tests/run.py test_dirty_at_focus test_execution` → exit 0 · Ran 31 tests in 12.9s (10 classes, 16 at a time; slowest: BoardClose 12s, DirtyAtFocus 10s, EditedUnderAnotherTask 3s) / OK [ran] [tree b1d536f7d5d7] (2026-10-31T05:02:26Z)
- (audit intent) `self: one flag (--no-renames) on both paths of fmmap.changed, matching the other task_diff callers; the root cause matches the T-2266 symptom exactly (near-identical renamed SKILL.md files)` → a file a task moves commits both names (test_dirty_at_focus rename test red-to-green proven) [tree b1d536f7d5d7] (2026-10-31T05:02:26Z)
- (audit edge) `self: one flag (--no-renames) on both paths of fmmap.changed, matching the other task_diff callers; the root cause matches the T-2266 symptom exactly (near-identical renamed SKILL.md files)` → a plain rm after focus already worked (kept as a regression test); listing both names of a rename is a superset, so nothing else is dropped [tree b1d536f7d5d7] (2026-10-31T05:02:26Z)
## Log
- 2026-10-31T04:38:56Z created
- 2026-10-31T04:42:12Z set tier=M, type=FIX
- 2026-10-31T04:42:13Z planned: it has criteria and steps
- 2026-10-31T04:42:25Z criterion 1 verify: `python3 plugin/tests/run.py test_commit` → `python3 plugin/tests/run.py test_dirty_at_focus test_execution`
- 2026-10-31T04:42:26Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2268.builder.md
- 2026-10-31T04:42:41Z focused
- 2026-10-31T04:57:48Z merged worktree-agent-aa1db47f73895bd3e (2 file(s))
- 2026-10-31T04:57:48Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa1db47f73895bd3e
- 2026-10-31T04:57:49Z focused
- 2026-10-31T05:02:10Z scope: plugin/lib/fmmap.py (changed: --no-renames), plugin/tests/test_dirty_at_focus.py, CHANGELOG.md
- 2026-10-31T05:03:02Z done
- 2026-10-31T05:03:05Z committed fdba78a1 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- research T-0078-review: Verdict: changes needed (one MEDIUM, fail-open, plus a LOW).** `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0078.diff` is …
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
## Why not caught
no test moved a file after focus; test_dirty_at_focus now does
## Lessons
- A changed-file list built from git diff must pass --no-renames, or a move reports only its destination and the source's deletion is lost
## Files touched
- plugin/tests/test_dirty_at_focus.py
- plugin/lib/fmmap.py
- CHANGELOG.md
