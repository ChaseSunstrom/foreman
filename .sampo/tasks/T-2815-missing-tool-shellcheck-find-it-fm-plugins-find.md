---
id: T-2815
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-03T16:25:35Z
updated: 2026-11-03T21:08:53Z
trigger: self
---
# Missing tool shellcheck: find it (fm plugins find shellcheck) or build it (script + test)
## Raw request
> Missing tool shellcheck: find it (fm plugins find shellcheck) or build it (script + test)
> capability-miss: shellcheck
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
- 2026-11-03T16:25:35Z created
- 2026-11-03T21:08:53Z dropped: the user's standing rule is no software installs, and Sampo installs nothing; install.sh's syntax is checked with bash -n at each close that touches it; listed in the final report as a tool the user may add
## Follow-ups captured
