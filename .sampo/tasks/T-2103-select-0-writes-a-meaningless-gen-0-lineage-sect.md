---
id: T-2103
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmexam.py, plugin/tests/test_exam.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-30T05:54:47Z
updated: 2026-10-30T13:14:24Z
base: 9027c9d5bb88e1bdc3f3fcc1bd2d16461882dce3
base_tree: d384cff80e8d60cee54442423b4a634268a20d1a
plan0_at: 2026-10-30T13:05:20Z
plan0_scope: [plugin/lib/fmexam.py, plugin/tests/test_exam.py, CHANGELOG.md]
verified: strong
---
# Select 0` writes a meaningless `## gen-0` lineage section and decision. A vacuously…
## Raw request
> select 0` writes a meaningless `## gen-0` lineage section and decision. A vacuously closed scenario (nothing keyed, no errors) counts toward selection. Either could be its own task
> (noticed by an agent; research T-2102-review)
## Interpretation
select 0 is already refused (T-2102). The live gap: fm exam grade reads a corrupt or non-object answer file as an empty answer, so a restraint scenario (none, clean) closes and nothing counts as an error; a JSON list crashes grade. Such a file grades as an errored session instead.
## Assumptions (confidence)
## Acceptance criteria
- [x] A corrupt or non-object answer file counts as an error and never closes its scenario — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a clean scenario with a corrupt answer is not closed and counts an error
2. [x] grade treats an unreadable or non-dict answer as an error
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_exam.ExamGen.test_an_unreadable_answer_is_an_error_not_a_quiet_close` → ✗ exit 1 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: ExamGen 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 2e8f8bd960c7] (2026-10-30T13:05:41Z)
- `python3 plugin/tests/run.py test_exam.ExamGen.test_an_unreadable_answer_is_an_error_not_a_quiet_close` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: ExamGen 0s) / FAILED (1 classes) [ran] [tree 2e8f8bd960c7] (2026-10-30T13:05:41Z)
- (step 1) `python3 plugin/tests/run.py test_exam.ExamGen.test_an_unreadable_answer_is_an_error_not_a_quiet_close` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: ExamGen 0s) / OK [ran] [tree fda174603e7b] (2026-10-30T13:06:03Z)
- (step 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 25 tests in 21.0s (10 classes, 16 at a time; slowest: ExamGen 21s, ExamAuthors 12s, ExamRust 12s) / OK [ran] [tree fda174603e7b] (2026-10-30T13:06:25Z)
- `python3 plugin/tests/run.py test_exam.ExamGen.test_an_unreadable_answer_is_an_error_not_a_quiet_close` → ✗ exit 1 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: ExamGen 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree fda174603e7b] (2026-10-30T13:06:35Z)
- `python3 plugin/tests/run.py test_exam.ExamGen.test_an_unreadable_answer_is_an_error_not_a_quiet_close` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: ExamGen 0s) / OK [ran] [tree fda174603e7b] (2026-10-30T13:06:35Z)
- (audit adversary) `a hostile answer file: truncated JSON, a list, a string, a number, an object with error set; json.load only, no pickle` → every non-dict and every parse failure becomes error=1 and stays unclosed; dict answers grade as before; the one reader of answer files (grade.one) is the only path [tree fda174603e7b] (2026-10-30T13:06:35Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 25 tests in 20.8s (10 classes, 16 at a time; slowest: ExamGen 21s, ExamAuthors 12s, ExamRust 12s) / OK [ran] [tree fda174603e7b] (2026-10-30T13:07:03Z)
- (audit edge) `read grade.one end to end and grepped every reader of answer files (one); an unreadable or non-dict answer now sets error, which _closed already refuses, so restraint kinds can't close on junk; the test covers truncated JSON and a list` → a valid dict answer with no findings still closes a clean scenario (the empty agent's 3rd case) [tree fda174603e7b] (2026-10-30T13:07:03Z)
- (audit self) `read grade.one end to end and grepped every reader of answer files (one); an unreadable or non-dict answer now sets error, which _closed already refuses, so restraint kinds can't close on junk; the test covers truncated JSON and a list` → no findings [tree fda174603e7b] (2026-10-30T13:07:03Z)
## Log
- 2026-10-30T05:54:47Z created
- 2026-10-30T13:05:18Z set type=FIX, tier=S
- 2026-10-30T13:05:19Z set scope=['plugin/lib/fmexam.py', 'plugin/tests/test_exam.py', 'CHANGELOG.md']
- 2026-10-30T13:05:19Z planned: it has criteria and steps
- 2026-10-30T13:05:19Z focused
- 2026-10-30T13:05:20Z set approved=True
- 2026-10-30T13:06:35Z scope: interpretation narrowed to the grade hole; select 0 was already refused by T-2102 (n < 1 raises)
- 2026-10-30T13:07:06Z done
- 2026-10-30T13:07:07Z committed cfcf35af (3 files)
- 2026-10-30T13:11:51Z guard authorization added: publish
- 2026-10-30T13:14:24Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2102-review: Verdict:** changes needed. Finding 1 is a MEDIUM that breaks the "seed N output passes step's seed-row rules (<= 8 rows)" MUST. I read the code a…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- decision 2026-10-30: T-2112: #13's draft kinds live in fmgenesis (fm genesis exam) reusing fmexam.draw/render and cover; G-tower is a 'genesis' session arm on fmexam's d…
- likely tests for the scope: plugin/tests/test_exam.py
## Preflight
Changed in scope since this was planned (2026-10-30): CHANGELOG.md, plugin/lib/fmexam.py, plugin/tests/test_exam.py; re-ground the plan against them before editing
## Lessons
- An except that substitutes an empty default turns a corrupt input into a confident answer; make the fallback an error the grader already counts
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
