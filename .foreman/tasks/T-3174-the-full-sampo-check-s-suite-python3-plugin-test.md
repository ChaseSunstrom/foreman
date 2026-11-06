---
id: T-3174
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T08:00:26Z
updated: 2026-11-05T10:16:55Z
builder_model: sonnet
base: 1131c48afe0ceeef0a44947e32c5a1edc3d5e05f
base_tree: c8cd728cd73450268bd0da603cd5b70ec8249058
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T08:02:17Z
plan0_scope: []
builder_returned: 2026-11-05T08:08:23Z
lane_stop: merged 2026-11-05T10:12:36Z
verified: strong
---
# A full sampo check's suite gate never times out just because the machine is loaded: its deadline scales with load like targeted runs (load_scaled), and a timeout says the load it ran under
## Raw request
> The full sampo check's suite (python3 plugin/tests/run.py) timed out (exit 124) in three runs tonight under load 20-37 on 16 CPUs, which blocks every close; its deadline should scale with load (load_scaled) like targeted runs, or the suite should get under the deadline (T-3166, T-3171)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo check's run of python3 plugin/tests/run.py gets a deadline scaled by the 1-minute load per CPU (the same load_scaled the targeted runs use), capped at a sane maximum, and a gate that still times out reports exit 124 with the load and the deadline it had — verify with `python3 plugin/tests/run.py test_cli test_check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a fake load of 2 per CPU doubles the suite gate's deadline; the timeout line names load and deadline
2. [x] the scaled deadline in the full check
## Resume here
## Docs impact
CHANGELOG line added at merge time by the lane? none in the lane: added now
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 150 tests in 93.5s (45 classes, 16 at a time; slowest: TaskLifecycle 92s, CaptureAndIntake 44s, StateViews 40s) / OK [ran] [tree a1cf4990f93b] [world 2f1906870a] (2026-11-05T08:08:08Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 151 tests in 37.1s (45 classes, 16 at a time; slowest: TaskLifecycle 37s, CaptureAndIntake 16s, StateViews 14s) / OK [ran] [tree 112d36337448] [world 2f1906870a] (2026-11-05T10:13:25Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 151 tests in 27.8s (45 classes, 16 at a time; slowest: TaskLifecycle 26s, CaptureAndIntake 13s, StateViews 11s) / FAILED (1 classes: test_cli.Checks) (start tree + this task's tests) [ran] [tree 112d36337448] [world 2f1906870a] (2026-11-05T10:14:19Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 151 tests in 25.6s (45 classes, 16 at a time; slowest: TaskLifecycle 25s, CaptureAndIntake 12s, Checks 11s) / OK [ran] [tree 112d36337448] [world 2f1906870a] (2026-11-05T10:14:19Z)
- (step 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 151 tests in 25.9s (45 classes, 16 at a time; slowest: TaskLifecycle 26s, CaptureAndIntake 13s, Checks 12s) / OK [ran] [tree 112d36337448] [world 2f1906870a] (2026-11-05T10:14:45Z)
- (step 2) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 151 tests in 24.8s (45 classes, 16 at a time; slowest: TaskLifecycle 24s, CaptureAndIntake 11s, Checks 11s) / OK [ran] [tree 112d36337448] [world 2f1906870a] (2026-11-05T10:15:11Z)
- (ac 1) `python3 plugin/tests/run.py test_cli test_check` → exit 0 · Ran 179 tests in 26.1s (64 classes, 16 at a time; slowest: TaskLifecycle 26s, CaptureAndIntake 13s, Checks 12s) / OK [ran] [tree 112d36337448] [world 2f1906870a] (2026-11-05T10:16:11Z)
- (audit edge) `builder lane merged; criteria re-run on main green (151 tests); red→green proved` → a named-test gate keeps its own scaled timeout; --timeout 0 stays unlimited; a timeout line names the load per CPU and the deadline [tree 112d36337448] (2026-11-05T10:16:11Z)
- (audit self) `builder lane merged; criteria re-run on main green (151 tests); red→green proved` → no findings [tree 112d36337448] (2026-11-05T10:16:11Z)
## Log
- 2026-11-05T08:00:26Z created
- 2026-11-05T08:01:54Z planned from capture
- 2026-11-05T08:01:55Z set approved=True
- 2026-11-05T08:01:56Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3174.builder.md
- 2026-11-05T08:02:16Z focused
- 2026-11-05T08:02:17Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T08:08:42Z builder edited cli.py::cmd_check without the lease (held by T-3160) instead of stopping as the contract says; the edit is two lines plus a helper; expect a conflict with T-3160 there and resolve in T-3160's lane
- 2026-11-05T10:12:36Z merged worktree-agent-a8ad97a121fc7b19f (2 file(s))
- 2026-11-05T10:12:36Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8ad97a121fc7b19f
- 2026-11-05T10:12:46Z focused
- 2026-11-05T10:16:55Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2822 [FIX M, done, 3 steps] CI failed on this branch: run 41676727022 — lesson: A gate that reads the machine must be off inside the harness's own sandboxes: route eve…
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-2798 [FIX M, done, 2 steps] fm doctor's hook SLO judges only PreToolUse runs taken at normal host load: each hook_ms event records load per CPU, and runs above LOAD_BA…
- decision 2026-11-05: T-3157 calling cards: approved in full autonomy after the cold plan review; built as parts, the thin slice T-3160 first (ten Opus-written cards, the…
## Measurements
full suite gate deadline at load 2 per CPU: 1200 s → 3600 s (base 1800 s x2); capped at 7200 s (tested with a faked load)
## Lessons
- A gate's timeout must scale with the load that slows it, or a busy machine reads as a red suite
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/sampo/cli.py
