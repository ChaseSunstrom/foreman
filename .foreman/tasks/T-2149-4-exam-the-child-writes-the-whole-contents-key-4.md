---
id: T-2149
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T11:02:28Z
updated: 2026-10-30T12:28:35Z
base: 0ebbd4aca9609be677b90920dce2b13f68b21fb2
base_tree: f5e5b72f5e7413614c4205c22e94730a09767248
plan0_at: 2026-10-30T12:15:13Z
plan0_scope: []
verified: strong
---
# #4 exam: the child writes the whole contents key (4-6 items, tests and README patterns),…
## Raw request
> #4 exam: the child writes the whole contents key (4-6 items, tests and README patterns), not one gap beside template items
## Interpretation
For the goal and resume kinds under --author child, the tool-less child writes every item of the key: 4 to 6 items, each a code gap (one function as shipped without the handling, plus the test that catches it: a run check), a missing test (a function the finished suite must call; its visible test is removed: a static check on test files), or a README item (a line the finished README holds plus a regex for it: a static check on README.md). No template item is scored in those keys (gen-1: template scenarios are a free fixture, never the score).
## Assumptions (confidence)
## Acceptance criteria
- [x] child goal and resume keys hold only the child's 4-6 items with at least one code, one test and one README item; fm exam check passes them, the oracle closes all, empty none — verify with `python3 plugin/tests/run.py test_exam.ExamAuthors`
- [x] a reply with under 4 items, two code items on one function, a README regex the planted README already matches, or a bad regex is dropped with its reason — verify with `python3 plugin/tests/run.py test_exam.ExamAuthors`
## Non-goals
Other kinds keep the one-plant author. No change to grading: items reuse the run and static check types.
## Approach (options → choice → why)
A) one child reply with the whole key as {items: [...]} (chosen: one call, covers code, tests and README). B) call the one-plant author N times (N times the cost, still no test or README items). C) keep the template's untested and docs items beside more plants (the template still scores, against gen-1). Rendering: each code item becomes planted entry gapN (distinct functions), its hidden check checks/gapN and its overlay planted/gapN; resume ticks every third item (index 2, 5) done, so 1 to 2 of them are met on disk and in PLAN.md.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test (stub writes a whole key), then AUTHOR_GOAL + _author_key + render items
## Resume here
## Docs impact
MASTER.md exam section and CHANGELOG: the child writes the whole goal/resume key (T-2149)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ExamAuthors` → exit 0 · Ran 8 tests in 5.5s (1 classes, 16 at a time; slowest: ExamAuthors 5s) / OK [ran] [tree 16c4876f2bf6] (2026-10-30T12:17:56Z)
- (step 1) `python3 plugin/tests/run.py test_exam.ExamAuthors` → exit 0 · Ran 8 tests in 5.8s (1 classes, 16 at a time; slowest: ExamAuthors 6s) / OK [ran] [tree 9b1934d8ba3e] (2026-10-30T12:21:08Z)
- (audit intent) `fm-reviewer` → ok; README overlap fixed (cross-match reject + test) [tree 9b1934d8ba3e] (2026-10-30T12:21:21Z)
- (audit adversary) `fm-reviewer` → regex backtracking: quantified-group reject + test [tree 9b1934d8ba3e] (2026-10-30T12:21:21Z)
- (audit edge) `fm-reviewer` → ok: anchored patterns fail closed; bad items drop the scenario [tree 9b1934d8ba3e] (2026-10-30T12:21:21Z)
- (audit operator) `fm-reviewer` → 2-3x builds per child key in check, bounded by the pool; noted [tree 9b1934d8ba3e] (2026-10-30T12:21:21Z)
- (audit maintainer) `fm-reviewer` → dead goal text removed; GOALS clause in render is live (guards plant['request']); reject tests added [tree 9b1934d8ba3e] (2026-10-30T12:21:22Z)
- (ac 1) `python3 plugin/tests/run.py test_exam.ExamAuthors` → exit 0 · Ran 8 tests in 5.8s (1 classes, 16 at a time; slowest: ExamAuthors 6s) / OK [ran] [tree 9b1934d8ba3e] (2026-10-30T12:21:33Z)
- (ac 2) `python3 plugin/tests/run.py test_exam.ExamAuthors` → exit 0 · Ran 8 tests in 5.8s (1 classes, 16 at a time; slowest: ExamAuthors 6s) / OK [ran] [tree 9b1934d8ba3e] (2026-10-30T12:21:39Z)
- (ac 1) `python3 plugin/tests/run.py test_exam.ExamAuthors` → exit 0 · Ran 8 tests in 5.8s (1 classes, 16 at a time; slowest: ExamAuthors 6s) / OK [ran] [tree 9b1934d8ba3e] (2026-10-30T12:21:52Z)
- (ac 2) `python3 plugin/tests/run.py test_exam.ExamAuthors` → exit 0 · Ran 8 tests in 5.8s (1 classes, 16 at a time; slowest: ExamAuthors 6s) / OK [ran] [tree 9b1934d8ba3e] (2026-10-30T12:21:52Z)
## Log
- 2026-10-30T11:02:28Z created
- 2026-10-30T12:03:41Z planned: it has criteria and steps
- 2026-10-30T12:15:13Z focused
- 2026-10-30T12:21:39Z scope: fmexam.py + test_exam.py for the key; MASTER.md and CHANGELOG.md for docs
- 2026-10-30T12:22:14Z done
- 2026-10-30T12:22:16Z committed 4eab1f8f (4 files)
- 2026-10-30T12:25:50Z guard authorization added: publish
- 2026-10-30T12:28:35Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2140 [FEATURE M, done, 3 steps] #4 exam: G-goal and G-resume kinds, child-authored contents keys, foreman vs plain, false done graded (Mission 4 brief 6) — lesson: a r…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- decision 2026-10-30: [cites: T-2149] #4 exam keys reuse the defect machinery: the child writes one key item (its gap), the goal text is the template's, resume's done ite…
## Lessons
- A child-written regex is untrusted code for re: screen quantified groups and cross-matches at authoring, since check only proves each pattern alone
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
- MASTER.md
