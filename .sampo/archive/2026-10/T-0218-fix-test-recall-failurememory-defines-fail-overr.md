---
id: T-0218
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-04T04:48:06Z
updated: 2026-10-04T04:51:55Z
base: 8f06b7ab22b6b50ac771d66c2838e5d747a8d295
base_tree: 85768eb1aaed48ced7f343de95773b60b14e81e6
verified: strong
---
# test_recall.FailureMemory's fail() helper overrode TestCase.fail, so its assertions could never fail
## Raw request
> FIX!: test_recall.FailureMemory defines fail(), overriding unittest.TestCase.fail, so every assertion in that class passes silently — rename the helper and fix whatever the now-live assertions find
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] FailureMemory's helper no longer shadows TestCase.fail, its assertions are live and pass, and a suite check fails on any test class that redefines a TestCase method — verify with `python3 plugin/tests/run.py -k test_recall -k test_suite_hygiene`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Rename the helper, then fix whatever the now-live assertions find
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_recall` → ✗ exit 1 · Ran 11 tests in 6.6s (4 classes, 16 at a time; slowest: Recall 6s, RedGreen 1s, Memory 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree e4a9a93ee4a6] (2026-10-04T04:49:59Z)
- `python3 plugin/tests/run.py -k test_recall` → ✗ exit 1 · Ran 11 tests in 6.5s (4 classes, 16 at a time; slowest: Recall 6s, RedGreen 1s, Memory 1s) / FAILED (1 classes) [ran] [tree e4a9a93ee4a6] (2026-10-04T04:49:59Z)
- `python3 plugin/tests/run.py -k test_recall` → exit 0 · Ran 11 tests in 6.7s (4 classes, 16 at a time; slowest: Recall 7s, RedGreen 1s, Memory 1s) / OK (start tree + this task's tests) [ran] [tree fc0741a130c4] (2026-10-04T04:50:29Z)
- `python3 plugin/tests/run.py -k test_recall` → exit 0 · Ran 11 tests in 6.5s (4 classes, 16 at a time; slowest: Recall 6s, RedGreen 1s, Memory 1s) / OK [ran] [tree fc0741a130c4] (2026-10-04T04:50:29Z)
- `python3 plugin/tests/run.py -k test_recall -k test_suite_hygiene` → exit 0 · Ran 12 tests in 6.7s (5 classes, 16 at a time; slowest: Recall 7s, RedGreen 1s, Memory 1s) / OK (start tree + this task's tests) [ran] [tree 8e86d961dc59] (2026-10-04T04:50:58Z)
- `python3 plugin/tests/run.py -k test_recall -k test_suite_hygiene` → exit 0 · Ran 12 tests in 6.6s (5 classes, 16 at a time; slowest: Recall 7s, RedGreen 1s, Memory 1s) / OK [ran] [tree 8e86d961dc59] (2026-10-04T04:50:58Z)
- (step 1) `python3 plugin/tests/run.py -k test_recall -k test_suite_hygiene` → exit 0 · Ran 12 tests in 6.6s (5 classes, 16 at a time; slowest: Recall 7s, RedGreen 1s, Memory 1s) / OK [ran] [tree 8e86d961dc59] (2026-10-04T04:51:16Z)
- (ac 1) `python3 plugin/tests/run.py -k test_recall -k test_suite_hygiene` → exit 0 · Ran 12 tests in 6.5s (5 classes, 16 at a time; slowest: Recall 6s, RedGreen 1s, Memory 1s) / OK [ran] [tree 8e86d961dc59] (2026-10-04T04:51:55Z)
- (audit self) `self checklist: the renamed helper makes FailureMemory's assertions live; they found one real interaction (T-0211's hint on first sighting) and passed after asserting the test's intent; the hygiene check scans every test file's classes` → pass [tree 8e86d961dc59] (2026-10-04T04:51:55Z)
## Log
- 2026-10-04T04:48:06Z created
- 2026-10-04T04:49:31Z planned from capture
- 2026-10-04T04:49:31Z focused
- 2026-10-04T04:50:44Z steer: criterion widened to a permanent suite check (test_suite_hygiene) instead of a one-off grep
- 2026-10-04T04:51:55Z done
- 2026-10-04T04:51:55Z committed b80023e (2 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0078-review: Verdict: changes needed (one MEDIUM, fail-open, plus a LOW).** `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0078.diff` is …
- playbook Python Testing Patterns (skills/playbooks/references/lang/python-testing.md)
- research T-0212-review: Verdict: changes needed.** There are no CRITICAL or HIGH findings. Two MEDIUM issues are worth fixing before relying on `compare`. I read the cod…
- research t0036-maintainer: MEDIUM** — `~/.claude/foreman/plugin/lib/fmhooks.py:341-364` (`_pin_problem`) and `~/.claude/foreman/plugin/lib/fmguard.py…
## Regression test
test_suite_hygiene: fails on any test class that redefines a TestCase method. Red by hand against HEAD's test_recall.py (['test_recall.py:118 FailureMemory.fail'] != []), green now; fm task prove can't show it because the fix lives in the test files it copies.
## Files touched
- plugin/tests/test_recall.py
- plugin/tests/test_suite_hygiene.py
