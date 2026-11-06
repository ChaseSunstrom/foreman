---
id: T-1143
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:07:02Z
updated: 2026-10-16T10:12:42Z
base: c75bfff689160926482b7d5f899108e48226f43d
base_tree: b465173657720cae2dc607ce2aeda9bbf2c8238d
plan0_at: 2026-10-16T10:07:02Z
plan0_scope: []
verified: ok
---
# Release Foreman 1.2.32 (foreman-ui 0.18.0) and push to main (the user: 'push to main when you get a chance, and when you're done with everything too')
## Raw request
> Release Foreman 1.2.32 (foreman-ui 0.18.0) and push to main (the user: 'push to main when you get a chance, and when you're done with everything too')
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] versions say 1.2.32 and main has the release — verify with `git log origin/main --oneline -1`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Full gates green; bump versions, CHANGELOG heading, commit
2. [x] Merge into main in a temporary worktree, push
## Resume here
## Docs impact
## Verification evidence
- (step 1) `tail -4 /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/tasks/b077kppml.output` → exit 0 · ! the gates changed the working tree: one of them writes files (a check should only read) / [exited with code 0] [ran] [tree 84ea54cfce55] (2026-10-16T10:11:06Z)
- (step 2) `git log origin/main --oneline -1` → exit 0 · 9876489 Merge foreman/build: Foreman 1.2.32 [ran] [tree d0b30fee36d6] (2026-10-16T10:12:00Z)
- (ac 1) `git log origin/main --oneline -1` → exit 0 · 9876489 Merge foreman/build: Foreman 1.2.32 [ran] [tree d0b30fee36d6] (2026-10-16T10:12:01Z)
- (audit self) `self: full gates green before the bump (1,921 tests OK, replay 0 newly allowed); fm release-check OK after it; merged --no-ff in a temporary worktree like 1.2.31 and pushed 20ff93a..9876489` → no findings [tree d0b30fee36d6] (2026-10-16T10:12:01Z)
## Log
- 2026-10-16T10:07:02Z created
- 2026-10-16T10:07:02Z focused
- 2026-10-16T10:12:00Z scope: CHANGELOG.md, README.md, version files — the release commit 72f7222, merged to main as 9876489 and pushed
- 2026-10-16T10:12:42Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1091 [CLEAN S, done, 2 steps] Release Foreman 1.2.31 and push to main (the user: push to main when you get a chance)
- T-0953 [FEATURE S, done, 1 steps] Release 1.2.30 to GitHub main (user asked to push) — lesson: Run the full suite before release.py when a session changed hook wiring: t…
- playbook Release and changelog (skills/playbooks/references/release/release-and-changelog.md)
- decision 2026-10-15: Release as 1.2.28 via release.py --push, not a raw push
- similar finished tasks took 1–2 steps
- start here (files T-1091 touched): .claude-plugin/marketplace.json, CHANGELOG.md, plugin/.claude-plugin/plugin.json, plugin/tests/test_loop.py
## Behaviour lock
none: a release changes only versions, the CHANGELOG heading and README prose; the full gates (1,921 tests, fm replay 0 new bypasses) passed on the code it ships, and fm release-check passed after the bump
## Lessons
- Run the release gates on a quiet tree: edits during the run read as a gate writing files
## Files touched
- README.md
- .claude-plugin/marketplace.json
- CHANGELOG.md
- mods/foreman-ui/.claude-plugin/plugin.json
- plugin/.claude-plugin/plugin.json
