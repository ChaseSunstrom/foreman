---
id: T-2660
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T20:13:16Z
updated: 2026-11-02T20:24:31Z
---
# Fmmandate (close-time estimates), fmwatch and fmloop read task_done and still print zero…
## Raw request
> fmmandate (close-time estimates), fmwatch and fmloop read task_done and still print zero rates silently when the class is missing; reuse fmoutcomes.dropped_class_lines
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
- 2026-11-02T20:13:16Z created
- 2026-11-02T20:24:31Z dropped: second-order: removing task_done lines breaks the ledger's hash chain, which fm verify-ledger and fm drill --restore report first; fm outcomes and fm digest already name a missing class (T-2648)
## Follow-ups captured
