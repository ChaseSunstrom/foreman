---
id: T-2264
type: FIX
tier: M
status: dropped
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-31T03:44:37Z
updated: 2026-10-31T04:27:31Z
baseline: true
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_orchestration.ConflictBrief.test_a_conflicting_merge_leaves_a_brief_and_the_way_to_resolve_it. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-31T03:44:37Z created
- 2026-10-31T04:27:31Z dropped: fixed by T-2265 (the conflict-brief test reads T-2208's steps); test_orchestration.ConflictBrief passes
## Follow-ups captured
