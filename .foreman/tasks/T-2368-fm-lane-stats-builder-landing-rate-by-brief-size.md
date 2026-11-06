---
id: T-2368
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/lib/fmcli.py, plugin/tests/test_lanes.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-31T14:01:22Z
updated: 2026-11-01T23:27:20Z
group: Mission 8 surfaces
base: 353076c7653add117893596b8ecfd70dc3574a68
base_tree: ef9118cb779e3ba7c0d9c258620ae3b31f0b9197
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-01T23:16:26Z
plan0_scope: [plugin/lib/fmlanes.py, plugin/lib/fmcli.py, plugin/tests/test_lanes.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# fm lane stats: builder landing rate by brief size
## Raw request
> fm lane stats: builder landing rate by brief size, so lane briefs can be trimmed where long ones land worse (Mission 8 inbox, tier 2)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane brief records the builder brief's size on its lane_builder event; fm lane stats (and --json) lists, per size bucket (up to 4k, 8k, 16k chars, more, unsized for older events), the briefs, how many landed (a lane_merge after the brief) and the share — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: two lane_builder events of 3k and 12k chars, one followed by lane_merge and one by lane_rm; fm lane stats --json gives up-to-4k 1 of 1 landed, up-to-16k 0 of 1; an event without chars counts as unsized
2. [x] fmlanes: mark() logs chars with the path; stats(p) joins each lane_builder to the task's next lane_merge, lane_rm or lane_stop; 'stats' in fm lane's choices; MASTER and CHANGELOG lines
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes.test_lane_stats_rates_landing_by_brief_size` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Lanes 0s) / FAILED (1 classes: test_lanes.Lanes) [ran] [tree a6da0d9e599c] (2026-11-01T23:16:46Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.Lanes.test_lane_stats_rates_landing_by_brief_size` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Lanes 0s) / OK [ran] [tree 40a6d27069dd] (2026-11-01T23:17:39Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_cli` → exit 0 · Ran 281 tests in 27.0s (56 classes, 16 at a time; slowest: LaneRecovery 27s, TaskLifecycle 25s, Lanes 22s) / OK [ran] [tree 40a6d27069dd] (2026-11-01T23:18:06Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_cli` → exit 0 · Ran 281 tests in 43.8s (56 classes, 16 at a time; slowest: TaskLifecycle 43s, LaneRecovery 41s, Lanes 41s) / OK [ran] [tree eb1e85af090f] (2026-11-01T23:19:49Z)
- (step 2) `fm lane stats` → exit 0 · unsized: 4 of 73 briefs landed (5%) / (unsized: a brief a later one overwrote, so that row leans toward lanes that were re-briefed) [ran] [tree eb1e85af090f] (2026-11-01T23:19:50Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 138 tests in 21.4s (12 classes, 16 at a time; slowest: LaneRecovery 21s, Lanes 15s, RaceEvidence 10s) / OK [ran] [tree eb1e85af090f] (2026-11-01T23:26:37Z)
- (audit edge) `self-review: stats() reads only lane_builder and lane_merge events, joins each brief to its task's next one (a merge lands it, a later brief or nothing doesn't), buckets by the event's chars, else by the task's audits/ brief file only when the event's path is exactly that file and no later brief overwrote it (no path from elsewhere is opened); the text says the unsized row leans toward re-briefed lanes; the brief text is computed once and its length logged` → a merge after a re-brief counts for the re-brief only; an event path outside audits/ isn't read; an overwritten brief stays unsized; no events prints 'No builder briefs on record yet.' [tree eb1e85af090f] (2026-11-01T23:26:37Z)
- (audit self) `self-review: stats() reads only lane_builder and lane_merge events, joins each brief to its task's next one (a merge lands it, a later brief or nothing doesn't), buckets by the event's chars, else by the task's audits/ brief file only when the event's path is exactly that file and no later brief overwrote it (no path from elsewhere is opened); the text says the unsized row leans toward re-briefed lanes; the brief text is computed once and its length logged` → no findings [tree eb1e85af090f] (2026-11-01T23:26:37Z)
## Log
- 2026-10-31T14:01:22Z created
- 2026-11-01T22:32:07Z planned from capture
- 2026-11-01T23:16:25Z focused
- 2026-11-01T23:16:26Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-01T23:27:17Z done
- 2026-11-01T23:27:20Z committed ddd253b6 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2353 [FEATURE M, done, 3 steps] The router picks the cheapest model that holds: probing down a tier, and fm run uses it too (Mission 8, #9) — lesson: A confirmation st…
- T-2355 [FEATURE M, done, 3 steps] One trigger table routes every event to inbox, queue, lane or mute, with budgets, learned from outcomes (Mission 8, #11) — lesson: A ro…
- T-2382 [FEATURE S, planned, 2 steps] Unknown fm verbs and flags as feature votes in fm friction
- decision 2026-10-31: Mission 6 (tools, #5) approach A: wire the parts Foreman has into one loop on the active task (T-2270's hook notices the miss; fm which, fm lib and …
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_lanes.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/tests/test_lanes.py; re-ground the plan against them before editing
## Lessons
- Backfill a new measure from what is still on disk, and say which rows the backfill can't reach and which way they lean
## Plan gaps
- failed first: step 1 red test: two lane_builder events of 3k and 12k chars, one followed by lane_merge and one by lane_r…
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmcli.py
- plugin/lib/fmlanes.py
- MASTER.md
- CHANGELOG.md
