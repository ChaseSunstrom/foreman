---
id: T-0083
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-02T18:34:51Z
updated: 2026-10-02T19:01:08Z
done_in: T-0088
---
# fm task new plans an M/L brief in one call (--interpretation, --approach)
## Raw request
> fm task new plans an M/L brief in one call (--interpretation, --approach)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm task new --tier M --interpretation X --approach Y --ac .. --step .. --focus starts the task — verify with `python3 -m unittest discover -s plugin/tests -p test_round_i.py -q`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red test  <- CURRENT
2. [ ] add flags to task new, write sections
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-02T18:34:51Z created
- 2026-10-02T19:01:08Z done in T-0088
## Follow-ups captured
