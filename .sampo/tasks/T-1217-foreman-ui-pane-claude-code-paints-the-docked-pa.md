---
id: T-1217
type: FIX
tier: S
status: blocked
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T15:23:33Z
updated: 2026-10-20T17:21:09Z
---
# Foreman-ui pane: Claude Code paints the docked pane's background #262626 (48;2;38;38;38, 4
## Raw request
> foreman-ui pane: Claude Code paints the docked pane's background #262626 (48;2;38;38;38, 43,894 cells in the 1.2.35 recording) while the mod's Raster charts use the terminal's default background, so the pane reads as gray and dark patches; make the chart cells use the pane's background (or none of their own) so the pane is one surface
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
- 2026-10-16T15:23:33Z created
- 2026-10-20T17:21:09Z blocked: needs the foreman-ui mod update the user must approve (installed 0.7.0, repo 0.18.2); the pane background can't be checked or changed on the old mod
## Follow-ups captured
