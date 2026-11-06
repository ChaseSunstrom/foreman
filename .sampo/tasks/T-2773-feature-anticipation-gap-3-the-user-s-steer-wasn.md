---
id: T-2773
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: genesis-anticipation
created: 2026-11-03T04:47:12Z
updated: 2026-11-03T04:50:56Z
trigger: genesis-anticipation
trigger_key: 001f284c6a753785
---
# FEATURE: anticipation gap (#3): the user's steer wasn't among gen-4's sealed…
## Raw request
> FEATURE: anticipation gap (#3): the user's steer wasn't among gen-4's sealed predictions: Standing rule: when a task finishes, keep working the rest of the queue (open tasks, lanes, inbox) without waiting for a prompt; stop only when nothing is left or only the user can unblock it user steer 2026-11-03: make sure to keep going with everything else when done (nearest: keep Foreman lean: trim what each session injects and the 2.4 GB of exam state, overlap 0.12)
> genesis-anticipation 4:466ff2bc3a
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
- 2026-11-03T04:47:12Z created
- 2026-11-03T04:50:56Z dropped: covered: T-2771 recorded the keep-going rule; the miss stays scored in gen-4/prediction-score.jsonl
## Follow-ups captured
