---
id: T-2564
type: FEATURE
tier: M
status: blocked
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-02T07:20:39Z
updated: 2026-11-02T07:30:39Z
trigger: self
---
# Missing tool actionlint: find it (fm plugins find actionlint) or build it (script + test)
## Raw request
> Missing tool actionlint: find it (fm plugins find actionlint) or build it (script + test)
> capability-miss: actionlint
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
- 2026-11-02T07:20:39Z created
- 2026-11-02T07:30:39Z blocked: needs the user: actionlint is in no known marketplace (fm plugins find actionlint), and fm prove --infra by design installs and downloads nothing (fminfra docstring). Installing the binary (the distro package or go install) is the user's call; until then fm prove --infra leaves workflow files unproven and CI's own run plus test_ci_matrix prove .github/workflows/test.yml. Building a clone of actionlint is out of proportion to one workflow file.
## Follow-ups captured
