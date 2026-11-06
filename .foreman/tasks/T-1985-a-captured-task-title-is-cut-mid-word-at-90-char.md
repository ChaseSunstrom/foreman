---
id: T-1985
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T13:23:04Z
updated: 2026-10-29T13:33:15Z
done_in: T-1987
---
# A captured task title is cut mid-word at 90 characters ("…DONE-WHEN fallbac") and its firs
## Raw request
> FIX: a captured task title is cut mid-word at 90 characters ("…DONE-WHEN fallbac") and its first word is capitalized even when it is a command or identifier ("Fm batch", "C.first_touch"); cut at a word boundary with an ellipsis and leave an identifier-like first word as typed
> DONE-WHEN: a long capture's title ends at a word boundary with … and "fm batch …" stays lowercase :: python3 plugin/tests/run.py test_cli
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
- 2026-10-29T13:23:04Z created
- 2026-10-29T13:23:09Z batched into T-1987
- 2026-10-29T13:33:15Z done in T-1987 (batch)
## Follow-ups captured
