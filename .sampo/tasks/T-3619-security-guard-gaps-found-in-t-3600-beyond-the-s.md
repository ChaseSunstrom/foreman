---
id: T-3619
type: SECURITY
tier: L
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T04:57:55Z
updated: 2026-11-07T04:57:55Z
---
# SECURITY: guard gaps found in T-3600 beyond the sampo verb: (1) an alias for a non-sampo…
## Raw request
> SECURITY: guard gaps found in T-3600 beyond the sampo verb: (1) an alias for a non-sampo command (alias r='rm -rf' then r ~ on the next line) passes: the guard doesn't read alias values as the commands they run; (2) watch runs its words as a shell command (watch 'rm -rf ~', watch sampo serve) and isn't read as a wrapper; (3) a sampo flag the shell fills in ($R with R=--run, or --ac/--verify) hides the command after it: sampo task evidence T-1 --step 1 $R 'rm -rf ~' passes; (4) an unquoted $( ) as a command word ($(echo rm) -rf ~) passes: the tokenizer splits it into $, the body and the rest. Each probed on the T-3600 lane guard
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
- 2026-11-07T04:57:55Z created
## Follow-ups captured
