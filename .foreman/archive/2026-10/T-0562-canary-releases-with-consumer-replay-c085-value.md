---
id: T-0562
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:43Z
---
# Canary releases with consumer replay (C085, value 3/5, effort M, risk low)
## Raw request
> FEATURE: Canary releases with consumer replay (C085, value 3/5, effort M, risk low)
>   first version: Before a release, run fm replay, fm bench and fm sentinel across every project from fm projects and print per-project deltas; skip channels and synthetic fixtures.
>   what it is: Replay consumer projects against a release candidate and close a release only after consumers ran it.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:43Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
