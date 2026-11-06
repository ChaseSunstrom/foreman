---
id: T-1319
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T01:04:02Z
updated: 2026-10-21T01:30:32Z
base: 2e316e7f892820ce176056ae86d13995ede0a499
base_tree: 09f9e718a066ef7be7393ceb066e593fb91b0b13
plan0_at: 2026-10-21T01:04:03Z
plan0_scope: []
verified: strong
---
# Release 1.2.45: fm code tui in motion, guard hints for unreadable programs, macOS green
## Raw request
> Release 1.2.45: fm code tui in motion, guard hints for unreadable programs, macOS green
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 1.2.45 is on main with its changelog and CI starts — verify with `git log -1 --format=%s origin/main`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.45 --push
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `git log -1 --format=%s origin/main` → exit 0 · Foreman 1.2.45 [ran] [tree 7086f938b751] (2026-10-21T01:26:24Z)
- (step 1) `git log -1 --format=%s origin/main` → exit 0 · Foreman 1.2.45 [ran] [tree 7086f938b751] (2026-10-21T01:26:24Z)
- (audit operator) `self: 1.2.45 commit on origin/main; changelog carries T-1300, T-1298, T-1296, T-1284` → CI starts on the push; macOS job watched next [tree 7086f938b751] (2026-10-21T01:26:24Z)
- (audit self) `self: 1.2.45 commit on origin/main; changelog carries T-1300, T-1298, T-1296, T-1284` → no findings [tree 7086f938b751] (2026-10-21T01:26:24Z)
## Log
- 2026-10-21T01:04:02Z created
- 2026-10-21T01:04:03Z focused
- 2026-10-21T01:20:00Z user approved publish in Claude Code's permission prompt
- 2026-10-21T01:20:00Z undo point at this yes for publish: HEAD 2e316e7f8928
- 2026-10-21T01:26:01Z publish grant used by fm release --push
- 2026-10-21T01:30:32Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1300 [FEATURE L, done, 7 steps] Foreman Code TUI in motion: a truecolor renderer, eased animation (pulse, spinner, travelling light, rolling counters, growing bars, fl…
- T-1299 [FEATURE S, done, 1 steps] Release 1.2.44: fm code bench, worker leases fixed, macOS CI fixes, run.py unknown names, research --append, guard hints, stack cards, …
- research mission-20261020-183042: Request: super improve the foreman code tui, better animations/looks/not just static colors, etc. etc.
- decision 2026-10-21: T-1300 ships the renderer, motion, gradients, recording and round 1 of the TUI brainstorm; round 2 is queued as T-1305..T-1315 (with T-1301 wide cha…
- similar finished tasks took 1–7 steps
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
