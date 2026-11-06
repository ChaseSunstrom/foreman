---
id: T-1367
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T06:07:30Z
updated: 2026-10-21T06:21:22Z
base: 28a773ef6bb306a5d2c144b2284323fd84bdecda
base_tree: b2eae48126ebaeb8ee9c9c2a7b9369c94afafbb9
plan0_at: 2026-10-21T06:07:32Z
plan0_scope: []
verified: strong
---
# Release Foreman 1.2.47 (runners, live progress, detached canary, TUI firewall, veto fix)
## Raw request
> Release Foreman 1.2.47 (runners, live progress, detached canary, TUI firewall, veto fix)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] Foreman 1.2.47 is released and pushed to origin's main — verify with `git log origin/main -1 --format=%s | grep -q 'Foreman 1.2.47'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.47 --push
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git log origin/main -1 --format=%s | grep 'Foreman 1.2.47'` → exit 0 · Foreman 1.2.47 [ran] [tree 19add743662c] (2026-10-21T06:16:49Z)
- (ac 1) `git log origin/main -1 --format=%s | grep -q 'Foreman 1.2.47'` → exit 0 · (no output) [ran] [tree 19add743662c] (2026-10-21T06:16:50Z)
- (audit intent) `self: fm release 1.2.47 --push ran every gate (check, release-check), committed, pushed to origin main, tagged round-14; canary detached` → released and pushed; origin/main's head is Foreman 1.2.47 [tree 19add743662c] (2026-10-21T06:16:50Z)
- (audit self) `self: fm release 1.2.47 --push ran every gate (check, release-check), committed, pushed to origin main, tagged round-14; canary detached` → no findings [tree 19add743662c] (2026-10-21T06:16:50Z)
## Log
- 2026-10-21T06:07:30Z created
- 2026-10-21T06:07:31Z focused
- 2026-10-21T06:07:37Z guard authorization added: publish
- 2026-10-21T06:16:37Z publish grant used by fm release --push
- 2026-10-21T06:21:22Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261020-222446.pack: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage ANY CL…
- T-1319 [FEATURE S, done, 1 steps] Release 1.2.45: fm code tui in motion, guard hints for unreadable programs, macOS green
- T-1362 [FIX S, done, 2 steps] fm release's canary (fm sentinel in every local project) runs after the push without blocking the release command; its result lands in the …
- decision 2026-10-20: Abandoned the unfinished 1.2.40 release state: it was pushed; only its advisory canary was left, which 1.2.41's release runs
- similar finished tasks took 1–2 steps
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
