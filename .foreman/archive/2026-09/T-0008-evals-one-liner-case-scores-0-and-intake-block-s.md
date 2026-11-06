---
id: T-0008
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-09-26T05:54:08Z
updated: 2026-09-26T13:42:25Z
---
# Evals: one-liner case scores 0 and intake-block's order grader fails even with rules embed
## Raw request
> Evals: one-liner case scores 0 and intake-block's order grader fails even with rules embedded — evidence: eval-live2.json (0.7 overall; guard x2 and mid-task-capture 1.0). Likely the intake skill isn't invoked for plain one-liners in a fresh sandbox, or the canonical order isn't restated in the reply; tune intake skill description / reply format and re-run the suite.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Verification evidence
## Log
- 2026-09-26T05:54:08Z created
- 2026-09-26T13:42:25Z dropped: merged into T-0009: blocks T-0009's eval criterion; eval cases get code scaffolds and fair graders, the prompt hook names classification for untagged requests
## Follow-ups captured
