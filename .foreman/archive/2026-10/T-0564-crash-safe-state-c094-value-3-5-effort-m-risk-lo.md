---
id: T-0564
type: FEATURE
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:44Z
---
# Crash-safe state (C094, value 3/5, effort M, risk low)
## Raw request
> FEATURE: Crash-safe state (C094, value 3/5, effort M, risk low)
>   first version: First version: `fm doctor --repair` for briefs vs STATE vs ledger mismatches and torn-file recovery, with a torn-write unit test; skip the single append-only log rewrite and git-ref store.
>   what it is: Version, migrate and write state transactionally with locks, repair commands and a git-ref backup.
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
- 2026-10-09T14:30:44Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
