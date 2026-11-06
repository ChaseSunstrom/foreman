---
id: T-3079
type: FIX
tier: L
status: dropped
priority: low
scope: []
depends_on: []
source: genesis-review
created: 2026-11-05T00:31:18Z
updated: 2026-11-05T04:43:23Z
trigger: genesis-review
trigger_key: a8765711fefdd5c8
---
# FIX: cross-cutting review gen-4 #23 (what a demanding user would complain about first):…
## Raw request
> FIX: cross-cutting review gen-4 #23 (what a demanding user would complain about first): The site was re-skinned six times (T-2753, T-2759, T-2851, T-2852, T-2957, T-2964) while the user's own asks for feature pages with charts (T-1792, T-2082) stay open. [T-2082 Can you add pages for ALL]
> genesis-review 4:23
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
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
- 2026-11-05T00:31:18Z created
- 2026-11-05T04:43:23Z dropped: its examples are served: the feature pages with charts the user asked for exist (T-1220, 29 pages today; T-2082 and T-1792 were resurfaced duplicates left waiting on a needless confirm, now closed); the lesson goes to T-3127: a stalled-ask check must first test whether the ask is already built
## Follow-ups captured
