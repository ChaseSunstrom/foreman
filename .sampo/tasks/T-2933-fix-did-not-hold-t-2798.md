---
id: T-2933
type: FIX
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py, plugin/tests/test_perf_cost.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-04T08:30:24Z
updated: 2026-11-06T17:31:13Z
trigger: did-not-hold
trigger_key: d9b7abe3c2d7a06d
lane: ~/.claude/foreman/.claude/worktrees/agent-adaffb74a41ffae35
lane_branch: worktree-agent-adaffb74a41ffae35
base: 9d9fa0fbb24df1b029200903120bfec2db40d1de
base_tree: 99dd50385e0908d624cbfe75a56d634f010a38bb
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T09:32:35Z
plan0_scope: [plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py, CHANGELOG.md]
builder_returned: 2026-11-06T09:59:27Z
lane_passed: {"tree": "698321386936fe3f7c7512d4901519568d6f1b41", "cmds": ["python3 plugin/tests/run.py test_doctor"]}
---
# fm doctor's hook SLO judges PreToolUse runs taken under 0.5 load per CPU, where the hooks' own speed shows, not runs up to 1.5 that measure the machine
## Raw request
> Fix did not hold: T-2798
> did-not-hold T-2798 e8e5d23829be
> (the failure fm doctor fail hook slo: pretooluse p0 0 ms over the last 0 runs > the 0 ms slo (bench_hooks' budget); over since 0.0.0… hit 2026-11-04 after T-2798 closed: read T-2798's evidence for what it missed and fix the cause, not the symptom)
## Interpretation
T-2798 filtered at LOAD_BAR (1.5/CPU, the lane-start bar), which still lets runs at 0.5-1.5 in, where p95 is 174-269 ms vs 150 SLO; and counted load-less events as calm. Fix: a calm bar SLO_LOAD=0.5 for the SLO row only; unknown load is not calm.
## Assumptions (confidence)
## Acceptance criteria
- [ ] check_hook_slo counts only hook_ms runs with load under SLO_LOAD = 0.5 per CPU (measured 2026-11-05 over 7,420 runs: p95 103 ms under 0.25, 121 ms at 0.25-0.5, 174-269 ms at 0.5-1.5, against the 150 ms SLO), says how many it left out and why, and with fewer than 20 such runs reports 'not judged' as a pass; LOAD_BAR's other uses are unchanged — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
Add doctor.SLO_LOAD=0.5; judge only events with recorded load <= it; reword row; under 20 calm samples PASS 'not judged'. Hooks already record load. Rejected: lowering core.LOAD_BAR (other uses).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: 200 runs at load 0.3 under budget and 200 at load 1.2 over it pass; 200 at load 0.3 over budget warn
2. [ ] SLO_LOAD in doctor.check_hook_slo  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_perf_cost.HookSlo` → exit 0 · Ran 4 tests in 186.9s (1 jobs, 16 at a time; slowest: HookSlo 1s) / OK [ran] [tree bae70221342e] [world 2f1906870a] (2026-11-06T09:36:46Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_perf_cost test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [15.19s] [ran] [tree bae70221342e] [world 2f1906870a] (2026-11-06T09:42:24Z)
- (step 1) `python3 plugin/tests/run.py test_perf_cost.HookSlo` → exit 0 · Ran 4 tests in 12.3s (1 jobs, 16 at a time; slowest: HookSlo 0s) / OK [ran] [tree 698321386936] [world 2f1906870a] (2026-11-06T09:57:11Z)
## Log
- 2026-11-04T08:30:24Z created
- 2026-11-05T03:48:23Z planned from capture
- 2026-11-05T03:48:23Z set approved=True
- 2026-11-05T03:48:24Z set scope=['plugin/lib/sampo/doctor.py', 'plugin/tests/test_doctor.py', 'CHANGELOG.md']
- 2026-11-05T03:48:24Z blocked: approved; waits for a builder slot (or the main thread after T-3131 closes)
- 2026-11-06T03:53:24Z unblocked
- 2026-11-06T09:32:25Z focused
- 2026-11-06T09:32:35Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T09:33:37Z set scope=['plugin/lib/sampo/doctor.py', 'plugin/tests/test_doctor.py', 'plugin/tests/test_perf_cost.py', 'CHANGELOG.md']
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2798 [FIX M, done, 2 steps] fm doctor's hook SLO judges only PreToolUse runs taken at normal host load: each hook_ms event records load per CPU, and runs above LOAD_BA…
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (seventh): STANDING INTENT] [check: pending T-2191] The user's standing intent (on top of every earlier steer, u…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_doctor.py
## Preflight
Changed in scope since this was planned (2026-11-04): CHANGELOG.md, plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py; re-ground the plan against them before editing
