---
id: T-2473
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T15:20:02Z
updated: 2026-11-01T15:32:30Z
base: 099f595b647830be94ffba8d1a0dc4fb6519051c
base_tree: 3ea7c196b9e5bb049eb475b7a4181558bfe87a3d
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-01T15:20:03Z
plan0_scope: []
verified: strong
---
# The cold reader's exam summary drops the per-kind closed counts and the forecast, breakage and replay numbers, so a critique's true lines citing them fail as unverifiable (blocks Missions 7 and 8's filing)
## Raw request
> The cold reader's exam summary drops the per-kind closed counts and the forecast, breakage and replay numbers, so a critique's true lines citing them fail as unverifiable (blocks Missions 7 and 8's filing)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the exam tail shows closed by kind, forecast, breakage and replay numbers — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then add them to _exam_tail's score line
## Resume here
## Docs impact
none: the tail is internal to the cold read; MASTER's T-2366 note covers what it carries
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_the_cold_reads_exam_tail_carries_the_numbers_critiques_cite test_genesis` → ✗ exit 1 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / FAILED (1 classes: test_genesis.GenesisDraft) [ran] [tree a3f2cf34af92] (2026-11-01T15:20:18Z)
- `python3 plugin/tests/run.py -k test_the_cold_reads_exam_tail_carries_the_numbers_critiques_cite test_genesis` → ✗ exit 1 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / FAILED (1 classes: test_genesis.GenesisDraft) (start tree + this task's tests) [ran] [tree 0c9c12da5cb9] (2026-11-01T15:20:35Z)
- `python3 plugin/tests/run.py -k test_the_cold_reads_exam_tail_carries_the_numbers_critiques_cite test_genesis` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / OK [ran] [tree 0c9c12da5cb9] (2026-11-01T15:20:35Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 181 tests in 11.7s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 8s, GenesisCheck 8s) / OK [ran] [tree 0c9c12da5cb9] (2026-11-01T15:20:47Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 181 tests in 11.0s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 8s, GenesisCheck 7s) / OK [ran] [tree 0c9c12da5cb9] (2026-11-01T15:21:09Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 181 tests in 11.2s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisCheck 8s, GenesisSweep 8s) / OK [ran] [tree 0c9c12da5cb9] (2026-11-01T15:27:00Z)
- (audit intent) `main-thread lens pass over the 15-line diff and its test; Missions 7 and 8 and their critiques then filed with the numbers it exposes` → the reader's exam summary now carries closed scenarios by kind, forecast type against naive, breakage flagged and false, and the replay's type and path scores, so a critique's true numbers are checkable [tree 0c9c12da5cb9] (2026-11-01T15:27:00Z)
- (audit edge) `main-thread lens pass over the 15-line diff and its test; Missions 7 and 8 and their critiques then filed with the numbers it exposes` → non-numeric or missing fields are skipped (num() and the replay all() guard); an id without KIND-LANG-HASH shape is not counted; booleans never count as numbers [tree 0c9c12da5cb9] (2026-11-01T15:27:00Z)
- (audit operator) `main-thread lens pass over the 15-line diff and its test; Missions 7 and 8 and their critiques then filed with the numbers it exposes` → the tail grows by one 'closed by kind' clause per row (34 kinds at most), within the read prompt [tree 0c9c12da5cb9] (2026-11-01T15:27:00Z)
- (audit self) `main-thread lens pass over the 15-line diff and its test; Missions 7 and 8 and their critiques then filed with the numbers it exposes` → no findings [tree 0c9c12da5cb9] (2026-11-01T15:27:00Z)
## Log
- 2026-11-01T15:20:02Z created
- 2026-11-01T15:20:02Z focused
- 2026-11-01T15:20:03Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-01T15:20:57Z scope: plugin/lib/fmgenesis.py (_exam_tail) and plugin/tests/test_genesis.py only
- 2026-11-01T15:27:27Z done
- 2026-11-01T15:27:30Z committed be067f4d (2 files)
- 2026-11-01T15:27:44Z guard authorization added: publish
- 2026-11-01T15:32:30Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2471 [FEATURE L, done, 3 steps] Cold read made reliable: Haiku first and Sonnet decides on a non-pass, a FAIL counts only with the quoted line and the MUST/NEVER or st…
- T-2409 [FEATURE M, done, 4 steps] #3 exam kinds forecast and breakage: next-request prediction against a naive baseline, and breakage flagged before it bites (Mission 8,…
- T-2366 [FIX S, done, 1 steps] The cold read's exam tail carries the numbers critiques cite: exam defects, ranking, recall by language and kind, and long-tier true done, …
- decision 2026-10-31: [costly] Tower filing waits for the user's call on the cold-read rule: Missions 5-8's files and the Mission 3-4 critiques stay unfiled after 4-12 pu…
## Lessons
- When a reader must check numbers, the summary it gets must hold every number the writer is told to cite; otherwise true lines fail as unverifiable
## Plan gaps
- failed first: step 1 red test, then add them to _exam_tail's score line
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
