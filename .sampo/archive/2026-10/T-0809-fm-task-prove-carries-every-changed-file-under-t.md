---
id: T-0809
type: FIX
tier: S
status: dropped
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_verifying.py]
depends_on: []
source: discovered
created: 2026-10-14T17:10:03Z
updated: 2026-10-14T17:21:42Z
---
# fm task prove treats only test files as tests, not every file in a tests folder
## Raw request
> fm task prove carries every changed file under the tests folder into the start tree, so a fix to a test harness file (bench_hooks.py T-0805, run.py T-0808) can never prove red→green: treat only files the test runner collects (test_*.py) as tests
## Interpretation
fm task prove runs the check on the start tree plus the task's changed test files (fmcli.py, fmmap._TEST = c.TESTISH). TESTISH matches any file under a tests/ folder, so a fix to a harness file there (plugin/tests/bench_hooks.py in T-0805, plugin/tests/run.py in T-0808) was carried into the start tree with the tests and prove reported 'passes without the change too'. Prove carries only files that look like tests by name (test_*.py, *_test.*, *.test.*, *.spec.*, conftest.py, fixtures/); other files in a tests folder stay as they were at the start.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a task that changes plugin/tests/helper.py and adds a test using it proves red→green; a changed test file is still carried — verify with `python3 plugin/tests/run.py -k test_prove_keeps_harness_files_at_the_start`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing test  <- CURRENT
2. [ ] Name-based test selection in prove
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-14T17:10:03Z created
- 2026-10-14T17:21:34Z planned from capture
- 2026-10-14T17:21:42Z dropped: by design: carrying only test_*.py would let a test that needs a helper changed in the same task fail on the start tree for the wrong reason and count as proved; a false proof is worse than 'not proved', and a harness fix under tests/ records its red run and uses the Regression test section (T-0805, T-0808 did)
## Follow-ups captured
