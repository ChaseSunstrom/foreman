---
id: T-1142
type: PERFORMANCE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-16T09:55:34Z
updated: 2026-10-16T10:07:23Z
---
# Hook import cost: about 217 regex compiles (≈80 ms profiled) on every hook process: compil
## Raw request
> Hook import cost: about 217 regex compiles (≈80 ms profiled) on every hook process: compile the rarely used guard and hook patterns lazily (first use), keeping the hot ones eager; measure with the T-1140 A/B script
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
- 2026-10-16T09:55:34Z created
- 2026-10-16T10:07:23Z dropped: premise false: python3 -X importtime puts the whole fmhooks import at 22 ms (fmguard 5 ms, fmcore 6 ms self, regex compiles included); the 80 ms was cProfile's own overhead. The hook is 72 ms median after T-1140, of which import is a third; lazy regexes would save a few ms
## Follow-ups captured
