---
id: T-3142
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/agents/fm-builder.md, plugin/tests/test_builder.py]
depends_on: []
source: discovered
created: 2026-11-05T04:56:58Z
updated: 2026-11-05T05:35:40Z
base: 9bb63c17fb770e1f5c44063ed82b088c495eb852
base_tree: ede7eb5b3ebe6b2f29dcd1efed0e73895c5e1baf
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T05:03:54Z
plan0_scope: [plugin/agents/fm-builder.md, plugin/tests/test_builder.py]
verified: strong
unproven: [docs]
---
# A builder whose worktree starts ahead of its brief's BASE (main moved between brief and launch) builds on it when BASE is an ancestor, instead of stopping
## Raw request
> fm-builder contract: a builder whose worktree HEAD descends from the brief's BASE (main moved after the brief was written) stops and asks; accept a HEAD that has BASE as an ancestor and say so, or have lane brief record main's HEAD at launch (T-3126's builder stopped on 2026-11-05 when T-3135 committed between its brief and its launch)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm-builder.md's base rule: HEAD equal to BASE, or BASE an ancestor of HEAD (say so in the report), builds; HEAD behind BASE fast-forwards as today; anything else stops and reports both commits; the contract copy lanes.contract() carries the same text — verify with `python3 plugin/tests/run.py test_builder test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: the contract text names the ancestor case
2. [x] the rule in fm-builder.md
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_builder` → ✗ exit 1 · Ran 28 tests in 42.2s (9 classes, 16 at a time; slowest: Contract 39s, Brief 21s, LaneMergeGate 12s) / FAILED (1 classes: test_builder.Brief) [ran] [tree fa45ae4e0288] [world 2f1906870a] (2026-11-05T05:05:26Z)
- (step 2) `python3 plugin/tests/run.py test_builder test_lanes` → exit 0 · Ran 186 tests in 55.1s (22 classes, 16 at a time; slowest: Lanes 55s, LaneRecovery 44s, RaceEvidence 36s) / OK [ran] [tree e2aa1b52f5b7] [world 2f1906870a] (2026-11-05T05:10:16Z)
- (ac 1) `python3 plugin/tests/run.py test_builder test_lanes` → exit 0 · Ran 186 tests in 34.0s (22 classes, 16 at a time; slowest: Lanes 34s, LaneRecovery 27s, RaceEvidence 15s) / OK [ran] [tree e2aa1b52f5b7] [world 2f1906870a] (2026-11-05T05:10:56Z)
- (step 1) `python3 plugin/tests/run.py test_builder test_lanes` → exit 0 · Ran 187 tests in 55.6s (22 classes, 16 at a time; slowest: Lanes 55s, LaneRecovery 37s, RaceEvidence 26s) / OK [ran] [tree 39051bf1655c] [world 2f1906870a] (2026-11-05T05:30:54Z)
- `python3 plugin/tests/run.py test_builder` → ✗ exit 1 · Ran 28 tests in 15.7s (9 classes, 16 at a time; slowest: Contract 13s, Brief 6s, LaneMergeGate 4s) / FAILED (1 classes: test_builder.Brief) (start tree + this task's tests) [ran] [tree 39051bf1655c] [world 2f1906870a] (2026-11-05T05:31:28Z)
- `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 28 tests in 17.2s (9 classes, 16 at a time; slowest: Contract 17s, Brief 7s, LaneMergeGate 5s) / OK [ran] [tree 39051bf1655c] [world 2f1906870a] (2026-11-05T05:31:28Z)
- (ac 1) `python3 plugin/tests/run.py test_builder test_lanes` → exit 0 · Ran 187 tests in 34.4s (22 classes, 16 at a time; slowest: Lanes 34s, LaneRecovery 27s, RaceEvidence 17s) / OK [ran] [tree 4761a60076dc] [world 2f1906870a] (2026-11-05T05:34:40Z)
- (audit edge) `self: one sentence in the contract adds the BASE-is-ancestor-of-HEAD case between the fast-forward case and the stop; lanes.contract() reads the same file, so the brief carries it; the merge side already checks ancestry` → a worktree that diverged from BASE (neither is an ancestor) still stops and reports both commits [tree 4761a60076dc] (2026-11-05T05:34:40Z)
- (audit self) `self: one sentence in the contract adds the BASE-is-ancestor-of-HEAD case between the fast-forward case and the stop; lanes.contract() reads the same file, so the brief carries it; the merge side already checks ancestry` → no findings [tree 4761a60076dc] (2026-11-05T05:34:40Z)
## Log
- 2026-11-05T04:56:58Z created
- 2026-11-05T05:03:44Z planned from capture
- 2026-11-05T05:03:45Z set approved=True
- 2026-11-05T05:03:45Z set scope=['plugin/agents/fm-builder.md', 'plugin/tests/test_builder.py']
- 2026-11-05T05:03:53Z focused
- 2026-11-05T05:03:54Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T05:13:02Z paused: focus moved to T-3145
- 2026-11-05T05:28:39Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-05T05:28:39Z focused
- 2026-11-05T05:35:38Z done
- 2026-11-05T05:35:40Z committed cc8559af (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- research T-2038-review: Verdict: approve with nits.** The acceptance tests cover the two stated behaviours: a clean, quiet lane that is ahead gets a merge line, and a di…
- T-2334 [FIX M, done, 2 steps] A task always gets a start point: a git timeout at focus or at finish is retried, never read as no start commit — lesson: A timeout is not …
- decision 2026-11-04: Filed gen-4's Missions 2-8 past rune step's 'build: Mission 1, focus T-2910' line instead of stopping there; the main thread builds the eight tasks …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_agents.py, plugin/tests/test_audit.py, plugin/tests/test_builder.py, plugin/tests/test_claims.py, plugin/tests/test_claude.py, plugin/test…
## Plan gaps
- failed first: step 1 failing test: the contract text names the ancestor case
## Files touched
- plugin/tests/test_builder.py
- plugin/agents/fm-builder.md
