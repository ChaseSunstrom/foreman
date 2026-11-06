---
id: T-1247
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T21:42:49Z
updated: 2026-10-16T22:54:37Z
base: da7e4e2311d8782da4974b51adaef9105499b071
base_tree: c6efa6291cee54e28d3bd840e05e87290de0e25b
plan0_at: 2026-10-16T21:42:52Z
plan0_scope: []
verified: ok
---
# Release 1.2.39 and push: long-session benchmark, site review fixes, CI fix
## Raw request
> Release 1.2.39 and push: long-session benchmark, site review fixes, CI fix
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] 1.2.39 on origin/main — verify with `git fetch -q origin && git log origin/main -1 --format=%s | grep -x 'Foreman 1.2.39'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.39 --push
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git fetch -q origin && test "$(git log origin/main -1 --format=%s)" = 'Foreman 1.2.39'` → exit 0 · (no output) [ran] [tree 37c05a4efdeb] (2026-10-16T22:53:36Z)
- (ac 1) `git fetch -q origin && git log origin/main -1 --format=%s | grep -x 'Foreman 1.2.39'` → exit 0 · Foreman 1.2.39 [ran] [tree 37c05a4efdeb] (2026-10-16T22:53:37Z)
- (audit self) `self: origin/main is Foreman 1.2.39 (fm release pushed it after the gates and release-check)` → no findings [tree 37c05a4efdeb] (2026-10-16T22:53:37Z)
## Log
- 2026-10-16T21:42:49Z created
- 2026-10-16T21:42:52Z focused
- 2026-10-16T22:52:31Z user approved publish in Claude Code's permission prompt
- 2026-10-16T22:52:31Z undo point at this yes for publish: HEAD da7e4e2311d8
- 2026-10-16T22:52:51Z publish grant used by fm release --push
- 2026-10-16T22:54:37Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1218 [CLEAN S, done, 1 steps] Release Foreman 1.2.35 and push to main so the Pages site publishes
- T-1243 [CLEAN S, done, 1 steps] Release 1.2.38 and push: Benchmarks page fixes
- T-1220 [FEATURE L, done, 3 steps] Feature pages for the site: one page per Foreman capability, each with real graphs from Foreman's own history — lesson: A stdlib site g…
- decision 2026-10-15: Release as 1.2.28 via release.py --push, not a raw push
- similar finished tasks took 1–3 steps
- start here (files T-1218 touched): .claude-plugin/marketplace.json, CHANGELOG.md, mods/foreman-ui/.claude-plugin/plugin.json, plugin/.claude-plugin/plugin.json
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
