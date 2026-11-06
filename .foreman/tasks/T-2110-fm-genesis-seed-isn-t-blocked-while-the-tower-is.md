---
id: T-2110
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-30T06:36:03Z
updated: 2026-10-30T13:02:12Z
base: 261626b852c7884f4d0e2a09d4d86737cee1a97e
base_tree: 733e9f05837415958ac6b4b691b4eb23adbe7808
plan0_at: 2026-10-30T12:59:28Z
plan0_scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# fm genesis seed` isn't blocked while the tower is stopped, so the breaker is advisory
## Raw request
> fm genesis seed` isn't blocked while the tower is stopped, so the breaker is advisory
> (noticed by an agent; research T-2105-review)
## Interpretation
step() reports kind stopped after three reverted generations, but fm genesis seed N still writes a seed, so the breaker only advises. seed() must refuse while the tower is stopped; a hand-written seed through fm genesis put stays the way out (step's own command).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis seed refuses on a stopped tower and a hand-written put still restarts it — verify with `python3 plugin/tests/run.py test_genesis.GenesisPropose`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: seed(p, 4) raises on three reverted generations
2. [x] _stopped helper shared by step() and _seed()
## Resume here
## Docs impact
MASTER.md fmgenesis T-2105 sentence; CHANGELOG
## Verification evidence
- `python3 plugin/tests/run.py test_genesis.GenesisPropose` → ✗ exit 1 · Ran 4 tests in 2.6s (1 classes, 16 at a time; slowest: GenesisPropose 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 57e654e3acb0] (2026-10-30T12:59:35Z)
- `python3 plugin/tests/run.py test_genesis.GenesisPropose` → ✗ exit 1 · Ran 4 tests in 1.3s (1 classes, 16 at a time; slowest: GenesisPropose 1s) / FAILED (1 classes) [ran] [tree 57e654e3acb0] (2026-10-30T12:59:35Z)
- `python3 plugin/tests/run.py test_genesis.GenesisPropose` → ✗ exit 1 · Ran 4 tests in 2.3s (1 classes, 16 at a time; slowest: GenesisPropose 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 4f04902cdd90] (2026-10-30T12:59:43Z)
- `python3 plugin/tests/run.py test_genesis.GenesisPropose` → exit 0 · Ran 4 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisPropose 1s) / OK [ran] [tree 4f04902cdd90] (2026-10-30T12:59:43Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisPropose` → exit 0 · Ran 4 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisPropose 1s) / OK [ran] [tree 4f04902cdd90] (2026-10-30T12:59:49Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 74 tests in 8.5s (12 classes, 16 at a time; slowest: GenesisLive 8s, GenesisSweep 7s, GenesisCheck 6s) / OK [ran] [tree 4f04902cdd90] (2026-10-30T12:59:58Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.GenesisPropose` → exit 0 · Ran 4 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisPropose 1s) / OK [ran] [tree 4f04902cdd90] (2026-10-30T12:59:59Z)
- (audit intent) `diff re-read against the raw request (breaker advisory)` → seed() now refuses on the same condition step() reports stopped; put stays the way out, as step's own command names [tree 2cfee3053adf] (2026-10-30T13:00:22Z)
- (audit edge) `n-1 < 3 can't stop (helper's n >= 3); a non-reverted gen in the last three lets seed go; the refusal is a ValueError, which cmd_genesis turns into a usage error (exit 2), not a crash` → holds; the stop test now covers seed refusing then a hand put restarting [tree 2cfee3053adf] (2026-10-30T13:00:22Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.GenesisPropose` → exit 0 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: GenesisPropose 1s) / OK [ran] [tree 2cfee3053adf] (2026-10-30T13:01:59Z)
- (audit edge) `self-review of a 14-line diff: step() and seed() share _stopped; red→green proved` → n<3 never stops; a non-reverted gen in the last three lets seed go; refusal is a usage error, not a crash [tree 2cfee3053adf] (2026-10-30T13:01:59Z)
- (audit self) `self-review of a 14-line diff: step() and seed() share _stopped; red→green proved` → no findings [tree 2cfee3053adf] (2026-10-30T13:01:59Z)
## Log
- 2026-10-30T06:36:03Z created
- 2026-10-30T12:56:19Z set type=FIX, tier=S
- 2026-10-30T12:56:19Z planned: it has criteria and steps
- 2026-10-30T12:56:19Z set scope=['plugin/lib/fmgenesis.py', 'plugin/tests/test_genesis.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-30T12:56:30Z criterion 1 verify: `python3 plugin/tests/run.py test_genesis.GenesisStops` → `python3 plugin/tests/run.py test_genesis.GenesisPropose`
- 2026-10-30T12:59:27Z focused
- 2026-10-30T12:59:29Z set approved=True
- 2026-10-30T13:00:22Z scope: MASTER.md, CHANGELOG.md — the stop rule's docs line and an Unreleased entry
- 2026-10-30T13:02:10Z done
- 2026-10-30T13:02:12Z committed 54a116da (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2095 [FEATURE M, done, 3 steps] fm genesis step: the tower's next action from its files, resumable after any kill — lesson: A resumable state machine over files has to…
- research T-2105-review: Verdict** — changes needed. The confirm task shows the user a false reason, and nothing tests the site export that AC3 relies on. Both fixes are …
- decision 2026-10-30: T-2112: #13's draft kinds live in fmgenesis (fm genesis exam) reusing fmexam.draw/render and cover; G-tower is a 'genesis' session arm on fmexam's d…
- likely tests for the scope: plugin/tests/test_genesis.py
## Preflight
Changed in scope since this was planned (2026-10-30): CHANGELOG.md, MASTER.md, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py; re-ground the plan against them before editing
## Why not caught
T-2105's test checked step() and fm next but never called seed() on a stopped tower
## Lessons
- A breaker the status reports must also be enforced by every verb that would cross it; test the verb, not only the report
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
