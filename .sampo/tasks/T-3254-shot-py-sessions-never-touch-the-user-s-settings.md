---
id: T-3254
type: FIX
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T00:17:41Z
updated: 2026-11-06T00:17:41Z
inferred_deps: [T-3163]
inferred_why: T-3163: named in its request
---
# shot.py sessions never touch the user's settings: start uses its own settings file (a…
## Raw request
> shot.py sessions never touch the user's settings: start uses its own settings file (a /model typed in a shot rewrote ~/.claude/settings.json's model, T-3163) and turns the installed foreman-ui plugin off so --plugin-dir shows the worktree's mod, not main's
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
- 2026-11-06T00:17:41Z created
## Follow-ups captured
