---
id: T-1078
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmwatch.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/lib/ui-demo.json, plugin/tests/test_splits.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T09:22:16Z
base: 56f910e69aaccf69826cfa5b34b36fbecc996e47
base_tree: 405e02a1877b26d197fa12f80252e1c3acf7c150
plan0_at: 2026-10-16T09:13:22Z
plan0_scope: [plugin/lib/fmwatch.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/lib/ui-demo.json, plugin/tests/test_splits.py]
verified: strong
---
# Pane speedrun splits: each stage's time against the project's typical time, green or red,
## Raw request
> FEATURE: Pane speedrun splits: each stage's time against the project's typical time, green or red, in the pane's task block (wild C22)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
The pane's task block shows speedrun splits: time in each stage (planning, executing, verifying…) for the active task against the project's typical time for that type and tier, green when under and red when over.
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm ui --json` active has splits with typical and a sign per stage — verify with `python3 plugin/tests/run.py test_splits`
- [x] the pane shows the splits in the task block — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
fmwatch.splits() computes stage durations from ledger stage events, with medians over closed same type/tier tasks (at least 3 samples). fm ui carries it in active.splits; the mod renders one compact row. Options considered: a separate pane section (the user wants less clutter), or totals only (no per-stage signal).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: seed a ledger with 3 closed FIX/M tasks and an active one whose executing stage is slow. `splits` has an executing entry with `delta>0`. Stages with fewer than 3 samples have no typical value. Pane test: a split row renders for each stage and the over-typical one uses the err colour.
2. [x] Add `splits()` to `fmwatch.py` and wire it into `view()`.
3. [x] Add the TS type and the rendering in `register.tsx`.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_splits` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Splits 0s) / FAILED (1 classes) [ran] [tree 8642100fe13d] (2026-10-16T09:14:11Z)
- (step 2) `python3 plugin/tests/run.py test_splits` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Splits 1s) / OK [ran] [tree a6bef8c55867] (2026-10-16T09:15:34Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 121 tests across 2 files. [10.89s] [ran] [tree 8f5f9710cd04] (2026-10-16T09:16:33Z)
- (step 1) `python3 plugin/tests/run.py test_splits test_ui test_board_surfaces` → exit 0 · Ran 31 tests in 11.5s (8 classes, 16 at a time; slowest: UiView 11s, BoardSurfaces 2s, UiSkills 1s) / OK [ran] [tree 6971269dceab] (2026-10-16T09:21:12Z)
- (ac 1) `python3 plugin/tests/run.py test_splits` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Splits 0s) / OK [ran] [tree c6c48ab54c1f] (2026-10-16T09:21:44Z)
- (ac 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 121 tests across 2 files. [10.80s] [ran] [tree c6c48ab54c1f] (2026-10-16T09:21:44Z)
- (audit intent) `self review of the branch: fm ui measured 328 → 338 ms median over 5 runs (inside the 20 ms limit); typical needs 3 samples; stage times are proxies from ledger marks, said in the docs and captured as T-1137; pane row colours tested (over C.err, under C.ok, no typical no delta)` → see at a glance which stage is running long [tree c6c48ab54c1f] (2026-10-16T09:21:44Z)
- (audit edge) `self review of the branch: fm ui measured 328 → 338 ms median over 5 runs (inside the 20 ms limit); typical needs 3 samples; stage times are proxies from ledger marks, said in the docs and captured as T-1137; pane row colours tested (over C.err, under C.ok, no typical no delta)` → fewer than 3 samples shows no typical; tasks missing marks show fewer stages [tree c6c48ab54c1f] (2026-10-16T09:21:44Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T05:01:20Z set scope=['plugin/lib/fmwatch.py', 'mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/types/index.d.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'plugin/lib/ui-demo.json', 'plugin/tests/test_splits.py']
- 2026-10-16T05:01:20Z set tier=M
- 2026-10-16T09:13:15Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1078.builder.md
- 2026-10-16T09:13:22Z focused
- 2026-10-16T09:20:48Z merged worktree-agent-a9c724b3817277c24 (6 file(s))
- 2026-10-16T09:20:53Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9c724b3817277c24
- 2026-10-16T09:20:59Z focused
- 2026-10-16T09:21:31Z scope: CHANGELOG.md, MASTER.md — docs; plugin/lib/ui-demo.json — the demo carries every view key
- 2026-10-16T09:22:16Z done
- 2026-10-16T09:22:16Z committed ca85d4d (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
## Preflight
Changed in scope since this was planned (2026-10-16): mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/lib/fmwatch.py, plugin/lib/ui-demo.json, plugin/tests/test_splits.py; re-ground the plan against them before editing
## Lessons
- A derived metric should say where it is approximate, and the cheap record that would make it exact should be captured
## Plan gaps
- failed first: step 1 Failing tests: seed a ledger with 3 closed FIX/M tasks and an active one whose executing stage is s…
## Files touched
- plugin/tests/test_splits.py
- plugin/lib/fmwatch.py
- plugin/lib/ui-demo.json
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/types/index.d.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- CHANGELOG.md
- MASTER.md
