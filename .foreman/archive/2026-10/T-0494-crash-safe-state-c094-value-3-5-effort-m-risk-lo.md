---
id: T-0494
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T18:01:12Z
done_in: T-0679
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
- 2026-10-09T14:30:17Z created
- 2026-10-09T15:40:15Z batched into T-0679
- 2026-10-09T18:01:12Z done in T-0679 (batch)
## Follow-ups captured
