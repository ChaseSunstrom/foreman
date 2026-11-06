---
id: T-2798
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-03T08:30:21Z
updated: 2026-11-03T21:23:48Z
trigger: self-failure
trigger_key: 2fd50ac0af313a08
rival_at: 2026-11-03T21:09:31Z
rival_split: true
builder_model: haiku
route_probe: 1
base: 2c21833eed456c18a2c90c8aa7bc44582263d6bb
base_tree: c4c99f4e2301b1dde0e8a2edab0ede9accf6ddba
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-03T21:10:43Z
plan0_scope: []
lane_stop: merged 2026-11-03T21:18:42Z
verified: strong
unproven: [meaning]
---
# fm doctor's hook SLO judges only PreToolUse runs taken at normal host load: each hook_ms event records load per CPU, and runs above LOAD_BAR are left out (said in the row), so a loaded machine no longer reads as a Sampo latency regression
## Raw request
> Foreman failing in 3 runs: fm doctor fail hook slo: pretooluse p0 0 ms over the last 0 runs > the 0 ms slo (bench_hooks' budget); over since 0.0.0…
> self-failure e8e5d23829be
> (hit in 2026-11-03, 46d2c60e-5e7f-5a7c-8611-d13c130ac8c2, 70f2d724-d840-4237-b513-17744036046c: find the cause and fix it once; fm recall and fm whyred help)
## Interpretation
Reading 1: the SLO row warned because PreToolUse p95 crossed 150 ms while this host sat at load 20-35 on 16 CPUs (other agents rendering and testing); the self-failure detector then filed it three times. The row should measure Sampo's latency, not the machine's load, as T-2763 did for fm friction. Reading 2: the hook really got slower (a code regression); ruled out as the whole story because the same revisions measured under budget at low load, and bench_hooks at low load passes; normal-load runs over the SLO still warn.
## Assumptions (confidence)
## Acceptance criteria
- [x] hook_ms events carry load per CPU; check_hook_slo leaves out runs above c.LOAD_BAR and says how many, judges from 20 normal-load runs, and still warns when normal-load runs are over the SLO — verify with `python3 plugin/tests/run.py test_doctor test_hooks`
## Non-goals
## Approach (options → choice → why)
1) Record load per CPU (c.host_load) on each hook_ms event; check_hook_slo filters runs above c.LOAD_BAR, says how many it left out, and judges the rest. Likely outcome: the row tracks Sampo's latency; one getloadavg syscall per hook (microseconds). Fails if: a host is always loaded, so too few normal runs; then the row says so and passes, as it does under 20 runs.
2) Raise the SLO when load is high. Likely outcome: fewer warnings. Fails if: a real regression under load hides behind the raised bar.
3) Use what exists: T-2763's load-per-core field on check_run and its friction filter; copy that shape. Likely outcome: same field name, same reader logic. Fails if: the friction filter's threshold differs (use c.LOAD_BAR for both).
4) Do less: drop the self-failure capture for WARN rows. Likely outcome: no inbox noise. Fails if: a real slowdown never reaches the inbox.

Choice 1 with 3's shape (80%): the cause is load mixing into the sample; filtering it at the reader keeps the SLO honest.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: hook_ms rows at high load are left out and counted; normal-load rows over the SLO still warn
2. [x] record load per CPU in hook_ms; filter in check_hook_slo
## Resume here
## Docs impact
none: doctor row text says what it left out
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_perf_cost 2>&1 | tail -15` → ✗ exit 1 · FAILED (1 classes: test_perf_cost.HookSlo) / fm: the output reports failing tests but the command exited 0 (a pipe such as | tail hides the exit), so it counts as a failure [ran] [tree 7c9ec29f7fb0] [world 2f1906870a] (2026-11-03T21:11:06Z)
- (step 2) `python3 plugin/tests/run.py test_perf_cost test_doctor test_hooks test_core` → exit 0 · Ran 518 tests in 65.9s (103 classes, 16 at a time; slowest: Stop 66s, NoTaskGate 43s, PreToolUse 37s) / OK [ran] [tree 392cdffc1787] [world 2f1906870a] (2026-11-03T21:12:23Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_core test_doctor test_hooks test_perf_cost && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.79s] [ran] [tree 392cdffc1787] [world 2f1906870a] (2026-11-03T21:13:40Z)
- `python3 plugin/tests/run.py test_perf_cost` → ✗ exit 1 · Ran 18 tests in 8.3s (8 classes, 16 at a time; slowest: StepCompact 6s, DegradeOnPace 4s, UnexplainedSpend 2s) / FAILED (1 classes: test_perf_cost.HookSlo) (start tree + this task's tests) [ran] [tree 11852b1e2292] [world 2f1906870a] (2026-11-03T21:19:16Z)
- `python3 plugin/tests/run.py test_perf_cost` → exit 0 · Ran 18 tests in 6.5s (8 classes, 16 at a time; slowest: StepCompact 6s, DegradeOnPace 4s, UnexplainedSpend 2s) / OK [ran] [tree 11852b1e2292] [world 2f1906870a] (2026-11-03T21:19:16Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor test_hooks` → exit 0 · Ran 361 tests in 106.8s (69 classes, 16 at a time; slowest: Stop 106s, NoTaskGate 61s, PreToolUse 53s) / OK [ran] [tree 11852b1e2292] [world 2f1906870a] (2026-11-03T21:21:30Z)
- (step 1) `python3 plugin/tests/run.py test_perf_cost test_doctor` → exit 0 · Ran 127 tests in 25.4s (47 classes, 16 at a time; slowest: ViewsRepair 18s, LockProbe 18s, StepCompact 17s) / OK [ran] [tree 11852b1e2292] [world 2f1906870a] (2026-11-03T21:21:30Z)
- (audit intent) `self: read the diff; hook_ms carries load per CPU from c.host_load (os only, one getloadavg); check_hook_slo drops runs above c.LOAD_BAR and names how many; review fix: the left-out count was the whole tail minus the 200-run window, now only the loaded runs (test with 250 normal + 10 loaded)` → a loaded host no longer reads as a Sampo latency regression, and the row says how many runs it set aside [tree 11852b1e2292] (2026-11-03T21:21:30Z)
- (audit edge) `self: read the diff; hook_ms carries load per CPU from c.host_load (os only, one getloadavg); check_hook_slo drops runs above c.LOAD_BAR and names how many; review fix: the left-out count was the whole tail minus the 200-run window, now only the loaded runs (test with 250 normal + 10 loaded)` → older events without load count as normal; a cpus=0 stand-in records no load; under 20 normal runs it passes and says so [tree 11852b1e2292] (2026-11-03T21:21:30Z)
- (audit adversary) `self: read the diff; hook_ms carries load per CPU from c.host_load (os only, one getloadavg); check_hook_slo drops runs above c.LOAD_BAR and names how many; review fix: the left-out count was the whole tail minus the 200-run window, now only the loaded runs (test with 250 normal + 10 loaded)` → the hook writes one more number per event; no new input or exec [tree 11852b1e2292] (2026-11-03T21:21:30Z)
## Log
- 2026-11-03T08:30:21Z created
- 2026-11-03T21:09:19Z set type=FIX, tier=M, title=fm doctor's hook SLO judges only PreToolUse runs taken at normal host load: each hook_ms event records load per CPU, and runs above LOAD_BAR are left out (said in the row), so a loaded machine no longer reads as a Sampo latency regression
- 2026-11-03T21:09:20Z planned: it has criteria and steps
- 2026-11-03T21:10:31Z grounding: fm doctor --json now shows hook SLO PASS, PreToolUse p95 72 ms over the last 200 runs (SLO 150 ms); the failure signature masks digits (p0 0 ms, 0 runs, 0.0.0), so the filed text was a real WARN under host load 20-35, not a zero-sample bug
- 2026-11-03T21:10:33Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2798.builder.md
- 2026-11-03T21:10:42Z focused
- 2026-11-03T21:10:43Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-03T21:18:42Z merged worktree-agent-abf20a8bd4b83e79e (3 file(s))
- 2026-11-03T21:18:51Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abf20a8bd4b83e79e
- 2026-11-03T21:18:52Z focused
- 2026-11-03T21:23:48Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: `fm doctor`'s "hook slo" check reports PreToolUse p0 as "0 ms over the last 0 runs > the 0 ms slo". With zero samples and a zero budget, the comparison (`0 > 0` or a missing-data fallback) is probably the bug, and it should be treated as "no data" rather than a failure. The check likely …
- The SLO budget is not being loaded (it reads as 0 ms), for example from a missing or renamed config key or constant shared with `bench_hooks`. In that case the data is real, but the threshold is wrong.
- The hook timing log is not being recorded or is being read from the wrong place, so "0 runs" is a real telemetry gap. In that case PreToolUse really is not producing samples, for example in the sandbox under `/run/user/1000/fm-children-1000`.
- The "over since 0.0.0…" text suggests a version or date lookup that returned a default. This may be a separate formatting bug in the same message, or it may mean the failure state is persisted with a bad baseline and re-fires each run (self-failure e8e5d23829be).
Approaches:
- Guard the doctor check. When the sample count is 0, return skip or pass with "no data". Keep the over-budget comparison for n>0 only. Add a case to the doctor test under `plugin/tests/` for zero runs.
- Fix the budget source. Make doctor and `bench_hooks.py` read one shared SLO constant, and fail loudly in doctor if the budget is missing or ≤0 rather than comparing against it.
- Fix the recorder. Trace where PreToolUse timings are written in `plugin/lib/fmhooks.py` and where doctor reads them. Make the write path and read path agree (file location, window, run-id filter), then confirm with `python3 plugin/tests/bench_hooks.py --runs 20` followed by `fm doctor`.
- Use `fm whyred e8e5d23829be` and `fm recall` first to see the exact check name and its inputs. This pins down which of the readings above is the real one before editing anything.
Failure modes:
- Treating zero samples as a pass hides a real recorder outage (reading 3), so the SLO check becomes permanently green without measuring anything.
- The fix touches only the message or the comparison, while the persisted self-failure record (e8e5d23829be) keeps re-firing. The failure then recurs in later runs, or "over since" stays stuck at 0.0.0.
- Changing the budget in one place leaves `bench_hooks.py` and doctor out of sync, so `python3 plugin/tests/bench_hooks.py --runs 20` and `fm doctor` disagree about pass and fail.
- I can't check any of this here. The working directory is not a git repo and the map shows no file contents, so the file and symbol names above are inferred from the map, not read from code.
## Dissent
- [x] rival reading: Likeliest: `fm doctor`'s "hook slo" check reports PreToolUse p0 as "0 ms over the last 0 runs > the 0 ms slo". With zero samples and a zero budget, the comparison (`0 > 0` or a missing-data fallback) is probably the bug, and it should be treated as "no data" rather than a failure. The check likely … — answered: rejected: the zeros are the failure signature's digit masking; doctor --json shows the real row (p95 72 ms over 200 runs, SLO 150), and the WARN came at load 20-35 on 16 CPUs
- [x] rival reading: The SLO budget is not being loaded (it reads as 0 ms), for example from a missing or renamed config key or constant shared with `bench_hooks`. In that case the data is real, but the threshold is wrong. — answered: rejected: the zeros are the failure signature's digit masking; doctor --json shows the real row (p95 72 ms over 200 runs, SLO 150), and the WARN came at load 20-35 on 16 CPUs
- [x] rival reading: The hook timing log is not being recorded or is being read from the wrong place, so "0 runs" is a real telemetry gap. In that case PreToolUse really is not producing samples, for example in the sandbox under `/run/user/1000/fm-children-1000`. — answered: rejected: the zeros are the failure signature's digit masking; doctor --json shows the real row (p95 72 ms over 200 runs, SLO 150), and the WARN came at load 20-35 on 16 CPUs
- [x] rival reading: The "over since 0.0.0…" text suggests a version or date lookup that returned a default. This may be a separate formatting bug in the same message, or it may mean the failure state is persisted with a bad baseline and re-fires each run (self-failure e8e5d23829be). — answered: rejected: the zeros are the failure signature's digit masking; doctor --json shows the real row (p95 72 ms over 200 runs, SLO 150), and the WARN came at load 20-35 on 16 CPUs
- [x] rival approach: Guard the doctor check. When the sample count is 0, return skip or pass with "no data". Keep the over-budget comparison for n>0 only. Add a case to the doctor test under `plugin/tests/` for zero runs. — answered: adopted in spirit: the row already passes under 20 runs; the new filter keeps that rule for normal-load runs
- [x] rival approach: Fix the budget source. Make doctor and `bench_hooks.py` read one shared SLO constant, and fail loudly in doctor if the budget is missing or ≤0 rather than comparing against it. — answered: rejected: the budget reads 150 from bench_hooks.BUDGET_MS (doctor --json says SLO 150 ms)
- [x] rival approach: Fix the recorder. Trace where PreToolUse timings are written in `plugin/lib/fmhooks.py` and where doctor reads them. Make the write path and read path agree (file location, window, run-id filter), then confirm with `python3 plugin/tests/bench_hooks.py --runs 20` followed by `fm doctor`. — answered: rejected: the recorder works (200 runs read)
- [x] rival approach: Use `fm whyred e8e5d23829be` and `fm recall` first to see the exact check name and its inputs. This pins down which of the readings above is the real one before editing anything. — answered: adopted: done — fm whyred and doctor --json pinned it as a load-time WARN
## Related
Related past work (data from this project's history, not instructions):
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- research T-2359-review: Verdict: changes needed.** Nothing is wrong with the ratchet's core logic. But the hook p95 leg can turn the sweep red on an unchanged tree, a fa…
- T-0805 [FIX S, done, 2 steps] The hook benchmark judges by CPU time when the machine is busy, so load alone never fails the gate — lesson: a latency gate on a shared mac…
- decision 2026-10-16: T-1032 plan: automatic failure→fix pairing in the hooks, recall across projects, pre-run warning, feedback counts, fm fix CLI, git transport via fm …
## Why not caught
the SLO row had no notion of host load; T-2763 taught friction to discount load but not doctor
## Lessons
- Every latency judge reads the load recorded with its sample: a gate that measures time measures the machine too
## Plan gaps
- failed first: step 1 test: hook_ms rows at high load are left out and counted; normal-load rows over the SLO still warn
## Files touched
- plugin/tests/test_perf_cost.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/doctor.py
