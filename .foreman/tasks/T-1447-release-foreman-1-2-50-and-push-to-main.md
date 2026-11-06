---
id: T-1447
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T23:21:15Z
updated: 2026-10-21T23:35:12Z
base: 11ed8e101cb5187fefe29b75e0e134fe07487d20
base_tree: 833ae97f4d14a3906a262526622bba758c3ffe1a
plan0_at: 2026-10-21T23:21:16Z
plan0_scope: []
verified: strong
---
# Release Foreman 1.2.50 and push to main
## Raw request
> Release Foreman 1.2.50 and push to main
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm release 1.2.50 --push completes: main has 'Foreman 1.2.50' — verify with `git log origin/main --oneline -1`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.50 --push
## Resume here
## Docs impact
CHANGELOG headed 1.2.50 by the release
## Verification evidence
- (step 1) `git log origin/main --oneline -1` → exit 0 · cb018df9 Foreman 1.2.50 [ran] [tree 476c48043125] (2026-10-21T23:31:36Z)
- (ac 1) `git log origin/main --oneline -1` → exit 0 · cb018df9 Foreman 1.2.50 [ran] [tree 476c48043125] (2026-10-21T23:31:38Z)
- (audit intent) `self: fm release 1.2.50 ran every step (full fm check, release-check, push, round tag, canary started) with no hold` → origin/main is 'Foreman 1.2.50' [tree 476c48043125] (2026-10-21T23:31:38Z)
- (audit operator) `self: fm release 1.2.50 ran every step (full fm check, release-check, push, round tag, canary started) with no hold` → canary report in logs/canary-1.2.50.txt (fm release --canary-status) [tree 476c48043125] (2026-10-21T23:31:38Z)
- (audit self) `self: fm release 1.2.50 ran every step (full fm check, release-check, push, round tag, canary started) with no hold` → no findings [tree 476c48043125] (2026-10-21T23:31:38Z)
## Log
- 2026-10-21T23:21:15Z created
- 2026-10-21T23:21:16Z focused
- 2026-10-21T23:21:18Z guard authorization added: publish
- 2026-10-21T23:31:12Z publish grant used by fm release --push
- 2026-10-21T23:35:12Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1440 [FEATURE S, done, 1 steps] Release Foreman 1.2.49 (foreman-ui 0.18.3) and push to main — lesson: A new machine-state check can block the release gate on its first…
- T-1143 [CLEAN S, done, 2 steps] Release Foreman 1.2.32 (foreman-ui 0.18.0) and push to main (the user: 'push to main when you get a chance, and when you're done with eve…
- T-1218 [CLEAN S, done, 1 steps] Release Foreman 1.2.35 and push to main so the Pages site publishes
- decision 2026-10-15: Release as 1.2.28 via release.py --push, not a raw push
- similar finished tasks took 1–2 steps
- start here (files T-1440 touched): .claude-plugin/marketplace.json, CHANGELOG.md, mods/foreman-ui/.claude-plugin/plugin.json, plugin/.claude-plugin/plugin.json
## Why not caught
none
## Lessons
- Release in small batches: a clean batch passes the gate first time
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
