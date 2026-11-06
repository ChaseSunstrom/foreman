---
id: T-2421
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T15:15:04Z
updated: 2026-10-31T15:21:27Z
base: 1f2bb1dc4777fbaf28e364073abead7369dfc312
base_tree: 83f956bf8a2bfe99a0f64373a86a9ab994527a36
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-10-31T15:15:05Z
plan0_scope: []
verified: strong
---
# test_recall FailureMemory: resolve the capability miss T-2369 now records before fm task done (a later passing run of the same command)
## Raw request
> test_recall FailureMemory: resolve the capability miss T-2369 now records before fm task done (a later passing run of the same command)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the failure-memory test closes its task after a passing rerun resolves the miss — verify with `python3 plugin/tests/run.py test_recall`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Add a passing PostToolUse run of the same command after the failure, then run test_recall and the full suite
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_recall` → exit 0 · Ran 33 tests in 14.6s (10 classes, 16 at a time; slowest: Recall 14s, OtherProjects 5s, Consolidate 3s) / OK [ran] [tree b415a68886d1] (2026-10-31T15:19:59Z)
- `python3 plugin/tests/run.py test_recall -k failure_fixed_in_an_earlier` → exit 0 · Ran 1 tests in 4.7s (1 classes, 16 at a time; slowest: FailureMemory 3s) / OK (start tree + this task's tests) [ran] [tree b415a68886d1] (2026-10-31T15:20:08Z)
- `python3 plugin/tests/run.py test_recall -k failure_fixed_in_an_earlier` → exit 0 · Ran 1 tests in 3.0s (1 classes, 16 at a time; slowest: FailureMemory 3s) / OK [ran] [tree b415a68886d1] (2026-10-31T15:20:08Z)
- (ac 1) `python3 plugin/tests/run.py test_recall` → exit 0 · Ran 33 tests in 26.1s (10 classes, 16 at a time; slowest: Recall 26s, OtherProjects 11s, Consolidate 8s) / OK [ran] [tree b415a68886d1] (2026-10-31T15:20:57Z)
- (audit intent) `self-review: the failure-memory test now resolves the module miss T-2369 records with a later passing run of the same command (after a 1.05 s wait, as fmmiss compares whole seconds), so fm task done closes; full suite 4956 OK` → the test still checks failure memory; T-2369's gate behaves as designed [tree b415a68886d1] (2026-10-31T15:20:57Z)
- (audit self) `self-review: the failure-memory test now resolves the module miss T-2369 records with a later passing run of the same command (after a 1.05 s wait, as fmmiss compares whole seconds), so fm task done closes; full suite 4956 OK` → no findings [tree b415a68886d1] (2026-10-31T15:20:57Z)
## Log
- 2026-10-31T15:15:04Z created
- 2026-10-31T15:15:05Z focused
- 2026-10-31T15:15:05Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-10-31T15:20:08Z scope: plugin/tests/test_recall.py
- 2026-10-31T15:21:26Z done
- 2026-10-31T15:21:27Z committed 7dc0a3c3 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2369-review: Verdict: changes needed.** The core loop works: log the miss, lead in `fm next`, refuse finish and done, resolve by run evidence. But the module-…
- T-2369 [FEATURE M, done, 4 steps] Miss joins the task (Mission 6, #5): a capability miss during an active task becomes its find-build-test-use step, and fm task finish r…
- T-2370 [FEATURE S, active, 3 steps] Wider miss detection (Mission 6, #5): a non-Bash tool failure on an unsupported file type or an unknown tool, and a guard refusal of …
- decision 2026-10-30: [revisited: coverage by grid] [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] [check: python3 plugin/tests/run.py test_genesis.Genesis…
## Regression test
none: the change is to the test itself (the code under test, T-2369's miss gate, is correct); the red was the test failing on the tree before this edit (ship81's scratch tree and a main-tree run: test_recall.FailureMemory, fm task done exited 2), and it passes after
## Lessons
- A new close gate breaks old tests that close tasks after a failure: run the full suite, not only the affected set, before merging a gate
## Files touched
- plugin/tests/test_recall.py
