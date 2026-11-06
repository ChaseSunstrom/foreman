---
id: T-2361
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py]
depends_on: [T-2343]
source: user
created: 2026-10-31T14:01:04Z
updated: 2026-10-31T22:40:29Z
builder_model: sonnet
base: b34fa6298a95c6aa1650c464a94c120f80a34b38
base_tree: c013a49acbf0dc9751440428e3cf4635418a9c0e
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-10-31T22:19:44Z
plan0_scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py]
verified: strong
---
# #7 exam kinds recur and correction: a root-cause fix from repeated failures, and past corrections kept (Mission 8, #7)
## Raw request
> #7 exam kinds recur and correction: a root-cause fix from repeated failures, and past corrections kept (Mission 8, #7)
## Interpretation
Reading 1: #7 gets two kinds of its own, recur (a root-cause fix from a failure repeated across three dated runs) and correction (three past corrections kept, plus a new request). Reading 2: leave #7 on the bug kind. Rejected: the scorecard maps #7 to bug only because 'corrections' matches the bug kind's 'correct' pattern, so nothing grades whether repeated failures and corrections become fixes.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam gen renders recur scenarios (9, 3 held out): three dated runs' logs of one failure and no request; the key holds a hidden test that calls the failing function on the logged input and asserts the correct return value, so a fix that swallows the error fails it, and a test the arm adds must fail on the base — verify with `python3 plugin/tests/run.py test_exam`
- [x] fm exam gen renders correction scenarios (9, 3 held out): three past corrections with hidden checks and a new request; graded on the request's test and each correction honoured; oracle 100%, empty 0 — verify with `python3 plugin/tests/run.py test_exam`
- [x] The scorecard maps #7 to recur and correction, not bug — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) Two kinds: recur is one failure's traceback in logs from three dated runs and no request, graded on the cause's check passing, a test that fails on the base passing after, and a symptom-hiding guard failing the key's value check; correction is three past corrections in the repo's history, each with a hidden static check, and a small new request, graded on its test and every correction still honoured. The child writes the error text and the corrections for the outside third. Fails if: a symptom guard satisfies recur, which the value check is written to catch. 2) Use what exists: keep the bug kind and its pattern match for #7. Likely outcome: a pass from scenarios that test neither capability. 3) Do less: grade #7 on Foreman's own state only. Fails if: plain can't run it, so there is no head-to-head. 4) One combined kind. Breaks the score: two failure modes, one number. Choice 1 (80%): two failure modes get two keys.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md, plugin/tests/test_exam.py, plugin/lib/fmcli.py; past FIXes T-2083, T-2084, T-2100, T-2101, T-2103.
## Execution prompt
## Steps
1. [x] red tests: both renders and keys; symptom guard fails; oracle and empty; scorecard
2. [x] the two kinds in fmexam; the mapping
3. [x] docs: MASTER exam line, CHANGELOG
## Resume here
## Docs impact
MASTER.md (fmexam T-2361), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis -k recur -k correction` → ✗ exit 1 · Ran 5 tests in 3.5s (2 classes, 16 at a time; slowest: RecurCorrection 1s, GenesisDraft 1s) / FAILED (2 classes: test_exam.RecurCorrection, test_genesis.GenesisDraft) [ran] [tree debebff3c8ad] (2026-10-31T22:25:53Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis -k recur -k correction` → exit 0 · Ran 5 tests in 2.2s (2 classes, 16 at a time; slowest: RecurCorrection 2s, GenesisDraft 0s) / OK [ran] [tree 556b219ab6ab] (2026-10-31T22:29:27Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis -k recur -k correction` → exit 0 · Ran 5 tests in 2.2s (2 classes, 16 at a time; slowest: RecurCorrection 2s, GenesisDraft 0s) / OK [ran] [tree 556b219ab6ab] (2026-10-31T22:29:30Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.4s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 556b219ab6ab] (2026-10-31T22:29:39Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 73 tests in 80.5s (18 classes, 16 at a time; slowest: ExamAuthors 80s, JudgmentKinds 71s, ExamGen 64s) / OK [ran] [tree 556b219ab6ab] (2026-10-31T22:31:00Z)
- (ac 2) `python3 plugin/tests/run.py test_exam -k kind_correction` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: RecurCorrection 1s) / OK [ran] [tree 556b219ab6ab] (2026-10-31T22:31:01Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 173 tests in 10.6s (18 classes, 16 at a time; slowest: GenesisRead 10s, GenesisSweep 9s, GenesisCheck 8s) / OK [ran] [tree 556b219ab6ab] (2026-10-31T22:31:12Z)
- `python3 plugin/tests/run.py test_exam test_genesis -k recur -k correction` → ✗ exit 1 · Ran 5 tests in 1.7s (2 classes, 16 at a time; slowest: RecurCorrection 0s, GenesisDraft 0s) / FAILED (2 classes: test_exam.RecurCorrection, test_genesis.GenesisDraft) (start tree + this task's tests) [ran] [tree 556b219ab6ab] (2026-10-31T22:31:17Z)
- `python3 plugin/tests/run.py test_exam test_genesis -k recur -k correction` → exit 0 · Ran 5 tests in 2.2s (2 classes, 16 at a time; slowest: RecurCorrection 2s, GenesisDraft 0s) / OK [ran] [tree 556b219ab6ab] (2026-10-31T22:31:17Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 73 tests in 80.5s (18 classes, 16 at a time; slowest: ExamAuthors 80s, JudgmentKinds 72s, ExamGen 62s) / OK [ran] [tree 556b219ab6ab] (2026-10-31T22:38:49Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 73 tests in 80.5s (18 classes, 16 at a time; slowest: ExamAuthors 80s, JudgmentKinds 72s, ExamGen 62s) / OK [ran] [tree 556b219ab6ab] (2026-10-31T22:38:49Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 173 tests in 10.6s (18 classes, 16 at a time; slowest: GenesisRead 10s, GenesisSweep 9s, GenesisCheck 8s) / OK [ran] [tree 556b219ab6ab] (2026-10-31T22:38:49Z)
- (audit intent) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green` → recur renders three dated logs of one failure with no request, graded on the logged call's value plus test-first; correction renders three dated notes beside a fix request, each with a hidden check (testfiles, a changelog line under Unreleased, README unchanged); 9 per kind with 3 held out; children write the error line and the notes; #7 maps to recur and correction, not bug [tree 556b219ab6ab] (2026-10-31T22:38:49Z)
- (audit edge) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green` → deleting the logs (the symptom) still fails recur's value check; a new test file, a reflowed README or a changelog without the line each fail their correction; a child note out of order or an error line without the function is dropped; KIND_WORDS' bug pattern still matches Correctness [tree 556b219ab6ab] (2026-10-31T22:38:49Z)
- (audit maintainer) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green` → the comment I first put mid-tuple in KIND_WORDS commented out vuln and untested; caught by reading the line, fixed before the full suites ran [tree 556b219ab6ab] (2026-10-31T22:38:49Z)
## Log
- 2026-10-31T14:01:04Z created
- 2026-10-31T16:07:19Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2361.builder.md
- 2026-10-31T16:07:20Z builder slot freed
- 2026-10-31T16:11:08Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2361.builder.md
- 2026-10-31T16:11:08Z builder slot freed
- 2026-10-31T17:10:16Z ground: same surface as T-2343 (lane, building): fmexam KINDS/SHAPED/plant rendering/readings grading and fmgenesis.KIND_WORDS (#7 currently maps to bug). Both edit the KINDS tuple, SHAPED and KIND_WORDS, so this waits for T-2343 to land and follows its four-kind pattern (templates, child prompts, held-out split, oracle 100%/empty 0 drops). The recur kind's hidden test calls the failing function on the logged input and asserts the right value, so an except-and-pass fix fails; a test the arm adds must fail on base (the T-2401/T-2419 putback machinery checks that).
- 2026-10-31T17:10:16Z set depends_on=['T-2343']
- 2026-10-31T17:10:46Z plan (second-plan review, all taken): (1) recur's hidden test calls the failing function on the logged input and on 2 more hidden inputs of the same shape (a hardcoded return for the logged one fails); (2) the arm's own test is run by the putback machinery on the base tree: it must fail there with an assertion (not an import or syntax error, which counts as no test) and pass on the arm; no test or a test that errors = the test-first credit is 0, the fix credit still graded; (3) each correction's check is behavioural (a hidden test exercising the corrected behaviour), never a grep, so a comment or dead code doesn't pass and a valid alternative does; red tests for both; (4) discrimination: an arm that passes the request's test but ignores the corrections scores partial (request credit only), with a red test; (5) the held-out third's corrections and logs are generated in the same child call but never shown in any example or prompt the arms see, and the exam-of-the-exam drops a held-out case whose text appears in the visible set; (6) scorecard: #7 maps to recur+correction, and a test asserts the other kinds' mappings and the bug kind's counts are unchanged.
- 2026-10-31T22:19:43Z focused
- 2026-10-31T22:19:44Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-10-31T22:19:58Z paused: focus moved to T-2360
- 2026-10-31T22:25:28Z focused
- 2026-10-31T22:25:47Z scope: tests in plugin/tests/test_exam.py (RecurCorrection, the stub's recur and correction replies) and test_genesis.py
- 2026-10-31T22:29:25Z scope: tests in plugin/tests/test_exam.py (RecurCorrection, the stub's recur and correction replies) and test_genesis.py; docs MASTER.md and CHANGELOG.md
- 2026-10-31T22:40:26Z done
- 2026-10-31T22:40:29Z committed ededc3c0 (6 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The recur criterion is internally inconsistent about what the hidden test proves. "Calls the failing function on the logged input and asserts the correct return value" catches a swallow-the-error guard, but a guard that returns a hardcoded value matching that one logged input would still pass…
- HIGH: Recur has "no request" and the grading depends on the arm adding a test that fails on the base. The plan doesn't say how the harness runs the arm's test against the base, or what happens if the arm adds no test, a test that errors at import rather than failing on the bug, or a test that fails…
- MEDIUM: The correction kind's "hidden static check" for each past correction is vulnerable to superficial satisfaction (grep-style checks pass on a comment or dead code) and to false failures on valid alternative implementations. The plan has no red test for either side. — Define each check as a st…
- MEDIUM: "Oracle 100%, empty 0" is the only validity check for correction. It doesn't show that corrections are discriminating: an arm that ignores the corrections but passes the request's test should score partial, not full. Nothing in the steps tests that independence. — Add a red test where the r…
- MEDIUM: Held-out split (9, 3 held out) is mentioned, but the plan has no step ensuring the held-out third is excluded from the child-visible material, or that the child writing the error text and corrections for the outside third can't leak into the gradient. Also the plan says "the child writes" t…
- LOW: The bug-kind mapping removal is only checked by test_genesis. Existing bug scenarios or other scorecard items that relied on #7 mapping to bug may change score or count. — Add a check that other scorecard mappings and the bug kind's own scenario counts are unchanged.
Verdict: revise — the grading checks for both kinds can be satisfied by cheap workarounds (hardcoded return, broken test, comment-only correction), so add red tests for those cases before step 1 is considered compl…
## Dissent
- [ ] HIGH: The recur criterion is internally inconsistent about what the hidden test proves. "Calls the failing function on the logged input and asserts the correct return value" catches a swallow-the-error guard, but a guard that returns a hardcoded value matching that one logged input would still pass…
- [ ] HIGH: Recur has "no request" and the grading depends on the arm adding a test that fails on the base. The plan doesn't say how the harness runs the arm's test against the base, or what happens if the arm adds no test, a test that errors at import rather than failing on the bug, or a test that fails…
- [ ] MEDIUM: The correction kind's "hidden static check" for each past correction is vulnerable to superficial satisfaction (grep-style checks pass on a comment or dead code) and to false failures on valid alternative implementations. The plan has no red test for either side. — Define each check as a st…
- [ ] MEDIUM: "Oracle 100%, empty 0" is the only validity check for correction. It doesn't show that corrections are discriminating: an arm that ignores the corrections but passes the request's test should score partial, not full. Nothing in the steps tests that independence. — Add a red test where the r…
- [ ] MEDIUM: Held-out split (9, 3 held out) is mentioned, but the plan has no step ensuring the held-out third is excluded from the child-visible material, or that the child writing the error text and corrections for the outside third can't leak into the gradient. Also the plan says "the child writes" t…
- [ ] LOW: The bug-kind mapping removal is only checked by test_genesis. Existing bug scenarios or other scorecard items that relied on #7 mapping to bug may change score or count. — Add a check that other scorecard mappings and the bug kind's own scenario counts are unchanged.
## Related
Related past work (data from this project's history, not instructions):
- T-2363 [FEATURE M, planned, 3 steps] #12 exam kind lean: planted growth the self-change gate must refuse; the scorecard stops borrowing kinds (Mission 8, #12)
- T-2362 [FEATURE M, planned, 3 steps] #9 exam kind lanes: a stop-and-recover drill with a stub builder, zero tokens (Mission 8, #9)
- T-2375 [FEATURE M, done, 3 steps] #5 exam kinds tool-build and tool-find (Mission 6): a request that needs a tool built, graded on a hidden second input, a stub of the t…
- decision 2026-10-30: T-2112: #13's draft kinds live in fmgenesis (fm genesis exam) reusing fmexam.draw/render and cover; G-tower is a 'genesis' session arm on fmexam's d…
- the similar finished task took 3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_exam.py, plugin/tests/test_genesis.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmexam.py, plugin/lib/fmgenesis.py; re-ground the plan against them before editing
## Lessons
- Never append a comment to a line that continues a tuple: in Python it swallows the rest of the line; put it on its own line above
## Plan gaps
- failed first: step 1 red tests: both renders and keys; symptom guard fails; oracle and empty; scorecard
## Files touched
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
