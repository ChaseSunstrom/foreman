---
id: T-1083
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcost.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_cost_forecast.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T07:20:40Z
base: 649ef781113124d68574698988f924ee529259f9
base_tree: 876116799cc7ff387c689a296f80ba9d5482d71a
cost_cap: 500000000
plan0_at: 2026-10-16T07:17:27Z
plan0_scope: [plugin/lib/fmcost.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_cost_forecast.py]
verified: strong
---
# Per-task cost cap and forecast: a task's brief forecasts its cost from similar tasks; a ca
## Raw request
> FEATURE: Per-task cost cap and forecast: a task's brief forecasts its cost from similar tasks; a cap stops it with a checkpoint (catalogue C15)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
A task has a cost cap. A forecast, from the median cost of similar finished tasks (same type and tier), appears where the task's brief is read. When the task's spend passes the cap, the drive stops with a checkpoint. Covered already: per-task cost from transcripts (fmcost.py:180-189, the `by_task` logic, not callable on its own); USD caps per day and per command (fmbudget.py:17); window forecasts (`fm cost --forecast`, fmcost.py:153). Missing: a per-task figure, a similar-task forecast, a cap and the stop. The catalogue marked C15 "SKIP", but this task asks for it, so I build it.
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm cost --task` shows the forecast from two finished same-tier tasks; with a cap exceeded, the drive's Stop reason asks for a checkpoint — verify with `python3 plugin/tests/run.py test_cost_forecast`
## Non-goals
## Approach (options → choice → why)
(a) USD from spend.jsonl. (b) Input-equivalent tokens from transcripts, which is what `by_task` already measures. (c) Both. Choose (b), because spend.jsonl only has Foreman's own children, not the session's work. Refactor the `by_task` loop into `task_costs(p, days)` in fmcost.py. Add `forecast_task(p, b)` (median of done same-type/tier tasks, else None). Add `fm cost --task ID`, which prints spent, cap and forecast. Add `fm task set ID cost_cap=2M`, stored in brief meta through the existing assignments. In the Stop-hook drive (fmhooks.py, near 2531), when the active task's spend ≥ its cap, the reason says "cost cap hit: fm checkpoint, tell the user" and the drive ends. The check runs only when the task has a cap, and fails open.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: write fake transcripts (see how test_cost_forecast and test_perf_cost build them). Two done M tasks of about 100k each give a forecast near 100k. A task with `cost_cap` below its spend gives the Stop reason containing "cost cap". Without a cap, nothing changes.
2. [x] Extract `task_costs`, add `forecast_task` and `--task`, then the cap parse in `task set`.
3. [x] Add the Stop-hook check.
## Resume here
T-1083 review fixes: tests written (red), implementation next
<!-- auto -->
- 2026-10-16T07:14:18Z step 1/3: Failing tests: write fake transcripts (see how test_cost_forecast and test_perf_cost build them). Two done M tasks of about 100k each give a forecast near 100k. A task with `cost_cap` below its spend gives the Stop reason containing "cost cap". Without a cap, nothing changes.
- git: foreman/build; 1 uncommitted: plugin/tests/test_cost_forecast.py
- touched since last checkpoint: plugin/tests/test_cost_forecast.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cost_forecast` → ✗ exit 1 · Ran 4 tests in 7.1s (2 classes, 16 at a time; slowest: TaskCostCap 7s, CostForecast 2s) / FAILED (1 classes) [ran] [tree 277c3dda5135] (2026-10-16T07:00:54Z)
- (step 2) `python3 plugin/tests/run.py test_cost_forecast` → exit 0 · Ran 4 tests in 8.2s (2 classes, 16 at a time; slowest: TaskCostCap 8s, CostForecast 2s) / OK [ran] [tree 4d89275bd8f9] (2026-10-16T07:01:55Z)
- (step 3) `python3 plugin/tests/run.py test_cost_forecast` → exit 0 · Ran 4 tests in 4.8s (2 classes, 16 at a time; slowest: TaskCostCap 4s, CostForecast 1s) / OK [ran] [tree 4d89275bd8f9] (2026-10-16T07:02:00Z)
- (step 3) `python3 plugin/tests/run.py test_cost_forecast` → exit 0 · Ran 5 tests in 5.8s (2 classes, 16 at a time; slowest: TaskCostCap 6s, CostForecast 1s) / OK [ran] [tree 8a03d35dc152] (2026-10-16T07:05:04Z)
- (step 1) `python3 plugin/tests/run.py test_cost_forecast` → ✗ exit 1 · Ran 8 tests in 4.3s (2 classes, 16 at a time; slowest: TaskCostCap 4s, CostForecast 0s) / FAILED (1 classes) [ran] [tree dc17c1c275d5] (2026-10-16T07:13:49Z)
- (step 1) `python3 plugin/tests/run.py test_cost_forecast test_perf_cost test_economics test_cli` → exit 0 · Ran 126 tests in 22.2s (40 classes, 16 at a time; slowest: TaskLifecycle 22s, StateViews 9s, AuditPrep 8s) / OK [ran] [tree 9740928335c9] (2026-10-16T07:19:11Z)
- (ac 1) `python3 plugin/tests/run.py test_cost_forecast` → exit 0 · Ran 8 tests in 4.8s (2 classes, 16 at a time; slowest: TaskCostCap 5s, CostForecast 0s) / OK [ran] [tree 6cfb0aae26e7] (2026-10-16T07:19:29Z)
- (audit intent) `review: one fm-reviewer full pass on the merged change; fixed test-first: no inline transcript scan in the Stop hook (cache only, detached refresh with a claim), cache moved out of sessions/ and shape-checked, per-session attribution (fm cost too), cap changes logged and raises in the digest, empty/0 clears (T-1126 folded), input-equivalent wording, rough forecasts named` → a task can carry a token budget the drive respects, with a forecast from similar work [tree 6cfb0aae26e7] (2026-10-16T07:19:29Z)
- (audit adversary) `review: one fm-reviewer full pass on the merged change; fixed test-first: no inline transcript scan in the Stop hook (cache only, detached refresh with a claim), cache moved out of sessions/ and shape-checked, per-session attribution (fm cost too), cap changes logged and raises in the digest, empty/0 clears (T-1126 folded), input-equivalent wording, rough forecasts named` → raising a cap is logged with from→to and listed in the digest; the hook fails open, never traps the drive [tree 6cfb0aae26e7] (2026-10-16T07:19:29Z)
- (audit edge) `review: one fm-reviewer full pass on the merged change; fixed test-first: no inline transcript scan in the Stop hook (cache only, detached refresh with a claim), cache moved out of sessions/ and shape-checked, per-session attribution (fm cost too), cap changes logged and raises in the digest, empty/0 clears (T-1126 folded), input-equivalent wording, rough forecasts named` → wrong-shaped or shrunk caches are recomputed; concurrent sessions bill their own tasks; cap 0 or empty removes it [tree 6cfb0aae26e7] (2026-10-16T07:19:29Z)
- (audit operator) `review: one fm-reviewer full pass on the merged change; fixed test-first: no inline transcript scan in the Stop hook (cache only, detached refresh with a claim), cache moved out of sessions/ and shape-checked, per-session attribution (fm cost too), cap changes logged and raises in the digest, empty/0 clears (T-1126 folded), input-equivalent wording, rough forecasts named` → the Stop hook reads a small JSON file; the scan runs detached, once a minute at most [tree 6cfb0aae26e7] (2026-10-16T07:19:29Z)
- (audit maintainer) `review: one fm-reviewer full pass on the merged change; fixed test-first: no inline transcript scan in the Stop hook (cache only, detached refresh with a claim), cache moved out of sessions/ and shape-checked, per-session attribution (fm cost too), cap changes logged and raises in the digest, empty/0 clears (T-1126 folded), input-equivalent wording, rough forecasts named` → _timelines/_task_for shared by fm cost and task_costs; cache helpers in one place [tree 6cfb0aae26e7] (2026-10-16T07:19:29Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:23:04Z set scope=['plugin/lib/fmcost.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmhooks.py', 'plugin/tests/test_cost_forecast.py']
- 2026-10-16T04:23:04Z set tier=L
- 2026-10-16T05:13:21Z set tier=M
- 2026-10-16T06:59:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1083.builder.md
- 2026-10-16T06:59:24Z focused
- 2026-10-16T07:04:49Z set cost_cap=500000000
- 2026-10-16T07:09:52Z merged worktree-agent-a2675e071c9af14cc (4 file(s))
- 2026-10-16T07:10:00Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2675e071c9af14cc
- 2026-10-16T07:10:01Z focused
- 2026-10-16T07:11:33Z paused: focus moved to T-1063
- 2026-10-16T07:13:07Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T07:13:07Z focused
- 2026-10-16T07:13:13Z review: Stop hook scans transcripts inline on a cache miss (5 s timeout: kills the whole drive); cache file in state/sessions collides with session snapshots; attribution by global time across sessions; cap raise unlogged, cap can't be cleared (T-1126 folded in); cache shape/negative size; wording. Fixing test-first.
- 2026-10-16T07:14:19Z paused: focus moved to T-1061
- 2026-10-16T07:17:27Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T07:17:27Z focused
- 2026-10-16T07:17:30Z set scope=['plugin/lib/fmcost.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmhooks.py', 'plugin/tests/test_cost_forecast.py']
- 2026-10-16T07:19:24Z scope: CHANGELOG.md — release note
- 2026-10-16T07:20:39Z done
- 2026-10-16T07:20:40Z committed 9843156 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmhooks.py, plugin/tests/test_cost_forecast.py; re-ground the plan against them before editing
## Lessons
- Never do unbounded work on a hook's timed path: read a cache there and refresh it out of band
## Plan gaps
- failed first: step 1 Failing tests: write fake transcripts (see how test_cost_forecast and test_perf_cost build them). T…
## Files touched
- plugin/tests/test_cost_forecast.py
- plugin/lib/fmcost.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- plugin/lib/fmcore.py
- plugin/lib/fmguard.py
- plugin/lib/fmideas.py
- plugin/lib/fmlanes.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmserve.py
- plugin/skills/intake/references/planning.md
- plugin/tests/test_guard.py
- plugin/tests/test_hooks.py
- plugin/tests/test_planning.py
- plugin/tests/test_steer_compile.py
