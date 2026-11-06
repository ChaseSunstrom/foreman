---
id: T-0812
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-14T17:50:20Z
updated: 2026-10-14T17:59:07Z
base: 2aac7dbb124c04b48e9c750ed4e28fb446a28093
base_tree: 8f752e6c98e7c75e2cf987dcda7630dcd6841cd3
verified: strong
---
# Close warnings: the tier-drift size counts only the task's real diff, and CC's empty .claude/worktrees/ is never 'left behind'
## Raw request
> Close warnings: the tier-drift size counts only the task's real diff, and CC's empty .claude/worktrees/ is never 'left behind'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a lane-merged task's drift counts its numstat lines, not whole files; .claude/worktrees/ isn't reported as left behind — verify with `python3 plugin/tests/run.py test_safety test_planning test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test reproducing the 7,354-line count and the worktrees warning
2. [x] Fix _tier_drift and _CACHES
## Resume here
## Docs impact
none: internal close checks
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_safety test_planning test_lanes` → exit 0 · Ran 34 tests in 5.7s (16 classes, 16 at a time; slowest: Lanes 6s, UsualMinutes 1s, CleanupGate 1s) / OK [ran] [tree 5f647d91911c] (2026-10-14T17:56:34Z)
- (step 2) `python3 plugin/tests/run.py test_safety test_planning test_lanes` → exit 0 · Ran 34 tests in 5.8s (16 classes, 16 at a time; slowest: Lanes 6s, UsualMinutes 1s, CleanupGate 1s) / OK [ran] [tree 5f647d91911c] (2026-10-14T17:56:40Z)
- `python3 plugin/tests/run.py test_safety test_planning test_lanes` → ✗ exit 1 · Ran 34 tests in 6.1s (16 classes, 16 at a time; slowest: Lanes 6s, UsualMinutes 1s, TierDrift 1s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree 5f647d91911c] (2026-10-14T17:56:54Z)
- `python3 plugin/tests/run.py test_safety test_planning test_lanes` → exit 0 · Ran 34 tests in 5.8s (16 classes, 16 at a time; slowest: Lanes 6s, UsualMinutes 1s, CleanupGate 1s) / OK [ran] [tree 5f647d91911c] (2026-10-14T17:56:54Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.0    34.8     150  [0] / SessionEnd                  30.2    32.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree 5f647d91911c] (2026-10-14T17:58:45Z)
- (ac 1) `python3 plugin/tests/run.py test_safety test_planning test_lanes` → exit 0 · Ran 34 tests in 5.9s (16 classes, 16 at a time; slowest: Lanes 6s, UsualMinutes 1s, CleanupGate 1s) / OK [ran] [tree 5f647d91911c] (2026-10-14T17:59:06Z)
- (audit edge) `self: root-caused T-0777's 7,354-line warning (base_tree re-snapshotted at focus after the lane merge, so the diff held only the post-merge test edit; files absent from numstat were counted whole as new); retro secret scan of every file changed this session (40) found only the fake sk-ant fixtures in test_page.py's redaction test` → main checkout with uncommitted non-clashing changes at merge — base_tree is the pre-merge working snapshot (worktree_tree), so they still don't count as the task's; a touched file deleted since start stays counted by numstat [tree 5f647d91911c] (2026-10-14T17:59:06Z)
- (audit self) `self: root-caused T-0777's 7,354-line warning (base_tree re-snapshotted at focus after the lane merge, so the diff held only the post-merge test edit; files absent from numstat were counted whole as new); retro secret scan of every file changed this session (40) found only the fake sk-ant fixtures in test_page.py's redaction test` → no findings [tree 5f647d91911c] (2026-10-14T17:59:06Z)
## Log
- 2026-10-14T17:50:20Z created
- 2026-10-14T17:50:20Z focused
- 2026-10-14T17:54:18Z user approved core in Claude Code's permission prompt
- 2026-10-14T17:57:00Z criterion 1 verify: `python3 plugin/tests/run.py test_finish` → `python3 plugin/tests/run.py test_safety test_planning test_lanes`
- 2026-10-14T17:59:07Z done
- 2026-10-14T17:59:07Z committed faa491c (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0488 [FEATURE M, done, 0 steps] Scope and intent drift (C050, value 3/5, effort M, risk low)
- T-0558 [FEATURE M, dropped, 0 steps] Scope and intent drift (C050, value 3/5, effort M, risk low)
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- decision 2026-10-04: Bench-family inbox items (T-0231 judge, T-0240 duels, T-0241 counterfactual, T-0242 regression court, T-0243 shadow-user soak) are built together as…
- similar past tasks were M: consider --tier M
- similar finished tasks took 0–3 steps
## Lessons
- A start point re-taken after a merge hides the merged work from every close check; set it at merge time
## Files touched
- plugin/tests/test_safety.py
- plugin/tests/test_planning.py
- plugin/tests/test_lanes.py
- plugin/lib/fmcli.py
- plugin/lib/fmlanes.py
