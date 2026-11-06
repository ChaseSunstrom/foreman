---
id: T-1481
type: SECURITY
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T17:05:27Z
updated: 2026-10-22T17:15:16Z
---
# Guard gap: BASH_ENV=file (and ENV=, SHELLOPTS=, PROMPT_COMMAND=) prefixes that run code wh
## Raw request
> Guard gap: BASH_ENV=file (and ENV=, SHELLOPTS=, PROMPT_COMMAND=) prefixes that run code when a shell starts are unclassified even in plain form: BASH_ENV=payload.sh bash -c true is allowed (9 variants in guard_gaps.jsonl). Classify a startup-code env prefix on a shell command like the code it loads
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
- 2026-10-22T17:05:27Z created
- 2026-10-22T17:09:44Z from T-1263's corpus: the real BASH_ENV variants are env -S, a function, eval and a here-string (4 in guard_gaps.jsonl); a quoted or expanded NAME= word is a command name in bash, not an assignment, so those aren't evasions
- 2026-10-22T17:15:16Z dropped: premise false: with payload.sh present every BASH_ENV variant (plain, env -S, function, eval, here-string) is refused (rm-outside); the guard reads what BASH_ENV loads (_CODE_VARS). The corpus listed them only because it runs from the home folder, where payload.sh doesn't exist; T-1480 takes them out of the generator
## Follow-ups captured
