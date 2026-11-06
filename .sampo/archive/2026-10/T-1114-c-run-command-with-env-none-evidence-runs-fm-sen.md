---
id: T-1114
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_core.py]
depends_on: []
source: discovered
created: 2026-10-16T05:36:59Z
updated: 2026-10-16T05:38:37Z
base: b6bae374eaa8780d7fb17bad9a18364a513da8bd
base_tree: 2ca0aba5d3f10a7066da376cc8ee66d2e6d56da5
verified: strong
---
# C.run_command with env=None (evidence runs, fm sentinel, fm resume) inherits an exported F
## Raw request
> c.run_command with env=None (evidence runs, fm sentinel, fm resume) inherits an exported FOREMAN_SKIP_TESTS, so an evidence run could leave modules out silently; scrub it as fm check does
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A verification run never inherits FOREMAN_SKIP_TESTS from the environment — verify with `python3 plugin/tests/run.py test_core`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then scrub it in run_command
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core` → ✗ exit 1 · Ran 67 tests in 6.2s (16 classes, 16 at a time; slowest: PreToolUse 6s, WritesAndLocks 2s, PathsAndProjects 1s) / FAILED (1 classes) [ran] [tree 95db18705890] (2026-10-16T05:37:52Z)
- (step 1) `python3 plugin/tests/run.py test_core test_check_paths` → exit 0 · Ran 77 tests in 27.2s (18 classes, 16 at a time; slowest: CheckSkip 27s, CheckPaths 9s, PreToolUse 4s) / OK [ran] [tree 8a2b78206947] (2026-10-16T05:38:30Z)
- (ac 1) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 67 tests in 2.3s (16 classes, 16 at a time; slowest: PreToolUse 2s, WritesAndLocks 2s, PathsAndProjects 1s) / OK [ran] [tree bf9462183fd0] (2026-10-16T05:38:34Z)
- (audit self) `self: in-process test with the variable exported; fm check's explicit env path unchanged (test_check_paths)` → no findings [tree bf9462183fd0] (2026-10-16T05:38:34Z)
## Log
- 2026-10-16T05:36:59Z created
- 2026-10-16T05:37:24Z set scope=['plugin/lib/fmcore.py', 'plugin/tests/test_core.py']
- 2026-10-16T05:37:30Z focused
- 2026-10-16T05:38:31Z scope: CHANGELOG.md — release note
- 2026-10-16T05:38:36Z done
- 2026-10-16T05:38:37Z committed 4ea8e99 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1101 [FEATURE S, done, 2 steps] Fm check should not fail one task's close on another checkpointed task's recorded red test — lesson: A loop variable that reuses an out…
- research wave2-plan-af4fd23e40a859f90: === T-1028 [stale: plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/lib/fmtidy.py changed since it was written]
- research wave1-plan-a306a171bb6861f90: === T-1044 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-04: Landscape 2026-10-04 grounded: no new work
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_core.py
## Lessons
- Scrub control variables at the one function every run goes through, not at each caller
## Plan gaps
- failed first: step 1 Failing test, then scrub it in run_command
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- CHANGELOG.md
