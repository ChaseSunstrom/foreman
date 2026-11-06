---
id: T-0835
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-14T18:44:18Z
updated: 2026-10-14T18:45:04Z
base: 2f5cd14793442bea6f1bb7bfa4d0bda8b43e7b54
base_tree: 970cf624d69250bfd8dcc726ea8b3833d9897030
verified: ok
---
# CHANGELOG: Unreleased entries for the 2026-10-14 rounds (CC integration, compact output, fm page, review fixes)
## Raw request
> CHANGELOG: Unreleased entries for the 2026-10-14 rounds (CC integration, compact output, fm page, review fixes)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] CHANGELOG.md's Unreleased section lists this session's user-visible changes with task ids — verify with `grep -q T-0777 CHANGELOG.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Write the Unreleased entries from git log since 1.2.27
## Resume here
## Docs impact
CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `grep -q T-0777 CHANGELOG.md` → exit 0 · (no output) [ran] [tree e11ce2e8019c] (2026-10-14T18:44:40Z)
- (ac 1) `grep -q T-0777 CHANGELOG.md` → exit 0 · (no output) [ran] [tree e11ce2e8019c] (2026-10-14T18:45:03Z)
- (audit self) `self: one Unreleased block grouping the 39 commits since 1.2.27 by what the user sees, each with its task ids; checked each claim against its commit subject` → no findings [tree e11ce2e8019c] (2026-10-14T18:45:03Z)
## Log
- 2026-10-14T18:44:18Z created
- 2026-10-14T18:44:19Z focused
- 2026-10-14T18:45:04Z done
- 2026-10-14T18:45:04Z committed af24034 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0821 [FIX M, done, 4 steps] Round-1 review fixes (low): outward-tool gate fails closed, fm page warns in sensitive repos and redacts the username instead of refusing, …
- research brainstorm-round2-20261014: 437 ideas (9 lenses x 4 rounds + 3 deepen rounds, past every earlier run's ideas) in 29 capability clusters, each grounded in the co…
- T-0801 [RESEARCH M, done, 2 steps] Super-improve Foreman round 1: brainstorm, ground and queue (CC-feature integration) — lesson: a criterion's verify must check somethi…
- decision 2026-10-14: [revisit: after 2026-10-15] Round 1 of the T-0760 brainstorm: build 12 briefs (T-0775..T-0786) plus the 5 discovered fixes (T-0759, T-0765, T-0767, …
## Behaviour lock
none: CHANGELOG.md text only; fm check's self-docs tests cover its format
## Lessons
- Write the changelog line at each close, not at the end of a 40-commit run
## Files touched
- CHANGELOG.md
