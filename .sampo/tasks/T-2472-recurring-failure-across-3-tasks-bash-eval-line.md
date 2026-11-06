---
id: T-2472
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T15:06:51Z
updated: 2026-11-01T17:51:22Z
trigger: recurring-failure
trigger_key: 53b17bddfa3db09d
---
# Recurring failure across 3 tasks: bash: eval: line 0: unexpected eof while looking for…
## Raw request
> Recurring failure across 3 tasks: bash: eval: line 0: unexpected eof while looking for matching ``'
> recurring-failure 64a7b0529315
> (hit in T-0071, T-2104, T-2471: find the cause and fix it once; fm recall and fm whyred help)
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
- 2026-11-01T15:06:51Z created
- 2026-11-01T17:51:22Z dropped: not a Foreman defect: the 'unexpected EOF looking for matching backtick' runs were the session's own shell quoting (a literal triple backtick inside a double-quoted command); fm's known-fix hint already names the cause when it recurs
## Follow-ups captured
