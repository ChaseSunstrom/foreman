---
id: T-3077
type: FIX
tier: L
status: dropped
priority: low
scope: []
depends_on: []
source: genesis-review
created: 2026-11-05T00:31:17Z
updated: 2026-11-05T04:43:25Z
trigger: genesis-review
trigger_key: 02bf2aaba1db8f73
---
# FIX: cross-cutting review gen-4 #21 (what a demanding user would complain about first):…
## Raw request
> FIX: cross-cutting review gen-4 #21 (what a demanding user would complain about first): The guard blocked its own builders 18 times for running python against Sampo's modules, the top-firing rule, and T-2261 about that very rule has sat open in the self-inbox all generation. [11× core:interpreter-code-driving-foreman]
> genesis-review 4:21
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
- 2026-11-05T00:31:17Z created
- 2026-11-05T04:43:25Z dropped: duplicate of T-2261 (the interpreter rule refusing read-only python; its cause is traced to fmguard.py:1804/1810 and the fix written there); it touches the guard, so it is listed for the user's review in the final report
## Follow-ups captured
