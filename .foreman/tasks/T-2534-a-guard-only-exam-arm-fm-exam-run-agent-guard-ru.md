---
id: T-2534
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T04:14:14Z
updated: 2026-11-02T04:18:06Z
group: lean ratchet and exam subtraction
---
# A guard-only exam arm: fm exam run --agent guard runs a claude session with Foreman…
## Raw request
> FEATURE: a guard-only exam arm: fm exam run --agent guard runs a claude session with Foreman loaded and FOREMAN_QUIET=1 (only the guard), graded like foreman and plain on the same scenarios, so the end-of-run exam prices the injected context
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
- 2026-11-02T04:14:14Z created
- 2026-11-02T04:18:06Z dropped: built: the exam's plain arm is already Claude with only the guard (FOREMAN_QUIET=1 plus fmbench._bare_guard settings: fmexam.py:2893, fmbench.py:424, T-0963); foreman-minus-plain is the guard-only delta
## Follow-ups captured
