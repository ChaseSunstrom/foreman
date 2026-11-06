---
id: T-0586
type: SECURITY
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T15:02:03Z
updated: 2026-10-09T15:09:19Z
---
# SECURITY!: guard never reads a heredoc or here-string fed to a shell: bash <<'EOF' rm -rf
## Raw request
> SECURITY!: guard never reads a heredoc or here-string fed to a shell: bash <<'EOF' rm -rf ~ EOF runs unblocked (also sh -s, bash -, and check echo … | bash)
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
- 2026-10-09T15:02:03Z created
- 2026-10-09T15:09:19Z dropped: superseded by the planned task with the same scope
## Follow-ups captured
