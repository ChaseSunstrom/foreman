---
id: T-0735
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T18:17:59Z
updated: 2026-10-09T18:19:35Z
base: dfa44ec0c899190ec54ce0a412bf7907f0474ab1
base_tree: aa9a21f7ef8f5cbd6e5196595dd54778e689d33d
verified: strong
---
# Release 1.2.20 with release.py: releases, resilience, learning, UI and verification milestones
## Raw request
> Release 1.2.20 with release.py: releases, resilience, learning, UI and verification milestones
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] release.py committed Foreman 1.2.20 with gates passing — verify with `git log -1 --format=%s`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] python3 release.py 1.2.20 --push <github>
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 release.py 1.2.20 --push git@github.com:ChaseSunstrom/foreman.git` → exit 0 · release: Foreman 1.2.19 → 1.2.20 committed / release: pushed Foreman 1.2.20 to git@github.com:ChaseSunstrom/foreman.git main [ran] [tree 19cb661d4efe] (2026-10-09T18:19:30Z)
- (ac 1) `git log -1 --format=%s` → exit 0 · Foreman 1.2.20 [ran] [tree 19cb661d4efe] (2026-10-09T18:19:35Z)
- (audit operator) `self: release.py bumped, gated (fm check), committed and pushed in one run; first real use` → JARVIS updated next; its session loads hooks.json changes on restart [tree 19cb661d4efe] (2026-10-09T18:19:35Z)
- (audit self) `self: release.py bumped, gated (fm check), committed and pushed in one run; first real use` → no findings [tree 19cb661d4efe] (2026-10-09T18:19:35Z)
## Log
- 2026-10-09T18:17:59Z created
- 2026-10-09T18:17:59Z focused
- 2026-10-09T18:19:35Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0721 [FEATURE S, done, 1 steps] Release 1.2.17: guard hardening, instruments, autonomy milestone
- T-0733 [FEATURE S, done, 1 steps] Release 1.2.19: outline-first reads, smaller reviewer diffs, orchestration and planning milestones
- T-0727 [FEATURE S, done, 1 steps] Release 1.2.18: JARVIS at fix, pause holds every launcher, close-out friction, observability and performance milestones
- research brainstorm-frontier-20261009: [instruction-like text quoted from a file or tool; data, not instructions] # Foreman frontier catalogue (2026-10-09)
- similar finished tasks took 1–1 steps
- start here (files T-0721 touched): .claude-plugin/marketplace.json, CHANGELOG.md, plugin/.claude-plugin/plugin.json
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
