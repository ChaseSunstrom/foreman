---
id: T-0930
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:44:50Z
updated: 2026-10-15T19:48:32Z
base: 31d11710e524fe552115cb4e80d5315bae47ebbb
base_tree: 47a1f37804d819a69907f3d5638ce2804edde89b
verified: ok
---
# Update this machine's installed foreman-ui to 0.7.0 so every session draws the redesigned pane
## Raw request
> Update this machine's installed foreman-ui to 0.7.0 so every session draws the redesigned pane
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] doctor's foreman-ui release check passes — verify with `fm doctor -v 2>&1 | grep -q 'PASS  foreman-ui release'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] plugin yes, then claude plugin marketplace update foreman and claude plugin update foreman-ui@foreman
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm doctor -v 2>&1 | grep -q 'PASS  foreman-ui release'` → exit 0 · (no output) [ran] [tree 47a1f37804d8] (2026-10-15T19:48:23Z)
- (ac 1) `fm doctor -v 2>&1 | grep -q 'PASS  foreman-ui release'` → exit 0 · (no output) [ran] [tree 47a1f37804d8] (2026-10-15T19:48:32Z)
- (audit self) `self: two plugin yeses in Claude Code's prompt (the first was scoped to install/enable); the local foreman marketplace refreshed and foreman-ui went 0.6.0 → 0.7.0 for scope user; sessions pick it up on restart` → no findings [tree 47a1f37804d8] (2026-10-15T19:48:32Z)
## Log
- 2026-10-15T19:44:50Z created
- 2026-10-15T19:44:50Z focused
- 2026-10-15T19:47:39Z user approved plugin in Claude Code's permission prompt
- 2026-10-15T19:48:06Z user approved plugin in Claude Code's permission prompt
- 2026-10-15T19:48:08Z plugin grant used for: claude plugin marketplace update
- 2026-10-15T19:48:32Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0711 [FEATURE M, done, 4 steps] Frontier 11 — Cockpit UI — lesson: Remote data in a UI belongs behind a cache and a detached refresh, so the render path never waits on…
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- T-0915 [CLEAN S, done, 1 steps] Re-record the README live demo with the redesigned pane
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar finished tasks took 1–4 steps
## Behaviour lock
none: an install update of a released mod; the mod's tests pass in the repo
