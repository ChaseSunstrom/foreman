---
id: T-1127
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcost.py, plugin/lib/fmhooks.py, plugin/lib/fmserve.py, plugin/tests/test_cost_forecast.py]
depends_on: []
source: discovered
created: 2026-10-16T07:19:24Z
updated: 2026-10-16T07:33:17Z
base: 9843156b7c78c02184cef72658a82167078bdfb2
base_tree: 6cfb0aae26e7d1eaa55955b9ddd08fac576568e0
plan0_at: 2026-10-16T07:21:38Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmcost.py, plugin/lib/fmhooks.py, plugin/lib/fmserve.py, plugin/tests/test_cost_forecast.py]
verified: strong
---
# Fm run and fm next still dispatch a task whose cost cap was hit (only the interactive driv
## Raw request
> fm run and fm next still dispatch a task whose cost cap was hit (only the interactive drive holds it); route the capped set through _next_runnable and next_for
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A task whose cost cap was hit waits for the user in fm run's picker, fm next and the drive alike, until its cost_cap changes — verify with `python3 plugin/tests/run.py test_cost_forecast`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test (fm run picker and fm next), then record cap_hit on the brief and check it in waits_on_user
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cost_forecast` → ✗ exit 1 · Ran 9 tests in 19.3s (2 classes, 16 at a time; slowest: TaskCostCap 19s, CostForecast 1s) / FAILED (1 classes) [ran] [tree 56cfb936e215] (2026-10-16T07:22:05Z)
- (step 1) `python3 plugin/tests/run.py test_cost_forecast test_serve test_hooks` → ✗ exit 1 · Ran 191 tests in 280.0s (26 classes, 16 at a time; slowest: Stop 280s, PreToolUse 144s, SessionStart 103s) / FAILED (1 classes) [ran] [tree 665da1c8c15a] (2026-10-16T07:27:57Z)
- (step 1) `python3 plugin/tests/run.py test_cost_forecast test_serve` → exit 0 · Ran 35 tests in 36.9s (7 classes, 16 at a time; slowest: Run 36s, TaskCostCap 27s, Serve 16s) / OK [ran] [tree c684911e0b16] (2026-10-16T07:31:11Z)
- (ac 1) `python3 plugin/tests/run.py test_cost_forecast` → exit 0 · Ran 9 tests in 13.7s (2 classes, 16 at a time; slowest: TaskCostCap 13s, CostForecast 2s) / OK [ran] [tree 611d53cbb171] (2026-10-16T07:31:26Z)
- (audit self) `self: fm run's picker and fm next tested holding a capped task and releasing it on a new cap; the drive's cap check runs under the Stop hook's held lock (a nested lock had failed open — found by the test, now logged when it happens)` → no findings [tree 611d53cbb171] (2026-10-16T07:31:26Z)
## Log
- 2026-10-16T07:19:24Z created
- 2026-10-16T07:21:35Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmcost.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmserve.py', 'plugin/tests/test_cost_forecast.py']
- 2026-10-16T07:21:36Z focused
- 2026-10-16T07:31:11Z scope: CHANGELOG.md — release note
- 2026-10-16T07:33:16Z done
- 2026-10-16T07:33:17Z committed bf79bbb (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0761 [FIX S, dropped, 2 steps] Guard: a data heredoc that writes a Foreman source file isn't interpreter code driving Foreman
- research T-0291-review-1: Changes needed. Fix 2 (the `confirm` flag) can be bypassed by the working session itself, and fix 3 has one gap that runs a planted driver. [st…
- research wave1-plan-a2475fc5d2263de06: === T-1049 [stale: plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmhooks.py changed since it was written]
- decision 2026-10-04: Friction pass deferred to the next day
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_hooks.py, plugin/tests/test_serve.py
## Lessons
- A state every dispatcher must honour belongs on the record they all read (the brief), not in one dispatcher's session state
## Plan gaps
- failed first: step 1 Failing test (fm run picker and fm next), then record cap_hit on the brief and check it in waits_on…
## Files touched
- plugin/tests/test_cost_forecast.py
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmserve.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
