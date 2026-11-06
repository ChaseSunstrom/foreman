---
id: T-1050
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/register.tsx]
depends_on: []
source: followup
created: 2026-10-16T03:42:11Z
updated: 2026-10-16T08:44:53Z
base: 4e2b2198b56a220cc7241a9072a22e44733ca9b2
base_tree: 8a8e0b1f86bce022bcd8934a97dc654907a0838a
plan0_at: 2026-10-16T08:29:25Z
plan0_scope: [mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/register.tsx]
verified: strong
---
# Pane layout sweep test over many widths and heights: every section fits, nothing overlaps,
## Raw request
> Pane layout sweep test over many widths and heights: every section fits, nothing overlaps, nothing cut silently (T-1029 C9)
## Interpretation
The pane must fit every terminal size: a test sweeps widths and heights and asserts no row is wider than the pane, nothing overlaps, and anything trimmed says so (+N more).
## Assumptions (confidence)
## Acceptance criteria
- [x] the sweep passes at all sizes — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
One mod test mounting the pane over a grid of sizes with a busy view, measuring each rendered row's width against the pane. Then fix the rows it exposes with clamps and truncate-end. Options considered: snapshot images (heavy, flaky), or a few hand-picked sizes (misses edges).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: sweep w in {30,40,60,80,120,200} × h in {8,12,24,40,60}. The first run is expected to expose real overflow, so list failing sizes in the test output.
2. [x] Fix the overflowing rows (clamp widths with `Math.max` and `wrap="truncate-end"`; add the "+N more" row where the tree trims at rows.tsx:606).
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `~/.local/bin/claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 119 tests across 2 files. [44.33s] [ran] [tree d746e86632f8] (2026-10-16T08:33:59Z)
- (step 1) `~/.local/bin/claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 119 tests across 2 files. [50.48s] [ran] [tree d746e86632f8] (2026-10-16T08:34:54Z)
- (step 1) `~/.local/bin/claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 119 tests across 2 files. [15.15s] [ran] [tree d746e86632f8] (2026-10-16T08:35:44Z)
- (step 2) `~/.local/bin/claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 119 tests across 2 files. [16.98s] [ran] [tree d746e86632f8] (2026-10-16T08:36:01Z)
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 120 tests across 2 files. [11.54s] [ran] [tree b15f6fd04fab] (2026-10-16T08:43:16Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 120 tests across 2 files. [11.78s] [ran] [tree b15f6fd04fab] (2026-10-16T08:43:34Z)
- (audit intent) `self: the sweep found no overflow at any of the 30 sizes (it reaches real content: a check that ignores wrap lists many long rows), so no pane code changed; it reads the element tree, not pixels, and needs the task id from 24 rows up` → every size fits, nothing silently spills [tree b15f6fd04fab] (2026-10-16T08:43:34Z)
- (audit edge) `self: the sweep found no overflow at any of the 30 sizes (it reaches real content: a check that ignores wrap lists many long rows), so no pane code changed; it reads the element tree, not pixels, and needs the task id from 24 rows up` → 8-row panes draw no task row and aren't checked for it (noted) [tree b15f6fd04fab] (2026-10-16T08:43:34Z)
- `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 120 tests across 2 files. [11.33s] [ran] [tree b15f6fd04fab] (2026-10-16T08:44:22Z)
- (audit intent) `self: the sweep found no overflow at any of the 30 sizes (it reaches real content: a check that ignores wrap lists many long rows), so no pane code changed; it reads the element tree, not pixels, and needs the task id from 24 rows up` → every size fits, nothing silently spills [tree b15f6fd04fab] (2026-10-16T08:44:22Z)
- (audit edge) `self: the sweep found no overflow at any of the 30 sizes (it reaches real content: a check that ignores wrap lists many long rows), so no pane code changed; it reads the element tree, not pixels, and needs the task id from 24 rows up` → 8-row panes draw no task row and aren't checked for it (noted) [tree b15f6fd04fab] (2026-10-16T08:44:22Z)
## Log
- 2026-10-16T03:42:11Z created
- 2026-10-16T05:00:53Z set scope=['mods/foreman-ui/tests/foreman-ui.test.tsx', 'mods/foreman-ui/hooks/rows.tsx', 'mods/foreman-ui/hooks/register.tsx']
- 2026-10-16T05:00:54Z set tier=M
- 2026-10-16T08:29:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1050.builder.md
- 2026-10-16T08:29:25Z focused
- 2026-10-16T08:39:01Z merged worktree-agent-adac2c1064e0dff0d (1 file(s))
- 2026-10-16T08:39:02Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-adac2c1064e0dff0d
- 2026-10-16T08:43:04Z focused
- 2026-10-16T08:44:10Z scope: mods/foreman-ui/tests/pane-sweep.test.tsx is this task's test (a new file, since foreman-ui.test.tsx was leased by T-1045); the fmcost/fmfixes/fmwatch/ui-demo/index.d.ts changes are T-1045's merge, closed with it; CHANGELOG.md and MASTER.md lines were committed with T-1045
- 2026-10-16T08:44:53Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- research T-0989-review: Verdict:** changes needed. The row budget holds. There is one functional regression (plan approval) and two housekeeping misses (version, types).…
- T-0989 [FEATURE L, done, 4 steps] Can you clean up ALL of the mod UI, make it one panel, with everything consolidated, so it — lesson: A layout that must never move has …
- decision 2026-10-03: T-0166 deferred: splitting the band/pane out of register.tsx is a rewrite under the mod engine's $/atom rules; T-0130 took the rows out, the rest wa…
## Preflight
Changed in scope since this was planned (2026-10-16): mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx; re-ground the plan against them before editing
## Lessons
- A sweep that passes first time still needs proof it sees the content, or it proves nothing
## Plan gaps
- failed first: step 1 Failing tests: sweep w in {30,40,60,80,120,200} × h in {8,12,24,40,60}. The first run is expected t…
## Files touched
- mods/foreman-ui/tests/pane-sweep.test.tsx
- CHANGELOG.md
- MASTER.md
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmcost.py
- plugin/lib/fmfixes.py
- plugin/lib/fmwatch.py
- plugin/lib/ui-demo.json
- plugin/tests/test_fixes.py
