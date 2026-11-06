---
id: T-0457
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T18:17:52Z
done_in: T-0682
---
# Reject vacuous proof (C001, value 4/5, effort M, risk low)
## Raw request
> FEATURE: Reject vacuous proof (C001, value 4/5, effort M, risk low)
>   first version: Make fm task done refuse a criterion whose verify command also passes on the start tree (or with the diff's hunks reverted), reusing the prove --hunks machinery; today the user must run prove by hand.
>   what it is: Refuse a done claim whose verify command can't fail, by mutating the code or reverting the fix and checking the check goes red.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 16 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T15:40:16Z batched into T-0682
- 2026-10-09T18:17:52Z done in T-0682 (batch)
## Follow-ups captured
