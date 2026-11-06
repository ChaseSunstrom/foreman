---
id: T-2710
type: FIX
tier: L
status: dropped
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T23:14:45Z
updated: 2026-11-02T23:15:44Z
trigger: genesis-review
trigger_key: 17ade15718ab6fd6
---
# FIX: cross-cutting review gen-3 #17 (what is presented ahead of its proof): the…
## Raw request
> FIX: cross-cutting review gen-3 #17 (what is presented ahead of its proof): the session-start guess is documented with a worked example before the feature's own floor of "at least 20 scored rows" was shown met; no exam or outcome line reports a scored next-request prediction. [hit 52% vs 39%]
> genesis-review 3:17
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
- 2026-11-02T23:14:45Z created
- 2026-11-02T23:15:44Z dropped: premise false: the floor was met when the example was written: prediction_kinds read next-request n=23 scored (MUTE_MIN is 20), 52% vs 39%, recorded in T-2681's audit
## Follow-ups captured
