---
id: T-0374
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T00:10:21Z
updated: 2026-10-09T00:30:25Z
done_in: T-0370
---
# SECURITY: a write through a variable that is never set (echo x > $NOPE~/.claude/
## Raw request
> SECURITY: a write through a variable that is never set (echo x > $NOPE~/.claude/foreman/plugin/lib/fmguard.py, ${NOPE}/…/state/meta.json) is allowed: _target_cats returns nothing for names the command neither sets nor inherits (fmguard.py ~1408 'nothing in it says where they point'), but bash expands them to empty, so the target is the rest of the word — the guard file itself. Same for cp/tee/mv targets. rm already refuses unresolvable targets.
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
- 2026-10-09T00:10:21Z created
- 2026-10-09T00:30:25Z done in T-0370: fixed in T-0370's change to the same function: unknown and unset parts are tried empty, with tests and the real-bash differential
## Follow-ups captured
