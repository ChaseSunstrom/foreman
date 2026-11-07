---
id: T-3431
type: CLEAN
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/miss.py, plugin/lib/sampo/toolproof.py, plugin/lib/sampo/grants.py, plugin/lib/sampo/incident.py, plugin/lib/sampo/rollback.py, plugin/tests/test_hooks.py, plugin/lib/sampo/hooks.py]
depends_on: []
source: discovered
created: 2026-11-06T11:17:37Z
updated: 2026-11-06T11:37:33Z
lane: ~/.claude/foreman/.claude/worktrees/agent-ad4bf2732edb4db99
lane_branch: worktree-agent-ad4bf2732edb4db99
base: 98b2bb8fc9a7e725bc1e008d5b33e33f7eedcad1
base_tree: e79cc1b97bb4490d60a6e490e2a6c9c65a502a68
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T11:19:05Z
plan0_scope: [plugin/lib/sampo/miss.py, plugin/lib/sampo/toolproof.py, plugin/lib/sampo/grants.py, plugin/lib/sampo/incident.py, plugin/lib/sampo/rollback.py, plugin/tests/test_hooks.py]
builder_returned: 2026-11-06T11:37:33Z
inferred_deps: [T-3423]
inferred_why: T-3423: named in its request
group: hook lock contention and error logging
---
# miss.py, toolproof.py, grants.py, incident.py and rollback.py append to hooks.log…
## Raw request
> CLEAN: miss.py, toolproof.py, grants.py, incident.py and rollback.py append to hooks.log directly, bypassing hooks.log_error's 1 MB rotation and repeat collapse (T-3423); route them through log_error
## Interpretation
Reading 1: route the five direct appends through hooks.log_error, same line content. Reading 2 (ruled out): a new log API with a changed format; readers (doctor, friction) parse the current one.
## Assumptions (confidence)
## Acceptance criteria
- [ ] each caller writes '<ts> <event> <text>' once and collapses a repeat — verify with `python3 plugin/tests/run.py test_hooks.LogErrorCallers`
- [ ] log_error rotation/collapse unchanged — verify with `python3 plugin/tests/run.py test_hooks.LogErrorCap`
## Non-goals
## Approach (options → choice → why)
1) Use what exists: hooks.log_error, imported lazily in each failure path; likely outcome: five small diffs, fails if a cycle at call time (none: hooks imports these lazily). 2) Move log_error body to core.log_line and delegate; fails if tests patching hooks.HOOKS_LOG_MAX/time break. 3) Leave as is and rotate only in tidy; fails to collapse repeats. Choice 1 (80%): failure paths only, so no hook-path import cost.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmhooks.py, CHANGELOG.md, plugin/lib/sampo/hooks.py, MASTER.md, plugin/lib/fmcli.py; past FIXes T-1715, T-1759, T-1768, T-1839, T-1889.
## Execution prompt
## Steps
1. [x] Lock formats in LogErrorCallers, then route the five callers
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_hooks.LogErrorCallers 2>&1 | tail -8` → ✗ exit 1 · Ran 1 tests in 0.5s (1 jobs, 16 at a time; slowest: LogErrorCallers 0s) / FAILED (1 classes: test_hooks.LogErrorCallers) [ran] [tree 72da482cc850] [world 2f1906870a] (2026-11-06T11:19:14Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.LogErrorCallers test_hooks.LogErrorCap` → ✗ exit 1 · Ran 3 tests in 5.4s (2 jobs, 16 at a time; slowest: LogErrorCap 0s, LogErrorCallers 0s) / FAILED (1 classes: test_hooks.LogErrorCallers) [ran] [tree 9acfb45f0153] [world 2f1906870a] (2026-11-06T11:19:33Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.LogErrorCallers 2>&1 | head -30` → ✗ exit 1 · Ran 1 tests in 0.5s (1 jobs, 16 at a time; slowest: LogErrorCallers 0s) / FAILED (1 classes: test_hooks.LogErrorCallers) [ran] [tree 9acfb45f0153] [world 2f1906870a] (2026-11-06T11:19:36Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.LogErrorCallers test_hooks.LogErrorCap` → ✗ exit 1 · Ran 3 tests in 0.5s (2 jobs, 16 at a time; slowest: LogErrorCap 0s, LogErrorCallers 0s) / FAILED (1 classes: test_hooks.LogErrorCallers) [ran] [tree 142686d6041c] [world 2f1906870a] (2026-11-06T11:19:48Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.LogErrorCallers 2>&1 | head -60` → ✗ exit 1 · Ran 1 tests in 2.7s (1 jobs, 16 at a time; slowest: LogErrorCallers 0s) / FAILED (1 classes: test_hooks.LogErrorCallers) [ran] [tree f5616d8c7fb2] [world 2f1906870a] (2026-11-06T11:20:07Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.LogErrorCallers 2>&1 | head -20` → exit 0 · Ran 1 tests in 0.4s (1 jobs, 16 at a time; slowest: LogErrorCallers 0s) / OK [ran] [tree 4aa3b7c6d6b4] [world 2f1906870a] (2026-11-06T11:20:11Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.LogErrorCallers test_hooks.LogErrorCap` → exit 0 · Ran 3 tests in 0.4s (2 jobs, 16 at a time; slowest: LogErrorCap 0s, LogErrorCallers 0s) / OK [ran] [tree 4aa3b7c6d6b4] [world 2f1906870a] (2026-11-06T11:20:17Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_compact test_doctor test_hooks test_incident test_left_out test_models test_proof test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [16.44s] [ran] [tree 4aa3b7c6d6b4] [world 2f1906870a] (2026-11-06T11:21:00Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.LogErrorCallers test_hooks.LogErrorCap` → exit 0 · Ran 4 tests in 13.6s (2 jobs, 16 at a time; slowest: LogErrorCap 0s, LogErrorCallers 0s) / OK [ran] [tree 61d047f80bcd] [world 2f1906870a] (2026-11-06T11:37:20Z)
## Log
- 2026-11-06T11:17:37Z created
- 2026-11-06T11:18:52Z set scope=['plugin/lib/sampo/miss.py', 'plugin/lib/sampo/toolproof.py', 'plugin/lib/sampo/grants.py', 'plugin/lib/sampo/incident.py', 'plugin/lib/sampo/rollback.py', 'plugin/tests/test_hooks.py']
- 2026-11-06T11:18:52Z planned: it has criteria and steps
- 2026-11-06T11:19:04Z focused
- 2026-11-06T11:19:05Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T11:36:29Z set scope=['plugin/lib/sampo/miss.py', 'plugin/lib/sampo/toolproof.py', 'plugin/lib/sampo/grants.py', 'plugin/lib/sampo/incident.py', 'plugin/lib/sampo/rollback.py', 'plugin/tests/test_hooks.py', 'plugin/lib/sampo/hooks.py']
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3423 [FIX S, active, 1 steps] hooks.log_error appends to state/logs/hooks.log with no size cap or rotation (repeated…
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- decision 2026-11-01: [cites: user steer 2026-11-01: decision on the cold-read rule: keep it, make it reliable (Haiku first, Sonnet decides on FAIL; a FAIL quotes the lin…
- similar finished tasks took 2–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_incident.py, plugin/tests/test_proof.py
