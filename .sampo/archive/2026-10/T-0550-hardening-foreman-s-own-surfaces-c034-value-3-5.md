---
id: T-0550
type: SECURITY
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:18Z
updated: 2026-10-09T14:30:41Z
---
# Hardening Foreman's own surfaces (C034, value 3/5, effort M, risk med)
## Raw request
> SECURITY: Hardening Foreman's own surfaces (C034, value 3/5, effort M, risk med)
>   first version: First version: one sanitizer for rendered strings (strip ESC/OSC) applied to statusline and task output, plus a fuzz test of the approval-phrase parser in fmcore. Skip desktop IPC lockdown here.
>   what it is: Neutralise control sequences, audit symlinks and permissions, lock down the desktop IPC, fuzz the approval parser and keep an executable threat model.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
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
- 2026-10-09T14:30:18Z created
- 2026-10-09T14:30:41Z dropped: duplicate: the intake block ran twice by mistake; the first batch (T-0433..T-0502) carries these
## Follow-ups captured
