---
id: T-0549
type: SECURITY
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:41Z
---
# Supply-chain and install trust (C032, value 3/5, effort M, risk low)
## Raw request
> SECURITY: Supply-chain and install trust (C032, value 3/5, effort M, risk low)
>   first version: Record a content hash of each enabled plugin and MCP tool description in doctor and warn on change between runs. Detection only.
>   what it is: Gate dependency changes, quarantine unknown repos, pin and diff plugins and MCP descriptions, and sign releases.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:18Z created
- 2026-10-09T14:30:41Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
