---
id: T-1465
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T14:58:34Z
updated: 2026-10-22T14:59:22Z
---
# Fmplugins._ROOT_PATH` also truncates paths containing `+`, `@` or spaces for every `script
## Raw request
> fmplugins._ROOT_PATH` also truncates paths containing `+`, `@` or spaces for every `scripts` entry, not only in skipped folders
> (noticed by an agent; research T-1459-review)
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
- 2026-10-22T14:58:34Z created
- 2026-10-22T14:59:22Z dropped: covered by T-1459 (its builder is widening _ROOT_PATH to @ + ~ for every scripts entry); a space inside a hooked path is quoted shell text, out of scope
## Follow-ups captured
