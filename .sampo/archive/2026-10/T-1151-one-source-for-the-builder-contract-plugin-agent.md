---
id: T-1151
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/tests/test_lanes.py, plugin/agents/fm-builder.md, plugin/lib/fmlanes.py]
depends_on: []
source: discovered
created: 2026-10-16T10:16:20Z
updated: 2026-10-16T10:33:50Z
base: 358dbd8a2768e402890418cbb8e92d6bfae263e6
base_tree: fdf16603224df7bbb54e072da75dadaab69b7e34
plan0_at: 2026-10-16T10:22:21Z
plan0_scope: [plugin/tests/test_lanes.py, plugin/agents/fm-builder.md, plugin/lib/fmlanes.py]
verified: strong
---
# One source for the builder contract: plugin/agents/fm-builder.md's numbered rules duplicat
## Raw request
> One source for the builder contract: plugin/agents/fm-builder.md's numbered rules duplicate fmlanes.CONTRACT by hand and can drift; generate one from the other, or a test that compares them
## Interpretation
plugin/agents/fm-builder.md's numbered rules repeat fmlanes.CONTRACT by hand, so the two drift (T-1147 had to edit both).
## Assumptions (confidence)
## Acceptance criteria
- [x] a test fails when a CONTRACT rule is missing from fm-builder.md, and passes on the current texts — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
Keep both texts, and add a test asserting that every rule line in CONTRACT appears in fm-builder.md (normalised whitespace), so a change to one fails until the other matches. Options considered: generating the agent file at build time (the plugin ships static files), or deleting one (the agent needs it standalone, the brief needs it inline).
## Risks and rollback
## Execution prompt
## Steps
1. [x] The comparison test; align the texts where they differ
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 30 tests in 10.4s (5 classes, 16 at a time; slowest: Lanes 10s, BoardLanes 1s, SafeGitFailsClosed 0s) / FAILED (1 classes) [ran] [tree be1c101ee0b0] (2026-10-16T10:22:56Z)
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 30 tests in 15.9s (5 classes, 16 at a time; slowest: Lanes 16s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree deecd5a9a32d] (2026-10-16T10:23:29Z)
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 30 tests in 10.4s (5 classes, 16 at a time; slowest: Lanes 10s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree 916a372b80fe] (2026-10-16T10:31:44Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 30 tests in 25.2s (5 classes, 16 at a time; slowest: Lanes 25s, BoardLanes 2s, SafeGitFailsClosed 0s) / OK [ran] [tree 8499f7206c3d] (2026-10-16T10:32:16Z)
- (audit edge) `self: reviewed the merged diff; test compares each CONTRACT rule line against fm-builder.md with whitespace normalised; failed before alignment, passes now` → a rule reworded in only one file fails the test, extra lines in the agent file don't [tree 8499f7206c3d] (2026-10-16T10:32:16Z)
- (audit self) `self: reviewed the merged diff; test compares each CONTRACT rule line against fm-builder.md with whitespace normalised; failed before alignment, passes now` → no findings [tree 8499f7206c3d] (2026-10-16T10:32:16Z)
- (audit edge) `self: reviewed the merged diff; test compares each CONTRACT rule line against fm-builder.md with whitespace normalised; failed before alignment, passes now` → a rule reworded in only one file fails the test, extra lines in the agent file don't [tree 8499f7206c3d] (2026-10-16T10:33:07Z)
- (audit self) `self: reviewed the merged diff; test compares each CONTRACT rule line against fm-builder.md with whitespace normalised; failed before alignment, passes now` → no findings [tree 8499f7206c3d] (2026-10-16T10:33:07Z)
## Log
- 2026-10-16T10:16:20Z created
- 2026-10-16T10:22:07Z set scope=['plugin/tests/test_lanes.py', 'plugin/agents/fm-builder.md', 'plugin/lib/fmlanes.py']
- 2026-10-16T10:22:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1151.builder.md
- 2026-10-16T10:22:21Z focused
- 2026-10-16T10:31:18Z merged worktree-agent-ac7056dae3813f90a (2 file(s))
- 2026-10-16T10:31:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac7056dae3813f90a
- 2026-10-16T10:31:21Z focused
- 2026-10-16T10:31:50Z scope: moved test_lanes' __main__ guard to the end so a direct run reaches the later classes
- 2026-10-16T10:33:07Z scope: CHANGELOG.md line
- 2026-10-16T10:33:49Z done
- 2026-10-16T10:33:50Z committed d17015b (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0779 [PERFORMANCE S, done, 2 steps] Lane briefs pass a per-tier effort with the model — lesson: a lane's builder should record the failing run before the fix; when it …
- research t0018-final-maintainer: MEDIUM** — `~/.claude/foreman/plugin/lib/fmcli.py:607-622` (`_agent_report`) and `:625-631` (`cmd_research`) vs `:705-714` (`_…
- T-0713 [FEATURE M, done, 4 steps] Frontier 13 — Intent, planning and change skills — lesson: Generated code is safe to run only through an allowlist of AST shapes; a ren…
- decision 2026-10-14: Round 2 slate: 437 ideas in 29 clusters grounded → 3 build (compact spill cap T-0824, closed-pipe verb sweep T-0825, verb-usage evidence attached to…
- likely tests for the scope: plugin/tests/test_lanes.py
## Behaviour lock
The change adds a test and aligns doc wording; no runtime code path changed. The red run in step 1 (test failing on drifted texts) and the green run after alignment are the lock.
## Plan gaps
- failed first: step 1 The comparison test; align the texts where they differ
## Files touched
- plugin/tests/test_lanes.py
- plugin/agents/fm-builder.md
- CHANGELOG.md
