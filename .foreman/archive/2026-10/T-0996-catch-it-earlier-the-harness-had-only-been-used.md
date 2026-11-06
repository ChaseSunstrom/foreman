---
id: T-0996
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-15T23:51:22Z
updated: 2026-10-16T00:01:21Z
---
# Catch it earlier: the harness had only been used with local commands (/fm) or single promp
## Raw request
> T-0995 (The UI harness's interactive session (shot.py) was driven by the Stop hook into the queue: it planned three tasks and took focus from the working session) wasn't caught before it shipped: the harness had only been used with local commands (/fm) or single prompts in projects with drive off; full auto plus a prompt was never tried
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
- 2026-10-15T23:51:22Z created
- 2026-10-16T00:01:21Z dropped: covered: T-0995's test runs the harness case (FOREMAN_ONEOFF=1 never driven), and shot.py sets it
## Follow-ups captured
