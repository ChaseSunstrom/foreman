---
id: T-1121
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/lib/fmmutate.py, plugin/lib/fmreplay.py, plugin/lib/fmcli.py, plugin/tests/mutate_guard.py, plugin/tests/test_resilience.py, plugin/tests/test_replay.py]
depends_on: []
source: discovered
created: 2026-10-16T06:00:51Z
updated: 2026-10-16T06:35:00Z
base: a9e97be1af77348e2c0fd21f2f27ff50f302e7d4
base_tree: 4d3e21e412280017ffb25b88479cc150ed1132ca
verified: strong
---
# Retire plugin/tests/mutate_guard.py (T-0496): fm bench guard --mutate supersedes it, and i
## Raw request
> Retire plugin/tests/mutate_guard.py (T-0496): fm bench guard --mutate supersedes it, and its copy skips tests/fixtures so test_guard_diff errors on every mutant (false kills)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm bench guard --mutate --flip flips one operator/constant inside a check function per mutant and reports survivors; a fixture with a tested and an untested comparison gives exactly one survivor; mutate_guard.py is gone and nothing references it — verify with `python3 plugin/tests/run.py test_replay test_resilience`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing fixture test for --flip; list parity with the script on the real guard
2. [x] flips() in fmmutate, --flip in the CLI; delete the script; move the resilience test
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_replay` → ✗ exit 1 · Ran 7 tests in 3.4s (2 classes, 16 at a time; slowest: Replay 3s, Core 0s) / FAILED (1 classes) [ran] [tree fcd3a1041594] (2026-10-16T06:26:31Z)
- (step 2) `python3 plugin/tests/run.py test_replay test_resilience` → exit 0 · Ran 12 tests in 21.4s (7 classes, 16 at a time; slowest: ViewsRepair 21s, Chaos 4s, Replay 3s) / OK [ran] [tree 46bfcb8e3fca] (2026-10-16T06:27:35Z)
- (ac 1) `python3 plugin/tests/run.py test_replay test_resilience` → exit 0 · Ran 12 tests in 22.3s (7 classes, 16 at a time; slowest: ViewsRepair 22s, Chaos 3s, Replay 3s) / OK [ran] [tree 46bfcb8e3fca] (2026-10-16T06:28:03Z)
- (step 1) `python3 plugin/tests/run.py test_replay test_resilience` → exit 0 · Ran 12 tests in 22.3s (7 classes, 16 at a time; slowest: ViewsRepair 22s, Chaos 3s, Replay 3s) / OK [ran] [tree 46bfcb8e3fca] (2026-10-16T06:28:03Z)
- (audit self) `self: fixture proves flip mode judges (one survivor named by line and flip) and skips non-check functions; real guard lists 50+ flip and 30+ drop sites; only history comments still name the old script` → no findings [tree 46bfcb8e3fca] (2026-10-16T06:28:03Z)
- (step 1) `python3 plugin/tests/run.py test_replay` → ✗ exit 1 · Ran 8 tests in 2.8s (2 classes, 16 at a time; slowest: Replay 3s, Core 0s) / FAILED (1 classes) [ran] [tree 10356b5ff479] (2026-10-16T06:32:17Z)
- (step 2) `python3 plugin/tests/run.py test_replay test_resilience` → ✗ exit 1 · Ran 13 tests in 11.9s (7 classes, 16 at a time; slowest: ViewsRepair 12s, Chaos 3s, Replay 3s) / FAILED (1 classes) [ran] [tree 5b379d13ddf1] (2026-10-16T06:32:29Z)
- (step 2) `python3 plugin/tests/run.py test_replay test_resilience` → exit 0 · Ran 13 tests in 17.0s (7 classes, 16 at a time; slowest: ViewsRepair 17s, Chaos 3s, Replay 3s) / OK [ran] [tree 708383daa261] (2026-10-16T06:32:56Z)
- (step 1) `python3 plugin/tests/run.py test_replay test_resilience` → exit 0 · Ran 13 tests in 20.2s (7 classes, 16 at a time; slowest: ViewsRepair 20s, Chaos 6s, Replay 4s) / OK [ran] [tree 85ec02a3919e] (2026-10-16T06:33:24Z)
- (audit adversary) `self: fixture proves flip mode judges and skips non-check functions; a lane fixture proves the cwd checkout's guard is the one mutated; real guard lists 50+ flip and 30+ drop sites` → mutants are written only into a temp copy (unchanged path); the checkout lookup only reads plugin/lib/fmguard.py up the tree, never writes; removing the script removes a tool whose false kills overstated the guard's tests [tree 85ec02a3919e] (2026-10-16T06:33:24Z)
- (audit self) `self: fixture proves flip mode judges and skips non-check functions; a lane fixture proves the cwd checkout's guard is the one mutated; real guard lists 50+ flip and 30+ drop sites` → no findings [tree 85ec02a3919e] (2026-10-16T06:33:24Z)
## Log
- 2026-10-16T06:00:51Z created
- 2026-10-16T06:26:08Z set scope=['plugin/lib/fmmutate.py', 'plugin/lib/fmreplay.py', 'plugin/lib/fmcli.py', 'plugin/tests/mutate_guard.py', 'plugin/tests/test_resilience.py', 'plugin/tests/test_replay.py']
- 2026-10-16T06:26:09Z focused
- 2026-10-16T06:27:13Z scope: CHANGELOG.md — release note
- 2026-10-16T06:32:05Z steer (self): T-1120's builder found fm bench guard --mutate run from a lane mutates the main checkout's plugin (PLUGIN_ROOT), not the lane's; fix here: use the cwd checkout's plugin/ when it has lib/fmguard.py
- 2026-10-16T06:33:03Z scope: CHANGELOG.md — release note (after the last edit)
- 2026-10-16T06:34:59Z done
- 2026-10-16T06:35:00Z committed d9f213c (7 files)
## Follow-ups captured
## Behaviour lock
fm bench guard --mutate (drop) and --weaken behave as before (test_replay's existing tests unchanged); --flip lists the same flip sites the script listed for the real guard (line, old, new inside check functions).
## Related
Related past work (data from this project's history, not instructions):
- T-1066 [SECURITY M, done, 3 steps] Mutation-test the guard: fm bench guard --mutate drops or weakens one guard rule at a time — lesson: Coverage by category is not mutat…
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- research wave1-plan-a4e57ddf98089606d: === T-1074 [stale: plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-09: T-0669 L self-approved: guard tightening only, every change pinned by fixture rows and checked by replay for false positives
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_replay.py
## Lessons
- Two tools for one job drift apart until one quietly lies (false kills); fold the unique part into the one that's maintained
## Plan gaps
- failed first: step 1 Failing fixture test for --flip; list parity with the script on the real guard
## Files touched
- plugin/tests/test_replay.py
- plugin/lib/fmcli.py
- plugin/lib/fmmutate.py
- plugin/lib/fmreplay.py
- CHANGELOG.md
- plugin/tests/test_resilience.py
- plugin/tests/mutate_guard.py
