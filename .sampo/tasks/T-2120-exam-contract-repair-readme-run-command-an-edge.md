---
id: T-2120
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T08:06:47Z
updated: 2026-10-30T08:37:45Z
base: 6458fdfc5f181cdb7b42990e6584ee5a1947e40b
base_tree: 403a5734cc904b82a8d2e7c4ba2328af3c566460
plan0_at: 2026-10-30T08:10:53Z
plan0_scope: []
verified: strong
---
# Exam contract repair: README run command, an edge contract every clean app follows, a proven unkeyed finding counts as an exam defect (Mission 3 brief 1)
## Raw request
> Exam contract repair: README run command, an edge contract every clean app follows, a proven unkeyed finding counts as an exam defect (Mission 3 brief 1)
## Interpretation
The exam's clean base app has latent defects the arms rightly flag (page n<1, clamp lo>hi in C, C label sprintf, C dedupe indexed by value) and the C/Rust README run command quotes its &&. Fix the base so a clean render is truly clean, state the edge contract in the README, prove each clause with a visible test in all six languages, and count a proven unkeyed finding as an exam defect.
## Assumptions (confidence)
## Acceptance criteria
- [x] the README run command runs as shown and the clean render passes a hidden edge test per contract clause in all six languages — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
Chosen: fix the base apps to one stated contract and extend the visible base tests (page/clamp/label/dedupe edge asserts) so the clean suite proves it in every language; the planted variants keep the same guards so each differs from clean by one defect only. Rejected: (b) document the latent behaviour as intended (arms would still flag it; C UB can't be documented away); (c) separate hidden edge test files (more machinery than extending the base tests, which already run on clean and planted). Grading: answers may carry a proof command; a finding matching no keyed defect whose proof fails on the clean render counts as exam_defects, not a false alarm.
## Risks and rollback
## Execution prompt
## Steps
1. [x] README run command: the && unquoted
2. [x] edge contract in the README; clean apps follow it in six languages; hidden edge tests
3. [x] grading: a proven unkeyed finding failing on the clean base is an exam defect
## Resume here
<!-- auto -->
- 2026-10-30T08:32:34Z steps 3/3 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmexam.py, plugin/tests/test_exam.py, site/genesis/genesis.js
- touched since last checkpoint: plugin/tests/test_exam.py, plugin/lib/fmexam.py, site/genesis/genesis.js
- failures met: fm task audit: error: the following arguments are required: result
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_exam` → ✗ exit 1 · Ran 20 tests in 19.7s (9 classes, 16 at a time; slowest: ExamGen 19s, ExamRust 12s, ExamC 11s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree e66e61774a9d] (2026-10-30T08:22:24Z)
- `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 20 tests in 19.3s (9 classes, 16 at a time; slowest: ExamGen 19s, ExamRust 12s, ExamC 11s) / OK [ran] [tree e66e61774a9d] (2026-10-30T08:22:24Z)
- (step 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 20 tests in 19.3s (9 classes, 16 at a time; slowest: ExamGen 19s, ExamRust 12s, ExamTs 11s) / OK [ran] [tree e66e61774a9d] (2026-10-30T08:23:39Z)
- (step 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 20 tests in 19.3s (9 classes, 16 at a time; slowest: ExamGen 19s, ExamRust 12s, ExamC 11s) / OK [ran] [tree e66e61774a9d] (2026-10-30T08:23:59Z)
- (step 3) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 20 tests in 19.3s (9 classes, 16 at a time; slowest: ExamGen 19s, ExamRust 12s, ExamC 11s) / OK [ran] [tree e66e61774a9d] (2026-10-30T08:24:18Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmexam.py — commit it through a task, or git checkout it back / fm doctor: OK (47 pass, 7 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                27.9    29.6     150  [0] / SessionEnd                  24.4    26.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-u [ran] [tree e66e61774a9d] (2026-10-30T08:27:47Z)
- (audit intent) `fm-reviewer pass + fixes, test_exam` → the exam no longer counts a true latent defect of its own base against an arm: an unkeyed finding counts as an exam defect only with a test red on the clean render for an assertion and green on the arm's tree; README run command works in C/Rust; every clean app follows the stated edge contract [tree 37674d932d1b] (2026-10-30T08:30:14Z)
- (audit adversary) `fm-reviewer pass + fixes, test_exam` → reviewer MEDIUM fixed: a test of code the arm added (ImportError/NameError/missing export/build error on clean) is rejected by LOAD; paths outside work, absolute, or with a null byte give no proof; at most 10 proofs a scenario; model code runs with credentials stripped [tree 37674d932d1b] (2026-10-30T08:30:14Z)
- (audit edge) `fm-reviewer pass + fixes, test_exam` → page n<1/size<1, clamp lo>hi, label already wide, dedupe negatives, total of none, usize::MAX in Rust; Python mutants of each clause turn the hidden suite red; a flaky proof can move a finding between counts (accepted: same-run score) [tree 37674d932d1b] (2026-10-30T08:30:14Z)
- (audit operator) `fm-reviewer pass + fixes, test_exam` → fm exam summary says N exam defect(s); grade JSON carries exam_defects and exam_defect_findings; the Genesis site cell shows them; _run's why names the error line instead of node's version line [tree 37674d932d1b] (2026-10-30T08:30:14Z)
- (audit maintainer) `fm-reviewer pass + fixes, test_exam` → one helper (_exam_defect) and two regexes beside _run; mutants Python-only, the other five languages assert the same clauses (LangCheck runs them) [tree 37674d932d1b] (2026-10-30T08:30:14Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmexam.py — commit it through a task, or git checkout it back / fm doctor: OK (47 pass, 7 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                27.5    28.5     150  [0] / SessionEnd                  24.6    26.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-u [ran] [tree 37674d932d1b] (2026-10-30T08:33:19Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 20 tests in 19.3s (9 classes, 16 at a time; slowest: ExamGen 19s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 37674d932d1b] (2026-10-30T08:35:06Z)
## Log
- 2026-10-30T08:06:47Z created
- 2026-10-30T08:10:53Z focused
- 2026-10-30T08:29:45Z steer: reviewer MEDIUM fixed — a clean-side failure from a missing name or a build error is not a proof (LOAD); _run's why now names the error line; null-byte test path guarded; site shows exam defects
- 2026-10-30T08:35:08Z done
- 2026-10-30T08:35:10Z committed b4f9e0e2 (5 files)
- 2026-10-30T08:35:15Z guard authorization added: publish
- 2026-10-30T08:37:45Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2079 [FEATURE L, done, 6 steps] fm exam: generated multi-language exam with hidden keys, holdout third, finders and claude arms, scores to exam.jsonl — lesson: A claud…
- decision 2026-10-30: T-2079 exam design: one app API rendered in six languages with defect variants, keys outside the repo, hash holdout one in three; finders arm free, …
- research T-2052-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict: approve with nits.** I read the brief, the diff and the ful…
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
## Why not caught
the first exam-defect test only covered tests of existing code
## Lessons
- A proof test that fails on the clean side only because the names it imports don't exist there tests the arm's own new code; classify the failure text before counting it as a defect
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
- MASTER.md
- site/genesis/genesis.js
