---
id: T-1954
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T10:05:49Z
updated: 2026-10-29T10:13:45Z
done_in: T-1957
---
# Fm task new --json --focus prints fm focus's text on stdout after the JSON, so piping it i
## Raw request
> FIX: fm task new --json --focus prints fm focus's text on stdout after the JSON, so piping it into jq fails although the task was made; under --json the focus text goes to stderr
> DONE-WHEN: fm task new --json --focus prints one JSON document on stdout
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
- 2026-10-29T10:05:49Z created
- 2026-10-29T10:05:57Z batched into T-1957
- 2026-10-29T10:13:45Z done in T-1957 (batch)
## Follow-ups captured
