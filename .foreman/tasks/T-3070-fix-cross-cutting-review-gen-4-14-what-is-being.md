---
id: T-3070
type: FIX
tier: L
status: dropped
priority: low
scope: []
depends_on: []
source: genesis-review
created: 2026-11-05T00:31:14Z
updated: 2026-11-05T04:42:22Z
trigger: genesis-review
trigger_key: 131aa1554784a173
---
# FIX: cross-cutting review gen-4 #14 (what is being measured wrong): Live hook p95 is 315…
## Raw request
> FIX: cross-cutting review gen-4 #14 (what is being measured wrong): Live hook p95 is 315 ms over 11,974 runs while the lean gate reads ~36 ms by excluding runs above LOAD_BAR and holding only rises seen in two of three interleaved pairs; the SLO now measures the quiet machine, not the one users have. [p95 315 ms]
> genesis-review 4:14
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
- 2026-11-05T00:31:14Z created
- 2026-11-05T04:42:22Z dropped: covered by T-2933 (the hook SLO judges runs under 0.5 load per CPU: measured p95 103-121 ms there, 174-521 ms above) and T-3131 (the gate judges median CPU in every pair)
## Follow-ups captured
