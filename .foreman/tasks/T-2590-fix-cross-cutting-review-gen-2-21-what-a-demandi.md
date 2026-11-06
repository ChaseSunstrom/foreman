---
id: T-2590
type: FIX
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T08:23:32Z
updated: 2026-11-02T08:25:39Z
trigger: genesis-review
trigger_key: c58bee42ba55713d
---
# FIX: cross-cutting review gen-2 #21 (what a demanding user would complain about first):…
## Raw request
> FIX: cross-cutting review gen-2 #21 (what a demanding user would complain about first): A user handing the harness a long task gets six confident false completions; no entry in the 67-line CHANGELOG addresses it. [l002 (foreman, model default): 6 scenarios; true done 0/6, checks 4/20, false done 6]
> genesis-review 2:21
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
- 2026-11-02T08:23:32Z created
- 2026-11-02T08:25:39Z dropped: review.md marks it dismissed: the same finding as #1 (long-tier false dones), handled as a gap there
## Follow-ups captured
