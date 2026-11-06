---
id: T-0997
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-16T00:01:01Z
updated: 2026-10-16T00:01:22Z
---
# Catch it earlier: T-0705's fixture had one Python test and steps that were all code steps;
## Raw request
> T-0994 (Ambient runs close only the step whose own verify ran; unmappable files get no ambient evidence (T-0994)) wasn't caught before it shipped: T-0705's fixture had one Python test and steps that were all code steps; ambient was off in every real project until today, and the first real use (a TypeScript mod) showed both faults
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
- 2026-10-16T00:01:01Z created
- 2026-10-16T00:01:22Z dropped: covered: T-0994's test_a_test_the_runner_cant_run_is_left_out puts a .tsx test beside the Python fixture
## Follow-ups captured
