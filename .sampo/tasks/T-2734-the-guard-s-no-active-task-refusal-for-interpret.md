---
id: T-2734
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-03T00:20:06Z
updated: 2026-11-03T00:32:04Z
---
# The guard's no-active-task refusal for interpreter writes (fmguard.py:292) appends a…
## Raw request
> the guard's no-active-task refusal for interpreter writes (fmguard.py:292) appends a hint about trimming imports (fmguard.py:240); lead it with 'start a task first (fm task new … --focus)'
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
- 2026-11-03T00:20:06Z created
- 2026-11-03T00:32:04Z dropped: premise already met: the brief refusal leads with 'no active task … One command starts a small task: fm task new … --focus' (fmguard.py:292); the trailing hint (literal paths, builtin open) is the fix for the two hits, which passed the scratch path as $S, a path the guard can't resolve, so it read it as a project file
## Follow-ups captured
