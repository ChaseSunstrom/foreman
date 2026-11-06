---
id: T-0007
type: CLEAN
tier: S
status: done
priority: normal
scope: [install.sh]
depends_on: []
source: discovered
created: 2026-09-26T05:48:08Z
updated: 2026-09-26T06:03:15Z
---
# Update install.sh final hint after the build
## Raw request
> install.sh's final hint still says 'run /foreman:build'; after the build it should point at /foreman:status or intake
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Point install.sh one-liners and final hint at the built system
## Resume here
## Verification evidence
- (step 1) `bash -n install.sh; ./install.sh --help; eval final printf line` → syntax OK; help shows plain one-liners; hint names /foreman:status and MASTER.md (2026-09-26T06:03:15Z)
## Log
- 2026-09-26T05:48:08Z created
- 2026-09-26T05:59:50Z planned from capture
- 2026-09-26T06:03:12Z focused
- 2026-09-26T06:03:15Z done
## Follow-ups captured
