---
id: T-1918
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/agents/fm-builder.md, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-29T04:48:20Z
updated: 2026-10-29T05:48:38Z
base: 962230acaecd39001c47bf7c6b1face9905d270b
base_tree: 41ed8fb053df0833eeb5a22fbda951120e68cd2e
plan0_at: 2026-10-29T05:47:55Z
plan0_scope: [plugin/agents/fm-builder.md, CHANGELOG.md]
verified: strong
---
# Fm-builder.md says to probe code through the criteria's tests
## Raw request
> FIX: fm-builder.md never says fm modules live in plugin/lib, so builders probe with cd scripts; python3 -c 'import fmplaybooks' (3x exit 1); add one line: test through plugin/tests/run.py
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm-builder.md tells builders to probe through the named tests, not python3 -c imports — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Add the line and changelog; test_lanes green
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 34 tests in 13.8s (5 classes, 16 at a time; slowest: Lanes 14s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree d0087b515b98] (2026-10-29T05:48:16Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 34 tests in 13.8s (5 classes, 16 at a time; slowest: Lanes 14s, BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree d0087b515b98] (2026-10-29T05:48:35Z)
- (audit edge) `self: read the diff; one contract line plus changelog` → docs-only, test_lanes green [tree d0087b515b98] (2026-10-29T05:48:35Z)
- (audit intent) `self: read the diff; one contract line plus changelog` → the line names the criteria's tests as the probe route [tree d0087b515b98] (2026-10-29T05:48:35Z)
- (audit self) `self: read the diff; one contract line plus changelog` → no findings [tree d0087b515b98] (2026-10-29T05:48:35Z)
## Log
- 2026-10-29T04:48:20Z created
- 2026-10-29T04:48:25Z set tier=S
- 2026-10-29T05:17:28Z planned from capture
- 2026-10-29T05:47:55Z focused
- 2026-10-29T05:48:36Z done
- 2026-10-29T05:48:38Z committed a2204d4d (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1505-review: Verdict: approve with nits.** I found no HIGH issues and no failure of the acceptance criteria. I had no shell, so I read the code and ran nothin…
- research wave2-plan-af4fd23e40a859f90: === T-1028 [stale: plugin/lib/fmbus.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py changed since it was written]
- research T-1519-review-2: All six review points are fixed test-first, in one commit on top of a clean `foreman/build` merge. The 12 tests in `test_docs` (Fences, HelpAns…
- decision 2026-10-21: Accept foreman-ui's supply entry after T-1434 named its hooks module
## Regression test
none: docs-only; one line in an agent contract that no test reads
## Why not caught
none: docs-only; the builder contract never named a probe route, and no test reads the contract's wording
## Lessons
- Agent contracts should name the probe route, or agents invent costly ones
## Files touched
- CHANGELOG.md
- plugin/agents/fm-builder.md
