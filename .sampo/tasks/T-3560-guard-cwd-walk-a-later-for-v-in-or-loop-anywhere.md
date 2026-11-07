---
id: T-3560
type: FIX
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T00:45:34Z
updated: 2026-11-07T00:45:34Z
---
# Guard cwd walk: a later 'for V in $(…)' (or `…`) loop anywhere on a line makes the guard…
## Raw request
> FIX: guard cwd walk: a later 'for V in $(…)' (or `…`) loop anywhere on a line makes the guard judge earlier commands from the session cwd, dropping a certain head cd: 'cd /existing/lane && git merge x; for f in $(true); do :; done' and 'cd /tmp && echo x > plugin/lib/fmguard.py; for f in $(true); do :; done' are refused core on the main checkout (sampo replay --cmd shows it; 'for f in a' or 'echo $(true)' don't). Caused the 18:40 T-3265 lane-merge refusal (T-3537 found it; its hint now says to run the cd && merge as its own command)
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
- 2026-11-07T00:45:34Z created
## Follow-ups captured
