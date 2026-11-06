---
id: T-2433
type: FIX
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-31T17:55:03Z
updated: 2026-10-31T17:58:04Z
trigger: baseline
trigger_key: ba6b643ad11cd330
baseline: true
base: 88c580a8e1125fe390d3cd34cc83fb5ed514e560
base_tree: 2c76251b403cd26b5e8fbdd41722fd7e4ee2c022
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-10-31T17:56:40Z
plan0_scope: []
verified: strong
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_race.Race.test_l_tasks_and_second_races_are_refused. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
Reading 1: T-2340 made a planned L raceable (a design race), so an unplanned L is now refused by the plan check ('isn't planned enough'), not by the old 'S or M only' rule; test_race still expects 'S or M'. Reading 2: T-2340 broke the refusal. Ruled out: the refusal still happens, only its reason changed, as T-2340 intends.
## Assumptions (confidence)
## Acceptance criteria
- [x] test_race passes with an unplanned L race refused for its plan — verify with `python3 plugin/tests/run.py test_race`
## Non-goals
## Approach (options → choice → why)
1) assert the refusal and its current reason ('planned enough'); fails if: the planned-L path is untested here (DesignRace in test_lanes covers it). 2) use what exists: delete the L half of the test; fails if: the unplanned-L refusal loses its only test here. 3) do less: skip the test; fails if: hides a real refusal break. Choice 1 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] update the L expectation to the plan refusal
## Resume here
## Docs impact
none: a test expectation
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_race` → exit 0 · Ran 4 tests in 6.4s (1 classes, 16 at a time; slowest: Race 6s) / OK [ran] [tree 3a0012fa4088] (2026-10-31T17:56:57Z)
- (ac 1) `python3 plugin/tests/run.py test_race` → exit 0 · Ran 4 tests in 7.1s (1 classes, 16 at a time; slowest: Race 7s) / OK [ran] [tree 3a0012fa4088] (2026-10-31T17:57:15Z)
- (audit intent) `self-review: the L refusal still happens (exit nonzero), only its reason changed with T-2340's design race; DesignRace covers the planned-L path` → an unplanned L race stays refused [tree 3a0012fa4088] (2026-10-31T17:57:15Z)
- (audit edge) `self-review: the L refusal still happens (exit nonzero), only its reason changed with T-2340's design race; DesignRace covers the planned-L path` → the second-race refusal half of the test is unchanged and passes [tree 3a0012fa4088] (2026-10-31T17:57:15Z)
## Log
- 2026-10-31T17:55:03Z created
- 2026-10-31T17:56:38Z planned: it has criteria and steps
- 2026-10-31T17:56:39Z focused
- 2026-10-31T17:56:40Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-10-31T17:57:50Z done
- 2026-10-31T17:57:53Z committed e4301beb (1 file)
- 2026-10-31T17:58:04Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2429 [FIX M, done, 1 steps] Baseline red:… — lesson: A test that appends then shifts an mtime is shifting from the wall clock: read the mtime before the write
- T-2283 [FIX S, done, 1 steps] Baseline red: `python3 plugin/tests/run.py` fails… — lesson: A test that pins the live import graph should pick its example from a leaf mod…
- T-1790 [FIX S, done, 2 steps] Baseline red: `python3 plugin/tests/run.py` fails test_relate.Due.test_session_start_runs_
- decision 2026-10-30: [revisited: no idea is killed for ambition] [cites: user steer 2026-10-29: NO IDEA IS KILLED FOR AMBITION] [check: python3 plugin/tests/run.py test_…
- similar finished tasks took 1–2 steps
## Regression test
none: a stale expectation in a test, fixed in the test itself; the refusal it checks is unchanged
## Why not caught
T-2340's fm check --affected didn't select test_race; the full gates after its merge would have
## Lessons
- A lane that changes a refusal's reason must grep the suite for the old message: T-2340's builder ran only affected tests
## Files touched
- plugin/tests/test_race.py
