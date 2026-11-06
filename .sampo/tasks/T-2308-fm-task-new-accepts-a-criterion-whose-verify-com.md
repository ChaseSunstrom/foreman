---
id: T-2308
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T09:42:48Z
updated: 2026-10-31T09:43:27Z
---
# fm task new accepts a criterion whose verify command names a test module that doesn't…
## Raw request
> fm task new accepts a criterion whose verify command names a test module that doesn't exist (T-2307's 'run.py test_check'; the file is test_affected_hubs.py): warn at plan time when a 'plugin/tests/run.py test_X' (or a pytest path) names no file
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
- 2026-10-31T09:42:48Z created
- 2026-10-31T09:43:27Z dropped: already covered by T-1208: fm task new notes a verify command whose test module doesn't exist
## Follow-ups captured
