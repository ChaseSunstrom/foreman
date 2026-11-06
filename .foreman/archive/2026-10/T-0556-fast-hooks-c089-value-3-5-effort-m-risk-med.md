---
id: T-0556
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:42Z
---
# Fast hooks (C089, value 3/5, effort M, risk med)
## Raw request
> FEATURE: Fast hooks (C089, value 3/5, effort M, risk med)
>   first version: First version: record per-hook import time and an SLO burn counter in the ledger, and have fm doctor/friction flag regressions with the offending commit range. Skip daemon (adds a long-lived process near the guard).
>   what it is: Keep hooks fast with a resident daemon, lazy imports, fork servers and latency SLOs.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:42Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
