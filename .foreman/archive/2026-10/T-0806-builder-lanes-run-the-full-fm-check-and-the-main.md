---
id: T-0806
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/agents/fm-builder.md, plugin/tests/test_lanes.py]
depends_on: []
source: discovered
created: 2026-10-14T16:51:14Z
updated: 2026-10-14T17:02:38Z
base: 351996487fc40ff98505a03f1d92bf3511132482
base_tree: c233fc34bffa54721a93863b8578b1dfbb45b5a9
verified: strong
---
# Builders run only the affected tests; the full gates run once, in the main thread, after the merge
## Raw request
> Builder lanes run the full fm check and the main thread runs it again after the merge: with two lanes plus the main thread, load hit 74 and gates timed out (T-0784). Builders should run fm check --affected (the merge re-runs the full gates once)
## Interpretation
The builder brief (fmlanes.py:106) and fm-builder.md:19 have each builder run the full fm check --evidence; the main thread runs the full gates again after the merge (the delegate procedure). With two lanes and the main thread, three full gate runs shared the machine (load up to 74): doctor-calling tests timed out and two lanes reported red gates that were load. Builders run fm check --affected --evidence ID (the tests linked to their changed files) and say the full gates run after the merge.
## Assumptions (confidence)
## Acceptance criteria
- [x] the builder brief and fm-builder.md say fm check --affected --evidence ID and that the full gates run after the merge — verify with `cd plugin/tests && python3 -m unittest test_lanes`
## Non-goals
## Approach (options → choice → why)
Options: serialize gates with a machine-wide lock (slower wall clock); fewer lanes (less parallelism); affected-only in lanes (the merge's full run still decides). Chose affected-only.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing lanes test
2. [x] Brief and agent text
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_lanes.BuilderGates` → ✗ exit 1 · Ran 1 test in 0.015s / FAILED (errors=1) [ran] [tree 7e9446ec18e1] (2026-10-14T16:59:58Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_lanes.BuilderGates` → ✗ exit 1 · Ran 1 test in 0.051s / FAILED (failures=1) [ran] [tree 3d9590ab9ac6] (2026-10-14T17:00:03Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_lanes test_builder` → exit 0 · Ran 29 tests in 13.409s / OK [ran] [tree a6c8c8eec595] (2026-10-14T17:00:41Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_lanes` → exit 0 · Ran 12 tests in 4.932s / OK [ran] [tree a6c8c8eec595] (2026-10-14T17:00:46Z)
- `cd plugin/tests && python3 -m unittest test_lanes.BuilderGates` → ✗ exit 1 · Ran 1 test in 0.030s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree a6c8c8eec595] (2026-10-14T17:00:46Z)
- `cd plugin/tests && python3 -m unittest test_lanes.BuilderGates` → exit 0 · Ran 1 test in 0.009s / OK [ran] [tree a6c8c8eec595] (2026-10-14T17:00:46Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_lanes` → exit 0 · Ran 12 tests in 4.826s / OK [ran] [tree a6c8c8eec595] (2026-10-14T17:02:37Z)
- (audit edge) `self: diff read; the builder contract and fm-builder.md now say fm check --affected --evidence and that the full gates run after the merge in the main thread (the delegate flow already re-runs them); the test pins both texts` → a lane whose change has no linked tests runs no tests in the lane (affected is empty) and relies on the merge's full run, which already decides [tree a6c8c8eec595] (2026-10-14T17:02:37Z)
- (audit self) `self: diff read; the builder contract and fm-builder.md now say fm check --affected --evidence and that the full gates run after the merge in the main thread (the delegate flow already re-runs them); the test pins both texts` → no findings [tree a6c8c8eec595] (2026-10-14T17:02:37Z)
## Log
- 2026-10-14T16:51:14Z created
- 2026-10-14T16:57:12Z planned from capture
- 2026-10-14T16:59:51Z focused
- 2026-10-14T17:02:38Z done
- 2026-10-14T17:02:38Z committed b2fefa8 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0779 [PERFORMANCE S, done, 2 steps] Lane briefs pass a per-tier effort with the model — lesson: a lane's builder should record the failing run before the fix; when it …
- T-0371 [SECURITY S, done, 1 steps] Guard hook fails closed in Claude Code itself: onFailure: "block" on the PreToolUse hook (Claude Code ≥2.1.295) — lesson: A Sonnet bui…
- T-0698 [FIX M, done, 4 steps] Friction batch 2026-10-09: IFS false block from heredoc data, an undefined-name gate, MASTER.md read hint, builder refused-command list — l…
- decision 2026-10-14: [revisit: after 2026-10-15] Round 1 of the T-0760 brainstorm: build 12 briefs (T-0775..T-0786) plus the 5 discovered fixes (T-0759, T-0765, T-0767, …
- likely tests for the scope: plugin/tests/test_lanes.py
## Measurements
full gate runs per merged lane: 2 (builder + main thread after merge) → 1 (main thread); today 3 concurrent full runs drove load to 74 and timed out doctor-calling tests
## Lessons
- a gate that runs again after the merge shouldn't also run in every lane
## Plan gaps
- failed first: step 1 Failing lanes test
## Files touched
- plugin/tests/test_lanes.py
- plugin/agents/fm-builder.md
- plugin/lib/fmlanes.py
