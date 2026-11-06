---
id: T-0480
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:30:17Z
updated: 2026-10-09T16:27:38Z
done_in: T-0672
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
- 2026-10-09T14:30:17Z created
- 2026-10-09T15:40:13Z batched into T-0672
- 2026-10-09T16:27:38Z done in T-0672 (batch)
## Follow-ups captured
