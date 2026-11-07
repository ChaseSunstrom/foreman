---
id: T-3598
type: PERFORMANCE
tier: L
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T03:38:52Z
updated: 2026-11-07T03:38:52Z
---
# Something polls Ollama's /api/tags ~2 times a second (3714 GETs in 30 min on 2026-11-06,…
## Raw request
> PERFORMANCE: something polls Ollama's /api/tags ~2 times a second (3714 GETs in 30 min on 2026-11-06, plus 465 /api/show and 402 /v1/models) - each reads every manifest; find the caller (watch --web lanterns? _tags/_probe) and cache it (found in T-3588)
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
- 2026-11-07T03:38:52Z created
## Follow-ups captured
