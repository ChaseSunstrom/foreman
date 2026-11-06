---
id: T-2260
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T03:42:40Z
updated: 2026-10-31T03:57:15Z
base: 87575628580b7f12f6916ed7e0e689f1507ff93d
base_tree: 9aec6b917f18ed93308d0622b670ce88251abaca
plan0_at: 2026-10-31T03:44:07Z
plan0_scope: []
verified: strong
---
# fm task finish's Landed line names files another open task holds and checks the sha is this task's own
## Raw request
> fm task finish's Landed line hides files another open task holds and names the newest commit touching the files, not the task's own (fmcli.py:1539-1545): list held files as (+N held for T-…) and compare the sha to the task's commit
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] when a close leaves out files another open task holds, Landed adds '(+N held for T-…)', and the sha it prints is a commit this task made (else it says the files are in an older commit) — verify with `cd plugin/tests && python3 -m unittest -q test_execution test_close_gates`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test with an open task holding one changed file; Landed lists it and names this task's own commit
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_execution` → ✗ exit 1 · Ran 21 tests in 7.788s / FAILED (failures=2) (start tree + this task's tests) [ran] [tree ec7ee2ffcda9] (2026-10-31T03:55:10Z)
- `cd plugin/tests && python3 -m unittest -q test_execution` → exit 0 · Ran 21 tests in 14.507s / OK [ran] [tree ec7ee2ffcda9] (2026-10-31T03:55:10Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_execution test_close_gates` → exit 0 · Ran 37 tests in 26.502s / OK [ran] [tree ec7ee2ffcda9] (2026-10-31T03:56:00Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_execution test_close_gates` → exit 0 · Ran 37 tests in 21.640s / OK [ran] [tree ec7ee2ffcda9] (2026-10-31T03:56:23Z)
- (audit edge) `self: Landed adds (+N held for T-…) for files an open task holds; the sha counts as this task's when a first-parent non-merge commit since its base touches its files or a commit since base names its id (word-bounded), which covers a lane merge; otherwise 'files already in <sha> (not this task's commit)'; no base commit falls back to the old wording; test_execution test_close_gates green; red-to-green proven` → a fast-forwarded merge of another task's work reads as this task's (noted); an id prefix like T-12 vs T-123 is word-bounded [tree ec7ee2ffcda9] (2026-10-31T03:56:23Z)
- (audit self) `self: Landed adds (+N held for T-…) for files an open task holds; the sha counts as this task's when a first-parent non-merge commit since its base touches its files or a commit since base names its id (word-bounded), which covers a lane merge; otherwise 'files already in <sha> (not this task's commit)'; no base commit falls back to the old wording; test_execution test_close_gates green; red-to-green proven` → no findings [tree ec7ee2ffcda9] (2026-10-31T03:56:23Z)
## Log
- 2026-10-31T03:42:40Z created
- 2026-10-31T03:43:39Z planned from capture
- 2026-10-31T03:43:39Z set approved=True
- 2026-10-31T03:43:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2260.builder.md
- 2026-10-31T03:44:07Z focused
- 2026-10-31T03:54:46Z merged worktree-agent-ac565b12a4e4df353 (3 file(s))
- 2026-10-31T03:54:47Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac565b12a4e4df353
- 2026-10-31T03:54:47Z focused
- 2026-10-31T03:56:00Z scope: plugin/lib/fmcli.py (_landed), plugin/tests/test_execution.py, CHANGELOG.md
- 2026-10-31T03:57:15Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2251 [FIX M, done, 3 steps] fm task finish counts the docs it names as the task's own files — lesson: A file-ownership rule that infers from edit records needs the tas…
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1825 [FEATURE M, done, 3 steps] FEATURE: fm run (headless) skips a model call when the tree and the failing check's output — lesson: count list items by line start, no…
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Long-horizon tier is the deciding end-of-run score for every ca…
## Lessons
- A line that says 'committed' must check the commit is the task's own, not merely the newest touching its files
## Files touched
- plugin/tests/test_execution.py
- plugin/lib/fmcli.py
- CHANGELOG.md
