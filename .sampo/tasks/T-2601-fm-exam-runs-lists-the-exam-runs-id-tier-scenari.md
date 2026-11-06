---
id: T-2601
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-02T10:47:24Z
updated: 2026-11-02T11:59:11Z
base: f19090bea05233451c25312e5fcf26d39db1ebd6
base_tree: e58dae26cebdd9204191b87a21e5fb250b1b3e01
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T11:12:56Z
plan0_scope: []
verified: strong
---
# fm exam runs lists each exam run: id, tier, scenarios and how many held out, and per agent the newest grade's gen, model and date
## Raw request
> FEATURE: fm exam runs lists the exam runs (id, tier, scenarios, held out, which agents answered and graded, gen, date), the verb a session reached for (friction 2026-11-02: unknown 'fm exam runs'); today finding a run with train scenarios took several reads of exam dirs and exam.jsonl
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam runs prints one line per run under exam/ and exam/long/ (run.json present), newest first: id, tier, scenarios (held out N), and each graded agent with gen, model and date from exam.jsonl; --json gives the same rows; an ungraded run says so — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_exam
2. [x] runs action in fmexam (choices in fmcli)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ExamGen` → ✗ exit 1 · Ran 21 tests in 52.2s (1 classes, 16 at a time; slowest: ExamGen 52s) / FAILED (1 classes: test_exam.ExamGen) [ran] [tree 92c3112f231a] [world 2f1906870a] (2026-11-02T11:13:57Z)
- (step 2) `python3 plugin/tests/run.py test_exam.ExamGen test_redefinitions` → exit 0 · Ran 23 tests in 52.4s (2 classes, 16 at a time; slowest: ExamGen 52s, Redefinitions 1s) / OK [ran] [tree f2ec1f9f5d5d] [world 2f1906870a] (2026-11-02T11:18:45Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 96 tests in 90.0s (23 classes, 16 at a time; slowest: LeanKind 90s, ExamAuthors 76s, JudgmentKinds 71s) / OK [ran] [tree 31c4c99ee03c] [world 2f1906870a] (2026-11-02T11:26:48Z)
- (step 1) `python3 plugin/tests/run.py test_exam.ExamGen` → exit 0 · Ran 21 tests in 52.4s (1 classes, 16 at a time; slowest: ExamGen 52s) / OK [ran] [tree 31c4c99ee03c] [world 2f1906870a] (2026-11-02T11:26:48Z)
- (audit intent) `self-review: run_rows reads each run.json under exam/ and exam/long/ and the newest exam.jsonl line per (tier, run, agent); the runs action prints one line a run, --json the rows; the existing runs() (run ids for gen) is untouched after a name collision caught by the suite; load()'s error points at fm exam runs` → a fresh run lists its 3 scenarios, 1 held out and 'not graded'; after a grade its agent shows (test); the real store lists s32-015 with foreman gen 2 haiku [tree 31c4c99ee03c] (2026-11-02T11:26:48Z)
- (audit edge) `self-review: run_rows reads each run.json under exam/ and exam/long/ and the newest exam.jsonl line per (tier, run, agent); the runs action prints one line a run, --json the rows; the existing runs() (run ids for gen) is untouched after a name collision caught by the suite; load()'s error points at fm exam runs` → a run.json that fails to parse is skipped; long runs and short runs with the same id are kept apart by tier [tree 31c4c99ee03c] (2026-11-02T11:26:48Z)
- (audit self) `self-review: run_rows reads each run.json under exam/ and exam/long/ and the newest exam.jsonl line per (tier, run, agent); the runs action prints one line a run, --json the rows; the existing runs() (run ids for gen) is untouched after a name collision caught by the suite; load()'s error points at fm exam runs` → no findings [tree 31c4c99ee03c] (2026-11-02T11:26:48Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 0ec19e39d506] [world 2f1906870a] (2026-11-02T11:59:11Z)
## Log
- 2026-11-02T10:47:24Z created
- 2026-11-02T10:48:35Z planned from capture
- 2026-11-02T11:12:56Z set approved=True
- 2026-11-02T11:12:56Z focused
- 2026-11-02T11:12:56Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T11:18:46Z scope: plugin/lib/fmcli.py — the runs choice
- 2026-11-02T11:28:22Z done
- 2026-11-02T11:28:24Z committed 7c8b7fe3 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2158 [FEATURE M, done, 2 steps] Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done… — lesson: A line that records what produced it …
- T-2097 [FEATURE M, done, 3 steps] fm exam scorecard: per §2 capability, the held-out split's pass rate from graded runs,… — lesson: A gate that reads hand-written fixtur…
- decision 2026-10-30: Genesis selection (fm genesis select) scores the exam's train split, never the held-out third; held-out only grades a capability done
- similar past tasks were M: consider --tier M
## Lessons
- Before adding a module-level name, grep the module for it: the redefinition test catches it late, after the suite has already failed elsewhere
## Plan gaps
- failed first: step 1 red test in test_exam
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmcli.py
- plugin/lib/fmexam.py
- CHANGELOG.md
