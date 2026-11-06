---
id: T-0721
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T17:01:39Z
updated: 2026-10-09T17:04:07Z
base: bd1505cef3d11cae4bc98a3b9fed35f5a3a3e40e
base_tree: c88e83c3598c8246ea0f3f41df089b5d0c2ae562
verified: strong
---
# Release 1.2.17: guard hardening, instruments, autonomy milestone
## Raw request
> Release 1.2.17: guard hardening, instruments, autonomy milestone
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
- (step 1) `fm check` → exit 0 · ✓ python3 plugin/tests/run.py → exit 0 · Ran 1058 tests in 91.1s (271 classes, 16 at a time; slowest: Stop 78s, TaskLifecycle 49s, Bench 46s) / OK (91.2 s) — slower: 91.2 s vs a usual 59.3 s / ✓ fm re [ran] [tree 4c548934bc4b] (2026-10-09T17:04:02Z)
- (ac 1) `fm check` → exit 0 · ✓ all 6 gates passed on this exact tree already (run at 17:04 UTC); cached (fm check --fresh reruns) [ran] [tree 4c548934bc4b] (2026-10-09T17:04:06Z)
- (audit operator) `self: version bump in plugin.json and both marketplace entries, changelog heading in the 1.2.16 layout; full gates passed on this tree` → JARVIS picks it up with marketplace update + plugin update; its live session keeps the old hooks until restart [tree 4c548934bc4b] (2026-10-09T17:04:06Z)
- (audit self) `self: version bump in plugin.json and both marketplace entries, changelog heading in the 1.2.16 layout; full gates passed on this tree` → no findings [tree 4c548934bc4b] (2026-10-09T17:04:06Z)
## Log
- 2026-10-09T17:01:39Z created
- 2026-10-09T17:01:40Z focused
- 2026-10-09T17:04:06Z done
- 2026-10-09T17:04:07Z committed a3de9b7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0680 [FEATURE M, planned, 8 steps] Milestone: Features — Self-improvement and learning
- T-0678 [FEATURE M, planned, 2 steps] Milestone: Features — Releases and delivery
- research T-0258-review-1: Verdict:** changes needed. I found one HIGH cross-feature issue, two MEDIUM, and the rest are LOW doc or maintainer drift. I read the whole dif…
- decision 2026-09-26: Full autonomy never asks mid-run but still can't grant itself core or run destructive/irreversible guard categories: those are recorded with fm ask …
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
