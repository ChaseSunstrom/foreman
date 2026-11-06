---
id: T-2424
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmoutcomes.py, plugin/tests/test_judgment.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-31T15:38:28Z
updated: 2026-11-02T02:04:08Z
base: 33297402b3f668ad22f32d6c89cd1acf64e0f40e
base_tree: b6a2d639b2edca8540de1c229c315a8d31bed86c
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T01:52:17Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmoutcomes.py, plugin/tests/test_judgment.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# rival_split is read: a parked one-way door says whether the cold rival read the task differently, and ambiguous ones lead the final report
## Raw request
> nothing in `plugin/` outside the test files reads `rival_split`, so T-2338's ambiguity routing is unwired
> (noticed by an agent; research T-2341-review)
## Interpretation
Reading 1: wire rival_split (fmsecond) into the door park: door_park's line says 'one-way and ambiguous' only when the brief is rival_split and 'one-way' otherwise, and fm decide --review's priced doors list the ambiguous ones first; nothing parks less. Reading 2: gen-0 #8 literally: park only when one-way AND ambiguous, so an unambiguous one-way step proceeds with a costly decision recorded. Reading 1 fits now: Reading 2 loosens a stop on irreversible work, which is the user's call; it is recorded with fm decide --kind costly for the final report.
## Assumptions (confidence)
## Acceptance criteria
- [x] fmdoors._ambiguous reads rival_split: an M or L brief whose cold rival read differs (rival_split) is ambiguous even with one written reading, so its one-way step parks for the final report instead of running as a costly decision; a brief without the split behaves as before — verify with `python3 plugin/tests/run.py test_judgment`
## Non-goals
## Approach (options → choice → why)
1) door_park reads b.meta rival_split for its wording; fmoutcomes.priced_doors sorts ambiguous first and marks them; fm next's park line carries the same word; fails if: nobody reads the word (then the final report's order is the use). 2) use what exists: leave it unread; fails if: the T-2341 criterion says brief 8 reads it as ambiguous, so the signal is dead code. 3) do less: delete rival_split; fails if: the rival read's top-reading split is the only ambiguity signal Foreman has. Choice 1 (80%): read the signal where parks are said and ordered, loosen nothing.
## Risks and rollback
Risk: code matching the old 'one-way and ambiguous:' prefix (fm next, the drive's skip, tests) misses the new 'one-way:' wording; grep door_park's readers and match both. Rollback: revert; nothing parks less either way.
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/tests/test_guard.py, README.md; past FIXes T-0876, T-0907, T-0980, T-0985, T-0986.
## Execution prompt
## Steps
1. [x] red test: two briefs with an open one-way door, one rival_split: door_park words differ; priced_doors orders the split one first
2. [x] fmcore.door_park wording; fmoutcomes.priced_doors order and flag; fm decide --kind costly records the stricter reading (park only one-way and ambiguous) for the user; MASTER, CHANGELOG
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_judgment.DoorPark` → ✗ exit 1 · Ran 19 tests in 13.1s (1 classes, 16 at a time; slowest: DoorPark 13s) / FAILED (1 classes: test_judgment.DoorPark) [ran] [tree 5e8955f2228a] [world 2f1906870a] (2026-11-02T01:53:21Z)
- (step 1) `python3 plugin/tests/run.py test_judgment.DoorPark` → exit 0 · Ran 19 tests in 14.5s (1 classes, 16 at a time; slowest: DoorPark 14s) / OK [ran] [tree c472b0f81c2a] [world 2f1906870a] (2026-11-02T01:54:33Z)
- (step 2) `python3 plugin/tests/run.py test_judgment test_second` → exit 0 · Ran 101 tests in 20.5s (33 classes, 16 at a time; slowest: Rival 20s, DoorPark 18s, DoorGate 10s) / OK [ran] [tree c472b0f81c2a] [world 2f1906870a] (2026-11-02T01:54:54Z)
- `python3 plugin/tests/run.py test_judgment.DoorPark` → ✗ exit 1 · Ran 19 tests in 16.3s (1 classes, 16 at a time; slowest: DoorPark 14s) / FAILED (1 classes: test_judgment.DoorPark) (start tree + this task's tests) [ran] [tree c472b0f81c2a] [world 2f1906870a] (2026-11-02T01:55:24Z)
- `python3 plugin/tests/run.py test_judgment.DoorPark` → exit 0 · Ran 19 tests in 13.2s (1 classes, 16 at a time; slowest: DoorPark 13s) / OK [ran] [tree c472b0f81c2a] [world 2f1906870a] (2026-11-02T01:55:24Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment` → exit 0 · Ran 64 tests in 8.8s (20 classes, 16 at a time; slowest: DoorPark 8s, DoorGate 4s, Followups 3s) / OK [ran] [tree 5ab2aa26cabb] [world 2f1906870a] (2026-11-02T02:02:34Z)
- (audit intent) `self-review: fmdoors._ambiguous now returns true for an M/L brief marked rival_split as well as for two distinct readings; that only moves a named one-way step from 'run as a costly decision' to 'park', never the other way; S briefs are unaffected (the rival read doesn't split them); the test covers one written reading with and without the split` → T-2341's criterion said the door gate reads rival_split as ambiguous; it was written but never read [tree 5ab2aa26cabb] (2026-11-02T02:02:34Z)
- (audit edge) `self-review: fmdoors._ambiguous now returns true for an M/L brief marked rival_split as well as for two distinct readings; that only moves a named one-way step from 'run as a costly decision' to 'park', never the other way; S briefs are unaffected (the rival read doesn't split them); the test covers one written reading with and without the split` → no split and one reading runs as costly; a split with one reading parks; two readings park as before; an S brief never reads the split [tree 5ab2aa26cabb] (2026-11-02T02:02:34Z)
## Log
- 2026-10-31T15:38:28Z created
- 2026-11-02T01:04:13Z planned from capture
- 2026-11-02T01:04:13Z set approved=True
- 2026-11-02T01:52:15Z focused
- 2026-11-02T01:52:17Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T01:52:46Z criterion 1 text: a brief with an open one-way step parks as 'one-way and ambiguous: …' when rival_split is set and 'one-way: …' when not; priced_doors lists the rival_split ones first with ambiguous: true → fmdoors._ambiguous reads rival_split: an M or L brief whose cold rival read differs (rival_split) is ambiguous even with one written reading, so its one-way step parks for the final report instead of running as a costly decision; a brief without the split behaves as before
- 2026-11-02T01:52:46Z steer: re-scoped after reading fmdoors: the door gate already parks only irreversible AND ambiguous steps (_ambiguous: two readings), letting a named unambiguous one run as a costly decision; T-2341's criterion ('brief 8 reads rival_split as ambiguous') means _ambiguous should read it. That parks more, never less. The wording and priced-doors ordering idea is dropped
- 2026-11-02T01:55:25Z scope: plugin/lib/fmdoors.py (_ambiguous) is where the door gate reads ambiguity; fmcore/fmoutcomes untouched after the re-scope
- 2026-11-02T02:04:06Z done
- 2026-11-02T02:04:08Z committed e916a8db (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-02: [costly] One-way doors keep parking whether or not the task is ambiguous; rival_split only words and orders the park (T-2424)
- T-2342 [FEATURE M, done, 4 steps] Stop only at an irreversible, ambiguous step (Mission 5, #8): plan steps are classified one-way or two-way by the guard's own command p…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- decision 2026-11-01: [cites: user steer 2026-11-01: standing rule (3): never block on the user for a question about rules, gates or process; decide by gen-0 and the stan…
- similar finished tasks took 4–7 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_outcomes.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, MASTER.md, plugin/lib/fmcore.py, plugin/lib/fmoutcomes.py, plugin/tests/test_judgment.py; re-ground the plan against them before editing
## Lessons
- A signal that is written but never read is a promise the code doesn't keep; grep each new meta key for its reader before closing
## Plan gaps
- failed first: step 1 red test: two briefs with an open one-way door, one rival_split: door_park words differ; priced_doo…
## Files touched
- plugin/tests/test_judgment.py
- plugin/lib/fmdoors.py
- MASTER.md
- CHANGELOG.md
