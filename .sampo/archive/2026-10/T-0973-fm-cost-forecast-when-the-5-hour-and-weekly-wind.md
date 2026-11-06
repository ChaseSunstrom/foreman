---
id: T-0973
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-15T22:08:00Z
updated: 2026-10-15T22:22:42Z
base: 02c5c269cdad1b0479c88317de4a9545b9e59a08
base_tree: 34abfbd139aef3ea29cf5f2357be30899f288b15
verified: strong
---
# Fm cost --forecast: when the 5-hour and weekly windows fill at the current pace, from Clau
## Raw request
> fm cost --forecast: when the 5-hour and weekly windows fill at the current pace, from Claude Code Usage Monitor (research/T-0964-catalogue.md)
## Interpretation
Say when the 5-hour and weekly usage windows fill at the current pace, from the statusline's rate_limits snapshot, so a long unattended run knows whether it will hit a limit before the reset.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm cost --forecast prints, per window, the percent used, the pace-projected percent at reset, and the time it fills when that is before the reset; --json carries the same; no snapshot says so — verify with `python3 plugin/tests/run.py -k CostForecast`
## Non-goals
## Approach (options → choice → why)
Options: linear pace inside each window from used_percentage and resets_at in the newest snapshot (chosen: zero tokens, data already on disk); a history of snapshots for a moving rate (needs a new store); ccusage-style transcript token sums (no plan limits to compare with).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing CostForecast tests
2. [x] fmbudget.forecast and the --forecast flag; docs
## Resume here
## Docs impact
MASTER, CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k CostForecast` → ✗ exit 1 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: CostForecast 0s) / FAILED (1 classes) [ran] [tree 9579801c6177] (2026-10-15T22:21:59Z)
- (step 2) `python3 plugin/tests/run.py -k CostForecast && fm cost --forecast` → exit 0 · weekly: 27% used, on pace for 115.2% at its reset (Wed 02:00); fills about Tue 03:50, before the reset / (a straight line from the window's start: early on it swings) [ran] [tree 935fb10c70ac] (2026-10-15T22:22:34Z)
- (ac 1) `python3 plugin/tests/run.py -k CostForecast` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: CostForecast 0s) / OK [ran] [tree 935fb10c70ac] (2026-10-15T22:22:40Z)
- (step 1) `python3 plugin/tests/run.py -k CostForecast` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: CostForecast 0s) / OK [ran] [tree 935fb10c70ac] (2026-10-15T22:22:40Z)
- (audit self) `self: red then green; live run on this machine's snapshot gives a plausible weekly fill time` → per-window linear pace from used_percentage and resets_at; no snapshot or a past reset says nothing rather than guessing [tree 935fb10c70ac] (2026-10-15T22:22:40Z)
## Log
- 2026-10-15T22:08:00Z created
- 2026-10-15T22:21:48Z focused
- 2026-10-15T22:22:41Z done
- 2026-10-15T22:22:42Z committed 0ba0b38 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0320-review: Approve with nits. Nothing blocks. One MEDIUM and two LOW findings, all in snapshot parsing. I did not run the tests. [stale: plugin/lib/fmbudget…
- T-0320 [FEATURE M, done, 3 steps] Subagents budgeted by usage pace, not a daily token count — lesson: Budget by the real constraint: a proxy cap (tokens/day, with cache …
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
## Plan gaps
- failed first: step 1 Failing CostForecast tests
## Files touched
- plugin/tests/test_cost_forecast.py
- plugin/lib/fmbudget.py
- plugin/lib/fmcost.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
