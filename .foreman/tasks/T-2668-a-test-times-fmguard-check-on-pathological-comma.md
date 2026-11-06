---
id: T-2668
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T20:44:49Z
updated: 2026-11-02T21:09:15Z
builder_model: haiku
route_probe: 1
lane_branch: worktree-agent-af2bfab1c337c7fc2
base: 6716f9643748e59cddc470562a16753eaa827391
base_tree: 8b2ef9d9d02678c8a155e6435212d0d171dbc158
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T20:46:09Z
plan0_scope: []
lane_stop: refused 2026-11-02T20:58:51Z
verified: strong
---
# a test times fmguard.check on pathological commands and fails on any over its bar; a planted quadratic pattern proves it can fail
## Raw request
> FEATURE: a test times fmguard.check on pathological commands (long quoted runs, deep nesting, many heredocs, 50k-char lines) and fails on any over its bar, with a planted quadratic pattern proving the test can fail
> CONTEXT: Genesis gen-3 Mission 5 (#12 staying lean and safe), gen-3/mission-staying-lean-and-safe.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_guard_latency runs fmguard.check on long quoted runs, deep nesting, many heredocs and 50k-char lines, each under its bar, and a planted quadratic regex wired into the same harness fails it — verify with `python3 plugin/tests/run.py test_guard_latency`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the latency test with its pathological cases and the planted-quadratic self-check
2. [x] fix any case over its bar at its root (or capture it if it's a design change), CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_guard_latency 2>&1 | tail -15` → exit 0 · Ran 2 tests in 9.6s (1 classes, 16 at a time; slowest: Latency 9s) / OK [ran] [tree c367f49f3e97] [world 2f1906870a] (2026-11-02T20:53:47Z)
- (step 1) `python3 plugin/tests/run.py test_guard_latency 2>&1 | tail -15` → exit 0 · Ran 2 tests in 9.6s (1 classes, 16 at a time; slowest: Latency 9s) / OK [ran] [tree c367f49f3e97] [world 2f1906870a] (2026-11-02T20:53:47Z)
- (step 1) `python3 plugin/tests/run.py test_guard_latency` → exit 0 · Ran 2 tests in 9.9s (1 classes, 16 at a time; slowest: Latency 9s) / OK [ran] [tree c367f49f3e97] [world 2f1906870a] (2026-11-02T20:54:00Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_approve_reads test_guard test_guard_diff test_guard_evasions test_guard_exec_vectors test_guard_git test_guard_latency test_guard_pipes test_settings_scopes && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [20.44s] [ran] [tree c367f49f3e97] [world 2f1906870a] (2026-11-02T20:54:45Z)
- `python3 plugin/tests/run.py test_guard_latency` → ✗ exit 1 · Ran 0 tests in 481.5s (1 classes, 16 at a time; slowest: Latency 480s) / FAILED (1 classes: test_guard_latency.Latency) (start tree + this task's tests) [ran] [tree c1c40937f4d7] [world 2f1906870a] (2026-11-02T21:08:08Z)
- `python3 plugin/tests/run.py test_guard_latency` → exit 0 · Ran 2 tests in 3.3s (1 classes, 16 at a time; slowest: Latency 3s) / OK [ran] [tree c1c40937f4d7] [world 2f1906870a] (2026-11-02T21:08:08Z)
- (step 1) `python3 plugin/tests/run.py test_guard_latency test_guard test_guard_evasions` → exit 0 · Ran 319 tests in 8.5s (95 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 5s, Trust 4s) / OK [ran] [tree c1c40937f4d7] [world 2f1906870a] (2026-11-02T21:08:24Z)
- (step 2) `python3 plugin/tests/run.py test_guard_latency test_guard test_guard_evasions` → exit 0 · Ran 319 tests in 8.6s (95 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 5s, Trust 4s) / OK [ran] [tree c1c40937f4d7] [world 2f1906870a] (2026-11-02T21:08:33Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_latency` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T21:08:08Z [ran] [tree c1c40937f4d7] [world 2f1906870a] (2026-11-02T21:08:34Z)
- (audit adversary) `self: landed the builder's branch by hand after fm lane merge refused on a red criterion in the worktree; replaced the planted check's fixed 4 s bar (1.5x margin, machine-dependent) with one scaled to this machine's own check time; the nesting cap returns the guard's existing refusal tuple` → the cap fails closed (a refusal, never an allow); quotes are ignored so a quoted run of 9+ $( is refused too, which errs safe [tree c1c40937f4d7] (2026-11-02T21:08:34Z)
- (audit edge) `self: landed the builder's branch by hand after fm lane merge refused on a red criterion in the worktree; replaced the planted check's fixed 4 s bar (1.5x margin, machine-dependent) with one scaled to this machine's own check time; the nesting cap returns the guard's existing refusal tuple` → the start tree hung 480 s on the 500-deep case (the red run); 10k ;-joined commands is the slowest at 1.46 s CPU, linear [tree c1c40937f4d7] (2026-11-02T21:08:34Z)
- (audit self) `self: landed the builder's branch by hand after fm lane merge refused on a red criterion in the worktree; replaced the planted check's fixed 4 s bar (1.5x margin, machine-dependent) with one scaled to this machine's own check time; the nesting cap returns the guard's existing refusal tuple` → no findings [tree c1c40937f4d7] (2026-11-02T21:08:34Z)
## Log
- 2026-11-02T20:44:49Z created
- 2026-11-02T20:45:32Z planned from capture
- 2026-11-02T20:45:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2668.builder.md
- 2026-11-02T20:46:09Z focused
- 2026-11-02T20:46:09Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T20:58:51Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af2bfab1c337c7fc2 (branch worktree-agent-af2bfab1c337c7fc2 kept: not merged)
- 2026-11-02T20:58:51Z focused
- 2026-11-02T20:58:52Z scope: plugin/lib/fmguard.py (the hang the test found: >8 nested $( refused at once), CHANGELOG.md
- 2026-11-02T21:09:13Z done
- 2026-11-02T21:09:15Z committed 34a23208 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2666 [RESEARCH M, done, 3 steps] Genesis gen-3 Mission 5 (#12 staying lean and safe): ground the 525-idea brainstorm, record the catalogue, file the Mission and intake…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-11-02: Recommendation: Mission 5 builds three measured gaps (burden counts hook_success SessionStart context and splits it by source; a guard latency test …
- T-2461 [CLEAN L, done, 5 steps] Lean: fold six verbs into the verbs that already hold their job (proof → prove --rollup, triggers → outcomes --triggers, calibration → ou…
## Files touched
- plugin/tests/test_guard_latency.py
- .fm-scratch/probe.py
- .fm-scratch/nest.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MOONSHOT.md
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- plugin/lib/fmserve.py
- plugin/tests/test_burden_sources.py
- plugin/tests/test_serve.py
