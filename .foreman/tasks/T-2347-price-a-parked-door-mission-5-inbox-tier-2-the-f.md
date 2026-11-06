---
id: T-2347
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T13:59:19Z
updated: 2026-11-01T08:21:14Z
inferred_deps: [T-2346]
inferred_why: T-2346: prices the parked steps the doors tally lists
group: Mission 5 inbox items
base: a5bbf436ccc981853aae77d8f7f6d1ece7faea61
base_tree: 562cc897a25b8f77f1ef88588857118e6096d05f
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-01T08:08:35Z
plan0_scope: []
verified: strong
---
# Price a parked door: the final report (fm decide --review) lists each task parked at a one-way step with the days it has waited and the open tasks waiting behind it
## Raw request
> Price a parked door (Mission 5 inbox, tier 2): the final report shows what each parked one-way step blocks (tasks waiting behind it, days parked)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm decide --review shows a 'Parked at a one-way door' line per parked task: its step, days since it parked (the door_park event) and the open tasks that depend on it, and its JSON carries doors_parked with those fields; nothing when none is parked (the band stays ledger-free: only --review reads the ledger) — verify with `python3 plugin/tests/run.py test_judgment`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the price in fmoutcomes.extras and fm decide --review
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_judgment -k test_the_final_report_prices` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: DoorPark 0s) / FAILED (1 classes: test_judgment.DoorPark) [ran] [tree 054a3a6e5ffa] (2026-11-01T08:08:43Z)
- (step 2) `python3 plugin/tests/run.py test_judgment test_decide test_outcomes` → exit 0 · Ran 112 tests in 24.9s (31 classes, 16 at a time; slowest: Survival 24s, ModelRouter 19s, DoorPark 19s) / OK [ran] [tree bc20ce518aee] (2026-11-01T08:09:20Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment test_docs` → exit 0 · Ran 159 tests in 9.0s (39 classes, 16 at a time; slowest: DoorPark 9s, Fences 8s, DoorGate 4s) / OK [ran] [tree 21f264e11cfe] (2026-11-01T08:09:38Z)
- `python3 plugin/tests/run.py test_judgment -k test_the_final_report_prices` → ✗ exit 1 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: DoorPark 0s) / FAILED (1 classes: test_judgment.DoorPark) (start tree + this task's tests) [ran] [tree 21f264e11cfe] (2026-11-01T08:09:41Z)
- `python3 plugin/tests/run.py test_judgment -k test_the_final_report_prices` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: DoorPark 0s) / OK [ran] [tree 21f264e11cfe] (2026-11-01T08:09:41Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment` → exit 0 · Ran 57 tests in 8.5s (16 classes, 16 at a time; slowest: DoorPark 8s, DoorGate 4s, Followups 3s) / OK [ran] [tree 21f264e11cfe] (2026-11-01T08:15:15Z)
- (audit self) `self: fm check exit 0; red→green test (a parked task's line with its step, 0 days and the task waiting behind it; the JSON's doors_parked; nothing once unparked); fm task prove proved; only --review reads the ledger, the band's snapshot is unchanged` → no findings [tree 21f264e11cfe] (2026-11-01T08:15:15Z)
## Log
- 2026-10-31T13:59:19Z created
- 2026-11-01T07:51:06Z planned from capture
- 2026-11-01T08:08:34Z steer: criterion narrowed to fm decide --review (the final report); fm calibration's snapshot feeds the band, which must not read the ledger
- 2026-11-01T08:08:34Z focused
- 2026-11-01T08:08:35Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-01T08:09:41Z scope: plugin/lib/fmoutcomes.py (priced_doors), plugin/lib/fmcli.py (the --review lines), plugin/tests/test_judgment.py (the test), MASTER.md and CHANGELOG.md (docs)
- 2026-11-01T08:15:52Z done
- 2026-11-01T08:15:54Z committed 541ceeda (5 files)
- 2026-11-01T08:16:00Z guard authorization added: publish
- 2026-11-01T08:21:14Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2342 [FEATURE M, done, 4 steps] Stop only at an irreversible, ambiguous step (Mission 5, #8): plan steps are classified one-way or two-way by the guard's own command p…
- T-2346 [FEATURE S, done, 2 steps] Doors tally on the finish receipt: one line naming each one-way step and how it was undone or parked — lesson: A receipt line that only…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- decision 2026-10-31: Genesis gen 1's tower step waits on Mission 3's critique (T-2221, blocked: the cold read doesn't converge on it after 18 puts; proposal T-2246 goes …
## Lessons
- Put a ledger scan on the path a person asks for (the final report), never on one a hook runs every turn
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_judgment.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
