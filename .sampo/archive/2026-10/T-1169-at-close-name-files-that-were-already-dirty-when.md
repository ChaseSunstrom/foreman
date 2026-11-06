---
id: T-1169
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T11:55:53Z
base: 4b9f34dc0bef209438d03e15ae5c6d74418e278a
base_tree: 9ca1a2f75a8c8e37190733c20015cb23dadf6ae4
plan0_at: 2026-10-16T11:36:12Z
plan0_scope: []
verified: strong
---
# At close, name files that were already dirty when the task was focused and that the task a
## Raw request
> FEATURE: At close, name files that were already dirty when the task was focused and that the task also edited, and leave them out of the commit unless finish is given --with FILE (the user's own uncommitted work must not ride in a task commit).
> DONE-WHEN: a test dirties a file before `fm focus`, edits it as the task, and `fm task finish --commit` names it and leaves it uncommitted; with --with FILE it is committed; a clean file the task edits is committed as before
## Interpretation
The user's own uncommitted work must never ride in a task's commit. When a task is focused, record which files were already dirty (uncommitted) then; at fm task finish --commit (and fm lane merge's commit path if it commits the task's files), a file that was dirty at focus and that the task also edited is named and left out of the commit, unless finish is given --with FILE (repeatable). A clean file the task edits is committed as before.
## Assumptions (confidence)
## Acceptance criteria
- [x] a file dirty before fm focus and edited by the task is named by fm task finish --commit and left uncommitted; with --with FILE it is committed; a clean file the task edits is committed as before — verify with `python3 plugin/tests/run.py test_dirty_at_focus`
## Non-goals
## Approach (options → choice → why)
Options: (a) snapshot 'git status --porcelain -z' paths into the brief meta (dirty_at_focus) when fm focus runs, and filter the commit's path list at finish; (b) hash each dirty file at focus and compare at finish to separate the user's hunks (too clever: partial hunks can't be split safely); (c) refuse the close (the round-2 idea; rejected: it blocks legitimate work on a file the user asked to change). Choice: (a); why: cheap, explainable, the user decides with --with. Find where finish builds its commit file list (fmcli task_finish / commit helper) and where fm focus sets the active task.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_dirty_at_focus.py): dirty-before-focus file excluded and named; --with includes it; clean file committed; no snapshot (old briefs) behaves as before
2. [x] dirty_at_focus snapshot at focus; the commit filter and --with in finish
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_dirty_at_focus` → ✗ exit 1 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: DirtyAtFocus 1s) / FAILED (1 classes) [ran] [tree db6e4c27f1f6] (2026-10-16T11:36:41Z)
- (step 1) `python3 plugin/tests/run.py test_dirty_at_focus` → exit 0 · Ran 3 tests in 2.1s (1 classes, 16 at a time; slowest: DirtyAtFocus 2s) / OK [ran] [tree dd9ddd1d064e] (2026-10-16T11:36:59Z)
- (step 2) `python3 plugin/tests/run.py test_dirty_at_focus` → exit 0 · Ran 3 tests in 1.7s (1 classes, 16 at a time; slowest: DirtyAtFocus 2s) / OK [ran] [tree dd9ddd1d064e] (2026-10-16T11:37:01Z)
- (step 2) `python3 plugin/tests/run.py test_dirty_at_focus` → exit 0 · Ran 5 tests in 12.7s (1 classes, 16 at a time; slowest: DirtyAtFocus 12s) / OK [ran] [tree 332e4924ed27] (2026-10-16T11:49:31Z)
- (ac 1) `python3 plugin/tests/run.py test_dirty_at_focus test_execution test_bookkeeping` → exit 0 · Ran 30 tests in 9.4s (17 classes, 16 at a time; slowest: DirtyAtFocus 9s, BoardClose 8s, CommitOwnFiles 7s) / OK [ran] [tree cf66a7a7cb67] (2026-10-16T11:53:57Z)
- (ac 1) `python3 plugin/tests/run.py test_dirty_at_focus` → exit 0 · Ran 5 tests in 8.3s (1 classes, 16 at a time; slowest: DirtyAtFocus 8s) / OK [ran] [tree e1c98a17984f] (2026-10-16T11:54:19Z)
- (audit intent) `reviewer: one fm-reviewer pass found an earlier task's uncommitted files counted as the user's (contradicting _theirs), list meta corrupted by commas and ' #', a second status walk under the lock, unnormalised --with and the dry call missing with_; builder fixed all (ledger touched events, JSON sidecar capped at 500, diff-tree on the focus snapshot, path normalisation)` → the user's own WIP never rides in a task commit [tree e1c98a17984f] (2026-10-16T11:54:19Z)
- (audit adversary) `reviewer: one fm-reviewer pass found an earlier task's uncommitted files counted as the user's (contradicting _theirs), list meta corrupted by commas and ' #', a second status walk under the lock, unnormalised --with and the dry call missing with_; builder fixed all (ledger touched events, JSON sidecar capped at 500, diff-tree on the focus snapshot, path normalisation)` → a --with file still passes the credential scan before the close [tree e1c98a17984f] (2026-10-16T11:54:19Z)
- (audit edge) `reviewer: one fm-reviewer pass found an earlier task's uncommitted files counted as the user's (contradicting _theirs), list meta corrupted by commas and ' #', a second status walk under the lock, unnormalised --with and the dry call missing with_; builder fixed all (ledger touched events, JSON sidecar capped at 500, diff-tree on the focus snapshot, path normalisation)` → >500 dirty files: the rest count as the task's (flag stored); old briefs without a sidecar commit as before [tree e1c98a17984f] (2026-10-16T11:54:19Z)
- (audit operator) `reviewer: one fm-reviewer pass found an earlier task's uncommitted files counted as the user's (contradicting _theirs), list meta corrupted by commas and ' #', a second status walk under the lock, unnormalised --with and the dry call missing with_; builder fixed all (ledger touched events, JSON sidecar capped at 500, diff-tree on the focus snapshot, path normalisation)` → the left-out files are named with the --with hint [tree e1c98a17984f] (2026-10-16T11:54:19Z)
- (audit maintainer) `reviewer: one fm-reviewer pass found an earlier task's uncommitted files counted as the user's (contradicting _theirs), list meta corrupted by commas and ' #', a second status walk under the lock, unnormalised --with and the dry call missing with_; builder fixed all (ledger touched events, JSON sidecar capped at 500, diff-tree on the focus snapshot, path normalisation)` → one sidecar per task under audits/, read by _commit_task only [tree e1c98a17984f] (2026-10-16T11:54:19Z)
## Log
- 2026-10-16T10:45:53Z created
- 2026-10-16T11:36:01Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1169.builder.md
- 2026-10-16T11:36:12Z focused
- 2026-10-16T11:53:42Z merged worktree-agent-ad65e1a2a683dff70 (3 file(s))
- 2026-10-16T11:53:46Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad65e1a2a683dff70
- 2026-10-16T11:53:47Z focused
- 2026-10-16T11:54:09Z scope: MASTER.md and CHANGELOG.md lines
- 2026-10-16T11:55:52Z done
- 2026-10-16T11:55:53Z committed cf9972bf (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- research mission-20261009-091631.pack: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just sim…
- T-0174 [FIX M, done, 4 steps] Parallel runs clean up after a failure, re-check main before merging; task commits take paths literally — lesson: A cleanup that covers onl…
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
## Lessons
- store lists as JSON, never in the brief's flat frontmatter, whose parser splits on commas
## Plan gaps
- failed first: step 1 Failing tests (test_dirty_at_focus.py): dirty-before-focus file excluded and named; --with includes…
## Files touched
- plugin/tests/test_dirty_at_focus.py
- plugin/lib/fmcli.py
- plugin/tests/test_execution.py
- MASTER.md
- CHANGELOG.md
