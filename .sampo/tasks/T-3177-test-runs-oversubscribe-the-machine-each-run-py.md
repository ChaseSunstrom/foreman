---
id: T-3177
type: PERFORMANCE
tier: M
status: deferred
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T08:02:23Z
updated: 2026-11-05T12:39:16Z
builder_model: haiku
lane_branch: worktree-agent-a9eb1ff9655b728cc
base: 649c130fd5512e2b371e1ec37198dca24c3ba6e4
base_tree: 292a00f436290d2480ec6112a03703feab137ac5
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-05T11:45:26Z
plan0_scope: []
builder_returned: 2026-11-05T12:27:39Z
---
# Test runs oversubscribe the machine: each run.py starts 16 workers regardless of load,…
## Raw request
> Test runs oversubscribe the machine: each run.py starts 16 workers regardless of load, so three builders' suites plus a merge put ~48+ processes on 16 CPUs (load 40-62 tonight) and every timing gate goes noisy and slow; give run.py a machine-wide worker pool (a slot lock shared by all runs) or size workers by free CPUs
## Interpretation
Reading 1 (chosen): one machine-wide cap on concurrent test jobs, shared by every run.py (builders' gates, merges, sampo check, targeted runs), so N runs together use the cores instead of oversubscribing them. Reading 2 (ruled out): fewer builders at once; the lane cap (T-3145 slots) already limits builders, and the oversubscription comes from each run's 16 workers, not the builder count.
## Assumptions (confidence)
## Acceptance criteria
- [ ] run.py takes a slot from a machine-wide pool (os.cpu_count() flock'd slot files in a per-uid dir under tempdir; FM_TEST_SLOTS_DIR overrides) before starting each job's process and frees it when the job ends; a run.py started inside a job (an env marker run_one sets) skips the pool so nested runs never deadlock; a killed run's slots free themselves (flock); FM_TEST_POOL=0 turns it off; waiting for a slot counts against the run's deadline, not the job's own timeout — verify with `python3 plugin/tests/run.py test_run`
- [ ] Measured back to back: two run.py runs of the same module list started together, pooled vs FM_TEST_POOL=0: peak concurrent job processes (sampled) at most cpu_count when pooled, and the pair's wall time recorded both ways with sampo task evidence --bench — verify with `python3 plugin/tests/run.py test_run`
## Non-goals
## Approach (options → choice → why)
1) flock'd slot files shared by every run.py: likely outcome: concurrent jobs never exceed the cores; the kernel frees a dead holder's lock, no daemon, ~30 lines in run_one. 2) use what exists: run.py's -j flag and core.load_scaled (T-3174): have sampo check pass -j from free CPUs: fails if: builders start or stop after the run sizes itself (stale within seconds), and builders' direct run.py calls don't go through check. 3) a make-style jobserver pipe: fails if: runs share no parent, and builders are independent sessions. 4) do less: lower the lane cap to 2 builders: fails if: one run's long tail leaves most cores idle, and a merge plus 2 builders still puts 48 workers on 16 cores. Choice 1 (80%): the only one that holds across independent sessions and frees itself on a crash. Deadlock guard: each job exports a marker so a run.py inside a test skips the pool.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: the pool caps concurrent jobs across two runs, nested runs skip it, a killed holder frees its slot, the opt-out
2. [x] the slot pool in run_one
3. [x] the back-to-back bench, pooled vs unpooled
## Resume here
<!-- auto -->
- 2026-11-05T12:08:57Z steps 3/3 done
- git: worktree-agent-a9eb1ff9655b728cc; 2 uncommitted: plugin/tests/run.py, plugin/tests/test_run.py
- touched since last checkpoint: .fm-scratch/bench.py, plugin/tests/test_run.py, plugin/tests/run.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_run -k Pool` → red as expected (exit 1) · Ran 10 tests in 6.9s (1 jobs, 16 at a time; slowest: Pool 2s) / FAILED (1 classes: test_run.Pool) [ran] [tree a1c6a8a11d97] [world 2f1906870a] (2026-11-05T11:47:57Z)
- (ac 1) `python3 plugin/tests/run.py test_run 2>&1 | tail -30` → exit 0 · Ran 99 tests in 17.6s (48 jobs, 16 at a time; slowest: UnknownNames 16s, Pool 15s, Bench 14s) / OK [ran] [tree 026b3c3a8673] [world 2f1906870a] (2026-11-05T11:49:06Z)
- (ac 2) `python3 plugin/tests/run.py test_run 2>&1 | tail -30` → exit 0 · Ran 99 tests in 17.6s (48 jobs, 16 at a time; slowest: UnknownNames 16s, Pool 15s, Bench 14s) / OK [ran] [tree 026b3c3a8673] [world 2f1906870a] (2026-11-05T11:49:06Z)
- (step 2) `python3 plugin/tests/run.py test_run 2>&1 | tail -30` → exit 0 · Ran 99 tests in 17.6s (48 jobs, 16 at a time; slowest: UnknownNames 16s, Pool 15s, Bench 14s) / OK [ran] [tree 026b3c3a8673] [world 2f1906870a] (2026-11-05T11:49:06Z)
- (step 2) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 100 tests in 22.0s (76 jobs, 16 at a time; slowest: Bench 15s, Repeats 11s, State 10s) / OK [ran] [tree e0a484f19a8e] [world 2f1906870a] (2026-11-05T11:50:07Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ci_annotations test_doctor test_left_out test_models test_rename_scan test_run && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 164 tests across 6 files. [70.54s] [ran] [tree e0a484f19a8e] [world 2f1906870a] (2026-11-05T11:52:31Z)
- (ac 1) `python3 plugin/tests/run.py test_run 2>&1 | tail -n 15` → exit 0 · Ran 100 tests in 11.2s (76 jobs, 16 at a time; slowest: Bench 9s, State 7s, LouhiModels 6s) / OK [ran] [tree e0a484f19a8e] [world 2f1906870a] (2026-11-05T11:53:24Z)
- (ac 2) `python3 plugin/tests/run.py test_run 2>&1 | tail -n 15` → exit 0 · Ran 100 tests in 11.2s (76 jobs, 16 at a time; slowest: Bench 9s, State 7s, LouhiModels 6s) / OK [ran] [tree e0a484f19a8e] [world 2f1906870a] (2026-11-05T11:53:24Z)
- (step 3) `python3 plugin/tests/run.py test_run 2>&1 | tail -n 15` → exit 0 · Ran 100 tests in 11.2s (76 jobs, 16 at a time; slowest: Bench 9s, State 7s, LouhiModels 6s) / OK [ran] [tree e0a484f19a8e] [world 2f1906870a] (2026-11-05T11:53:24Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ci_annotations test_doctor test_left_out test_models test_rename_scan test_run && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [17.09s] [ran] [tree e0a484f19a8e] [world 2f1906870a] (2026-11-05T11:54:42Z)
- (step 3) `python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py pooled --assert` → ✗ exit 1 · pooled: wall 18.3s · exits [0, 0] · peak jobs 16 from the pair, 22 machine-wide · os.cpu_count 16 [ran] [tree e0a484f19a8e] [world 2f1906870a] (2026-11-05T11:55:23Z)
- (step 3) `python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py pooled --assert` → exit 0 · pooled: wall 31.7s · exits [0, 0] · peak jobs 16 started by the two runs (20 with nested runs inside their jobs) · machine-wide peak seen 36 · os.cpu_count 16 [ran] [tree e0a484f19a8e] [world 2f1906870a] (2026-11-05T12:00:33Z)
- (step 3) `python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py pooled` → python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py pooled: 29.968s → 28.196s (3 runs each) [ran] [tree e0a484f19a8e] [world 2f1906870a] (2026-11-05T12:03:35Z)
- (step 3) `python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py unpooled` → python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py unpooled: 21.836s → 21.436s (3 runs each) [ran] [tree e0a484f19a8e] [world 2f1906870a] (2026-11-05T12:05:55Z)
- (step 1) `python3 plugin/tests/run.py test_run.Pool` → red as expected (exit 1) · Ran 17 tests in 30.0s (15 jobs, 16 at a time; slowest: Pool.test_a_lock_error_that_is_not_busy_runs_the_job_unpooled_without_waiting 29s, Pool.test_a_nested_run_py_inside_a_job_does_not_wait_for_the_p [ran] [tree 87385ae23a90] [world 2f1906870a] (2026-11-05T12:08:44Z)
- (ac 1) `python3 plugin/tests/run.py test_run 2>&1 | tail -n 15` → exit 0 · Ran 104 tests in 6.6s (80 jobs, 16 at a time; slowest: Pool.test_a_job_waits_for_a_slot_and_the_wait_is_not_charged_to_its_timeout 5s, Bench 5s, Ambient.test_a_full_check_waits_for_fm_ships_test_run_b [ran] [tree c4ccebc3c1b2] [world 2f1906870a] (2026-11-05T12:10:00Z)
- (ac 2) `python3 plugin/tests/run.py test_run 2>&1 | tail -n 15` → exit 0 · Ran 104 tests in 6.6s (80 jobs, 16 at a time; slowest: Pool.test_a_job_waits_for_a_slot_and_the_wait_is_not_charged_to_its_timeout 5s, Bench 5s, Ambient.test_a_full_check_waits_for_fm_ships_test_run_b [ran] [tree c4ccebc3c1b2] [world 2f1906870a] (2026-11-05T12:10:00Z)
- (step 2) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 104 tests in 5.6s (63 jobs, 16 at a time; slowest: Pool.test_a_job_waits_for_a_slot_and_the_wait_is_not_charged_to_its_timeout 5s, Hang 5s, UnknownNames 4s) / OK [ran] [tree c4ccebc3c1b2] [world 2f1906870a] (2026-11-05T12:10:13Z)
- (step 3) `python3 .fm-scratch/bench.py pooled --runs 4 --assert` → exit 0 · pooled x4: wall 58.0s · exits [0, 0, 0, 0] · peak jobs 32 started by the runs (38 with nested runs inside their jobs) · machine-wide peak seen 67 · cap 32 · os.cpu_count 16 [ran] [tree c4ccebc3c1b2] [world 2f1906870a] (2026-11-05T12:11:34Z)
- (step 3) `python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py pooled --runs 4` → python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py pooled --runs 4: 39.604s → 37.260s (3 runs each) [ran] [tree c4ccebc3c1b2] [world 2f1906870a] (2026-11-05T12:15:33Z)
- (step 3) `python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py unpooled --runs 4` → python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py unpooled --runs 4: 36.831s → 46.404s (3 runs each) [ran] [tree c4ccebc3c1b2] [world 2f1906870a] (2026-11-05T12:19:45Z)
- (step 3) `python3 .fm-scratch/bench.py pooled --runs 4` → exit 0 · ×3 runs: median 45.577s, spread ±6.098s (13%), min 39.479s, max 58.198s · pooled x4: wall 39.4s · exits [0, 0, 0, 0] · peak jobs 32 started by the runs (39 with nested runs inside their jobs) · machine-wide peak seen 39 · cap 32 · os.cpu_count 16 [ran] [tree c4ccebc3c1b2] [world 2f1906870a] (2026-11-05T12:22:18Z)
- (step 3) `FM_TEST_POOL=0 python3 .fm-scratch/bench.py unpooled --runs 4` → exit 0 · ×3 runs: median 40.240s, spread ±0.716s (2%), min 39.036s, max 40.957s · unpooled x4: wall 40.9s · exits [0, 0, 0, 0] · peak jobs 64 started by the runs (76 with nested runs inside their jobs) · machine-wide peak seen 81 · cap 32 · os.cpu_count 16 [ran] [tree c4ccebc3c1b2] [world 2f1906870a] (2026-11-05T12:24:19Z)
- (step 3) `python3 .fm-scratch/bench.py pooled --runs 2` → exit 0 · ×3 runs: median 19.130s, spread ±0.442s (2%), min 18.688s, max 20.097s · pooled x2: wall 18.7s · exits [0, 0] · peak jobs 32 started by the runs (37 with nested runs inside their jobs) · machine-wide peak seen 37 · cap 32 · os.cpu_count 16 [ran] [tree c4ccebc3c1b2] [world 2f1906870a] (2026-11-05T12:25:23Z)
- (step 3) `FM_TEST_POOL=0 python3 .fm-scratch/bench.py unpooled --runs 2` → exit 0 · ×3 runs: median 18.690s, spread ±0.428s (2%), min 17.382s, max 19.118s · unpooled x2: wall 17.4s · exits [0, 0] · peak jobs 32 started by the runs (38 with nested runs inside their jobs) · machine-wide peak seen 38 · cap 32 · os.cpu_count 16 [ran] [tree c4ccebc3c1b2] [world 2f1906870a] (2026-11-05T12:26:19Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ci_annotations test_doctor test_left_out test_models test_rename_scan test_run && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [14.05s] [ran] [tree c4ccebc3c1b2] [world 2f1906870a] (2026-11-05T12:26:47Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ci_annotations test_doctor test_left_out test_models test_rename_scan test_run && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [13.26s] [ran] [tree 53e09f3d0840] [world 2f1906870a] (2026-11-05T12:27:16Z)
## Log
- 2026-11-05T08:02:23Z created
- 2026-11-05T08:02:35Z blocked: touches run.py like T-3166 (queued to merge): plan and build after it lands
- 2026-11-05T11:44:45Z set status=planned
- 2026-11-05T11:45:12Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3177.builder.md
- 2026-11-05T11:45:25Z focused
- 2026-11-05T11:45:26Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-05T12:07:20Z sent back: slots 2x cpu_count (FM_TEST_SLOTS override), OSError fallback, 4-run bench; 2-run result 28.2 vs 21.4 s recorded as a regression at cpu_count slots
- 2026-11-05T12:39:07Z set status=deferred
- 2026-11-05T12:39:08Z parked after the 4-run bench (pooled 45.6 s vs unpooled 40.2 s median; 2 runs equal); branch worktree-agent-a9eb1ff9655b728cc kept at f5e8ec11; lane not merged
- 2026-11-05T12:39:16Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc (branch worktree-agent-a9eb1ff9655b728cc kept: not merged); dropped: parked: pool slower at 4 concurrent runs with no measured gain (decisions.md); branch kept for a revisit
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-2797 [FIX M, done, 3 steps] Gates under machine load wait or stretch instead of failing: fm lane brief holds a new lane past 1.5 load per core, and fm task finish, fm …
- T-3174 [FIX S, done, 2 steps] A full sampo check's suite gate never times out just because the machine is loaded: its deadline scales with load like targeted runs (load_…
- decision 2026-11-04: Filed gen-4's Missions 2-8 past rune step's 'build: Mission 1, focus T-2910' line instead of stopping there; the main thread builds the eight tasks …
## Measurements
python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py pooled: 29.968s → 28.196s (3 runs each)
python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py unpooled: 21.836s → 21.436s (3 runs each)
python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py pooled --runs 4: 39.604s → 37.260s (3 runs each)
python3 ~/.claude/foreman/.claude/worktrees/agent-a9eb1ff9655b728cc/.fm-scratch/bench.py unpooled --runs 4: 36.831s → 46.404s (3 runs each)
