---
id: T-3342
type: CLEAN
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T05:09:41Z
updated: 2026-11-06T05:09:41Z
---
# The repo mirror is still named .foreman/ (sync.DIR, sync.py:23) and ~36 code sites name…
## Raw request
> The repo mirror is still named .foreman/ (sync.DIR, sync.py:23) and ~36 code sites name it (core mirror_ignored and audit pathspecs, hooks, playbooks, smith, stack, change, fixes); the product is Sampo. Rename the mirror to .sampo/ with one constant every caller reads (core.MIRROR); a repo that already has .foreman/ keeps working: sync reads it, and moves it to .sampo/ with git mv on the next export (one commit, logged), never two mirrors at once; the guard's state-direct rule covers both names. Also sweep every other user-visible 'foreman' name the rename left behind (FOREMAN_* env vars shown in docs, refs/foreman/*, the foreman/build branch name in messages, .foreman-state.json) with the rename scan, keeping old names as read-only aliases. User: 'How come the state is still called .foreman?'
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
- 2026-11-06T05:09:41Z created
## Follow-ups captured
