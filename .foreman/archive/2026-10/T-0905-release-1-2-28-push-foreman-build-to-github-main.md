---
id: T-0905
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T18:32:42Z
updated: 2026-10-15T18:34:59Z
base: fe127f480b7af3f3919952926cc9441729978eea
base_tree: 90734a7b7123c042c655ade8de96ba4322568851
verified: strong
---
# Release 1.2.28: push foreman/build to GitHub main (user asked)
## Raw request
> Release 1.2.28: push foreman/build to GitHub main (user asked)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] origin/main contains HEAD's tree as 'Foreman 1.2.28' — verify with `git fetch origin && git diff --quiet origin/main HEAD`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] release.py 1.2.28 --push (bumps, fm check, merge --no-ff into main, push)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git fetch -q origin && git diff --quiet origin/main HEAD && git log -1 --format=%s origin/main` → exit 0 · Foreman 1.2.28 [ran] [tree 3c89bc44fa99] (2026-10-15T18:34:48Z)
- (ac 1) `git fetch origin && git diff --quiet origin/main HEAD` → exit 0 · (no output) [ran] [tree 3c89bc44fa99] (2026-10-15T18:34:59Z)
- (audit edge) `self: release.py bumped 1.2.27→1.2.28, fm check green (1365 tests, roundtrip 17/17), --no-ff merge pushed; origin/main tree equals HEAD; outgoing diff scanned for home paths, names and e-mail (none; recordings scrubbed)` → origin/main had 15 release-merge commits not on this branch; release.py merges in a scratch clone, so no rewrite of main [tree 3c89bc44fa99] (2026-10-15T18:34:59Z)
- (audit self) `self: release.py bumped 1.2.27→1.2.28, fm check green (1365 tests, roundtrip 17/17), --no-ff merge pushed; origin/main tree equals HEAD; outgoing diff scanned for home paths, names and e-mail (none; recordings scrubbed)` → no findings [tree 3c89bc44fa99] (2026-10-15T18:34:59Z)
## Log
- 2026-10-15T18:32:42Z created
- 2026-10-15T18:32:43Z focused
- 2026-10-15T18:34:59Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0352 [FEATURE M, blocked, 3 steps] Publish Foreman Desktop on GitHub with CI and release pipelines
- research mission-20261009-091631.pack: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just sim…
- research mission-20261009-091631: Request: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just…
- decision 2026-09-26: Released: fast-forwarded main 924fe06 → bd86fd6 (43 commits: T-0018 rounds 1-10, T-0036, T-0038, T-0039) and pushed main + foreman/build to origin
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
