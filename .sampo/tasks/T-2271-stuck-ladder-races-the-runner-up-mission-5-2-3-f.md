---
id: T-2271
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T04:51:00Z
updated: 2026-10-31T05:50:46Z
base: c4fb8f08ff25021644c7e943935218cd52caa1b8
base_tree: 802db5f26117a5754f8afc8724647d195570dbe6
plan0_at: 2026-10-31T05:47:08Z
plan0_scope: []
verified: strong
---
# Stuck ladder races the runner-up (Mission 5, #2): 3 failed runs on a step of an S/M task whose Approach names an alternative and no race yet → fm lane race, before the hypothesis table
## Raw request
> Stuck ladder races the runner-up (Mission 5, #2): 3 failed runs on a step of an S/M task whose Approach names an alternative and no race yet → fm lane race, before the hypothesis table
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] stuck_rung at 3+ failed runs on an S/M task with 2+ Approach options and no race returns a race rung naming fm lane race ID; with one option, an L task or a race already run it returns today's hypothesis rungs; fm next shows it — verify with `python3 plugin/tests/run.py test_reasoning test_core`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests for the race rung and its exclusions, then the rung in fmcore.stuck_rung; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_reasoning` → ✗ exit 1 · Ran 9 tests in 5.665s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 20966b1f540b] (2026-10-31T05:47:56Z)
- `cd plugin/tests && python3 -m unittest -q test_reasoning` → exit 0 · Ran 9 tests in 6.008s / OK [ran] [tree 20966b1f540b] (2026-10-31T05:47:56Z)
- (step 1) `python3 plugin/tests/run.py test_reasoning test_core` → exit 0 · Ran 105 tests in 4.1s (28 classes, 16 at a time; slowest: BriefIndex 4s, Race 3s, Stall 3s) / OK [ran] [tree 20966b1f540b] (2026-10-31T05:48:01Z)
- (ac 1) `python3 plugin/tests/run.py test_reasoning test_core` → exit 0 · Ran 105 tests in 5.9s (28 classes, 16 at a time; slowest: BriefIndex 5s, Race 4s, Stall 4s) / OK [ran] [tree ed73bb9d327f] (2026-10-31T05:50:13Z)
- (audit intent) `self: one rung in stuck_rung reusing T-2269's _count_options; placed after the differential-table rung (cheap probes of existing hypotheses first) and before the plain hypotheses rung; S/M only (race's own limit), never twice (race/race_of)` → Mission 5's auto race by evidence: three failed runs with an alternative on file point at fm lane race, scored on the task's checks (test_reasoning red-to-green) [tree ed73bb9d327f] (2026-10-31T05:50:13Z)
- (audit edge) `self: one rung in stuck_rung reusing T-2269's _count_options; placed after the differential-table rung (cheap probes of existing hypotheses first) and before the plain hypotheses rung; S/M only (race's own limit), never twice (race/race_of)` → one approach, an L task or a task already raced keep the hypothesis rung [tree ed73bb9d327f] (2026-10-31T05:50:13Z)
- (audit self) `self: one rung in stuck_rung reusing T-2269's _count_options; placed after the differential-table rung (cheap probes of existing hypotheses first) and before the plain hypotheses rung; S/M only (race's own limit), never twice (race/race_of)` → no findings [tree ed73bb9d327f] (2026-10-31T05:50:13Z)
## Log
- 2026-10-31T04:51:00Z created
- 2026-10-31T04:51:13Z criterion 1 verify: `python3 plugin/tests/run.py test_core test_stuck` → `python3 plugin/tests/run.py test_reasoning test_core`
- 2026-10-31T05:47:07Z focused
- 2026-10-31T05:48:01Z scope: plugin/lib/fmcore.py (stuck_rung), plugin/tests/test_reasoning.py, CHANGELOG.md
- 2026-10-31T05:50:44Z done
- 2026-10-31T05:50:46Z committed 85b3b640 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0611 [FEATURE M, done, 0 steps] Hypothesis tournament (I050, value 4/5, effort M, risk low)
- T-2119 [FIX S, done, 1 steps] FIX S: fm genesis step reads a seed with no Missions table as a dry generation and jumps…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
- similar finished tasks took 0–5 steps
- start here (files T-2119 touched): plugin/tests/test_genesis.py, plugin/lib/fmgenesis.py, CHANGELOG.md, MASTER.md
## Lessons
- A ladder rung that costs more (a second builder) belongs after the cheaper probe rung that uses work already done
## Files touched
- plugin/tests/test_reasoning.py
- plugin/lib/fmcore.py
- CHANGELOG.md
