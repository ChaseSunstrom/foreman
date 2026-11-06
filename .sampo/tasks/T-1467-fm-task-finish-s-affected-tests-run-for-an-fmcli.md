---
id: T-1467
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_affected_hubs.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T15:22:58Z
updated: 2026-10-22T15:50:25Z
base: e6be6b8867c4434ffb3f515515aeca1f1df255b6
base_tree: b04b93387f983488d4bd5565e6cbe150f9a51156
plan0_at: 2026-10-22T15:37:47Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_affected_hubs.py, CHANGELOG.md]
verified: strong
---
# A file that co-changes with every test no longer runs them all
## Raw request
> fm task finish's affected-tests run for an fmcli.py change takes ~114 s of a 121 s close (T-1462's first 'Slowest' line): fmcli.py links nearly every test file. Narrow the link for big hub modules to the functions the diff touched (symbol-level: tests that name the changed functions or their verbs), falling back to the file link when unsure
## Interpretation
affected() adds co-change pairs both ways (fmcli.py ~4146-4148); 28 test files pair with CHANGELOG.md, which every task edits, so every close ran ~28 suites (114-142 s of 121-150 s closes, T-1462's Slowest line). The capture guessed fmcli.py's links; measured, it is the CHANGELOG pairs.
## Assumptions (confidence)
## Acceptance criteria
- [x] a CHANGELOG-only change runs no paired tests while a narrow pair still runs — verify with `cd plugin/tests && python3 -m unittest test_affected_hubs`
## Non-goals
## Approach (options → choice → why)
A changed file whose co-change fan-out (tests paired with it, either direction) exceeds HUB_PAIRS (10) is a hub and contributes no pairs; its direct map links (tests_for) still count. Options: drop pairs for *.md (misses a doc a test really reads; tests_for covers that), symbol-level links (M, later) → fan-out threshold.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] hub threshold in affected()
3. [x] measure a close before/after
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_affected_hubs` → exit 0 · Ran 1 test in 2.190s / OK [ran] [tree 490f1137d3c8] (2026-10-22T15:38:17Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_affected_hubs test_cli.AffectedPairs` → exit 0 · Ran 2 tests in 3.555s / OK [ran] [tree 490f1137d3c8] (2026-10-22T15:48:18Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_affected_hubs test_cli.AffectedPairs` → exit 0 · Ran 2 tests in 3.929s / OK [ran] [tree 490f1137d3c8] (2026-10-22T15:48:23Z)
- (step 3) `python3 -I -c "import json; m=json.load(open('state/projects/foreman-4a056f/map.json')); p=m.get('pairs') or {}; t=lambda f: '/test_' in f; fan=sum(1 for a,bs in p.items() if t(a) and 'CHANGELOG.md' in bs)+sum(1 for x in p.get('CHANGELOG.md',[]) if t(x)); print('CHANGELOG.md co-change fan-out', fan, '> HUB_PAIRS 10: pairs dropped')"` → exit 0 · CHANGELOG.md co-change fan-out 28 > HUB_PAIRS 10: pairs dropped [ran] [tree 490f1137d3c8] (2026-10-22T15:48:41Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_affected_hubs` → exit 0 · Ran 1 test in 2.331s / OK [ran] [tree 8152616d27b9] (2026-10-22T15:48:55Z)
- (audit intent) `builder (sonnet) test-first (red then green); merged; test_affected_hubs + test_cli.AffectedPairs (T-0952 narrow pair) green; the builder's one affected-run failure didn't reproduce in three split reruns (load flake).` → the 2-minute closes came from CHANGELOG pairs, not fmcli.py links as captured — measured and fixed at the cause [tree 8152616d27b9] (2026-10-22T15:48:55Z)
- (audit edge) `builder (sonnet) test-first (red then green); merged; test_affected_hubs + test_cli.AffectedPairs (T-0952 narrow pair) green; the builder's one affected-run failure didn't reproduce in three split reruns (load flake).` → a file paired with exactly 10 tests still pulls them in; a test file that itself pairs with >10 files stops pulling pairs; tests_for links unaffected [tree 8152616d27b9] (2026-10-22T15:48:55Z)
- (audit adversary) `builder (sonnet) test-first (red then green); merged; test_affected_hubs + test_cli.AffectedPairs (T-0952 narrow pair) green; the builder's one affected-run failure didn't reproduce in three split reruns (load flake).` → fewer tests run per close, never fewer gates: full fm check still runs everything [tree 8152616d27b9] (2026-10-22T15:48:55Z)
- (audit self) `builder (sonnet) test-first (red then green); merged; test_affected_hubs + test_cli.AffectedPairs (T-0952 narrow pair) green; the builder's one affected-run failure didn't reproduce in three split reruns (load flake).` → no findings [tree 8152616d27b9] (2026-10-22T15:48:55Z)
## Log
- 2026-10-22T15:22:58Z created
- 2026-10-22T15:36:15Z planned from capture
- 2026-10-22T15:37:21Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1467.builder.md
- 2026-10-22T15:37:44Z focused
- 2026-10-22T15:48:08Z merged worktree-agent-a609f1cdd8df03e4b (2 file(s))
- 2026-10-22T15:48:09Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a609f1cdd8df03e4b
- 2026-10-22T15:48:11Z focused
- 2026-10-22T15:50:18Z done
- 2026-10-22T15:50:25Z committed 55c54035 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-1462 [PERFORMANCE S, done, 2 steps] fm task finish names its slowest run
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-22: Recommendation: keep 2 SE as the bench gate's fail line (3-5% false alarms); add an inconclusive verdict for a pass-total loss between 1 and 2 SE th…
- similar finished tasks took 2–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Measurements
test files paired in by a CHANGELOG.md edit: 28 → 0 (its co-change fan-out is 28 > HUB_PAIRS 10; map.json). Affected run per close before: 114, 119, 129, 142 s (T-1462's Slowest lines on T-1462, T-1464, T-1424, T-1428); after: this task's own close line.
## Files touched
- plugin/tests/test_affected_hubs.py
- plugin/lib/fmcli.py
- CHANGELOG.md
