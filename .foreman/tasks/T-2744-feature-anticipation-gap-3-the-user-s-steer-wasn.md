---
id: T-2744
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: [T-2742]
source: genesis-anticipation
created: 2026-11-03T00:56:58Z
updated: 2026-11-03T04:50:55Z
trigger: genesis-anticipation
trigger_key: f50b263f21a0f184
inferred_deps: [T-2745]
inferred_why: T-2745: guard must recognise Sampo before sampo is honoured
group: Sampo rename and its steps
---
# FEATURE: anticipation gap (#3): the user's steer wasn't among gen-4's sealed…
## Raw request
> FEATURE: anticipation gap (#3): the user's steer wasn't among gen-4's sealed predictions: The rename's guard step comes first: sampo, the new verbs and SAMPO_* are honoured only once the guard (Ward) recognises them; until the user's yes on that protected-core change, sampo refuses inside agent sessions user steer: read SAMPO.md (protected core queued for the user; nothing a user has ma… (nearest: take M-02 past its kill test and build its slice on one of Foreman's own modules, overlap 0.0)
> genesis-anticipation 4:dca9b310bd
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
- 2026-11-03T00:56:58Z created
- 2026-11-03T01:00:41Z set depends_on=['T-2742']
- 2026-11-03T04:50:55Z dropped: covered: the guard-first order is T-2742/T-2745; the miss stays scored in gen-4/prediction-score.jsonl
## Follow-ups captured
