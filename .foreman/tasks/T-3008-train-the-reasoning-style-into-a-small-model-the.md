---
id: T-3008
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T19:26:32Z
updated: 2026-11-04T19:26:32Z
inferred_deps: [T-2971]
inferred_why: T-2971: named in its request
---
# Train the reasoning style into a small model: the 27B solves exam scenarios with the…
## Raw request
> Train the reasoning style into a small model: the 27B solves exam scenarios with the --reason state format, only test-passing runs are kept with the shortest correct trace per scenario preferred (concise-reasoning training against overthinking), and a 4B is LoRA-tuned on them through T-2971's pipeline; judged on held-out scenarios against its base with native thinking on and off by fix rate and tokens per fix (T-3005)
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
- 2026-11-04T19:26:32Z created
## Follow-ups captured
