---
id: T-0389
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T01:55:21Z
updated: 2026-10-09T01:57:53Z
inferred_deps: [T-0383]
inferred_why: T-0383: named in its request
base: badb0dc6786477fd7779135480646d13934b42c4
base_tree: 4e24a08e01879133616215e36c2b8eeb90f92ffb
verified: strong
---
# FIX: plugin/tests/run.py keeps only the last -p, so 'run.py -p a.py -p b.py' silently runs
## Raw request
> FIX: plugin/tests/run.py keeps only the last -p, so 'run.py -p a.py -p b.py' silently runs b.py alone (found by the T-0383 builder; I relied on it several times) — make -p repeatable
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] run.py -p a -p b runs both modules — verify with `python3 plugin/tests/run.py -k test_run_py_repeats_p`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then -p append
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_run_py_repeats_p` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: DiffGates 0s) / OK (start tree + this task's tests) [ran] [tree 07a41e2bc974] (2026-10-09T01:56:50Z)
- `python3 plugin/tests/run.py -k test_run_py_repeats_p` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: DiffGates 0s) / OK [ran] [tree 07a41e2bc974] (2026-10-09T01:56:50Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 01:54 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; pytho [ran] [tree 46a74688ef61] (2026-10-09T01:57:52Z)
- (ac 1) `python3 plugin/tests/run.py -k test_run_py_repeats_p` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: DiffGates 0s) / OK [ran] [tree 46a74688ef61] (2026-10-09T01:57:53Z)
- (audit intent) `self: patterns deduped, default unchanged; full gate runs the whole suite through the same path` → -p a -p b runs both (test); no -p still discovers test*.py (the gate) [tree 46a74688ef61] (2026-10-09T01:57:53Z)
- (audit edge) `self: patterns deduped, default unchanged; full gate runs the whole suite through the same path` → the same -p twice runs it once (dict.fromkeys) [tree 46a74688ef61] (2026-10-09T01:57:53Z)
- (audit self) `self: patterns deduped, default unchanged; full gate runs the whole suite through the same path` → no findings [tree 46a74688ef61] (2026-10-09T01:57:53Z)
## Log
- 2026-10-09T01:55:21Z created
- 2026-10-09T01:56:36Z focused
- 2026-10-09T01:57:53Z done
- 2026-10-09T01:57:53Z committed 53230ae (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0258 [RESEARCH L, done, 4 steps] After all of that, recursively brainstorm and improve yourself — lesson: Recursive brainstorming converges fast once each pass is grou…
- T-0099 [FEATURE M, done, 3 steps] Brainstorms find more, wilder and unspoken ideas and build off categories — lesson: Feed brainstormers the user's own words and a yes-a…
- playbook Agent Introspection Debugging (skills/playbooks/references/reflect/agent-introspection.md)
- decision 2026-10-03: T-0110 (one yes for several queued core tasks) closed as done in T-0119: the standing core yes covers every task; plugin and remote stay per-task by…
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–4 steps
## Regression test
test_run_py_repeats_p (test_diff_gates). Red before the fix, run by hand: 'AssertionError: Ran 2 tests not found in Ran 1 tests in 0.2s (1 classes ... slowest: Help 0s)' — only the last -p module ran. fm task prove can't show it: run.py lives under plugin/tests/, so prove copies the fixed runner onto the start tree as a test file.
## Files touched
- plugin/tests/test_diff_gates.py
- plugin/tests/run.py
- CHANGELOG.md
