---
id: T-1248
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T23:13:35Z
updated: 2026-10-16T23:15:53Z
base: 31d17c55ddb3feee8b70ef33c3de3021755ff2d7
base_tree: 9437afe4652af7bd17d596ffad91909472017e42
plan0_at: 2026-10-16T23:13:38Z
plan0_scope: []
verified: strong
---
# CI: CPU-time bounds that hold on GitHub's runners, and one annotation per failing test
## Raw request
> CI: CPU-time bounds that hold on GitHub's runners, and one annotation per failing test
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the guard scan timing tests allow a slow runner and run.py annotates each failing test — verify with `python3 plugin/tests/run.py test_guard_exec_vectors test_ci_annotations`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Loosen the two process_time bounds; per-failure ::error lines with a test
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_ci_annotations` → ✗ exit 1 · Ran 2 tests in 0.001s / FAILED (errors=2) [ran] [tree b21e7cc085e8] (2026-10-16T23:14:01Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_exec_vectors test_ci_annotations` → exit 0 · Ran 42 tests in 1.4s (7 classes, 16 at a time; slowest: ScriptCache 1s, ScriptHook 1s, Review 0s) / OK [ran] [tree 4297f9cb7c7d] (2026-10-16T23:14:16Z)
- (step 1) `python3 plugin/tests/run.py test_ci_annotations test_guard_exec_vectors` → exit 0 · Ran 42 tests in 1.4s (7 classes, 16 at a time; slowest: ScriptCache 1s, ScriptHook 1s, Review 0s) / OK [ran] [tree 4297f9cb7c7d] (2026-10-16T23:14:16Z)
- (audit edge) `self: annotations parsed from a real unittest failure layout; bounds still catch a runaway regex (seconds)` → an import error with no FAIL blocks keeps the old 4-line tail (test) [tree 4297f9cb7c7d] (2026-10-16T23:14:16Z)
- (audit self) `self: annotations parsed from a real unittest failure layout; bounds still catch a runaway regex (seconds)` → no findings [tree 4297f9cb7c7d] (2026-10-16T23:14:16Z)
- `python3 plugin/tests/run.py test_ci_annotations test_guard_exec_vectors` → exit 0 · Ran 42 tests in 1.4s (7 classes, 16 at a time; slowest: ScriptCache 1s, ScriptHook 1s, Review 0s) / OK [ran] [tree 4297f9cb7c7d] (2026-10-16T23:15:07Z)
- (audit edge) `self: annotations parsed from a real unittest failure layout; bounds still catch a runaway regex (seconds)` → an import error with no FAIL blocks keeps the old 4-line tail (test) [tree 4297f9cb7c7d] (2026-10-16T23:15:07Z)
- (audit adversary) `self: annotations parsed from a real unittest failure layout; bounds still catch a runaway regex (seconds)` → only test timing bounds changed in the guard tests; the guard's behaviour and every vector assertion are untouched, and a catastrophic-backtracking regex still fails the 0.5 s bound [tree 4297f9cb7c7d] (2026-10-16T23:15:07Z)
- (audit self) `self: annotations parsed from a real unittest failure layout; bounds still catch a runaway regex (seconds)` → no findings [tree 4297f9cb7c7d] (2026-10-16T23:15:07Z)
## Log
- 2026-10-16T23:13:35Z created
- 2026-10-16T23:13:38Z focused
- 2026-10-16T23:15:52Z done
- 2026-10-16T23:15:53Z committed 25e0f7ae (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1227 [FIX S, done, 1 steps] CI: the fm run --sandbox test needs no real bubblewrap
- playbook Profiling (skills/playbooks/references/perf/profiling.md)
- T-0805 [FIX S, done, 2 steps] The hook benchmark judges by CPU time when the machine is busy, so load alone never fails the gate — lesson: a latency gate on a shared mac…
- decision 2026-10-15: T-0970 dropped as a duplicate of T-0705's ambient runner; ambient tests switched on in this repo; stays opt-in by default (CPU on the user's machine…
- similar finished tasks took 1–2 steps
- start here (files T-1227 touched): plugin/tests/test_unattended.py, CHANGELOG.md
## Regression test
test_ci_annotations: red before annotations() existed, green after; the timing bound reproduced from the CI annotation (0.109 > 0.08)
## Plan gaps
- failed first: step 1 Loosen the two process_time bounds; per-failure ::error lines with a test
## Files touched
- plugin/tests/test_ci_annotations.py
- plugin/tests/run.py
- plugin/tests/test_guard_exec_vectors.py
- CHANGELOG.md
