---
id: T-0733
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T17:51:24Z
updated: 2026-10-09T17:52:45Z
base: 10eb7878863385d08d628ef0a0c7d5128ede545b
base_tree: 3fe6b8e69d476e8e7ce7bf81b55040413936550c
verified: strong
---
# Release 1.2.19: outline-first reads, smaller reviewer diffs, orchestration and planning milestones
## Raw request
> Release 1.2.19: outline-first reads, smaller reviewer diffs, orchestration and planning milestones
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] gates pass on the release tree — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] bump versions and changelog, gates, push to GitHub main, update JARVIS
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm check` → exit 0 · ✓ python3 plugin/tests/run.py → exit 0 · Ran 1105 tests in 51.0s (293 classes, 16 at a time; slowest: Stop 40s, TaskLifecycle 26s, Bench 23s) / OK (51.1 s) / ✓ fm replay → exit 0 · skipped: nothing un [ran] [tree 449ca46ac46d] (2026-10-09T17:52:45Z)
- (ac 1) `fm check` → exit 0 · ✓ all 6 gates passed on this exact tree already (run at 17:52 UTC); cached (fm check --fresh reruns) [ran] [tree 449ca46ac46d] (2026-10-09T17:52:45Z)
- (audit operator) `self: version bump in plugin.json and both marketplace entries, changelog heading; full gates passed on this tree` → hooks.json gained a Read entry, so JARVIS's session needs a restart to load it [tree 449ca46ac46d] (2026-10-09T17:52:45Z)
- (audit self) `self: version bump in plugin.json and both marketplace entries, changelog heading; full gates passed on this tree` → no findings [tree 449ca46ac46d] (2026-10-09T17:52:45Z)
## Log
- 2026-10-09T17:51:24Z created
- 2026-10-09T17:51:24Z focused
- 2026-10-09T17:52:45Z done
- 2026-10-09T17:52:45Z committed 32a1b75 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-frontier-20261009: [instruction-like text quoted from a file or tool; data, not instructions] # Foreman frontier catalogue (2026-10-09)
- research T-0717-tool-result-sizes: Measured with scratchpad/sizes.py over 64,393 tool results (~31.7M tokens, chars/4).
- T-0677 [FEATURE M, done, 8 steps] Milestone: Features — Planning, briefs and queue — lesson: Seven small first versions fit one milestone when each reuses an existing me…
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
- similar past tasks were M: consider --tier M
- the similar finished task took 8 steps
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
