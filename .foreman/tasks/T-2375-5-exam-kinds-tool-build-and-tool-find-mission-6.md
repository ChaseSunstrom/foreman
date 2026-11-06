---
id: T-2375
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md]
depends_on: [T-2343]
source: self
created: 2026-10-31T14:02:02Z
updated: 2026-10-31T20:01:01Z
builder_model: sonnet
base: 12009229b281223ec47a5e04322ace77f9c58c2c
base_tree: 15d6d7f7402e5a73546227e2aae9ce7455943618
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T19:40:03Z
plan0_scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# #5 exam kinds tool-build and tool-find (Mission 6): a request that needs a tool built, graded on a hidden second input, a stub of the tool and its use; a request a shelf tool already answers, graded on reuse
## Raw request
> #5 exam kinds tool-build and tool-find (Mission 6): a request that needs a tool built, graded on a hidden second input, a stub of the tool and its use; a request a shelf tool already answers, graded on reuse
## Interpretation
Reading 1: two new #5 exam kinds, tool-build (graded on a hidden second input, a stub of the tool and its use) and tool-find (graded on reuse of a shelf tool). Reading 2: grade the final answer's prose on the existing missing-tool kind. Rejected: words aren't proof that a tool exists or ran, and nothing today grades find, build, test or use.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam gen --kind tool-build,tool-find renders 9 per kind (3 held out) in each language; the oracle passes every hidden check and empty passes none; a hand-written output with no tool fails the second-input check; a tool whose test passes on a stub fails the mutation check; an arm that writes its own converter instead of running the shelf tool fails tool-find; fmgenesis's scorecard counts both kinds for #5 — verify with `python3 plugin/tests/run.py test_exam test_genesis`
## Non-goals
## Approach (options → choice → why)
1) Two kinds in fmexam beside missing-tool, child-authored through the SHAPED path (T-2217), 9 per kind with 3 held out, six languages. tool-build: the request needs data in a small invented format turned into an output no installed library makes; the key checks the output on the shown input and a second input the arm never sees, that the arm's test fails when the grader stubs its tool, and that the output came from running the tool. tool-find: the repo already holds a tool the request doesn't mention; the key checks the output, that the shelf tool ran (a run counter outside the tree), and that no new tool duplicates it. Both join #5 in fmgenesis's capability table. Fails if: the invented format leaks into the prompt, which the child author's check drops. 2) Use what exists: the exists kind for find. Likely outcome: it grades reusing a function in the module (#2), not reaching for a tool on the shelf. 3) Do less: keep missing-tool as #5's only kind. Fails if: #5 can't pass a held-out exam that means the capability. Choice 1 (80%): each capability gets a key that can fail it.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/lib/fmcore.py, plugin/tests/test_guard.py; past FIXes T-0980, T-0985, T-0986, T-0987, T-0988.
## Execution prompt
## Steps
1. [x] red tests first in test_exam and test_genesis: renders, oracle and empty, the second-input, mutation and run-counter checks, the capability table
2. [x] fmexam: the two kinds, their templates, child prompts and grading; fmgenesis capability table
3. [x] docs: MASTER.md exam section, CHANGELOG.md
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_exam test_genesis 2>&1 | grep -E "^(FAIL|ERROR):|^Ran .*s\)|^OK|^FAILED|AssertionError" | head -14` → exit 0 · Ran 230 tests in 86.8s (32 classes, 16 at a time; slowest: ExamAuthors 87s, JudgmentKinds 72s, ExamGen 56s) / OK [ran] [tree bda90b962f24] (2026-10-31T19:49:29Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis 2>&1 | grep -E "^(FAIL|ERROR):|^Ran .*s\)|^OK|^FAILED|AssertionError" | head -14` → exit 0 · Ran 230 tests in 86.8s (32 classes, 16 at a time; slowest: ExamAuthors 87s, JudgmentKinds 72s, ExamGen 56s) / OK [ran] [tree bda90b962f24] (2026-10-31T19:49:29Z)
- (step 1) `python3 plugin/tests/run.py test_exam -k ToolKinds` → exit 0 · Ran 4 tests in 1.7s (1 classes, 16 at a time; slowest: ToolKinds 1s) / OK [ran] [tree bda90b962f24] (2026-10-31T19:49:38Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 230 tests in 71.8s (32 classes, 16 at a time; slowest: ExamAuthors 72s, JudgmentKinds 71s, ExamGen 56s) / OK [ran] [tree bda90b962f24] (2026-10-31T19:50:50Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.3s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree d08acebce3e8] (2026-10-31T19:51:10Z)
- (ac 1) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 230 tests in 70.8s (32 classes, 16 at a time; slowest: JudgmentKinds 71s, ExamAuthors 69s, ExamGen 54s) / OK [ran] [tree d08acebce3e8] (2026-10-31T19:52:21Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 231 tests in 70.4s (32 classes, 16 at a time; slowest: JudgmentKinds 70s, ExamAuthors 69s, ExamGen 54s) / OK [ran] [tree e87e16699e7f] (2026-10-31T19:55:38Z)
- (ac 1) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 231 tests in 70.8s (32 classes, 16 at a time; slowest: JudgmentKinds 71s, ExamAuthors 68s, ExamGen 54s) / OK [ran] [tree e87e16699e7f] (2026-10-31T19:56:50Z)
- `python3 plugin/tests/run.py test_exam -k ToolKinds` → ✗ exit 1 · Ran 5 tests in 1.8s (1 classes, 16 at a time; slowest: ToolKinds 1s) / FAILED (1 classes: test_exam.ToolKinds) (start tree + this task's tests) [ran] [tree e87e16699e7f] (2026-10-31T19:56:54Z)
- `python3 plugin/tests/run.py test_exam -k ToolKinds` → exit 0 · Ran 5 tests in 1.8s (1 classes, 16 at a time; slowest: ToolKinds 1s) / OK [ran] [tree e87e16699e7f] (2026-10-31T19:56:54Z)
- (ac 1) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 231 tests in 70.5s (32 classes, 16 at a time; slowest: JudgmentKinds 70s, ExamAuthors 68s, ExamGen 54s) / OK [ran] [tree e87e16699e7f] (2026-10-31T19:59:35Z)
- (audit intent) `main-thread review (pace gate holds): two grading holes found and fixed test-first: a session arm works in a temp copy, so its shelf-tool run named the temp tree (now carried back with the tree), and a rerun could pass on the previous run's counter line (now dropped before each arm's run, under one lock for the parallel session arms); the oracle's copied tree had the same gap (carried)` → tool-build is graded on a hidden second input with other field orders, on the arm's own suite going red with a stub tool, and on the CSV it made; tool-find on the shelf tool's counter outside the tree plus the CSV, and a new app function counts as a duplicate; 9 a kind, 3 held out, all six languages pass fm exam check here; #5's words map to both [tree e87e16699e7f] (2026-10-31T19:59:35Z)
- (audit adversary) `main-thread review (pace gate holds): two grading holes found and fixed test-first: a session arm works in a temp copy, so its shelf-tool run named the temp tree (now carried back with the tree), and a rerun could pass on the previous run's counter line (now dropped before each arm's run, under one lock for the parallel session arms); the oracle's copied tree had the same gap (carried)` → the arm's tool runs only in a throwaway copy, credentials stripped, under the exec timeout; a symlinked tool is refused; the counter is read capped at 1 MB and only an exact realpath line counts; hand-written CSV and a line-order converter both fail (tested) [tree e87e16699e7f] (2026-10-31T19:59:35Z)
- (audit edge) `main-thread review (pace gate holds): two grading holes found and fixed test-first: a session arm works in a temp copy, so its shelf-tool run named the temp tree (now carried back with the tree), and a rerun could pass on the previous run's counter line (now dropped before each arm's run, under one lock for the parallel session arms); the oracle's copied tree had the same gap (carried)` → CRLF output normalised; a tool without the exec bit runs under sh; field order swapped in the shown input too, so the format is fair to read from what the arm sees [tree e87e16699e7f] (2026-10-31T19:59:35Z)
## Log
- 2026-10-31T14:02:02Z created
- 2026-10-31T16:07:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2375.builder.md
- 2026-10-31T16:07:45Z builder slot freed
- 2026-10-31T16:11:17Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2375.builder.md
- 2026-10-31T16:11:17Z builder slot freed
- 2026-10-31T17:13:00Z plan (second-plan review, taken): (1) tool-find grades two signals: the shelf tool's run counter (a grader-held file outside the arm's copy, written by a shim the grader installs, the arm can't see its path) AND the output file matching the shelf tool's output byte for byte; a forged counter without the output fails; (2) mutation: the grader finds the arm's tool and test from the answer JSON's named paths (missing = no credit), copies the tree, replaces the tool body with a stub returning the input unchanged, runs the arm's test there; failing = an assertion failure (not an import error); (3) duplication is behavioural: a new file whose output equals the shelf tool's on the hidden input; (4) one criterion per claim with its own test name, and a per-language oracle/empty check; (5) the hidden second input is drawn from a different generator seed and the exam-of-the-exam drops items where the shown solution passes it without the format logic.
- 2026-10-31T17:41:06Z set depends_on=['T-2343']
- 2026-10-31T19:40:02Z focused
- 2026-10-31T19:40:03Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T19:58:15Z scope: MASTER.md and CHANGELOG.md (step 3's docs); other tasks' commits (T-2344) landed while T-2375 was focused
- 2026-10-31T20:00:59Z done
- 2026-10-31T20:01:01Z committed 9a19656d (5 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The tool-find "shelf tool ran" check relies on a run counter outside the tree, but the plan never says how the counter is injected, protected, or kept from being gamed. An arm can call the tool trivially and still write its own converter, or can touch/forge the counter. Grade on both signals …
- HIGH: The mutation check ("a tool whose test passes on a stub fails") is underspecified. How the grader stubs the tool, how it finds the arm's tool and test across arbitrary child-authored layouts, and what counts as the test "failing" are all unstated. Without this, the check is flaky or trivially…
- MEDIUM: The "no new tool duplicates the shelf tool" check in tool-find is vague. Detecting duplication (a new script that reimplements the converter) by diffing the tree is heuristic and will either false-positive on legitimate helpers or miss renamed copies. — Define it behaviorally (output matche…
- MEDIUM: Acceptance criterion bundles about eight claims into one command, and "9 per kind (3 held out) in each language" × six languages is a big generated surface. A failure won't localise, and oracle/empty passing in all six languages may hide per-language template breakage. — Split into separate…
- MEDIUM: The hidden second input must be genuinely independent from the shown one. Child-authored items could produce a second input the shown solution trivially generalizes to, or the invented format could be guessable from the name. The plan only mentions a leak check on the prompt. — Add a check …
- LOW: There's no stated rollback or compatibility story for adding kinds to fmgenesis's #5 scorecard; existing scorecards/baselines with missing-tool only may shift scores. — State that existing missing-tool results are unchanged and note the scorecard change in CHANGELOG.md.
Verdict: revise — direction is right, but the run-counter and mutation checks, which are the core of what makes these kinds gradable, need concrete mechanisms and adversarial red tests before step 2.
## Dissent
- [ ] HIGH: The tool-find "shelf tool ran" check relies on a run counter outside the tree, but the plan never says how the counter is injected, protected, or kept from being gamed. An arm can call the tool trivially and still write its own converter, or can touch/forge the counter. Grade on both signals …
- [ ] HIGH: The mutation check ("a tool whose test passes on a stub fails") is underspecified. How the grader stubs the tool, how it finds the arm's tool and test across arbitrary child-authored layouts, and what counts as the test "failing" are all unstated. Without this, the check is flaky or trivially…
- [ ] MEDIUM: The "no new tool duplicates the shelf tool" check in tool-find is vague. Detecting duplication (a new script that reimplements the converter) by diffing the tree is heuristic and will either false-positive on legitimate helpers or miss renamed copies. — Define it behaviorally (output matche…
- [ ] MEDIUM: Acceptance criterion bundles about eight claims into one command, and "9 per kind (3 held out) in each language" × six languages is a big generated surface. A failure won't localise, and oracle/empty passing in all six languages may hide per-language template breakage. — Split into separate…
- [ ] MEDIUM: The hidden second input must be genuinely independent from the shown one. Child-authored items could produce a second input the shown solution trivially generalizes to, or the invented format could be guessable from the name. The plan only mentions a leak check on the prompt. — Add a check …
- [ ] LOW: There's no stated rollback or compatibility story for adding kinds to fmgenesis's #5 scorecard; existing scorecards/baselines with missing-tool only may shift scores. — State that existing missing-tool results are unchanged and note the scorecard change in CHANGELOG.md.
## Related
Related past work (data from this project's history, not instructions):
- T-2376 [FEATURE M, planned, 3 steps] #5 exam kind tool-grant (Mission 6): a request whose obvious path is an install, with package managers as logging shims and an injec…
- T-2362 [FEATURE M, planned, 3 steps] #9 exam kind lanes: a stop-and-recover drill with a stub builder, zero tokens (Mission 8, #9)
- research T-2097-review: Verdict** — approve with nits. The scorecard logic is correct on the cases I traced. The real `fm genesis exam` path that feeds #13 has no test. …
- decision 2026-10-31: Mission 6 (tools, #5) approach A: wire the parts Foreman has into one loop on the active task (T-2270's hook notices the miss; fm which, fm lib and …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_exam.py, plugin/tests/test_genesis.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, MASTER.md, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py; re-ground the plan against them before editing
## Lessons
- A counter outside the tree must follow every copy the harness makes of the tree (oracle copy, session temp copy) and start empty on a rerun; test each copy path, not just the arm's own run
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
