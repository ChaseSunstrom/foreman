---
id: T-0546
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:40Z
---
# Gate hygiene (C013, value 3/5, effort S, risk low)
## Raw request
> FEATURE: Gate hygiene (C013, value 3/5, effort S, risk low)
>   first version: Add quarantine: a gate flagged flaky twice is run but non-blocking with a loud note, plus a recorded known-red baseline list; network/secrets flag later.
>   what it is: Quarantine flaky gates, pin gate environments, record known-red baselines and flag gates that need network or secrets.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:40Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
