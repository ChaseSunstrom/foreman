---
id: T-2218
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T21:25:01Z
updated: 2026-10-31T08:17:20Z
group: exam grading robustness
builder_model: sonnet
base: 57d32d93a7b7862bc051a2ffd4a43da8ab9f3a80
base_tree: d46d0c6532ccf122f432413cd8f796e561984e83
plan0_at: 2026-10-31T07:49:13Z
plan0_scope: []
verified: strong
---
# _static` matches any file whose name holds "test" (broad); fm exam check never runs a…
## Raw request
> _static` matches any file whose name holds "test" (broad); fm exam check never runs a flaky repo test repeatedly (the planted side is exempt by design)
> (noticed by an agent; research T-2211-review)
## Interpretation
Two exam-quality gaps from T-2211's review: fmexam._static reads any file whose name contains 'test' (latest.py, contest.js, attestation.rb) as a test file for test-kind grading, and fm exam check runs each scenario's repo tests once, so a clean side that is itself flaky passes the check and later reads as a finding or a fix.
## Assumptions (confidence)
## Acceptance criteria
- [x] _static treats only TESTISH paths as tests (latest.py, contest.js not read; test_x.py, x.test.js read); fm exam check runs a scenario's clean tests 3 times and drops one whose clean side fails any run, naming it; the planted flaky kind is exempt — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
1) _static uses c.TESTISH (the one test-file pattern, T-0295) on the relative path; fm exam check reruns the scenario's clean-side test command 3 times and drops a scenario whose clean side doesn't pass all 3 (named in the check output), the planted flaky kind exempt as now. 2) a hand list of test dirs — rejected: TESTISH already exists. 3) rerun 10 times — rejected: check time triples for little gain; 3 catches the common flake. Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: the misnamed files; a stub repo whose clean test fails 1 run in 3 is dropped
2. [x] TESTISH in _static; the 3-run clean check
3. [x] docs lines in the report
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 41 tests in 73.4s (11 classes, 16 at a time; slowest: ExamAuthors 73s, ExamGen 57s, ExamRust 19s) / OK [ran] [tree 6e488ffe8e16] (2026-10-31T07:53:29Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_exam && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.35s] [ran] [tree 6e488ffe8e16] (2026-10-31T07:54:53Z)
- `cd plugin/tests && python3 -m unittest -q test_exam` → ✗ exit 1 · Ran 37 tests in 180.559s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 6cf29ae6eebe] (2026-10-31T08:03:16Z)
- `cd plugin/tests && python3 -m unittest -q test_exam` → exit 0 · Ran 37 tests in 183.860s / OK [ran] [tree 6cf29ae6eebe] (2026-10-31T08:03:16Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_docs` → exit 0 · Ran 124 tests in 72.6s (33 classes, 16 at a time; slowest: ExamAuthors 72s, ExamGen 56s, ExamRust 19s) / OK [ran] [tree 6cf29ae6eebe] (2026-10-31T08:04:39Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_docs` → exit 0 · Ran 124 tests in 72.7s (33 classes, 16 at a time; slowest: ExamAuthors 72s, ExamGen 57s, ExamRust 19s) / OK [ran] [tree 6cf29ae6eebe] (2026-10-31T08:05:52Z)
- (step 3) `python3 plugin/tests/run.py test_exam test_docs` → exit 0 · Ran 124 tests in 72.7s (33 classes, 16 at a time; slowest: ExamAuthors 72s, ExamGen 56s, ExamRust 19s) / OK [ran] [tree 6cf29ae6eebe] (2026-10-31T08:07:05Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 41 tests in 72.2s (11 classes, 16 at a time; slowest: ExamAuthors 72s, ExamGen 56s, ExamRust 18s) / OK [ran] [tree 4c51627d4db6] (2026-10-31T08:08:18Z)
- (audit intent) `self-review of the diff: TESTISH on the relative path; the clean suite runs up to 3 times and breaks on the first failure; the planted flaky kind keeps its exemption` → misnamed files no longer read as tests, and a flaky clean side can't pass the check (test_exam red-to-green) [tree 4c51627d4db6] (2026-10-31T08:08:18Z)
- (audit edge) `self-review of the diff: TESTISH on the relative path; the clean suite runs up to 3 times and breaks on the first failure; the planted flaky kind keeps its exemption` → a test in an unusual path fails its static check, flagged by fm exam check; check time up to 3x on clean suites only [tree 4c51627d4db6] (2026-10-31T08:08:18Z)
## Log
- 2026-10-30T21:25:01Z created
- 2026-10-31T07:49:01Z set tier=M
- 2026-10-31T07:49:01Z planned: it has criteria and steps
- 2026-10-31T07:49:02Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2218.builder.md
- 2026-10-31T07:49:12Z focused
- 2026-10-31T07:57:11Z merged worktree-agent-a27805d00157d4586 (2 file(s))
- 2026-10-31T07:57:11Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a27805d00157d4586
- 2026-10-31T07:57:11Z focused
- 2026-10-31T08:07:05Z scope: plugin/lib/fmexam.py (_static, _check_one), plugin/tests/test_exam.py, MASTER.md, CHANGELOG.md
- 2026-10-31T08:09:45Z done
- 2026-10-31T08:09:47Z committed 40ae9306 (2 files)
- 2026-10-31T08:09:53Z guard authorization added: publish
- 2026-10-31T08:17:20Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2211-review: Verdict: approve with nits (3 MEDIUM, 5 LOW); fixed or accepted with reason. Reviewer: one foreman:fm-reviewer, six lenses, read-only.
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- decision 2026-10-30: T-2112: #13's draft kinds live in fmgenesis (fm genesis exam) reusing fmexam.draw/render and cover; G-tower is a 'genesis' session arm on fmexam's d…
- the similar finished task took 4 steps
## Lessons
- Name matching by substring ('test' in name) is wrong on ordinary words: reuse the one pattern the rest of the code trusts
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
- MASTER.md
