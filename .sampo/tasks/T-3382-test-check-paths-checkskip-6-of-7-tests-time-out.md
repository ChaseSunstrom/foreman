---
id: T-3382
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:41:39Z
updated: 2026-11-06T21:59:33Z
lane_branch: worktree-agent-aaef5cc538514050f
base: 19cf45dc02be51d02cca75532c0a953687420bda
base_tree: f7e92771539040aa709b2972758be9d5f52b3845
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T08:46:53Z
plan0_scope: []
builder_returned: 2026-11-06T08:54:38Z
---
# test_check_paths.CheckSkip: 6 of 7 tests time out at load ~30+ on fm task evidence / fm…
## Raw request
> FIX: test_check_paths.CheckSkip: 6 of 7 tests time out at load ~30+ on fm task evidence / fm check subprocess calls (50-67 s caps), in the spirit of T-3367: scale those caps with busy_factor or stub the load (T-3338 builder)
## Interpretation
Reading 1: the 50-67 s caps are fixed subprocess timeouts to scale. Reading 2: they are fm's own load wait (core.wait_for_load, max 60 s per evidence/check call); helpers.fm's cap already scales by busy_factor, so Reading 2 is the cause.
## Assumptions (confidence)
## Acceptance criteria
- [ ] CheckSkip passes with load ~30 and no load wait — verify with `python3 plugin/tests/run.py test_check_paths.CheckSkip`
## Non-goals
## Approach (options → choice → why)
1) Scale caps with busy_factor: already done in helpers.fm; likely outcome: no change, still slow. 2) Stub FOREMAN_HOST; fails if fm still waits on the fake load. 3) FOREMAN_LOAD_GATE=0 in CheckSkip's fm calls; likely outcome: no wait, hang cap stays. 4) do less: leave it, fails if load stays high. Choice 3 (85%): the tests are not about load and it is the existing switch.
## Risks and rollback
## Execution prompt
## Steps
1. [x] CheckSkip.fm passes FOREMAN_LOAD_GATE=0
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_check_paths.CheckSkip` → exit 0 · Ran 8 tests in 56.0s (8 jobs, 16 at a time; slowest: CheckSkip.test_a_committed_test_file_is_shared_and_still_runs 24s, CheckSkip.test_run_py_leaves_out_the_named_modules 21s, CheckSkip.test_an_inheri [ran] [tree 3f3523bbc10a] [world 2f1906870a] (2026-11-06T08:48:41Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_check_paths test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 229 tests in 55.6s (71 jobs, 16 at a time; slowest: CheckSkip.test_a_red_test_in_this_tasks_scope_still_runs 55s, CheckSkip.test_a_look_alike_tests_folder_proves_nothing_about_the_gates_own 55s, C [ran] [tree 3f3523bbc10a] [world 2f1906870a] (2026-11-06T08:49:46Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_check_paths test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [32.03s] [ran] [tree 3f3523bbc10a] [world 2f1906870a] (2026-11-06T08:53:26Z)
## Log
- 2026-11-06T06:41:39Z created
- 2026-11-06T08:46:40Z planned: it has criteria and steps
- 2026-11-06T08:46:52Z focused
- 2026-11-06T08:46:53Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T17:43:23Z dropped: superseded by T-3442: CheckSkip's timeouts were nested run.py runs queuing on the machine-wide slot pool (FOREMAN_SLOT never read), fixed at the cause; this lane's two commits add and then revert a load-gate override, so it carries no change
- 2026-11-06T17:43:23Z work at drop saved: a74f7440847b (restore: git -C ~/.claude/foreman restore --source=a74f7440847b --worktree -- :/)
- 2026-11-06T21:59:33Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aaef5cc538514050f (branch worktree-agent-aaef5cc538514050f kept: not merged); dropped: its task is closed; the lane was left behind after the merge
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3338 [FIX S, active, 2 steps] Test runner under load: run.py scales each class's timer with busy_factor (the --deadline clamp unchanged) and records a killed class's t…
- T-2797 [FIX M, done, 3 steps] Gates under machine load wait or stretch instead of failing: fm lane brief holds a new lane past 1.5 load per core, and fm task finish, fm …
- T-3144 [PERFORMANCE S, done, 2 steps] Targeted runs never wait for load: task evidence, check --affected and a finish's criterion checks run at once with a load-scaled t…
- decision 2026-11-05: [costly] T-3177 parked, branch kept (f5e8ec11): the machine-wide test slot pool at 2x cpu matches unpooled at 2 concurrent runs (19.1 vs 18.7 s) and…
