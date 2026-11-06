---
id: T-3148
type: PERFORMANCE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T05:37:01Z
updated: 2026-11-05T05:45:48Z
---
# test_run's nested run.main calls can write the real test-result cache file…
## Raw request
> test_run's nested run.main calls can write the real test-result cache file (.fm-scratch); point it at a temp cache (T-3140 follow-up)
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
- 2026-11-05T05:37:01Z created
- 2026-11-05T05:45:48Z dropped: folded into T-3140: its builder is fixing review finding 5 (nested run.py writes the real cache) in the same branch
## Follow-ups captured
