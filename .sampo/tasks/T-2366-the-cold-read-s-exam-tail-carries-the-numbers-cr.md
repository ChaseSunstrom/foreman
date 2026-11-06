---
id: T-2366
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T14:01:20Z
updated: 2026-10-31T14:03:24Z
base: 9654cb8bb0df07201b2a0b90c72ecfb40389bdb4
base_tree: 2fc9e599b7b212afe62837cc779d345bef0f7635
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-10-31T14:01:22Z
plan0_scope: []
verified: strong
---
# The cold read's exam tail carries the numbers critiques cite: exam defects, ranking, recall by language and kind, and long-tier true done, checks and false done
## Raw request
> The cold read's exam tail carries the numbers critiques cite: exam defects, ranking, recall by language and kind, and long-tier true done, checks and false done
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the exam tail shows exam defects, ranked N/M, recall by language and kind, and long-tier true done/checks/false done — verify with `python3 plugin/tests/run.py test_genesis -k exam_tail_carries`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test with an s1 finders line and an l1 long line, then extend _exam_tail
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 162 tests in 15.5s (17 classes, 16 at a time; slowest: GenesisRead 15s, GenesisCheck 12s, GenesisLive 11s) / OK [ran] [tree bbb28c9a5d1a] (2026-10-31T14:02:24Z)
- `python3 plugin/tests/run.py test_genesis -k exam_tail_carries` → ✗ exit 1 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / FAILED (1 classes: test_genesis.GenesisDraft) (start tree + this task's tests) [ran] [tree bbb28c9a5d1a] (2026-10-31T14:02:28Z)
- `python3 plugin/tests/run.py test_genesis -k exam_tail_carries` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / OK [ran] [tree bbb28c9a5d1a] (2026-10-31T14:02:28Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis -k exam_tail_carries` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: GenesisDraft 0s) / OK [ran] [tree afd942523155] (2026-10-31T14:02:41Z)
- (audit edge) `self-review: _exam_tail gains exam defects, ranking, recall by language and kind, and a long line's true done/checks/false done; red→green; real tail previewed (4.6 KB, 20 lines); changing the tail changes the read key, so tower files re-read once` → lines without recall, rank or checks_passed print as before (older lines tested via the long test's checks guard) [tree afd942523155] (2026-10-31T14:02:41Z)
- (audit self) `self-review: _exam_tail gains exam defects, ranking, recall by language and kind, and a long line's true done/checks/false done; red→green; real tail previewed (4.6 KB, 20 lines); changing the tail changes the read key, so tower files re-read once` → no findings [tree afd942523155] (2026-10-31T14:02:41Z)
## Log
- 2026-10-31T14:01:20Z created
- 2026-10-31T14:01:21Z focused
- 2026-10-31T14:01:22Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-10-31T14:02:38Z scope: plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md
- 2026-10-31T14:03:21Z done
- 2026-10-31T14:03:24Z committed db1c051d (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- T-2177 [FEATURE M, done, 3 steps] G-sweep exam kind grades only that each brief names a tier (a format check): grade… — lesson: A 'super improve' exam with one planted g…
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fourth): standing rule for #1 detection] [check: pending T-2185] Standing rule: exam recall for #1 is reported …
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Lessons
- A reader can only verify what it's shown: give the cold read the fields a tower file cites
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
