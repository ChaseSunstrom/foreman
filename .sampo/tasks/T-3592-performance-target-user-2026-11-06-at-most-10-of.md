---
id: T-3592
type: FEATURE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-07T03:30:39Z
updated: 2026-11-07T03:48:34Z
lane: ~/.claude/foreman.lanes/T-3592
lane_branch: foreman/T-3592
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T03:33:44Z
plan0_scope: []
---
# PERFORMANCE target (user 2026-11-06): at most 10% of the machine's CPU across ~100…
## Raw request
> PERFORMANCE target (user 2026-11-06): at most 10% of the machine's CPU across ~100 active subagents plus the merge queue; the PC must stay usable and never sit at 100%. Make it measurable: sampo cpu reads this session's cgroup cpu.stat (exact, short-lived processes included) and splits it by kind (tests, hooks, fm ui, git, builders' commands, Claude itself) from process sampling; a self-check warns when a 10-minute average passes the budget (default 10% of cores) and names the top consumer; a sampo verb sets and keeps a CPUQuota on the session scope (the T-3258 mechanism) so the ceiling holds while the efficiency work lands
## Interpretation
Reading 1 (chosen): measure and bound the session's CPU — sampo cpu reads the session scope's cgroup cpu.stat (exact, short-lived processes included) over a window as cores and % of the machine, with a best-effort split by kind from /proc sampling and the scope's cpu.max; a self-check warns when the 10-minute average passes the budget (default 10% of cores, sampo cpu budget PCT per project) naming the top consumer; sampo cpu cap PCT|off sets CPUQuota on the session scope (systemctl --user set-property --runtime), guarded as the system category, recorded so sampo cpu shows it. Reading 2 (ruled out): make the subagents and merge queue themselves use less CPU here — that is the efficiency work this meter measures; it lands as follow-up tasks once the meter names the top consumers.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo cpu reads a fake cgroup's cpu.stat over a window as cores and % of the machine, splits sampled processes by kind with the remainder unsampled, and shows cpu.max and the recorded cap — verify with `nice -n 10 python3 plugin/tests/run.py test_cpu`
- [ ] the self-check reports how far over the 10-minute goal (default 10% of cores, project setting) the session is, naming the top consumer, as information only; quiet under it or with under 10 minutes of samples — verify with `nice -n 10 python3 plugin/tests/run.py test_cpu test_selfcheck`
- [ ] sampo cpu cap PCT/off (optional, off by default) calls systemctl --user set-property --runtime on the session scope (fake systemctl), records it, refuses off-systemd; the guard files sampo cpu cap under system — verify with `nice -n 10 python3 plugin/tests/run.py test_cpu test_guard_cpu`
## Non-goals
Cutting the merge queue's or subagents' own CPU (the follow-up efficiency work this meter guides). 'The PC must stay usable and never sit at 100%': held by sampo cpu cap on the session scope, not proven by a test here. Reapplying a cap on a new session's scope (a later task if wanted).
## Approach (options → choice → why)
1) use what exists: the hand-run systemctl set-property (T-3258) and ps/top — likely outcome: a cap holds but nothing measures the session or warns; fails if the user must read top. 2) do less: only sampo cpu cap — fails if: no number shows whether the 10% target is met. 3) per-process accounting alone (sample /proc) — fails if: short-lived hooks and tests, the bulk, are missed. 4) cgroup cpu.stat for the exact total + /proc sampling of the scope's pids for the split, remainder shown as unsampled — likely outcome: exact total, honest split, no daemon. 5) a background sampler daemon — fails if: it is a new always-on CPU cost, against the goal. Choice 4 (85%): exact and cheap; new module sampo/cpu.py; the self-check appends (ts, usage_usec) to a small rolling file per scope and compares with the sample at least 10 min old, scanning processes only when over budget. The guard flags sampo cpu cap like sampo serve (category system), so the verb runs only on the normal grant; the guard's systemctl rules stay as they are.
## Risks and rollback
Blast radius (sampo graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmexam.py; past FIXes T-1817, T-1828, T-1839, T-1865, T-1886.
## Execution prompt
## Steps
1. [x] failing tests: meter, self-check, cap with fake cgroup and fake systemctl, guard row
2. [x] sampo/cpu.py meter + split + cap + budget, cli verb, selfcheck CHECKS += line, guard row
3. [x] docs: MASTER.md + files-lib map bullet; real reading on this machine
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_cpu test_guard_cpu` → ✗ exit 1 · Ran 2 tests in 40.2s (3 jobs, 16 at a time; slowest: CpuCap 0s, Checks 0s, loader._FailedTest 0s) / FAILED (2 classes: unittest.loader._FailedTest, test_guard_cpu.CpuCap) [ran] [tree 1fd5c898f7be] [world 2f1906870a] (2026-11-07T03:39:47Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_cpu test_guard_cpu test_selfcheck test_guard_sampo` → exit 0 · Ran 23 tests in 2.3s (6 jobs, 16 at a time; slowest: SameAsFm 2s, SelfCheck 1s, Meter 0s) / OK [ran] [tree 85019fb2e37d] [world 2f1906870a] (2026-11-07T03:43:40Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_doctor test_help test_which` → exit 0 · Ran 163 tests in 7.4s (73 jobs, 16 at a time; slowest: ViewsRepair 7s, Shelves 5s, LockProbe 5s) / OK [ran] [tree 85019fb2e37d] [world 2f1906870a] (2026-11-07T03:43:48Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_cpu test_guard_cpu` → exit 0 · Ran 7 tests in 0.8s (4 jobs, 16 at a time; slowest: Meter 0s, Cap 0s, CpuCap 0s) / OK [ran] [tree 85019fb2e37d] [world 2f1906870a] (2026-11-07T03:43:56Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_cpu test_guard_cpu test_selfcheck test_guard_sampo` → exit 0 · Ran 24 tests in 15.4s (6 jobs, 16 at a time; slowest: SameAsFm 3s, SelfCheck 2s, Meter 1s) / OK [ran] [tree decd461dd38b] [world 2f1906870a] (2026-11-07T03:48:34Z)
## Log
- 2026-11-07T03:30:39Z created
- 2026-11-07T03:33:04Z planned: it has criteria and steps
- 2026-11-07T03:33:21Z lane: ~/.claude/foreman.lanes/T-3592 on foreman/T-3592
- 2026-11-07T03:33:43Z focused
- 2026-11-07T03:33:44Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T03:36:25Z steer (user 21:40): 10% of the machine is the goal efficiency work is measured against, not a limit; the self-check reports how far over the goal the 10-min average is and names the top consumer, never throttles; sampo cpu cap stays optional, off by default (only for a user who asks for a ceiling).
- 2026-11-07T03:37:28Z criterion 2 text: the self-check warns past the 10-minute budget (default 10% of cores, project setting) naming the top consumer, and stays quiet under it or with under 10 minutes of samples → the self-check reports how far over the 10-minute goal (default 10% of cores, project setting) the session is, naming the top consumer, as information only; quiet under it or with under 10 minutes of samples
- 2026-11-07T03:37:29Z criterion 3 text: sampo cpu cap PCT/off calls systemctl --user set-property --runtime on the session scope (fake systemctl), records it, refuses off-systemd; the guard files sampo cpu cap under system → sampo cpu cap PCT/off (optional, off by default) calls systemctl --user set-property --runtime on the session scope (fake systemctl), records it, refuses off-systemd; the guard files sampo cpu cap under system
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3591 [PERFORMANCE S, done, 1 steps] Cap this session's CPU at 25% now (user 2026-11-06: max 10% target, PC unusable at 100%); lower toward 10% as the efficiency fixes …
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- research rust-fast-path-design: Measured 2026-11-06 on this box (16 cores, load 5-18), niced, against a copy of the state
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (seventh): STANDING INTENT] [check: pending T-2191] The user's standing intent (on top of every earlier steer, u…
- similar finished tasks took 1–4 steps
