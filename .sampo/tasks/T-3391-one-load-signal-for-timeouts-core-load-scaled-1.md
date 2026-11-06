---
id: T-3391
type: CLEAN
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:54:37Z
updated: 2026-11-06T10:09:36Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a44a6d8d156401580
lane_branch: worktree-agent-a44a6d8d156401580
base: 9d9fa0fbb24df1b029200903120bfec2db40d1de
base_tree: 99dd50385e0908d624cbfe75a56d634f010a38bb
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T09:33:19Z
plan0_scope: []
builder_returned: 2026-11-06T10:09:36Z
---
# One load signal for timeouts: core.load_scaled (1-min average) and helpers.busy_factor…
## Raw request
> CLEAN: one load signal for timeouts: core.load_scaled (1-min average) and helpers.busy_factor (instant runnable count) disagree under bursts, so gates and run.py scale differently (T-3338 review)
## Interpretation
Reading 1: one function core.load_factor used by load_scaled, helpers.busy_factor and run.py. Reading 2: only alias one to the other.
## Assumptions (confidence)
## Acceptance criteria
- [ ] load_scaled and busy_factor give one factor for the same host state — verify with `python3 plugin/tests/run.py test_lanes.LoadGates test_run.Load`
## Non-goals
## Approach (options → choice → why)
1) keep both, document; fails if: still disagree 2) use what exists: busy_factor delegates to load_scaled; fails if: loses instant runnable 3) do less: only load_scaled uses runnable; fails if: tests differ. Choice 2b (80%): core.load_factor = max(avg, runnable)/cpus clamped; load_scaled and busy_factor both call it; FOREMAN_HOST gains optional runnable=; helpers' calm default reads real host.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test first, then core.load_factor + callers
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.LoadGates test_run.Load` → ✗ exit 1 · Ran 12 tests in 278.0s (2 jobs, 16 at a time; slowest: LoadGates 2s, Load 1s) / FAILED (1 classes: test_lanes.LoadGates) [ran] [tree 18f168456056] [world 2f1906870a] (2026-11-06T09:38:33Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.LoadGates test_run.Load` → exit 0 · Ran 12 tests in 57.5s (2 jobs, 16 at a time; slowest: LoadGates 2s, Load 1s) / OK [ran] [tree 7b952c0e1875] [world 2f1906870a] (2026-11-06T09:39:39Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_core test_doctor test_lanes test_left_out test_models test_rename_scan test_run test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [22.02s] [ran] [tree 7b952c0e1875] [world 2f1906870a] (2026-11-06T09:48:21Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.LoadGates test_run.Load` → exit 0 · Ran 12 tests in 40.9s (2 jobs, 16 at a time; slowest: LoadGates 1s, Load 0s) / OK [ran] [tree 1f5f825867fd] [world 2f1906870a] (2026-11-06T10:04:36Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_doctor test_kalevala test_lanes test_left_out test_louhi_models test_mint test_models test_rename_scan test_run test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [13.63s] [ran] [tree 1f5f825867fd] [world 2f1906870a] (2026-11-06T10:09:26Z)
## Log
- 2026-11-06T06:54:37Z created
- 2026-11-06T09:33:09Z planned: it has criteria and steps
- 2026-11-06T09:33:15Z focused
- 2026-11-06T09:33:19Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T09:33:53Z criterion 1 verify: `python3 plugin/tests/run.py test_lanes.GateLoadTests 2>&1` → `python3 plugin/tests/run.py test_lanes.LoadGates test_run.Load`
## Follow-ups captured
## Behaviour lock
test_lanes test_a_gate_scales_its_timeout_by_load_per_cpu_and_never_shrinks_it and test_run test_hang_guards_stretch_with_the_load_and_stay_bounded pin both signals today.
## Related
Related past work (data from this project's history, not instructions):
- T-2826 [FIX M, done, 0 steps] test_demo.DemoNext fails in the full suite under close-time load (3 of 3 runs during…
- T-3382 [FIX M, active, 1 steps] test_check_paths.CheckSkip: 6 of 7 tests time out at load ~30+ on fm task evidence / fm…
- T-3338 [FIX S, done, 2 steps] Test runner under load: run.py scales each class's timer with busy_factor (the --deadline clamp unchanged) and records a killed class's tim…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- similar finished tasks took 0–2 steps
