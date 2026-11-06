---
id: T-3087
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/tests/test_cli.py]
depends_on: []
source: self
created: 2026-11-05T00:46:14Z
updated: 2026-11-05T08:18:28Z
builder_model: haiku
route_probe: 1
base: cfa46b093f192b127dcba69839028a7d2dcafb44
base_tree: dae032d6b1feb68bc5b0d7916ad2fb1e84cfd3c9
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T01:16:18Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/tests/test_cli.py]
lane_stop: merged 2026-11-05T06:53:49Z
verified: strong
unproven: [docs]
---
# Sampo task new --from ID overwrites a planned task's title, tier, criteria and steps…
## Raw request
> sampo task new --from ID overwrites a planned task's title, tier, criteria and steps (cli.py:3321-3358): refuse --from on a planned task with criteria unless --replan is given; keep captured → planned working
## Interpretation
Reading 1 (taken): sampo task new --from ID on a planned task with criteria silently re-plans it (cli.py:3321-3358); refuse unless --replan, keep captured → planned. Reading 2 (ruled out): make --from always create a child: breaks the captured → planned path the intake uses.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo task new --from ID refuses a planned task that has criteria unless --replan is given, naming the flag; a captured task still becomes planned — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
1) use what exists: a guard at cli.py:3321 plus a --replan flag: likely outcome: a few lines. 2) do less: a warning only: fails if: the overwrite still happens (it did, three times on T-3042). Choice 1 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] guard and flag (test first)
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_cli 2>&1 | tail -8` → ✗ exit 1 · Ran 147 tests in 50.3s (45 classes, 16 at a time; slowest: TaskLifecycle 49s, CaptureAndIntake 32s, StateViews 28s) / FAILED (1 classes: test_cli.CaptureAndIntake) [ran] [tree b17aa2772292] [world 2f1906870a] (2026-11-05T01:17:35Z)
- (ac 1) `python3 plugin/tests/run.py test_cli 2>&1 | grep -B3 -A18 "^FAIL:"` → ✗ exit 1 · Ran 23 tests in 12.578s / FAILED (failures=1) [ran] [tree b17aa2772292] [world 2f1906870a] (2026-11-05T01:18:01Z)
- (step 1) `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 147 tests in 26.5s (45 classes, 16 at a time; slowest: TaskLifecycle 26s, CaptureAndIntake 12s, StateViews 10s) / FAILED (1 classes: test_cli.CaptureAndIntake) [ran] [tree e58c13f7c144] [world 2f1906870a] (2026-11-05T01:18:35Z)
- (step 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 147 tests in 24.0s (45 classes, 16 at a time; slowest: TaskLifecycle 24s, CaptureAndIntake 12s, StateViews 11s) / OK [ran] [tree ef099285520f] [world 2f1906870a] (2026-11-05T01:19:32Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 149 tests in 56.0s (45 classes, 16 at a time; slowest: TaskLifecycle 55s, CaptureAndIntake 35s, StateViews 33s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:45:06Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 149 tests in 91.6s (45 classes, 16 at a time; slowest: TaskLifecycle 80s, CaptureAndIntake 38s, StateViews 31s) / FAILED (3 classes: test_cli.TaskLifecycle, test_cli.CaptureAndIntake, test_cli.Red (start tree + this task's tests) [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:56:49Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 149 tests in 111.8s (45 classes, 16 at a time; slowest: TaskLifecycle 111s, CaptureAndIntake 51s, StateViews 48s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:56:49Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T07:56:49Z [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T08:16:14Z)
- (audit edge) `batch lane (T-3087, T-3088, T-3089) reviewed and merged; test_cli re-run on main green; red→green proved; full check green` → sampo task new --from on a planned task with evidence refuses to overwrite it; a captured one is planned as before [tree 9ff1569cf979] (2026-11-05T08:16:14Z)
- (audit self) `batch lane (T-3087, T-3088, T-3089) reviewed and merged; test_cli re-run on main green; red→green proved; full check green` → no findings [tree 9ff1569cf979] (2026-11-05T08:16:14Z)
## Log
- 2026-11-05T00:46:14Z created
- 2026-11-05T00:56:32Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_cli.py']
- 2026-11-05T00:56:34Z planned: it has criteria and steps
- 2026-11-05T00:56:44Z set approved=True
- 2026-11-05T01:16:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3087.builder.md
- 2026-11-05T01:16:16Z focused
- 2026-11-05T01:16:18Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T01:20:40Z paused: focus moved to T-3088
- 2026-11-05T06:53:49Z merged worktree-agent-a0cb64f7e606afe90 (18 file(s))
- 2026-11-05T06:53:49Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0cb64f7e606afe90
- 2026-11-05T07:43:59Z focused
- 2026-11-05T07:59:23Z scope: files outside its globs came from other tasks' merges and closes landing between the batch's merge and this close
- 2026-11-05T08:18:28Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3088 [FIX S, planned, 1 steps] Sampo task drop drops an active or verifying task silently (cli.py:1057-1066): refuse…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- decision 2026-11-03: SAMPO_X moves into FOREMAN_X when sampo.core loads and leaves the environment (SAMPO wins); FOREMAN_X is not copied back to SAMPO_X
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
## Preflight
Changed in scope since this was planned (2026-11-05): plugin/lib/sampo/cli.py, plugin/tests/test_cli.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 guard and flag (test first)
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/sampo/cli.py
- plugin/skills/next/SKILL.md
- plugin/tests/test_batch_edit.py
- plugin/tests/test_contract.py
- plugin/tests/test_docs.py
- plugin/tests/test_handoff.py
- plugin/tests/test_hunks.py
- plugin/tests/test_judgment.py
- plugin/tests/test_rewind.py
- plugin/tests/test_robustness.py
- plugin/tests/test_scout.py
- plugin/tests/test_second.py
- plugin/tests/test_snapshots.py
- plugin/tests/test_task_ergonomics.py
- plugin/tests/test_visibility.py
