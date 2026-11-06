---
id: T-2568
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T07:41:56Z
updated: 2026-11-02T08:28:35Z
base: dccffb968e3633b8660867b9ee05e57f83a90cd8
base_tree: 196313a865da25546ded17130561df4ee1bb0d91
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T08:00:19Z
plan0_scope: []
verified: strong
---
# fm tidy --apply prunes graded exam runs' work copies past 14 days, keeping the newest run per tier and agent, answers, grades and keys
## Raw request
> FEATURE: exam run work copies grow without bound (2329 MB of the 2471 MB state; fm doctor says fm tidy doesn't prune them): fm tidy --apply should prune work copies of exam runs no exam line or lineage cites and older than N days, keeping answers and grades
## Interpretation
Reading 1 (chosen): bound the exam store by pruning only the bulky, regenerable part (work copies) of runs nobody will regrade soon; answers, grades and keys stay so scorecards and lineage still read. Reading 2: delete whole old exam runs. Rejected: grades feed the scorecard, lineage and the final report.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm tidy lists exam work copies it would prune with their size; --apply removes only work/ of runs graded 14+ days ago that aren't the newest graded run of their tier for that agent; answers, grades, keys and ungraded runs stay — verify with `python3 plugin/tests/run.py test_tidy`
- [x] fm exam grade on a run whose work copy was pruned refuses with 'work copy pruned: rerun to regrade' instead of grading goal kinds as failed — verify with `python3 plugin/tests/run.py test_exam`
- [x] fm doctor's state-size row names fm tidy --apply for exam work copies instead of saying tidy doesn't prune them — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
1) fmtidy gains an exam work-copy pass: a run's work/ dir is a candidate once every grade line for it is 14+ days old and a newer graded run of the same tier exists for that agent; the dry run lists size, --apply removes; grading a pruned run refuses. Likely outcome: today nothing qualifies (all runs are under 14 days old), and the store stops growing once runs age. Fails if: a regrade of an old run is needed later (the refusal names the rerun). 2) use what exists: fmlong already removes work/AGENT before a rerun (fmlong.py:834); extend that cleanup to after grading, keeping only the newest run. Fails if: a key fix like T-2556's regrade needs yesterday's work copy right after the next run. 3) Hardlink identical files across agents' copies. Fails if: a session edits a file in place and changes every agent's copy, corrupting grades. 4) do less: doctor keeps naming the folder for hand deletion (today's state). Fails if: state keeps growing ~600 MB per long run and nobody deletes it. Choice 1 (80%): age plus newest-run keeps every recent regrade possible and bounds the store.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests in test_tidy, test_exam, test_doctor
2. [x] fmtidy: exam work-copy candidates (dry list + apply)
3. [x] fmexam grade + fmlong grade: refuse a pruned work copy
4. [x] doctor row text; CHANGELOG/MASTER
## Resume here
## Docs impact
CHANGELOG (Unreleased), MASTER.md (fmtidy._prune_exam_work entry); fm doctor's state-size advice now names fm tidy --apply for exam work copies.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tidy.ExamWork test_exam test_doctor` → ✗ exit 1 · Ran 204 tests in 120.7s (61 classes, 16 at a time; slowest: LeanKind 120s, ExamAuthors 91s, JudgmentKinds 85s) / FAILED (3 classes: test_exam.ExamGen, test_doctor.DoctorStateSize, test_tidy.ExamWork) [ran] [tree 9cdafca7048a] [world 2f1906870a] (2026-11-02T08:02:43Z)
- (ac 1) `python3 plugin/tests/run.py test_tidy 2>&1 | grep -E "^(ERROR|FAIL):|^OK|FAILED" | head -4` → exit 0 · OK [ran] [tree ab9b7d2e0d0d] [world 2f1906870a] (2026-11-02T08:06:43Z)
- (step 2) `python3 plugin/tests/run.py test_tidy test_doctor test_long` → exit 0 · Ran 203 tests in 44.5s (60 classes, 16 at a time; slowest: Long 44s, DeferredTriage 17s, StalePlans 17s) / OK [ran] [tree ab9b7d2e0d0d] [world 2f1906870a] (2026-11-02T08:07:40Z)
- (step 3) `python3 plugin/tests/run.py test_tidy test_doctor test_long` → exit 0 · Ran 203 tests in 36.4s (60 classes, 16 at a time; slowest: Long 36s, DeferredTriage 11s, StalePlans 10s) / OK [ran] [tree ab9b7d2e0d0d] [world 2f1906870a] (2026-11-02T08:08:17Z)
- (step 4) `python3 plugin/tests/run.py test_tidy test_doctor test_long` → exit 0 · Ran 203 tests in 68.9s (60 classes, 16 at a time; slowest: Long 69s, DeferredTriage 18s, StalePlans 17s) / OK [ran] [tree ab9b7d2e0d0d] [world 2f1906870a] (2026-11-02T08:09:26Z)
- `python3 plugin/tests/run.py test_tidy.ExamWork test_exam.ExamGen test_doctor.DoctorStateSize` → ✗ exit 1 · Ran 25 tests in 53.0s (3 classes, 16 at a time; slowest: ExamGen 52s, ExamWork 0s, DoctorStateSize 0s) / FAILED (3 classes: test_exam.ExamGen, test_tidy.ExamWork, test_doctor.DoctorStateSize) (start tree + this task's tests) [ran] [tree 71ca7901231a] [world 2f1906870a] (2026-11-02T08:17:34Z)
- `python3 plugin/tests/run.py test_tidy.ExamWork test_exam.ExamGen test_doctor.DoctorStateSize` → exit 0 · Ran 25 tests in 52.0s (3 classes, 16 at a time; slowest: ExamGen 52s, ExamWork 1s, DoctorStateSize 0s) / OK [ran] [tree 71ca7901231a] [world 2f1906870a] (2026-11-02T08:17:34Z)
- (ac 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 41 tests in 9.3s (14 classes, 16 at a time; slowest: DeferredTriage 9s, StalePlans 8s, DecisionSunset 7s) / OK [ran] [tree 71ca7901231a] [world 2f1906870a] (2026-11-02T08:19:55Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 95 tests in 84.0s (23 classes, 16 at a time; slowest: LeanKind 84s, ExamAuthors 76s, JudgmentKinds 71s) / OK [ran] [tree 71ca7901231a] [world 2f1906870a] (2026-11-02T08:19:55Z)
- (ac 3) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 107 tests in 4.1s (37 classes, 16 at a time; slowest: ViewsRepair 3s, LockProbe 3s, Command 2s) / OK [ran] [tree 71ca7901231a] [world 2f1906870a] (2026-11-02T08:19:55Z)
- (step 1) `python3 plugin/tests/run.py test_tidy test_doctor test_long` → exit 0 · Ran 203 tests in 34.8s (60 classes, 16 at a time; slowest: Long 35s, DeferredTriage 10s, StalePlans 9s) / OK [ran] [tree 71ca7901231a] [world 2f1906870a] (2026-11-02T08:19:55Z)
- (audit intent) `self-review of the diff against the 3 ACs: candidates come only from exam.jsonl grade lines; newest run per (tier, agent) and runs under 14 days kept; dry run lists size; apply removes work/AGENT and leaves a PRUNED marker; both grade paths refuse a pruned run with the rerun command; both run paths clear the marker; doctor advice updated; full gate green; real dry run lists nothing today (all runs recent)` → ACs met — dry list with MB, apply removes only old superseded graded runs' work copies, answers/grades/keys/ungraded runs stay (test); grade of a pruned run refuses with 'work copy pruned' and a rerun clears it (test_exam); doctor names fm tidy --apply (test_doctor) [tree 71ca7901231a] (2026-11-02T08:19:55Z)
- (audit adversary) `self-review of the diff against the 3 ACs: candidates come only from exam.jsonl grade lines; newest run per (tier, agent) and runs under 14 days kept; dry run lists size; apply removes work/AGENT and leaves a PRUNED marker; both grade paths refuse a pruned run with the rerun command; both run paths clear the marker; doctor advice updated; full gate green; real dry run lists nothing today (all runs recent)` → rmtree targets are built from exam.jsonl text, so a run or agent containing '/' or starting with '.' is skipped (test with ../../x), and a symlinked work dir is never followed (test: the link target keeps its files and gets no marker) [tree 71ca7901231a] (2026-11-02T08:19:55Z)
- (audit edge) `self-review of the diff against the 3 ACs: candidates come only from exam.jsonl grade lines; newest run per (tier, agent) and runs under 14 days kept; dry run lists size; apply removes work/AGENT and leaves a PRUNED marker; both grade paths refuse a pruned run with the rerun command; both run paths clear the marker; doctor advice updated; full gate green; real dry run lists nothing today (all runs recent)` → an exam line without at, run or agent is ignored; a run with only one graded run per tier is the newest and stays; an already-pruned dir isn't listed again (test); long and short tiers are judged separately [tree 71ca7901231a] (2026-11-02T08:19:55Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 71ca7901231a] [world 2f1906870a] (2026-11-02T08:22:35Z)
## Log
- 2026-11-02T07:41:56Z created
- 2026-11-02T07:44:15Z planned from capture
- 2026-11-02T08:00:18Z set approved=True
- 2026-11-02T08:00:19Z focused
- 2026-11-02T08:00:19Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T08:09:26Z scope: plugin/lib/fmexam.py, plugin/lib/fmlong.py, plugin/lib/fmdoctor.py and their tests — the grade refusal, the rerun clearing the marker, and doctor's advice
- 2026-11-02T08:21:38Z done
- 2026-11-02T08:21:40Z committed c2c0683d (9 files)
- 2026-11-02T08:22:35Z guard authorization added: publish
- 2026-11-02T08:28:35Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2158 [FEATURE M, done, 2 steps] Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done… — lesson: A line that records what produced it …
- T-2097 [FEATURE M, done, 3 steps] fm exam scorecard: per §2 capability, the held-out split's pass rate from graded runs,… — lesson: A gate that reads hand-written fixtur…
- research T-2097-review: Verdict** — approve with nits. The scorecard logic is correct on the cases I traced. The real `fm genesis exam` path that feeds #13 has no test. …
- decision 2026-10-30: [revisited: until the end-of-run exam, selection] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] [check: pytho…
## Lessons
- A cleanup that removes what a later command reads must leave a marker that command checks, so the reader refuses with the way back instead of misgrading on missing files
## Plan gaps
- failed first: step 1 red tests in test_tidy, test_exam, test_doctor
## Files touched
- plugin/tests/test_tidy.py
- plugin/tests/test_exam.py
- plugin/tests/test_doctor.py
- plugin/lib/fmexam.py
- plugin/lib/fmlong.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmtidy.py
- CHANGELOG.md
- MASTER.md
