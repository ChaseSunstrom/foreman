---
id: T-0747
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_execution.py]
depends_on: []
source: user
created: 2026-10-09T21:02:27Z
updated: 2026-10-09T21:02:55Z
base: 8106b40f7ff6045ef7a119022a64d72d0f35000e
base_tree: 669f9136eebb03c3a14c15ec0d5a2c8162d4b694
verified: strong
---
# Debug-scaffolding scan flags string literals that name debug calls (test_execution.py:102 at T-0746's close)
## Raw request
> Debug-scaffolding scan flags string literals that name debug calls (test_execution.py:102 at T-0746's close)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a quoted breakpoint() isn't flagged, a bare one is — verify with `python3 plugin/tests/run.py -p test_execution.py -k Scaffold`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: a string literal naming breakpoint() stays quiet; match outside quotes only
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_execution.py -k Scaffold` → ✗ exit 1 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Scaffold 0s) / FAILED (1 classes) [ran] [tree 631c305d6738] (2026-10-09T21:02:33Z)
- (step 1) `python3 plugin/tests/run.py -p test_execution.py -k Scaffold` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Scaffold 0s) / OK [ran] [tree 783168128f95] (2026-10-09T21:02:38Z)
- (step 1) `python3 plugin/tests/run.py -p test_execution.py -k Scaffold` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Scaffold 0s) / OK [ran] [tree 514c817aaa50] (2026-10-09T21:02:49Z)
- (ac 1) `python3 plugin/tests/run.py -p test_execution.py -k Scaffold` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Scaffold 0s) / OK [ran] [tree 514c817aaa50] (2026-10-09T21:02:54Z)
- `python3 plugin/tests/run.py -p test_execution.py` → exit 0 · Ran 7 tests in 0.5s (6 classes, 16 at a time; slowest: Tried 0s, Scaffold 0s, ResumeCheck 0s) / OK [ran] [tree 514c817aaa50] (2026-10-09T21:02:54Z)
- (audit self) `self: calls are matched with string literals blanked; DEBUG prints are matched on the raw line (their marker is in the string); tested bare call, quoted call, plain print and DEBUG print` → no findings [tree 514c817aaa50] (2026-10-09T21:02:54Z)
## Log
- 2026-10-09T21:02:27Z created
- 2026-10-09T21:02:27Z focused
- 2026-10-09T21:02:54Z done
- 2026-10-09T21:02:55Z committed 5a6d477 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0746 [FIX S, done, 1 steps] Debug-scaffolding scan flags docs that mention debug calls (CHANGELOG.md:10 at T-0695's close)
- T-0650 [FEATURE M, done, 0 steps] Keep steps in scope (I047, value 3/5, effort M, risk low)
- T-0174 [FIX M, done, 4 steps] Parallel runs clean up after a failure, re-check main before merging; task commits take paths literally — lesson: A cleanup that covers onl…
- decision 2026-10-04: T-0224 (L) self-approved under full autonomy: tool-less mutation child, candidate on an evolve branch outside the live plugin, merge stays the user'…
- similar finished tasks took 0–4 steps
- start here (files T-0746 touched): plugin/tests/test_execution.py, plugin/lib/fmcli.py
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
none: T-0746's fix covered prose files only; its own close showed string literals in code — the test now has quoted and bare cases side by side
## Plan gaps
- failed first: step 1 test: a string literal naming breakpoint() stays quiet; match outside quotes only
## Files touched
- plugin/tests/test_execution.py
- plugin/lib/fmcli.py
