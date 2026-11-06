---
id: T-1116
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcost.py, plugin/tests/test_perf_cost.py]
depends_on: []
source: discovered
created: 2026-10-16T05:44:49Z
updated: 2026-10-16T05:48:04Z
base: fbbede8656d5b94f393bc520a1d132d25cd5c052
base_tree: 83a270fd5d30bdd6a062ccb5262f101b62e2427e
verified: strong
---
# Fm cost takes 6.8 s on the real state: fmcost._task_at is a linear scan per turn (11,993 c
## Raw request
> fm cost takes 6.8 s on the real state: fmcost._task_at is a linear scan per turn (11,993 calls, 4.1 s); bisect over sorted focus events
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] Turns are attributed to the same tasks as before (incl. a turn at an event's exact second and one before any event), and events from rolled months count — verify with `python3 plugin/tests/run.py test_perf_cost`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test the attribution edges, then bisect and read c.ledger_events
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_perf_cost` → exit 0 · Ran 15 tests in 2.5s (7 classes, 16 at a time; slowest: StepCompact 2s, DegradeOnPace 2s, UnexplainedSpend 1s) / OK [ran] [tree c3f2c1813904] (2026-10-16T05:45:34Z)
- (step 1) `python3 plugin/tests/run.py test_perf_cost` → ✗ exit 1 · Ran 15 tests in 5.9s (7 classes, 16 at a time; slowest: TaskAt 6s, StepCompact 5s, DegradeOnPace 4s) / FAILED (1 classes) [ran] [tree e6a8c5d96a65] (2026-10-16T05:46:10Z)
- (step 1) `python3 plugin/tests/run.py test_perf_cost test_economics` → exit 0 · Ran 17 tests in 5.0s (9 classes, 16 at a time; slowest: StepCompact 5s, DegradeOnPace 4s, UnexplainedSpend 2s) / OK [ran] [tree 0fbadab733a9] (2026-10-16T05:46:24Z)
- (step 1) `python3 plugin/tests/run.py test_perf_cost test_economics test_cost` → exit 0 · Ran 24 tests in 2.7s (14 classes, 16 at a time; slowest: StepCompact 3s, DegradeOnPace 2s, UnexplainedSpend 1s) / OK [ran] [tree 529700370921] (2026-10-16T05:47:46Z)
- (ac 1) `python3 plugin/tests/run.py test_perf_cost` → exit 0 · Ran 16 tests in 2.6s (8 classes, 16 at a time; slowest: StepCompact 2s, DegradeOnPace 2s, UnexplainedSpend 1s) / OK [ran] [tree ec30c97949e8] (2026-10-16T05:48:02Z)
- (audit self) `self: attribution edges (same second, before any event, empty) and the prefilter's nested-stamp case tested; numbers measured on the real state` → no findings [tree ec30c97949e8] (2026-10-16T05:48:02Z)
## Log
- 2026-10-16T05:44:49Z created
- 2026-10-16T05:45:21Z set scope=['plugin/lib/fmcost.py', 'plugin/tests/test_perf_cost.py']
- 2026-10-16T05:45:24Z focused
- 2026-10-16T05:47:22Z steer (self): the bisect took _task_at 4.1 s → 0.04 s; the rest is scan and timing each json-parsing 559 MB of transcripts. Widening: one shared reader that skips files not modified since the cutoff and lines whose timestamps are all older, before parsing
- 2026-10-16T05:47:59Z scope: CHANGELOG.md — release note
- 2026-10-16T05:48:03Z done
- 2026-10-16T05:48:04Z committed c299f04 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- research wave1-plan-a306a171bb6861f90: === T-1044 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- T-0959 [FEATURE M, done, 3 steps] Brainstorm and cost: keep a child's partial answer, a run manifest, cache-bust causes, friction minutes, unused verbs — lesson: A repor…
- decision 2026-10-06: [revisit: after 2026-12-01] Drop T-0356: keep 'fm task new --focus' and the first edit as separate calls
- similar finished tasks took 2–3 steps
## Measurements
fm cost on the real state (559 MB of transcripts, 7-day window), wall clock: 7.6 s before → 3.8 s after. cProfile: _task_at 4.1 s → 0.04 s (bisect); scan + timing now skip files not written since the cutoff and lines whose newest timestamp is older, before json parsing.
## Lessons
- Before parsing a big log, skip by file mtime and a cheap substring check; parse only what can be in the window
## Files touched
- plugin/tests/test_perf_cost.py
- plugin/lib/fmcost.py
- CHANGELOG.md
