---
id: T-1225
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T16:33:03Z
updated: 2026-10-16T17:19:56Z
done_in: T-1231
---
# Fm task ac/step: 'fm task ac T-1 "text"' and 'fm task ac add T-1 …' fail with a bare argpa
## Raw request
> fm task ac/step: 'fm task ac T-1 "text"' and 'fm task ac add T-1 …' fail with a bare argparse choice error; accept either order or say 'did you mean fm task ac T-1 add …'
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
- 2026-10-16T16:33:03Z created
- 2026-10-16T17:19:56Z done in T-1231: fm task ac/step take their action on either side of the id (T-1231's argv shaper)
## Follow-ups captured
