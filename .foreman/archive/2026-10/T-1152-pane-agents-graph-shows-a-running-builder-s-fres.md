---
id: T-1152
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmwatch.py, plugin/tests/test_ui.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-16T10:23:41Z
updated: 2026-10-16T10:31:04Z
base: 48b0dfc7a7f9ca0160ce3add6214fdc432938ec4
base_tree: 16315f879933b06df8aa94658a87e84d3944d6d3
plan0_at: 2026-10-16T10:24:19Z
plan0_scope: [plugin/lib/fmwatch.py, plugin/tests/test_ui.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md]
verified: strong
---
# Pane Agents graph shows a running builder's fresh worktree as 'merged': a branch with no c
## Raw request
> Pane Agents graph shows a running builder's fresh worktree as 'merged': a branch with no commits beyond HEAD passes the is-ancestor test; seen with 4 live builders (T-1145, T-1146, T-1149, T-1151) all reading 'merged'
## Interpretation
The Agents graph marks a worktree 'merged' when its branch has 0 commits beyond HEAD. A fresh builder's branch has none yet, so four running builders all read 'merged'.
## Assumptions (confidence)
## Acceptance criteria
- [x] a lane whose task is open and has no commits reads 'working', not 'merged'; a closed task's lane with none ahead still reads 'merged' — verify with `python3 plugin/tests/run.py test_ui`
- [x] the pane draws 'working' for such a lane — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
fm ui's worktree rows carry 'open': the lane's task exists and isn't closed. The pane shows 'working' for an open lane with nothing ahead, and 'merged' only when its task is closed (or it has no task). No extra git call per poll.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests (view 'open', pane 'working') then the field and the label
## Resume here
<!-- auto -->
- 2026-10-16T10:27:08Z steps 1/1 done
- git: foreman/build; 5 uncommitted: mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/lib/fmwatch.py, plugin/tests/test_ui.py
- touched since last checkpoint: plugin/tests/test_ui.py, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/hooks/register.tsx, plugin/lib/fmwatch.py, mods/foreman-ui/types/index.d.ts
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ui test_board_surfaces` → exit 0 · Ran 30 tests in 11.7s (7 classes, 16 at a time; slowest: UiView 12s, BoardSurfaces 2s, UiSkills 1s) / OK [ran] [tree 542268ae06a5] (2026-10-16T10:26:23Z)
- (ac 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 124 tests across 2 files. [11.98s] [ran] [tree 542268ae06a5] (2026-10-16T10:26:36Z)
- (ac 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 124 tests across 2 files. [10.61s] [ran] [tree 1a78abe6574a] (2026-10-16T10:29:03Z)
- (ac 1) `python3 plugin/tests/run.py test_ui` → exit 0 · Ran 24 tests in 11.2s (7 classes, 16 at a time; slowest: UiView 11s, UiSkills 1s, CloseOut 1s) / OK [ran] [tree 1a78abe6574a] (2026-10-16T10:29:15Z)
- `python3 plugin/tests/run.py test_ui` → ✗ exit 1 · Ran 24 tests in 11.2s (7 classes, 16 at a time; slowest: UiView 11s, UiSkills 1s, SkillRoute 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 1a78abe6574a] (2026-10-16T10:29:42Z)
- `python3 plugin/tests/run.py test_ui` → exit 0 · Ran 24 tests in 10.9s (7 classes, 16 at a time; slowest: UiView 11s, UiSkills 1s, SkillRoute 1s) / OK [ran] [tree 1a78abe6574a] (2026-10-16T10:29:42Z)
- (ac 1) `python3 plugin/tests/run.py test_ui` → exit 0 · Ran 24 tests in 22.4s (7 classes, 16 at a time; slowest: UiView 22s, UiSkills 2s, CloseOut 2s) / OK [ran] [tree fdf16603224d] (2026-10-16T10:30:23Z)
- (ac 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 124 tests across 2 files. [10.88s] [ran] [tree fdf16603224d] (2026-10-16T10:30:23Z)
- (audit edge) `self: open flag comes from the lane task's open state; closed lanes with none ahead still read merged (test_ui); pane test asserts working and no merged` → lane with no task id → open False → merged, as before; ahead>0 wins over open [tree fdf16603224d] (2026-10-16T10:30:23Z)
- (audit self) `self: open flag comes from the lane task's open state; closed lanes with none ahead still read merged (test_ui); pane test asserts working and no merged` → no findings [tree fdf16603224d] (2026-10-16T10:30:23Z)
## Log
- 2026-10-16T10:23:41Z created
- 2026-10-16T10:24:18Z set scope=['plugin/lib/fmwatch.py', 'plugin/tests/test_ui.py', 'mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/types/index.d.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'CHANGELOG.md']
- 2026-10-16T10:24:19Z focused
- 2026-10-16T10:31:04Z done
- 2026-10-16T10:31:04Z committed 358dbd8 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-1023 [FEATURE M, done, 4 steps] Can you have a graph of sub agents/worktrees/brainstorms? — lesson: A list kept for a time window must be filtered at every draw, not o…
- T-1119 [FEATURE S, done, 2 steps] Pane flag for a stopped builder: its lane node shows 'stopped · fm lane resume ID' (fm ui — lesson: A state the CLI already knows (stop…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
## Files touched
- plugin/tests/test_ui.py
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- plugin/lib/fmwatch.py
- mods/foreman-ui/types/index.d.ts
- CHANGELOG.md
