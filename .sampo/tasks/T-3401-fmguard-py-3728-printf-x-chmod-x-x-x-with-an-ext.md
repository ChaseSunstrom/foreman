---
id: T-3401
type: SECURITY
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T07:50:27Z
updated: 2026-11-06T07:50:27Z
---
# fmguard.py:~3728: 'printf ... > x; chmod +x x; ./x' with an extensionless x is neither…
## Raw request
> SECURITY: fmguard.py:~3728: 'printf ... > x; chmod +x x; ./x' with an extensionless x is neither refused nor read (the write-then-run refusal covers only .sh-like suffixes); treat any file written in the same command line and then run by path as a script to read or refuse (T-3387 review)
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
- 2026-11-06T07:50:27Z created
## Follow-ups captured
