---
id: T-1811
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T07:30:15Z
updated: 2026-10-28T07:55:32Z
---
# The T-1800 burn scan has the same gap, because `burn.json` is also written only from `--re
## Raw request
> the T-1800 burn scan has the same gap, because `burn.json` is also written only from `--refresh-cache`, so it is likewise absent without a cap or contract
> (noticed by an agent; research T-1810-review)
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
- 2026-10-28T07:30:15Z created
- 2026-10-28T07:55:32Z dropped: already covered by T-1810: fmcost.sweep (every project's Stop hook, no cap or contract) rewrites burn.json when it is over 10 min old or the setup changed (plugin/lib/fmcost.py:444-458; test_foresight test_a_setup_change_reruns_the_burn_scan_at_once)
## Follow-ups captured
