---
id: T-3493
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T18:45:21Z
updated: 2026-11-06T18:45:21Z
steer_method_rate: 0.218
---
# Sampo must not use a risk budget for this project: disable the risk-budget setting in…
## Raw request
> you don;'t need a risk budget, so disable it for this project
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Sampo must not use a risk budget for this project: disable the risk-budget setting in this project's Sampo configuration (project-scoped only, leaving user-level and other projects' settings unchanged).
- Remove or bypass every place the risk budget acts in this project, including planning, gating, scoring, prompts, reports, and status displays, so nothing allocates, tracks, or reports against one.
- Do not let work be blocked, throttled, downgraded, or asked for confirmation solely because a risk budget would be exceeded or exhausted.
- Keep the setting off persistently across sessions, restarts, and config reloads, and do not re-enable it unless the user asks.
- Preserve the user's other safeguards: confirmation before outward-facing, destructive, or irreversible actions, and any explicit grants or limits (e.g., the spending cap), which stay in force; removing the risk budget is not a grant for those.
- Verify the change by checking the project config shows the risk budget disabled and that a representative plan or run proceeds without any risk-budget step or output.
- Report what was changed and where, and note any places the risk budget could not be removed.
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
- 2026-11-06T18:45:21Z created
## Follow-ups captured
