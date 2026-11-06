---
id: T-0890
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T15:29:55Z
updated: 2026-10-15T15:37:51Z
base: f53629a7c110cda87a33842430f48a797d6945ab
base_tree: dd2d85b2d0ad370d87c58e56a2f6b3d583b8be9c
verified: strong
---
# Fm projects --next ranks the next action across every project in one list
## Raw request
> FEATURE: fm projects --next ranks the next action across every project in one list
> CONTEXT: round 5 #24. fm projects lists projects; SOURCE_VALUE scoring in fmcore could rank
## Interpretation
fm projects --next prints one ranked list of each project's next action: a project waiting on the user first, then active tasks, then queued, then inbox, most recently active first within a rank
## Assumptions (confidence)
## Acceptance criteria
- [x] fm projects --next ranks a waiting/active project above an inbox-only one — verify with `python3 plugin/tests/run.py test_projects`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_projects, then the next field and --next
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_projects test_help test_watch` → exit 0 · Ran 11 tests in 0.8s (8 classes, 16 at a time; slowest: Help 1s, Projects 1s, Follow 1s) / OK [ran] [tree 4658b5c400b2] (2026-10-15T15:36:08Z)
- `python3 plugin/tests/run.py test_projects` → ✗ exit 1 · Ran 6 tests in 1.0s (5 classes, 16 at a time; slowest: Projects 1s, Follow 1s, VersionSkew 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 4658b5c400b2] (2026-10-15T15:36:10Z)
- `python3 plugin/tests/run.py test_projects` → exit 0 · Ran 6 tests in 0.7s (5 classes, 16 at a time; slowest: Projects 1s, Follow 1s, VersionSkew 0s) / OK [ran] [tree 4658b5c400b2] (2026-10-15T15:36:10Z)
- (ac 1) `python3 plugin/tests/run.py test_projects` → exit 0 · Ran 6 tests in 0.7s (5 classes, 16 at a time; slowest: Projects 1s, Follow 1s, VersionSkew 0s) / OK [ran] [tree 4658b5c400b2] (2026-10-15T15:37:50Z)
- (audit self) `self review: each project row carries next=(rank, line); --next sorts by rank (stable, so most recently active first within one); tried live across 5 projects; JSON consumers get one additive field` → no findings [tree 4658b5c400b2] (2026-10-15T15:37:50Z)
## Log
- 2026-10-15T15:29:55Z created
- 2026-10-15T15:30:04Z set tier=S
- 2026-10-15T15:35:43Z focused
- 2026-10-15T15:37:50Z done
- 2026-10-15T15:37:51Z committed 8e02e1f (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0673 [FEATURE M, done, 7 steps] Milestone: Features — Multi-machine, multi-project and ecosystem — lesson: a capture into another project must not run that project's e…
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- research brainstorm-20261002-round2: Source: research/brainstorm-20261002-145137 (3 lenses, 21 ideas) merged with own list; user steer: queue/inbox/activity must match t…
- decision 2026-09-27: Recursion bound for T-0063: after R5, one more round (R6: auto-evidence from Bash results matching a criterion's verify command) from the existing R…
## Files touched
- plugin/tests/test_projects.py
- plugin/lib/fmwatch.py
- plugin/lib/fmcli.py
