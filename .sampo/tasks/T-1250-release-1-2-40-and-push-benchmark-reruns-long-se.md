---
id: T-1250
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-17T00:12:23Z
updated: 2026-10-20T13:44:12Z
base: 741be0875a5d343f41cfb83739cdd4229aebc3d2
base_tree: 793e6e1f862758863511efd4b05dd2556e181049
plan0_at: 2026-10-17T00:12:26Z
plan0_scope: []
verified: ok
---
# Release 1.2.40 and push: benchmark reruns, long-session cost cuts, CI annotations
## Raw request
> Release 1.2.40 and push: benchmark reruns, long-session cost cuts, CI annotations
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 1.2.40 on origin/main — verify with `git fetch -q origin && test "$(git log origin/main -1 --format=%s)" = 'Foreman 1.2.40'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.40 --push
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git fetch -q origin && test "$(git log origin/main -1 --format=%s)" = 'Foreman 1.2.40'` → exit 0 · (no output) [ran] [tree 77c6a28e6a3d] (2026-10-17T00:29:36Z)
- (ac 1) `git fetch -q origin && test "$(git log origin/main -1 --format=%s)" = 'Foreman 1.2.40'` → exit 0 · (no output) [ran] [tree 77c6a28e6a3d] (2026-10-17T00:29:38Z)
- (audit self) `self: origin/main is Foreman 1.2.40, pushed by fm release after its gates` → no findings [tree 77c6a28e6a3d] (2026-10-17T00:29:38Z)
- (audit self) `self: origin/main is Foreman 1.2.40, pushed by fm release after its gates` → no findings [tree 77c6a28e6a3d] (2026-10-20T13:43:28Z)
## Log
- 2026-10-17T00:12:23Z created
- 2026-10-17T00:12:26Z focused
- 2026-10-17T00:26:45Z user approved publish in Claude Code's permission prompt
- 2026-10-17T00:26:45Z undo point at this yes for publish: HEAD 741be0875a5d
- 2026-10-17T00:27:08Z publish grant used by fm release --push
- 2026-10-20T13:44:12Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1247 [CLEAN S, done, 1 steps] Release 1.2.39 and push: long-session benchmark, site review fixes, CI fix
- T-1243 [CLEAN S, done, 1 steps] Release 1.2.38 and push: Benchmarks page fixes
- T-0953 [FEATURE S, done, 1 steps] Release 1.2.30 to GitHub main (user asked to push) — lesson: Run the full suite before release.py when a session changed hook wiring: t…
- decision 2026-10-16: T-1231 L plan approval under standard autonomy: the user's explicit request ('I want foreman to be better than CC though, and cheaper/faster') is th…
- similar finished tasks took 1–1 steps
- start here (files T-1247 touched): .claude-plugin/marketplace.json, CHANGELOG.md, plugin/.claude-plugin/plugin.json
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
