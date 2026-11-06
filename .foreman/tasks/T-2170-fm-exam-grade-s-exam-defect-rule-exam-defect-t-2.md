---
id: T-2170
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T15:02:34Z
updated: 2026-10-30T18:14:27Z
base: 65aca49e93ec8d39cca93b681101c5065dfb8c2e
base_tree: c09eef84a852257906b4b1623247a1cd25b89093
plan0_at: 2026-10-30T18:01:30Z
plan0_scope: []
verified: strong
---
# fm exam grade's exam-defect rule (_exam_defect, T-2120) takes the arm's own test as…
## Raw request
> FIX: fm exam grade's exam-defect rule (_exam_defect, T-2120) takes the arm's own test as proof: a test that asserts the arm's own change fails on the clean render and passes on its tree, so any unkeyed finding leaves the false-alarm column. Count it as an exam defect only when an outside check agrees (the finding breaks a README edge-contract clause and the hidden edge test for that clause fails on clean), else keep it a false alarm; scorecard shows both columns
## Interpretation
fm exam grade moves an unkeyed finding out of false_alarms into exam_defects when the arm's own test fails on the clean render and passes on its tree (T-2120). The arm wrote both the change and the test, so the proof is the arm grading itself: any finding with a self-written test leaves the false-alarm column. The outside check the request names (a README edge-contract clause with a hidden edge test) doesn't exist in the generator yet, so with no outside agreement a finding stays a false alarm; the self-proved ones are still counted and listed (proved_by_arm, exam_defect_findings) so a real exam defect can be read and fixed in the generator.
## Assumptions (confidence)
## Acceptance criteria
- [x] an unkeyed finding whose only proof is the arm's own test stays a false alarm and is counted as proved_by_arm; the exam line and scorecard show both — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
Options: (a) every unkeyed finding counts as a false alarm; the arm's own proof becomes a separate count shown beside it ('4 false alarms (1 with the arm's own proof)') and its findings stay listed for reading; exam_defects counts only outside agreement, which nothing gives yet (chosen: honest now, no new generator feature); (b) build README edge-contract clauses and hidden edge tests per clause in the generator (rejected for this task: a generator change across every template and language, its own L task, captured); (c) cross-arm agreement (another arm names the same file and symbol) as the outside check (rejected: grading is per agent and order-dependent; a regrade would be needed when a later arm lands). Old exam lines keep their numbers; the scorecard reads proved_by_arm when present.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a self-proved unkeyed finding stays in false_alarms, proved_by_arm counts it, the exam line shows both
2. [x] implement in grade/COUNTS/summary; capture the edge-contract outside check; docs
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md ~/.claude/foreman/site/genesis/genesis.js
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam` → ✗ exit 1 · Ran 27 tests in 24.2s (10 classes, 16 at a time; slowest: ExamGen 24s, ExamAuthors 18s, ExamRust 13s) / FAILED (1 classes) [ran] [tree 840b2d077c6d] (2026-10-30T18:01:56Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 116 tests in 26.0s (23 classes, 16 at a time; slowest: ExamGen 25s, ExamAuthors 23s, GenesisCheck 20s) / OK [ran] [tree 1e560707d406] (2026-10-30T18:02:37Z)
- `python3 plugin/tests/run.py test_exam` → ✗ exit 1 · Ran 27 tests in 25.2s (10 classes, 16 at a time; slowest: ExamGen 24s, ExamAuthors 18s, ExamRust 13s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree d855f408c35c] (2026-10-30T18:03:47Z)
- `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 27 tests in 25.9s (10 classes, 16 at a time; slowest: ExamGen 25s, ExamAuthors 20s, ExamRust 13s) / OK [ran] [tree d855f408c35c] (2026-10-30T18:03:47Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis test_site` → exit 0 · Ran 142 tests in 20.7s (33 classes, 16 at a time; slowest: ExamGen 20s, ExamAuthors 15s, GenesisCheck 14s) / OK [ran] [tree 3f177004d772] (2026-10-30T18:05:59Z)
- `python3 plugin/tests/run.py test_exam` → ✗ exit 1 · Ran 27 tests in 22.2s (10 classes, 16 at a time; slowest: ExamGen 21s, ExamAuthors 13s, ExamRust 12s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 74b5a50a4478] (2026-10-30T18:06:51Z)
- `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 27 tests in 21.6s (10 classes, 16 at a time; slowest: ExamGen 21s, ExamAuthors 13s, ExamRust 12s) / OK [ran] [tree 74b5a50a4478] (2026-10-30T18:06:51Z)
- (audit intent) `foreman:fm-reviewer` → changes needed -> shown on every reader (exam line, genesis tail, site); outside check unbuildable by construction, documented [tree 74b5a50a4478] (2026-10-30T18:06:59Z)
- (audit maintainer) `foreman:fm-reviewer` → new key proved_by_arm_findings, _arm_proof; old lines keep theirs [tree 74b5a50a4478] (2026-10-30T18:07:00Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 27 tests in 21.7s (10 classes, 16 at a time; slowest: ExamGen 21s, ExamAuthors 13s, ExamRust 12s) / OK [ran] [tree 74b5a50a4478] (2026-10-30T18:08:00Z)
- `python3 plugin/tests/run.py test_exam test_genesis test_site` → exit 0 · Ran 142 tests in 20.5s (33 classes, 16 at a time; slowest: ExamGen 20s, ExamAuthors 15s, GenesisCheck 13s) / OK [ran] [tree 74b5a50a4478] (2026-10-30T18:08:00Z)
- (audit intent) `one foreman:fm-reviewer pass (five lenses); 2 MEDIUM + 3 LOW: shown on every reader, keys renamed, the outside check documented as unbuildable by construction` → a finding proved only by the arm's own test stays a false alarm, counted as proved_by_arm on the exam line, genesis tail and site [tree 74b5a50a4478] (2026-10-30T18:08:00Z)
- (audit edge) `one foreman:fm-reviewer pass (five lenses); 2 MEDIUM + 3 LOW: shown on every reader, keys renamed, the outside check documented as unbuildable by construction` → old lines keep exam_defects and exam_defect_findings and still print; holdout counts carry proved_by_arm too [tree 74b5a50a4478] (2026-10-30T18:08:00Z)
- (audit adversary) `one foreman:fm-reviewer pass (five lenses); 2 MEDIUM + 3 LOW: shown on every reader, keys renamed, the outside check documented as unbuildable by construction` → the proof path checks (inside the work tree, no absolute or NUL paths) are unchanged [tree 74b5a50a4478] (2026-10-30T18:08:00Z)
## Log
- 2026-10-30T15:02:34Z created
- 2026-10-30T15:26:10Z also: the tf-first rule counts any failing agent test on the planted file, even one unrelated to the defect (T-2166 cold read of mission-exam.md); the outside check should decide tf-first too
- 2026-10-30T17:59:43Z planned: it has criteria and steps
- 2026-10-30T18:01:29Z focused
- 2026-10-30T18:08:35Z done
- 2026-10-30T18:08:37Z committed 9f7875f3 (6 files)
- 2026-10-30T18:10:01Z guard authorization added: publish
- 2026-10-30T18:14:27Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2120 [FIX M, done, 3 steps] Exam contract repair: README run command, an edge contract every clean app follows, a proven unkeyed finding counts as an exam defect (Miss…
- research T-2120-review: Verdict:** changes needed. One MEDIUM finding: the exam-defect proof can be satisfied without any exam defect. [stale: plugin/lib/fmexam.py, plug…
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- decision 2026-10-30: Recommendation: keep the free finders arm as the zero-token per-generation check for the find capabilities; on s0-001 it found 90/108 (held out 30/3…
- the similar finished task took 3 steps
## Why not caught
T-2120's test asserted the self-proof moved the finding out of false alarms, encoding the bug as the spec
## Lessons
- A score the graded party can move with its own artifact (its test proving its finding) is self-grading; keep the honest column and show the claim beside it
## Plan gaps
- failed first: step 1 red test: a self-proved unkeyed finding stays in false_alarms, proved_by_arm counts it, the exam li…
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmgenesis.py
- site/genesis/genesis.js
