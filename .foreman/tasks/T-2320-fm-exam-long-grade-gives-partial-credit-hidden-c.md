---
id: T-2320
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T11:19:37Z
updated: 2026-10-31T11:27:57Z
base: 3339f087d82cac3767a8ffa5e474b79239338685
base_tree: 2c2c9cff101a39a9d33851b70187a47c9adae37a
plan0_at: 2026-10-31T11:19:39Z
plan0_scope: []
verified: strong
---
# fm exam long grade gives partial credit: hidden checks passed per goal and in total
## Raw request
> fm exam long grade gives partial credit: hidden checks passed per goal and in total
## Interpretation
l001 and l002 read 0/6 true done for the foreman arm, yet on l002 it passed 4 of 20 hidden checks; all-or-nothing hides near misses and leaves two arms that both read 0/6 indistinguishable.
## Assumptions (confidence)
## Acceptance criteria
- [x] A long grade carries checks_passed per goal and checks_passed/checks in total, and the summary line (fm exam long grade, fm exam status, fm genesis) shows 'N/M checks' beside true done — verify with `python3 plugin/tests/run.py test_long`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test: an answer passing one of two checks grades true_done False with checks_passed 1 and the line says 1/2 checks; then count it in grade and print it in both summary lines
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_long -k half_done` → ✗ exit 1 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: Long 2s) / FAILED (1 classes: test_long.Long) [ran] [tree e27ac2c553cc] (2026-10-31T11:19:54Z)
- `python3 plugin/tests/run.py test_long -k half_done` → ✗ exit 1 · Ran 1 tests in 3.0s (1 classes, 16 at a time; slowest: Long 1s) / FAILED (1 classes: test_long.Long) (start tree + this task's tests) [ran] [tree 1ec343169bdf] (2026-10-31T11:20:31Z)
- `python3 plugin/tests/run.py test_long -k half_done` → exit 0 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: Long 1s) / OK [ran] [tree 1ec343169bdf] (2026-10-31T11:20:31Z)
- (step 1) `python3 plugin/tests/run.py test_long test_exam` → exit 0 · Ran 78 tests in 95.6s (18 classes, 16 at a time; slowest: ExamAuthors 95s, ExamGen 66s, Long 58s) / OK [ran] [tree 1ec343169bdf] (2026-10-31T11:22:07Z)
- (ac 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 36 tests in 76.6s (7 classes, 16 at a time; slowest: Long 75s, Approvals 6s, Stop 5s) / OK [ran] [tree f134bbf4009e] (2026-10-31T11:24:56Z)
- (audit intent) `self-review: checks_passed counts the goal's hidden checks in the runner's ok set (0 when unanswered or the runner failed); totals sum over every goal like true_done; both summary lines show N/M checks, and old exam lines without the key still render; l002 re-graded: foreman 4/20, oracle 20/20` → the deciding tier now shows how close an arm got and separates two arms that both read 0/6 [tree f134bbf4009e] (2026-10-31T11:24:56Z)
- (audit edge) `self-review: checks_passed counts the goal's hidden checks in the runner's ok set (0 when unanswered or the runner failed); totals sum over every goal like true_done; both summary lines show N/M checks, and old exam lines without the key still render; l002 re-graded: foreman 4/20, oracle 20/20` → an unanswered goal adds its checks to the denominator with 0 passed; a runner failure (ok None) leaves checks_passed 0; true_done still needs every check [tree f134bbf4009e] (2026-10-31T11:24:56Z)
- (audit self) `self-review: checks_passed counts the goal's hidden checks in the runner's ok set (0 when unanswered or the runner failed); totals sum over every goal like true_done; both summary lines show N/M checks, and old exam lines without the key still render; l002 re-graded: foreman 4/20, oracle 20/20` → no findings [tree f134bbf4009e] (2026-10-31T11:24:56Z)
## Log
- 2026-10-31T11:19:37Z created
- 2026-10-31T11:19:38Z focused
- 2026-10-31T11:23:29Z scope: plugin/lib/fmlong.py (grade, cmd line), plugin/lib/fmexam.py (summary line), plugin/tests/test_long.py, MASTER.md, CHANGELOG.md
- 2026-10-31T11:27:50Z done
- 2026-10-31T11:27:57Z committed ca9a7811 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-31: Long tier l001's foreman 0/6 is an exam defect, not a score: hidden checks need private names the goal never states (fmwatch._shown, fmlong.KILL_T) …
- T-2304 [FIX M, done, 2 steps] Long-tier goals are passable from their text: checks only from the task's own commits, the goal names the new names and flags the checks re…
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- T-2263 [FEATURE M, done, 3 steps] Long-horizon exam (3/3): per-goal metrics and the deciding scorecard row — lesson: A deciding metric must not merge different events: '…
## Lessons
- An all-or-nothing score on a hard tier reads the same for nothing and almost: keep the strict rate, add the partial one beside it
## Plan gaps
- failed first: step 1 Red test: an answer passing one of two checks grades true_done False with checks_passed 1 and the l…
## Files touched
- plugin/tests/test_long.py
- plugin/lib/fmexam.py
- plugin/lib/fmlong.py
- MASTER.md
- CHANGELOG.md
