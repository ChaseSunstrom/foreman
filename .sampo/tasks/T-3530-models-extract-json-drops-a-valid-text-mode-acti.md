---
id: T-3530
type: FIX
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T19:50:52Z
updated: 2026-11-06T19:50:52Z
inferred_deps: [T-2878]
inferred_why: T-2878: named in its request
---
# models.extract_json drops a valid text-mode action whose string holds an invalid JSON…
## Raw request
> FIX: models.extract_json drops a valid text-mode action whose string holds an invalid JSON escape (\' from code like name.replace('\'', ...)): retry the decode with lone backslashes doubled. Seen T-2878 step 1, exam s28-020 slow-rust-602726: jarvis-nothink's {"action": "done"} refused 5 turns running as 'No action found'
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
- 2026-11-06T19:50:52Z created
## Follow-ups captured
