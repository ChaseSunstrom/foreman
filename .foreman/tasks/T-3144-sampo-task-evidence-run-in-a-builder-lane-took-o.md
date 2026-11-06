---
id: T-3144
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/lanes.py, plugin/lib/sampo/core.py, plugin/tests/test_cli.py, plugin/tests/test_bookkeeping.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T05:11:32Z
updated: 2026-11-05T09:51:41Z
builder_model: sonnet
base: 99d985d4ca090f0796647cbaf49c614c62b2a8c2
base_tree: 64c1651d6901af3c02e4a741fe34a5eded2fe7fd
plan0_at: 2026-11-05T05:36:47Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/lanes.py, plugin/lib/sampo/core.py, plugin/tests/test_cli.py, plugin/tests/test_bookkeeping.py, CHANGELOG.md]
builder_returned: 2026-11-05T05:42:58Z
lane_stop: merged 2026-11-05T09:45:10Z
verified: strong
unproven: [perf-typed]
---
# Targeted runs never wait for load: task evidence, check --affected and a finish's criterion checks run at once with a load-scaled timeout; only a full suite waits, at most 60 s, and lane merge's wait is capped the same
## Raw request
> sampo task evidence --run in a builder lane took over 3 minutes on a test that runs in about 2 s directly (T-3126's lane, 2026-11-05); find what it waits on (load wait, a lock, the ambient run, a guard replay) and cut it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo task evidence --run CMD and sampo check --affected start without calling wait_for_load (their run timeout still scales with load); sampo check (the full suite), task finish's full gates and lane merge wait at most 60 s; a 2-second test under load 3 per CPU records its evidence in under 10 s — verify with `python3 plugin/tests/run.py test_cli test_bookkeeping`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: evidence under a faked load of 3 per CPU doesn't wait; the full check waits at most 60 s
2. [x] the wait_for_load call sites (cli.py:814, 1326, 1670, 4954, 5679; lanes.py:1807)
## Resume here
## Docs impact
CHANGELOG line added
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_cli test_bookkeeping 2>&1 | tail -6` → exit 0 · Ran 170 tests in 34.0s (55 classes, 16 at a time; slowest: TaskLifecycle 33s, CaptureAndIntake 17s, StateViews 16s) / OK [ran] [tree 20a3c901d180] [world 2f1906870a] (2026-11-05T05:40:19Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_bookkeeping 2>&1 | tail -6` → exit 0 · Ran 170 tests in 34.0s (55 classes, 16 at a time; slowest: TaskLifecycle 33s, CaptureAndIntake 17s, StateViews 16s) / OK [ran] [tree 20a3c901d180] [world 2f1906870a] (2026-11-05T05:40:19Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_bookkeeping` → exit 0 · Ran 170 tests in 34.1s (55 classes, 16 at a time; slowest: TaskLifecycle 34s, CaptureAndIntake 16s, StateViews 15s) / OK [ran] [tree 20a3c901d180] [world 2f1906870a] (2026-11-05T05:40:56Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_bookkeeping test_lanes` → exit 0 · Ran 331 tests in 51.1s (69 classes, 16 at a time; slowest: Lanes 51s, TaskLifecycle 37s, LaneRecovery 35s) / OK [ran] [tree 20a3c901d180] [world 2f1906870a] (2026-11-05T05:41:48Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_doctor test_left_out test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [20.77s] [ran] [tree 20a3c901d180] [world 2f1906870a] (2026-11-05T05:42:49Z)
- `python3 plugin/tests/run.py test_cli test_bookkeeping` → exit 0 · Ran 172 tests in 47.6s (55 classes, 16 at a time; slowest: TaskLifecycle 47s, CaptureAndIntake 25s, StateViews 23s) / OK [ran] [tree 96e1ca009cf1] [world 2f1906870a] (2026-11-05T09:48:55Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 150 tests in 28.4s (45 classes, 16 at a time; slowest: TaskLifecycle 26s, CaptureAndIntake 13s, StateViews 12s) / FAILED (1 classes: test_cli.TaskLifecycle) (start tree + this task's tests) [ran] [tree 96e1ca009cf1] [world 2f1906870a] (2026-11-05T09:49:50Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 150 tests in 25.3s (45 classes, 16 at a time; slowest: TaskLifecycle 25s, CaptureAndIntake 12s, StateViews 11s) / OK [ran] [tree 96e1ca009cf1] [world 2f1906870a] (2026-11-05T09:49:50Z)
- (ac 1) `python3 plugin/tests/run.py test_cli test_bookkeeping` → exit 0 · Ran 172 tests in 26.5s (55 classes, 16 at a time; slowest: TaskLifecycle 26s, CaptureAndIntake 13s, StateViews 12s) / OK [ran] [tree c8cd728cd734] [world 2f1906870a] (2026-11-05T09:50:30Z)
- (audit edge) `builder lane reviewed and merged; criteria re-run on main green (172 tests); red→green proved` → a bad or empty FOREMAN_LOAD_WAIT falls back to 60 s; a negative one clamps to 0; targeted runs still scale their timeouts by load, so they can't hang [tree c8cd728cd734] (2026-11-05T09:50:30Z)
- (audit self) `builder lane reviewed and merged; criteria re-run on main green (172 tests); red→green proved` → no findings [tree c8cd728cd734] (2026-11-05T09:50:30Z)
## Log
- 2026-11-05T05:11:32Z created
- 2026-11-05T05:12:10Z planned from capture
- 2026-11-05T05:12:11Z set approved=True
- 2026-11-05T05:12:11Z set scope=['plugin/lib/sampo/cli.py', 'plugin/lib/sampo/lanes.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_cli.py', 'plugin/tests/test_bookkeeping.py', 'CHANGELOG.md']
- 2026-11-05T05:36:37Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3144.builder.md
- 2026-11-05T05:36:46Z focused
- 2026-11-05T09:45:10Z merged worktree-agent-a0c2d3f6f7f7eb843 (3 file(s))
- 2026-11-05T09:45:11Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0c2d3f6f7f7eb843
- 2026-11-05T09:48:05Z focused
- 2026-11-05T09:50:02Z scope: files outside its globs came from other tasks' merges and closes landing between its merge and this close
- 2026-11-05T09:51:39Z done
- 2026-11-05T09:51:41Z committed 1131c48a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3090 [FIX S, dropped, 2 steps] sampo check --affected says it started before it runs, and waits at most 60 s for load
- T-2797 [FIX M, done, 3 steps] Gates under machine load wait or stretch instead of failing: fm lane brief holds a new lane past 1.5 load per core, and fm task finish, fm …
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-11-05: merge speed order: T-3118 (bench only the hook path) first, the biggest cut; then T-3109 (closes yield to a waiting merge), T-3120 (closes reuse a g…
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–5 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_lane_twins.py, plugin/tests/test_lanes.py, plugin/tests/test_mint.py, plugin/tests/te…
## Preflight
Changed in scope since this was planned (2026-11-05): CHANGELOG.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/lanes.py, plugin/tests/test_cli.py; re-ground the plan against them before editing
## Measurements
load wait before a targeted run: up to 300 s → 0 s; full check or merge wait: up to 300 s → at most 60 s (by construction, tested with a faked load)
## Lessons
- A wait meant to protect timing gates should only guard the runs that time things; everything else just scales its timeout
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/cli.py
- CHANGELOG.md
