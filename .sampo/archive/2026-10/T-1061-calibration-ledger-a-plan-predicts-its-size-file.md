---
id: T-1061
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmoutcomes.py, plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/tests/test_outcomes.py, plugin/tests/test_planning.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T07:17:05Z
base: 23ee9a3c7c5ede9e85e97ec1a88b2b9ac55013dc
base_tree: dc17c1c275d5731c8c10d3b62bee6cf251c375e0
plan0_at: 2026-10-16T07:14:19Z
plan0_scope: [plugin/lib/fmoutcomes.py, plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/tests/test_outcomes.py, plugin/tests/test_planning.py]
verified: strong
---
# Calibration ledger: a plan predicts its size (files touched, minutes, attempts); the close
## Raw request
> FEATURE: Calibration ledger: a plan predicts its size (files touched, minutes, attempts); the close compares; a project whose predictions keep missing gets a slower autonomy (approval for M) until they recover (wild C2)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
A plan states predicted files touched, minutes, and attempts. The close compares them with what happened and records a calibration event. When the last 5+ closes mostly missed, the project's autonomy slows, so M tier needs approval until the closes recover. Present: `planned`/`changed` file counts already recorded at close (fmcli.py:600; the digest uses them at fmcost.py:367); the Brier calibration over stated confidence (fmoutcomes.py:134); `needs_approval` (fmcore.py:1866), which only gates L and explore items. Missing: minute and attempt predictions, a miss rule, and the slowdown.
## Assumptions (confidence)
## Acceptance criteria
- [x] After 5 missed closes an M brief reports needing plan approval; after 3 good closes it doesn't. — verify with `python3 plugin/tests/run.py test_outcomes test_planning`
## Non-goals
## Approach (options → choice → why)
(a) a new calibration module, (b) extend fmoutcomes plus `needs_approval`, (c) a meta flag set at close. Choice is (b). Add `predict_minutes=` and `predict_attempts=` task fields (via `fm task set`). Add `misses(p)` in fmoutcomes.py, which scores the last 8 closes. A close misses when changed > 2×planned, or minutes > 2×predicted, or attempts > predicted. A project is "slow" at ≥5 closes and ≥60% missed, and the digest prints a "Calibration ledger" line. The autonomy value is computed at fmcore.py:2478 and 2568; return "slow" there. `needs_approval` then gates tier M when autonomy is "slow" (not for full autonomy).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: seed `task_done` events carrying planned/changed/predictions. Assert `outcomes.misses` is true at 3 of 5 and false at 1 of 5. Assert `needs_approval(M, "slow")` is true and `needs_approval(S, "slow")` is false. Assert `fm digest` shows the "slows to approval for M" line.
2. [x] Record the predictions in the `task_done` data at fmcli.py:600; add `misses()` and the `slow_autonomy()` helper; wire up the two autonomy lines in fmcore.py and `needs_approval`.
## Resume here
## Docs impact
CHANGELOG.md; plugin/skills/intake/references/planning.md (Size line)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_planning` → ✗ exit 1 · Ran 12 tests in 3.4s (9 classes, 16 at a time; slowest: UsualMinutes 3s, TierDrift 3s, AssumptionCheck 2s) / FAILED (1 classes) [ran] [tree 4b40fa0a0fbb] (2026-10-16T06:48:19Z)
- (step 2) `python3 plugin/tests/run.py test_outcomes test_planning` → exit 0 · Ran 27 tests in 11.3s (18 classes, 16 at a time; slowest: Survival 11s, Outcomes 3s, TrackRecord 3s) / OK [ran] [tree 5c3e619f6123] (2026-10-16T06:49:16Z)
- (step 2) `python3 plugin/tests/run.py test_outcomes test_planning test_hooks` → exit 0 · Ran 187 tests in 63.2s (38 classes, 16 at a time; slowest: Stop 63s, PreToolUse 40s, SessionStart 32s) / OK [ran] [tree 2af9e95b78ed] (2026-10-16T06:59:27Z)
- (step 2) `python3 plugin/tests/run.py test_outcomes test_planning` → exit 0 · Ran 33 tests in 26.9s (18 classes, 16 at a time; slowest: Survival 27s, CalibrationLedger 7s, Outcomes 4s) / OK [ran] [tree dec98401f60d] (2026-10-16T07:07:17Z)
- (ac 1) `python3 plugin/tests/run.py test_outcomes test_planning` → exit 0 · Ran 33 tests in 20.6s (18 classes, 16 at a time; slowest: Survival 20s, CalibrationLedger 8s, Reopen 6s) / OK [ran] [tree 396b337b8330] (2026-10-16T07:16:18Z)
- (step 1) `python3 plugin/tests/run.py test_outcomes test_planning test_hooks test_cost_forecast` → ✗ exit 1 · Ran 197 tests in 84.0s (40 classes, 16 at a time; slowest: Stop 84s, PreToolUse 58s, SessionStart 41s) / FAILED (1 classes) [ran] [tree 396b337b8330] (2026-10-16T07:16:18Z)
- (step 1) `python3 plugin/tests/run.py test_outcomes test_planning test_hooks` → exit 0 · Ran 189 tests in 37.4s (38 classes, 16 at a time; slowest: Stop 37s, PreToolUse 20s, SessionStart 16s) / OK [ran] [tree 396b337b8330] (2026-10-16T07:17:03Z)
- (audit intent) `review: two fm-reviewer passes; round 1: 8 findings (bypassing readers, circular files signal, editable predictions, missing-focus minutes, window cost/recovery, wording, validation); round 2: 5 (self-approval wording, wall-clock minutes, panic disagreement, lock, malformed verdicts) — all fixed by the builder; merge conflicts with T-1083/T-1085/T-1063 resolved keeping both sides` → a run of plans that miss slows autonomy until plans land again [tree 396b337b8330] (2026-10-16T07:17:03Z)
- (audit adversary) `review: two fm-reviewer passes; round 1: 8 findings (bypassing readers, circular files signal, editable predictions, missing-focus minutes, window cost/recovery, wording, validation); round 2: 5 (self-approval wording, wall-clock minutes, panic disagreement, lock, malformed verdicts) — all fixed by the builder; merge conflicts with T-1083/T-1085/T-1063 resolved keeping both sides` → predictions frozen at first focus; the gap message sends approval to the user, never self-approval [tree 396b337b8330] (2026-10-16T07:17:03Z)
- (audit edge) `review: two fm-reviewer passes; round 1: 8 findings (bypassing readers, circular files signal, editable predictions, missing-focus minutes, window cost/recovery, wording, validation); round 2: 5 (self-approval wording, wall-clock minutes, panic disagreement, lock, malformed verdicts) — all fixed by the builder; merge conflicts with T-1083/T-1085/T-1063 resolved keeping both sides` → no-focus closes omit minutes; idle gaps over 30 min don't count; malformed verdicts ignored; panic agrees everywhere [tree 396b337b8330] (2026-10-16T07:17:03Z)
- (audit operator) `review: two fm-reviewer passes; round 1: 8 findings (bypassing readers, circular files signal, editable predictions, missing-focus minutes, window cost/recovery, wording, validation); round 2: 5 (self-approval wording, wall-clock minutes, panic disagreement, lock, malformed verdicts) — all fixed by the builder; merge conflicts with T-1083/T-1085/T-1063 resolved keeping both sides` → last 5 verdicts in meta, 14-day horizon, O(1) per turn; fm autonomy shows slow and why [tree 396b337b8330] (2026-10-16T07:17:03Z)
- (audit maintainer) `review: two fm-reviewer passes; round 1: 8 findings (bypassing readers, circular files signal, editable predictions, missing-focus minutes, window cost/recovery, wording, validation); round 2: 5 (self-approval wording, wall-clock minutes, panic disagreement, lock, malformed verdicts) — all fixed by the builder; merge conflicts with T-1083/T-1085/T-1063 resolved keeping both sides` → effective_autonomy is the one reader every approval path uses [tree 396b337b8330] (2026-10-16T07:17:03Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:22:49Z set scope=['plugin/lib/fmoutcomes.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmcost.py', 'plugin/tests/test_outcomes.py', 'plugin/tests/test_planning.py']
- 2026-10-16T04:22:49Z set tier=L
- 2026-10-16T05:13:21Z set tier=M
- 2026-10-16T06:47:18Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1061.builder.md
- 2026-10-16T06:47:26Z focused
- 2026-10-16T07:10:59Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7c99dba9ce0fd2fd (branch worktree-agent-a7c99dba9ce0fd2fd kept: not merged)
- 2026-10-16T07:11:15Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1061.builder.md
- 2026-10-16T07:11:24Z focused
- 2026-10-16T07:14:12Z merged worktree-agent-aeb6aa53ca55c8a6b (10 file(s))
- 2026-10-16T07:14:17Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aeb6aa53ca55c8a6b
- 2026-10-16T07:14:19Z focused
- 2026-10-16T07:14:32Z scope: CHANGELOG.md — release note; the merge (with conflicts resolved by a builder) brought fmhooks, fmlanes, fmserve, planning.md and test changes
- 2026-10-16T07:17:04Z affected tests waived: the linked tests include test_cost_forecast, which holds T-1083's red-first tests in this checkout (the T-1101 skip covers fm check, not the close's linked run)
- 2026-10-16T07:17:04Z done
- 2026-10-16T07:17:05Z committed fa1674a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_outcomes.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py, plugin/lib/fmoutcomes.py, plugin/tests/test_outcomes.py, plugin/tests/test_planning.py; re-ground the plan against them before editing
## Lessons
- A self-regulating gate needs one reader every path uses, or the paths that skip it make it a lie
## Plan gaps
- failed first: step 1 Failing tests: seed `task_done` events carrying planned/changed/predictions. Assert `outcomes.misse…
## Files touched
- plugin/tests/test_planning.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmcost.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmlanes.py
- plugin/lib/fmhooks.py
- plugin/lib/fmserve.py
- plugin/tests/test_hooks.py
- plugin/skills/intake/references/planning.md
- CHANGELOG.md
