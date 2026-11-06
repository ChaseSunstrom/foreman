---
id: T-0330
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-06T02:25:26Z
updated: 2026-10-06T03:01:51Z
done_in: T-0338
---
# Guard: D=~/x; mkdir -p $D && cd $D leaves D unknown (fmguard _track_vars drops ~ values) s
## Raw request
> Guard: D=~/x; mkdir -p $D && cd $D leaves D unknown (fmguard _track_vars drops ~ values) so a cd into a home path guesses the Foreman checkout as target; expand leading ~ to ctx.home first
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
- 2026-10-06T02:25:26Z created
- 2026-10-06T02:40:56Z batched into T-0338
- 2026-10-06T03:01:51Z done in T-0338 (batch)
## Follow-ups captured
