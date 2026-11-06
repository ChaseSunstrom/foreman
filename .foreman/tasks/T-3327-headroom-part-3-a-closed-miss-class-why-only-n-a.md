---
id: T-3327
type: FEATURE
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/selfaware.py, plugin/tests/test_self_aware.py]
depends_on: []
source: followup
created: 2026-11-06T04:31:26Z
updated: 2026-11-06T04:31:27Z
---
# Headroom part 3: a 'closed' miss class: 'why only N' and 'more than this' steers are logged as closed-set misses
## Raw request
> Headroom part 3: a 'closed' miss class: 'why only N' and 'more than this' steers are logged as closed-set misses
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] selfaware.CLASSES has 'closed'; the user's message 'there's only 26 tower ideas, but how come there's not more than that?' is classed closed; existing classes unchanged — verify with `python3 plugin/tests/run.py test_self_aware`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] test with the user's own message, red  <- CURRENT
2. [ ] add the class and its pattern
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:31:26Z created
## Follow-ups captured
