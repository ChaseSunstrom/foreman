---
id: T-3005
type: FEATURE
tier: L
status: blocked
priority: normal
scope: []
depends_on: [T-3006, T-3007, T-3008]
source: user
created: 2026-11-04T19:24:49Z
updated: 2026-11-05T04:44:09Z
---
# A model-agnostic reasoning layer for Smith, so any model reasons better without…
## Raw request
> A model-agnostic reasoning layer for Smith, so any model reasons better without overthinking: a compact structured thought state carried between turns (goal, facts, hypothesis, next check, confidence) instead of prose thinking; native thinking off and an adaptive budget per step (none, brief, deliberate when confidence is low or a check failed); hypotheses turned into checks before commits; a cheap vote only on low-confidence steps; measured on Louhi held-out against native thinking on and off by fix rate and tokens per fix, adopted per model only where it beats both. User: 'a generic like neuralese like structure that allows reasoning on any model, but genuinely better and really really good, almost like yours, and not over doing it like qwen, and can work on any model'
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
- 2026-11-04T19:24:49Z created
- 2026-11-04T19:25:24Z set depends_on=['T-3006']
- 2026-11-04T19:26:32Z set depends_on=['T-3006', 'T-3007', 'T-3008']
- 2026-11-05T04:44:09Z blocked: umbrella: part 1 T-3006 done; parts T-3010 (verifier search) and T-3007 (hidden-state probe) planned
## Follow-ups captured
