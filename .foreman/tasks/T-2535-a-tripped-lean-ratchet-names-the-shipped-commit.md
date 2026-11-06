---
id: T-2535
type: FEATURE
tier: M
status: deferred
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T04:14:14Z
updated: 2026-11-02T04:21:39Z
revisit: 2026-12-01
---
# A tripped lean ratchet names the shipped commit behind each grown static metric (rules,…
## Raw request
> FEATURE: a tripped lean ratchet names the shipped commit behind each grown static metric (rules, descriptions, largest SKILL chars, measured per commit with git show), at fm ship and in fm doctor
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
- 2026-11-02T04:14:14Z created
- 2026-11-02T04:19:57Z dropped: measured: the lean ratchet has never tripped at a ship (no decision names a grown metric; the one sweep check on record shrank: rules 6395->6391, largest SKILL 9742->9269); attribution waits for a first trip
- 2026-11-02T04:21:38Z set status=planned
- 2026-11-02T04:21:39Z deferred: revive at the first lean-ratchet trip at fm ship whose cause takes more than one look at the shipped commits (revisit 2026-12-01)
## Follow-ups captured
