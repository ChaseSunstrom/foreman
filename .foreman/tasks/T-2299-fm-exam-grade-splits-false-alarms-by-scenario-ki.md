---
id: T-2299
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T08:56:51Z
updated: 2026-10-31T09:03:30Z
base: e56bc16c351bcccb4b46860585e81d8660aa89d2
base_tree: ce83c2e2f9410f86fa78c311e8d310823f26630f
plan0_at: 2026-10-31T08:56:54Z
plan0_scope: []
verified: strong
---
# fm exam grade splits false alarms by scenario kind, so I-clean's zero-findings bar reads directly
## Raw request
> fm exam grade splits false alarms by scenario kind, so I-clean's zero-findings bar reads directly
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A graded run carries false_by_kind ({scenario kind: false alarms}) overall and per split, summing to false_alarms, and the summary line prints it when nonzero; an unkeyed finding added to a clean scenario's answer counts under clean — verify with `python3 plugin/tests/run.py test_exam -k false_alarms_are_split`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test: an oracle answer on a clean scenario gains an unkeyed finding; the regrade shows false_by_kind clean 1 and the summary names it; then tally it in grade and print it in the summary
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam -k false_alarms_are_split` → ✗ exit 1 · Ran 1 tests in 3.1s (1 classes, 16 at a time; slowest: ExamGen 2s) / FAILED (1 classes) [ran] [tree 1bf72d30e450] (2026-10-31T08:57:13Z)
- `python3 plugin/tests/run.py test_exam -k false_alarms_are_split` → ✗ exit 1 · Ran 1 tests in 7.5s (1 classes, 16 at a time; slowest: ExamGen 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f5da1d49c4e1] (2026-10-31T08:58:03Z)
- `python3 plugin/tests/run.py test_exam -k false_alarms_are_split` → exit 0 · Ran 1 tests in 2.3s (1 classes, 16 at a time; slowest: ExamGen 1s) / OK [ran] [tree f5da1d49c4e1] (2026-10-31T08:58:03Z)
- (step 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 42 tests in 133.1s (11 classes, 16 at a time; slowest: ExamAuthors 132s, ExamGen 92s, ExamRust 33s) / OK [ran] [tree f5da1d49c4e1] (2026-10-31T09:00:17Z)
- (ac 1) `python3 plugin/tests/run.py test_exam -k false_alarms_are_split` → exit 0 · Ran 1 tests in 1.9s (1 classes, 16 at a time; slowest: ExamGen 1s) / OK [ran] [tree e5f7629888ed] (2026-10-31T09:00:45Z)
- (audit intent) `self-review of the diff: the tally runs only for graded scenarios with false alarms, keyed by the answered scenario's kind, added to the overall and the split dicts like recall; summary prints sorted kinds through c.plain; the test plants an unkeyed finding on a clean scenario's oracle answer and checks overall, split and summary` → the 19 false alarms on s70-010 couldn't be placed; now each run says which scenario kinds they fell in, so I-clean's zero bar is read from the line [tree e5f7629888ed] (2026-10-31T09:00:45Z)
- (audit edge) `self-review of the diff: the tally runs only for graded scenarios with false alarms, keyed by the answered scenario's kind, added to the overall and the split dicts like recall; summary prints sorted kinds through c.plain; the test plants an unkeyed finding on a clean scenario's oracle answer and checks overall, split and summary` → an ungraded scenario adds nothing; no false alarms means no key (old lines and readers unaffected); the per-kind sum equals false_alarms [tree e5f7629888ed] (2026-10-31T09:00:45Z)
- (audit self) `self-review of the diff: the tally runs only for graded scenarios with false alarms, keyed by the answered scenario's kind, added to the overall and the split dicts like recall; summary prints sorted kinds through c.plain; the test plants an unkeyed finding on a clean scenario's oracle answer and checks overall, split and summary` → no findings [tree e5f7629888ed] (2026-10-31T09:00:45Z)
## Log
- 2026-10-31T08:56:51Z created
- 2026-10-31T08:56:53Z focused
- 2026-10-31T09:00:39Z scope: plugin/lib/fmexam.py (grade tally, summary), plugin/tests/test_exam.py, MASTER.md, CHANGELOG.md
- 2026-10-31T09:03:27Z done
- 2026-10-31T09:03:30Z committed 7d3fe368 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- decision 2026-10-30: Recommendation: keep the free finders arm as the zero-token per-generation check for the find capabilities; on s0-001 it found 90/108 (held out 30/3…
- similar past tasks were M: consider --tier M
- the similar finished task took 4 steps
## Lessons
- Every total that decides a bar needs the breakdown that bar reads (here false alarms by scenario kind), or the critique can't tell which bar failed
## Plan gaps
- failed first: step 1 Red test: an oracle answer on a clean scenario gains an unkeyed finding; the regrade shows false_by…
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- MASTER.md
- CHANGELOG.md
