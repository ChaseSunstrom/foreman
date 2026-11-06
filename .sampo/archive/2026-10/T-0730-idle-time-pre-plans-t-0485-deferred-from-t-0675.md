---
id: T-0730
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmnight.py, plugin/tests/test_night.py]
depends_on: []
source: followup
created: 2026-10-09T17:41:38Z
updated: 2026-10-09T21:32:59Z
base: a6c57993b63d690889144da5fc59f78244591fd3
base_tree: dc0b79f3560cdc926eb789d123234bee18c24439
verified: strong
---
# Idle-time pre-plans: fm night reads the plan of a queued L task without one
## Raw request
> Idle-time pre-plans (T-0485, deferred from T-0675): fm night writes a read-only pre-plan (fm second plan) for queued L tasks without one, and runs a friction pass over the log; skipped while usage runs ahead of pace
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a queued L task without a plan review gets a night pre-plan job, skipped while usage runs ahead of pace — verify with `python3 plugin/tests/run.py -p test_night.py -k PrePlan`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test and night job
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_night.py -k PrePlan` → ✗ exit 1 · Ran 0 tests in 0.0s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree 51e5c754d6b6] (2026-10-09T21:31:16Z)
- (step 1) `python3 plugin/tests/run.py -p test_night.py -k PrePlan` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: PrePlan 0s) / FAILED (1 classes) [ran] [tree b687a08d9a66] (2026-10-09T21:31:27Z)
- (step 1) `python3 plugin/tests/run.py -p test_night.py -k PrePlan` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: PrePlan 0s) / OK [ran] [tree 73c05b621fa8] (2026-10-09T21:31:33Z)
- (ac 1) `python3 plugin/tests/run.py -p test_night.py -k PrePlan` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: PrePlan 0s) / OK [ran] [tree bb6cd532bb91] (2026-10-09T21:32:52Z)
- `python3 plugin/tests/run.py -p test_night.py` → exit 0 · Ran 12 tests in 1.6s (5 classes, 16 at a time; slowest: NightGuards 2s, Night 1s, PrePlan 0s) / OK [ran] [tree bb6cd532bb91] (2026-10-09T21:32:52Z)
- (audit self) `self: one job, budget-estimated like the other paid night jobs, skipped while degrade() says usage runs ahead of pace; the friction-pass half is left out — fm next already triggers it every N closed tasks and holds it while ahead of pace, so a night copy would only duplicate it` → no findings [tree bb6cd532bb91] (2026-10-09T21:32:52Z)
- `python3 plugin/tests/run.py -p test_night.py` → exit 0 · Ran 12 tests in 1.6s (5 classes, 16 at a time; slowest: NightGuards 2s, Night 1s, PrePlan 0s) / OK [ran] [tree bb6cd532bb91] (2026-10-09T21:32:59Z)
- (audit self) `self: one job, budget-estimated like the other paid night jobs, skipped while degrade() says usage runs ahead of pace; the friction-pass half is left out — fm next already triggers it every N closed tasks and holds it while ahead of pace, so a night copy would only duplicate it` → no findings [tree bb6cd532bb91] (2026-10-09T21:32:59Z)
## Log
- 2026-10-09T17:41:38Z created
- 2026-10-09T21:31:04Z planned from capture
- 2026-10-09T21:31:07Z focused
- 2026-10-09T21:32:57Z scope: CHANGELOG.md gets this task's line and the T-0744/T-0749/T-0750 fixes' line (they closed without one)
- 2026-10-09T21:32:59Z done
- 2026-10-09T21:32:59Z committed c05a8e0 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0485 [FEATURE M, done, 0 steps] Speculative and idle-time work (C022, value 3/5, effort M, risk med)
- T-0555 [FEATURE M, dropped, 0 steps] Speculative and idle-time work (C022, value 3/5, effort M, risk med)
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- decision 2026-10-09: [costly] T-0712's overnight run (fm night generating guard and hook candidates with model calls, scored by fm replay --candidate and fm burden) defe…
- similar past tasks were M: consider --tier M
- similar finished tasks took 0–7 steps
- likely tests for the scope: plugin/tests/test_night.py
## Preflight
Changed in scope since this was planned (2026-10-09): plugin/lib/fmnight.py, plugin/tests/test_night.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 test and night job
## Files touched
- plugin/tests/test_night.py
- plugin/lib/fmnight.py
- CHANGELOG.md
