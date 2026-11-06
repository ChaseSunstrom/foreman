---
id: T-2208
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T20:13:55Z
updated: 2026-10-31T03:28:38Z
base: 458f5e0a6b4e63338a3ca7f637e2cb6ed340a029
base_tree: f2006e4ec926b3b6e6f0d4eb9065e1ed497204bb
plan0_at: 2026-10-31T03:11:26Z
plan0_scope: []
verified: strong
---
# A lane conflict brief tells the main session how to resolve it from where it stands
## Raw request
> Lane conflict brief's resolve steps (git -C <worktree> merge …) are refused from the main checkout with 'no active task' because the guard reads the session's cwd, and fm focus refuses a lane-held task: the brief should say cd into the worktree as its own command first, or the guard should count writes under a held lane's worktree as that lane's task
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the conflict brief fm lane merge writes says: send the lane's builder the merge (SendMessage) or run each git step with the worktree as its own cd command first; and its git steps don't fail with 'no active task' when followed — verify with `cd plugin/tests && python3 -m unittest -q test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test on the brief's text; rewrite the resolve steps
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_lanes 2>&1 | tail -8` → ✗ exit 1 · Ran 40 tests in 16.666s / FAILED (failures=1) [ran] [tree 2d697a483f2f] (2026-10-31T03:11:54Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_lanes 2>&1 | tail -4` → exit 0 · Ran 40 tests in 12.677s / OK [ran] [tree cbfdd2c5dd33] (2026-10-31T03:12:10Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_lanes 2>&1 | tail -4` → exit 0 · Ran 40 tests in 12.677s / OK [ran] [tree cbfdd2c5dd33] (2026-10-31T03:12:10Z)
- `cd plugin/tests && python3 -m unittest -q test_lanes` → ✗ exit 1 · Ran 40 tests in 12.882s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree fde14686a897] (2026-10-31T03:27:35Z)
- `cd plugin/tests && python3 -m unittest -q test_lanes` → exit 0 · Ran 40 tests in 12.493s / OK [ran] [tree fde14686a897] (2026-10-31T03:27:35Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_lanes` → exit 0 · Ran 40 tests in 12.464s / OK [ran] [tree fde14686a897] (2026-10-31T03:27:57Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_lanes` → exit 0 · Ran 40 tests in 12.487s / OK [ran] [tree d23b4b587cf2] (2026-10-31T03:28:10Z)
- (audit edge) `self: the brief no longer says git -C <worktree> (refused from the main checkout); it says message the builder first, else cd into the worktree as its own command (the guard then resolves the lane's task while it's active or verifying), else drop and redo; guard untouched; test_lanes 40 green; red-to-green proven` → a lane task that closed or blocked meanwhile gets the drop-and-redo path, named in the brief [tree d23b4b587cf2] (2026-10-31T03:28:10Z)
- (audit self) `self: the brief no longer says git -C <worktree> (refused from the main checkout); it says message the builder first, else cd into the worktree as its own command (the guard then resolves the lane's task while it's active or verifying), else drop and redo; guard untouched; test_lanes 40 green; red-to-green proven` → no findings [tree d23b4b587cf2] (2026-10-31T03:28:10Z)
## Log
- 2026-10-30T20:13:55Z created
- 2026-10-31T03:10:22Z planned from capture
- 2026-10-31T03:10:22Z set approved=True
- 2026-10-31T03:10:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2208.builder.md
- 2026-10-31T03:11:26Z focused
- 2026-10-31T03:27:08Z merged worktree-agent-a89e3933da41b6b3d (2 file(s))
- 2026-10-31T03:27:08Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a89e3933da41b6b3d
- 2026-10-31T03:27:08Z focused
- 2026-10-31T03:27:57Z scope: plugin/lib/fmlanes.py (_conflict_brief), plugin/tests/test_lanes.py, CHANGELOG.md
- 2026-10-31T03:28:36Z done
- 2026-10-31T03:28:38Z committed 42fedb8d (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower. [stale: plugin/lib/fmcore.py…
- T-2212 [FEATURE M, done, 1 steps] fm ship can't ship a lane merged after a conflict resolution: it cherry-picks the lane's… — lesson: Replay a merged branch by its first…
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar past tasks were M: consider --tier M
## Lessons
- Instructions a tool writes for its operator must be run from where the operator stands before they ship
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
