---
id: T-1208
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T14:52:18Z
updated: 2026-10-16T15:19:08Z
---
# A criterion's verify command that runs a test module which doesn't exist (python3 plugin/t
## Raw request
> A criterion's verify command that runs a test module which doesn't exist (python3 plugin/tests/run.py test_lease) is accepted at fm task new and only fails at finish with NO TESTS RAN; warn at plan time like the missing npm script check (T-1145)
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
- 2026-10-16T14:52:18Z created
- 2026-10-16T15:19:08Z dropped: already covered: fm task new notes a verify command whose test module doesn't exist ('test_lease.py doesn't exist yet'); the T-1205 note was printed and missed because only the last output line was read
## Follow-ups captured
