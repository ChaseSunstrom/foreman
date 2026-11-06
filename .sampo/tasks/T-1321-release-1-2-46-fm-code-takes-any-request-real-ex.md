---
id: T-1321
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T02:23:11Z
updated: 2026-10-21T03:57:29Z
base: 5f59d05ccb54b0ca87867e283ec3e8e6d05ea7d2
base_tree: e65de4ba50ca469a1f4466a1d014b41921ee48e0
plan0_at: 2026-10-21T02:23:13Z
plan0_scope: []
verified: strong
---
# Release 1.2.46: fm code takes any request, real examples on the site, linked state folders
## Raw request
> Release 1.2.46: fm code takes any request, real examples on the site, linked state folders
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 1.2.46 is on main — verify with `git log -1 --format=%s origin/main`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.46 --push
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `git log -1 --format=%s origin/main` → exit 0 · Foreman 1.2.46 [ran] [tree c7bcd5ba5f46] (2026-10-21T03:54:28Z)
- (step 1) `git log -1 --format=%s origin/main` → exit 0 · Foreman 1.2.46 [ran] [tree c7bcd5ba5f46] (2026-10-21T03:54:28Z)
- (audit operator) `self: 1.2.46 on origin/main (db2d00ae); the first attempt's check failed under two concurrent full checks, the full suite then passed alone (2429 tests) and --resume released` → CI starts on the push [tree c7bcd5ba5f46] (2026-10-21T03:54:28Z)
- (audit self) `self: 1.2.46 on origin/main (db2d00ae); the first attempt's check failed under two concurrent full checks, the full suite then passed alone (2429 tests) and --resume released` → no findings [tree c7bcd5ba5f46] (2026-10-21T03:54:28Z)
## Log
- 2026-10-21T02:23:11Z created
- 2026-10-21T02:23:12Z focused
- 2026-10-21T03:13:17Z user approved publish in Claude Code's permission prompt
- 2026-10-21T03:13:17Z undo point at this yes for publish: HEAD 5f59d05ccb54
- 2026-10-21T03:24:18Z paused: focus moved to T-1326
- 2026-10-21T03:32:23Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-21T03:32:23Z focused
- 2026-10-21T03:39:29Z publish grant used by fm release --push
- 2026-10-21T03:57:29Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1320 [FEATURE M, done, 5 steps] Can you show better examples of fm code on the website? and I should be able to do anythin — lesson: Probe a capability with real runs …
- T-1220 [FEATURE L, done, 3 steps] Feature pages for the site: one page per Foreman capability, each with real graphs from Foreman's own history — lesson: A stdlib site g…
- T-1318 [SECURITY M, done, 3 steps] Guard: ctx.state_dir and foreman_home/state are compared as given, not at their real path — lesson: Resolve the folder above a path so…
- decision 2026-10-16: Round 4 skips 'bare fm re-executes the worktree's own copy'
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–5 steps
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
- plugin/lib/fmcode.py
- plugin/lib/fmpr.py
- plugin/lib/fmrelease.py
- plugin/tests/test_code_worker.py
- plugin/tests/test_release.py
