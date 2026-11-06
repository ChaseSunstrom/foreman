---
id: T-1243
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T19:45:12Z
updated: 2026-10-16T20:08:17Z
base: b6f06e0ef74ec781fa3fdd8d2d09b6a32ce6764c
base_tree: 6dd9858c91a751125c3a0ed5b9954985633b07a6
plan0_at: 2026-10-16T19:45:15Z
plan0_scope: []
verified: ok
---
# Release 1.2.38 and push: Benchmarks page fixes
## Raw request
> Release 1.2.38 and push: Benchmarks page fixes
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 1.2.38 on origin/main and the Pages deploy green — verify with `git fetch -q origin && git log origin/main -1 --format=%s`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.38 --push
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git fetch -q origin && git log origin/main -1 --format=%s | grep -x 'Foreman 1.2.38'` → exit 0 · Foreman 1.2.38 [ran] [tree 49e5a1e2057d] (2026-10-16T20:06:48Z)
- (ac 1) `git fetch -q origin && git log origin/main -1 --format=%s` → exit 0 · Foreman 1.2.38 [ran] [tree 49e5a1e2057d] (2026-10-16T20:06:50Z)
- (audit self) `self: origin/main is Foreman 1.2.38; the Pages deploy for 58ad5df9 succeeded (GitHub API)` → no findings [tree 49e5a1e2057d] (2026-10-16T20:06:50Z)
## Log
- 2026-10-16T19:45:12Z created
- 2026-10-16T19:45:15Z focused
- 2026-10-16T20:00:02Z user approved publish in Claude Code's permission prompt
- 2026-10-16T20:00:02Z undo point at this yes for publish: HEAD b6f06e0ef74e
- 2026-10-16T20:00:20Z publish grant used by fm release --push
- 2026-10-16T20:08:17Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1218 [CLEAN S, done, 1 steps] Release Foreman 1.2.35 and push to main so the Pages site publishes
- T-1238 [CLEAN S, done, 1 steps] Release 1.2.37: guard credential reads, approval binding, fm code, cheaper Foreman turns, neutral benchmark suites and the Benchmarks page
- T-1143 [CLEAN S, done, 2 steps] Release Foreman 1.2.32 (foreman-ui 0.18.0) and push to main (the user: 'push to main when you get a chance, and when you're done with eve…
- decision 2026-10-15: T-0964: queue 7 of the rival gaps (T-0969..T-0975); keep the LATER ones (PR-per-task flow, best-of-N lanes, diff-comment review page, plan/edit mode…
- similar finished tasks took 1–2 steps
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
