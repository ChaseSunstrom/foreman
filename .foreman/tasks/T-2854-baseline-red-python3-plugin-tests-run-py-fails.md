---
id: T-2854
type: FIX
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-11-03T22:22:47Z
updated: 2026-11-03T22:41:51Z
trigger: baseline
trigger_key: 3f2a9c9ef7666722
baseline: true
done_in: T-2855
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_claims.Claims.test_a_lane_brief_preclaims_its_concrete_scope_and_names_the_command, test_unattended.Unattended.test_usage_measures_whether_next_was_followed. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
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
- 2026-11-03T22:22:47Z created
- 2026-11-03T22:41:51Z done in T-2855: the same two tests (test_claims lane brief, test_unattended Next-followed) T-2855 fixed; the full gates ran green after it
## Follow-ups captured
