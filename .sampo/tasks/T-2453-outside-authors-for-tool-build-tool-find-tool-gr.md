---
id: T-2453
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T06:42:18Z
updated: 2026-11-01T06:57:17Z
base: 2976bb13cf7cb71bc009e523c47b146bddcada8c
base_tree: 9070660e133cc701b1c60707a11bb99925e2e40d
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-01T06:42:25Z
plan0_scope: []
verified: strong
---
# Outside authors for tool-build, tool-find, tool-grant, proof and beyond (no child writes them, so #5, #6 and #10 can never pass the held-out scorecard)
## Raw request
> Outside authors for tool-build, tool-find, tool-grant, proof and beyond (no child writes them, so #5, #6 and #10 can never pass the held-out scorecard)
## Interpretation
Readings: (a) the outside author must write the scenario's words (data or request) while the hidden checks stay Foreman's, as for watch and recur; (b) the child writes whole scenarios. (a) is the existing rule (CHILD_KINDS: the stream, the log line, the issue texts; the checks are ours), so (a). Outcome: #5, #6 and #10 become passable on the scorecard once held-out child scenarios are graded.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam gen --author child renders tool-build and tool-find from a child's record dialect (fields, separator, rows), and tool-grant, proof and beyond from a child's rewording of the request that keeps every requirement; each passes fm exam check and the oracle closes it; a reply that drops a requirement or breaks the dialect is dropped with its reason — verify with `python3 plugin/tests/run.py test_exam`
- [x] fm exam scorecard no longer says no outside author for #5, #6 or #10 — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) The child writes only the words, our checks stay: the record dialect for the tool kinds, a rewording of our request (validated term by term) for tool-grant, proof and beyond; fails if: a rewording drifts past the regex checks, which fm exam check catches 2) use what exists: the ASKS path (child writes the request) as is; fails if: tool-grant's package names and proof's protocol line must survive, which ASKS can't guarantee 3) do less: mark these kinds template-only and exempt them from the outside-author rule; fails if: the scorecard rule exists so Foreman can't grade its own homework 4) a child that writes whole scenarios (repo and checks); fails if: hidden checks written by the author leak into what it knows Choice 1 (80%): the cheapest outside author that keeps the checks ours
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: child renders per kind, oracle closes, a bad reply dropped
2. [x] CHILD_KINDS, SHAPED prompts, _author_shaped validation, _template/render use the child's words
3. [x] docs: MASTER, CHANGELOG
## Resume here
## Docs impact
MASTER.md (fmexam T-2453), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam -k OutsideAuthorsForToolsProofBeyond` → ✗ exit 1 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: OutsideAuthorsForToolsProofBeyond 0s) / FAILED (1 classes: test_exam.OutsideAuthorsForToolsProofBeyond) [ran] [tree 53f5949a4d2c] (2026-11-01T06:43:07Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis test_find` → exit 0 · Ran 388 tests in 110.5s (61 classes, 16 at a time; slowest: LeanKind 96s, ExamAuthors 82s, JudgmentKinds 77s) / OK [ran] [tree 76ac93f4d1a3] (2026-11-01T06:46:07Z)
- (ac 1) `python3 plugin/tests/run.py test_exam -k OutsideAuthorsForToolsProofBeyond` → exit 0 · Ran 2 tests in 5.9s (1 classes, 16 at a time; slowest: OutsideAuthorsForToolsProofBeyond 5s) / OK [ran] [tree 76ac93f4d1a3] (2026-11-01T06:46:21Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis && ! fm exam scorecard | grep -E '^ +(5|6|10)\.' | grep -q 'no outside author'` → exit 0 · Ran 177 tests in 16.3s (18 classes, 16 at a time; slowest: GenesisRead 16s, GenesisCheck 13s, GenesisSweep 12s) / OK [ran] [tree 76ac93f4d1a3] (2026-11-01T06:46:38Z)
- (step 3) `python3 plugin/tests/run.py test_docs; grep -c 'T-2453' MASTER.md` → exit 0 · OK / 1 [ran] [tree e404109831e7] (2026-11-01T06:46:53Z)
- `python3 plugin/tests/run.py test_exam -k OutsideAuthorsForToolsProofBeyond` → ✗ exit 1 · Ran 2 tests in 1.6s (1 classes, 16 at a time; slowest: OutsideAuthorsForToolsProofBeyond 0s) / FAILED (1 classes: test_exam.OutsideAuthorsForToolsProofBeyond) (start tree + this task's tests) [ran] [tree e404109831e7] (2026-11-01T06:46:58Z)
- `python3 plugin/tests/run.py test_exam -k OutsideAuthorsForToolsProofBeyond` → exit 0 · Ran 2 tests in 3.1s (1 classes, 16 at a time; slowest: OutsideAuthorsForToolsProofBeyond 3s) / OK [ran] [tree e404109831e7] (2026-11-01T06:46:58Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 90 tests in 86.2s (23 classes, 16 at a time; slowest: LeanKind 86s, ExamAuthors 77s, JudgmentKinds 72s) / OK [ran] [tree e404109831e7] (2026-11-01T06:55:24Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 177 tests in 9.4s (18 classes, 16 at a time; slowest: GenesisRead 9s, GenesisSweep 8s, GenesisCheck 7s) / OK [ran] [tree e404109831e7] (2026-11-01T06:55:24Z)
- (audit intent) `fm check exit 0 (5523 tests); red→green tests for each of the five kinds (child renders, fm exam check, the oracle closes, a broken dialect or a dropped requirement is dropped with its reason); fm task prove proved; fm exam scorecard no longer says no outside author for #5, #6 or #10` → #5, #6 and #10 can now pass the held-out scorecard, whose rule counts only outside-authored scenarios; the hidden checks stay Foreman's [tree e404109831e7] (2026-11-01T06:55:24Z)
- (audit adversary) `fm check exit 0 (5523 tests); red→green tests for each of the five kinds (child renders, fm exam check, the oracle closes, a broken dialect or a dropped requirement is dropped with its reason); fm task prove proved; fm exam scorecard no longer says no outside author for #5, #6 or #10` → child text is c.plain'd with @ stripped before PACKAGE and MANAGER become placeholders, so a child can't inject other @name@ fills; record values are a strict pattern (no colons, commas or newlines) so the .rec parser and CSV can't be broken; the proof protocol line is ours, appended [tree e404109831e7] (2026-11-01T06:55:24Z)
- (audit edge) `fm check exit 0 (5523 tests); red→green tests for each of the five kinds (child renders, fm exam check, the oracle closes, a broken dialect or a dropped requirement is dropped with its reason); fm task prove proved; fm exam scorecard no longer says no outside author for #5, #6 or #10` → a rewording that drops a requirement (the package, the production check, the migration, check_health.sh, the workflow, the examples) is dropped; beyond's required terms follow the scenario's deliverable; the hidden second input for tool-build stays template-drawn [tree e404109831e7] (2026-11-01T06:55:24Z)
## Log
- 2026-11-01T06:42:18Z created
- 2026-11-01T06:42:24Z focused
- 2026-11-01T06:42:25Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-01T06:46:58Z scope: plugin/tests/test_exam.py (tests and stub replies), MASTER.md and CHANGELOG.md (docs)
- 2026-11-01T06:57:15Z done
- 2026-11-01T06:57:17Z committed 4e0a1989 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- T-2216 [FEATURE L, done, 6 steps] Exam kinds for gen-0 #2 Exhaustive thinking, #9 Orchestration and #11 Self-triggering,… — lesson: An exam kind must test the capability…
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- decision 2026-10-30: [revisited: weakness-finding uses signals] [cites: user steer 2026-10-30] [check: python3 plugin/tests/run.py test_exam.ExamAuthors] Standing rule: …
- similar finished tasks took 4–6 steps
## Lessons
- An exam kind is passable only when it has an outside author and a KIND_WORDS mapping; read fm exam scorecard's why line after adding one
## Plan gaps
- failed first: step 1 red tests: child renders per kind, oracle closes, a bad reply dropped
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
- MASTER.md
