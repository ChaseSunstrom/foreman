---
id: T-3332
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/kalevala.py, plugin/tests/test_kalevala.py]
depends_on: []
source: discovered
created: 2026-11-06T04:32:01Z
updated: 2026-11-06T06:57:14Z
lane: ~/.claude/foreman/.claude/worktrees/agent-acd1b9b94054d0907
lane_branch: worktree-agent-acd1b9b94054d0907
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: 1b9837219c451629fdffd9906b71771442a157e6
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T06:27:01Z
plan0_scope: [plugin/lib/sampo/kalevala.py, plugin/tests/test_kalevala.py]
builder_returned: 2026-11-06T06:57:14Z
---
# Kalevala: _decide and the restarted check run outside the project lock, so two concurrent steps can snapshot a tower twice and log an act twice
## Raw request
> Kalevala: _decide and the restarted check run outside the project lock, so two concurrent steps can snapshot a tower twice and log an act twice
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] two concurrent kalevala.step calls on one project log each act once and snapshot a stalled tower once — verify with `python3 plugin/tests/run.py test_kalevala`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] concurrency test, red  <- CURRENT
2. [x] take c.lock around _decide and the restarted check (kalevala.py:228-230, :584)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_kalevala.KalevalaWatch.test_two_concurrent_steps_snapshot_a_stalled_tower_and_log_its_restart_once` → ✗ exit 1 · Ran 1 tests in 91.6s (1 jobs, 16 at a time; slowest: KalevalaWatch 1s) / FAILED (1 classes: test_kalevala.KalevalaWatch) (ran] (tree 066f746bb15e] (world 2f1906870a] (2026-11-06T06:29:11Z)
- (step 2) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 71 tests in 203.7s (9 jobs, 16 at a time; slowest: KalevalaStep 12s, KalevalaWatch 4s, Kalevala 2s) / OK (ran] (tree 95ccfd8ea349] (world 2f1906870a] (2026-11-06T06:32:50Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala` → ✗ exit 1 · Ran 72 tests in 37.0s (9 jobs, 16 at a time; slowest: KalevalaStep 12s, KalevalaWatch 5s, Kalevala 2s) / FAILED (1 classes: test_kalevala.KalevalaWatch) (ran] (tree 309c26711f19] (world 2f1906870a] (2026-11-06T06:54:16Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 72 tests in 131.3s (9 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, KalevalaGen 2s) / OK (ran] (tree e63f8e020e33] (world 2f1906870a] (2026-11-06T06:56:44Z)
## Log
- 2026-11-06T04:32:01Z created
- 2026-11-06T06:26:58Z focused
- 2026-11-06T06:27:01Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T06:53:30Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3326 [FEATURE M, planned, 3 steps] Headroom part 2: Kalevala opens towers for new Frame areas, at most 2 a generation, each an act with an undo
- T-2555 [FEATURE S, done, 2 steps] fm ship retries its push when main moved between the last check and the push, through the same re-pick check, up to 3 tries — lesson: a…
- T-3081 [FEATURE M, done, 4 steps] Kalevala part 2: the towers per aspect, seeded and sealed, run at once as jobs; Kalevala's own generations and the capability registry …
- decision 2026-11-06: Recommendation: none to act on; route to plugin/lib/sampo/ rather than the fm*.py aliases, and drop the aliases when their two releases end (T-2742)…
- similar finished tasks took 2–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_kalevala.py
## Preflight
Changed in scope since this was planned (2026-11-06): plugin/lib/sampo/kalevala.py, plugin/tests/test_kalevala.py; re-ground the plan against them before editing
