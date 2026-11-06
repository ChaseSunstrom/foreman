---
id: T-1118
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/test_builder.py]
depends_on: []
source: user
created: 2026-10-16T05:50:55Z
updated: 2026-10-16T05:51:26Z
base: c299f04be53a61aa708863bd0a6bea0a9c7b2698
base_tree: 8b2953de173aa549661345d026632796a0854341
verified: strong
---
# Baseline red: test_builder expects 'two builders' but the cap message (T-1089) reads '2 builders are already out … the cap is 2'
## Raw request
> Baseline red: test_builder expects 'two builders' but the cap message (T-1089) reads '2 builders are already out … the cap is 2'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_builder passes — verify with `python3 plugin/tests/run.py test_builder`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Assert the cap message T-1089 introduced
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_builder` → ✗ exit 1 · Ran 22 tests in 6.3s (7 classes, 16 at a time; slowest: Contract 6s, Brief 3s, LaneMergeGate 2s) / FAILED (1 classes) [ran] [tree 8b2953de173a] (2026-10-16T05:51:05Z)
- (step 1) `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 22 tests in 6.9s (7 classes, 16 at a time; slowest: Contract 7s, Brief 3s, LaneMergeGate 2s) / OK [ran] [tree 1a5f636da24f] (2026-10-16T05:51:17Z)
- (ac 1) `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 22 tests in 6.9s (7 classes, 16 at a time; slowest: Contract 7s, Brief 3s, LaneMergeGate 2s) / OK [ran] [tree 1a5f636da24f] (2026-10-16T05:51:25Z)
- (audit self) `self: the assertion now names the cap message T-1089 introduced; the full suite had only this failure` → no findings [tree 1a5f636da24f] (2026-10-16T05:51:25Z)
## Log
- 2026-10-16T05:50:55Z created
- 2026-10-16T05:50:55Z focused
- 2026-10-16T05:51:26Z done
- 2026-10-16T05:51:26Z committed 0bbee98 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1101 [FEATURE S, done, 2 steps] Fm check should not fail one task's close on another checkpointed task's recorded red test — lesson: A loop variable that reuses an out…
- T-0779 [PERFORMANCE S, done, 2 steps] Lane briefs pass a per-tier effort with the model — lesson: a lane's builder should record the failing run before the fix; when it …
- T-0806 [PERFORMANCE S, done, 2 steps] Builders run only the affected tests; the full gates run once, in the main thread, after the merge — lesson: a gate that runs again…
- decision 2026-10-14: Round 2 slate: 437 ideas in 29 clusters grounded → 3 build (compact spill cap T-0824, closed-pipe verb sweep T-0825, verb-usage evidence attached to…
## Plan gaps
- failed first: step 1 Assert the cap message T-1089 introduced
## Files touched
- plugin/tests/test_builder.py
