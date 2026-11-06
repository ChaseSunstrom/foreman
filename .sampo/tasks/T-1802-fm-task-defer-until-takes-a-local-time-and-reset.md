---
id: T-1802
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T00:52:28Z
updated: 2026-10-28T00:54:43Z
base: e021641fb7bdd2c7afad5abcea74a6f448331b07
base_tree: 4fa4cbd0499c35e8314e454156a093a00d97090b
plan0_at: 2026-10-28T00:52:28Z
plan0_scope: []
verified: strong
---
# fm task defer --until takes a local time and "reset" (the weekly usage reset)
## Raw request
> fm task defer --until takes a local time and "reset" (the weekly usage reset)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a deferral to YYYY-MM-DDTHH:MM comes due at that minute, not at midnight; --until reset stores the weekly reset as a local time — verify with `python3 plugin/tests/run.py test_until_conditions`
- [x] T-1800, T-1799, T-1797, T-1798, T-1231 come back at the reset, not at midnight — verify with `fm task show T-1800`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] deferral_due honors a time; defer --until accepts YYYY-MM-DDTHH:MM and reset; test
2. [x] re-defer the five tasks to the reset
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_until_conditions` → exit 0 · Ran 6 tests in 3.6s (1 classes, 16 at a time; slowest: UntilConditions 3s) / OK [ran] [tree 7ea87a2b9ae9] (2026-10-28T00:53:33Z)
- (step 2) `fm task show T-1800` → exit 0 · - 2026-10-28T00:53:10Z deferred: waits for the weekly usage reset (95% used) (revisit 2026-10-28T02:00) / ## Follow-ups captured [ran] [tree 7ea87a2b9ae9] (2026-10-28T00:53:34Z)
- (ac 1) `python3 plugin/tests/run.py test_until_conditions` → exit 0 · Ran 6 tests in 3.6s (1 classes, 16 at a time; slowest: UntilConditions 3s) / OK [ran] [tree 7ea87a2b9ae9] (2026-10-28T00:54:15Z)
- (ac 2) `fm task show T-1800` → exit 0 · - 2026-10-28T00:53:10Z deferred: waits for the weekly usage reset (95% used) (revisit 2026-10-28T02:00) / ## Follow-ups captured [ran] [tree 7ea87a2b9ae9] (2026-10-28T00:54:15Z)
- (audit edge) `self: read the diff; a time on today's date compares HH:MM to the local clock, other days compare dates as before; reset uses forecast(), which drops stale or millisecond readings, so no reading means a clear error; old fm copies read the time as the next day (late, never early)` → 23:59/00:00 today, invalid 25:00 refused, stale snapshot refused, +59 s so never a minute early [tree 7ea87a2b9ae9] (2026-10-28T00:54:15Z)
- (audit self) `self: read the diff; a time on today's date compares HH:MM to the local clock, other days compare dates as before; reset uses forecast(), which drops stale or millisecond readings, so no reading means a clear error; old fm copies read the time as the next day (late, never early)` → no findings [tree 7ea87a2b9ae9] (2026-10-28T00:54:15Z)
## Log
- 2026-10-28T00:52:28Z created
- 2026-10-28T00:52:28Z focused
- 2026-10-28T00:54:41Z done
- 2026-10-28T00:54:43Z committed 1033aefb (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-27: Start T-1800 at the 02:00 weekly reset, not now
- T-1798 [FEATURE M, deferred, 0 steps] Recursive brainstorm round after the weekly reset (user: 'super recursive brainstorm impro
- research T-0320-review: Approve with nits. Nothing blocks. One MEDIUM and two LOW findings, all in snapshot parsing. I did not run the tests. [stale: plugin/lib/fmbudget…
- T-0973 [FEATURE S, done, 2 steps] Fm cost --forecast: when the 5-hour and weekly windows fill at the current pace, from Clau
- the similar finished task took 2 steps
- start here (files T-0973 touched): plugin/tests/test_cost_forecast.py, plugin/lib/fmbudget.py, plugin/lib/fmcost.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md
## Files touched
- plugin/tests/test_until_conditions.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
