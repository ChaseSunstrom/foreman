---
id: T-0357
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-06T04:57:15Z
updated: 2026-10-06T04:58:35Z
base: 7158e9166d80997057a4fbd8399aa4632da51236
base_tree: cea9473299dbdb5f03bcfc82f775ce7344b3a40e
verified: strong
---
# run.py refuses a -k with spaces; lint_verify flags it at task creation
## Raw request
> run.py -k is a substring: '-k "a or b"' runs 0 tests and only fails at fm task finish; refuse a -k with whitespace up front and have lint_verify flag it at task creation
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] run.py -k 'a or b' exits with a usage error before running anything, and fm task new warns about such a verify — verify with `python3 plugin/tests/run.py -k test_diff_gates`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red) + fix
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_diff_gates` → ✗ exit 1 · Ran 11 tests in 9.0s (1 classes, 16 at a time; slowest: DiffGates 9s) / FAILED (1 classes) [ran] [tree 7317814e6d6b] (2026-10-06T04:57:55Z)
- (step 1) `python3 plugin/tests/run.py -k test_diff_gates` → exit 0 · Ran 11 tests in 9.3s (1 classes, 16 at a time; slowest: DiffGates 9s) / OK [ran] [tree 822250fc36aa] (2026-10-06T04:58:25Z)
- (ac 1) `python3 plugin/tests/run.py -k test_diff_gates` → exit 0 · Ran 11 tests in 9.0s (1 classes, 16 at a time; slowest: DiffGates 9s) / OK [ran] [tree 822250fc36aa] (2026-10-06T04:58:34Z)
- (audit self) `self-review: run.py refuses a whitespace -k with a usage error naming the fix; lint_verify flags only Foreman's own plugin/tests/run.py -k with a quoted spaced pattern (pytest -k 'a or b' is valid pytest and stays unflagged)` → no findings [tree 822250fc36aa] (2026-10-06T04:58:34Z)
## Log
- 2026-10-06T04:57:15Z created
- 2026-10-06T04:57:21Z planned from capture
- 2026-10-06T04:57:21Z focused
- 2026-10-06T04:57:30Z criterion 1 verify: `python3 plugin/tests/run.py -k test_cli.Lint` → `python3 plugin/tests/run.py -k test_diff_gates`
- 2026-10-06T04:58:34Z done
- 2026-10-06T04:58:35Z committed 4bb88bd (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261006b: 1. **Answer.** I found three grounded findings, one for each of your frictions. For friction (1) I traced the code path but did not run a reprodu…
- research T-0286-review-1: Changes needed. I found no new hole that the `cd` prefix itself opens. The `cd` chain does make four existing parse mismatches reachable from a…
- research T-0274-review-1: Verdict: approve with nits.** `note_flakes` can't change the exit code or hide a failure. The findings are a regex false-name problem, one miss…
- decision 2026-09-26: User approved (AskUserQuestion, 2026-09-26): once everything is finished and all gates pass, fast-forward main to foreman/build and push both branch…
## Files touched
- plugin/tests/test_diff_gates.py
- plugin/lib/fmcore.py
- plugin/tests/run.py
