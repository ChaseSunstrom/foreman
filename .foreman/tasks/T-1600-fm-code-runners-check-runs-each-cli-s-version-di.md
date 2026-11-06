---
id: T-1600
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-22T20:19:34Z
updated: 2026-10-22T20:37:23Z
---
# Fm code runners --check runs each CLI's --version directly, not through worker_argv, so it
## Raw request
> fm code runners --check runs each CLI's --version directly, not through worker_argv, so it skips code.toml's dangerous-flag check that the app's runner test applies; route it through worker_argv
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
- 2026-10-22T20:19:34Z created
- 2026-10-22T20:37:23Z dropped: no risk: runners --check runs only the installed binary with --version, never the work template, so the dangerous-flag lint (which all_runners already applies to templates) has nothing to check; the app's runner test goes through worker_argv because it builds from the template
## Follow-ups captured
