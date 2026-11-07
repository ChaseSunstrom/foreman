---
id: T-3205
type: SECURITY
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T13:50:36Z
updated: 2026-11-05T13:50:36Z
---
# Guard: _proved_writes trusts exec(open(path).read()) inside a heredoc fed to python, so…
## Raw request
> guard: _proved_writes trusts exec(open(path).read()) inside a heredoc fed to python, so code read from a scratch file runs unexamined and can write anywhere (seen in T-2261's replay: a fed heredoc exec'ing a file and writing meta.json was allowed)
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
- 2026-11-05T13:50:36Z created
## Follow-ups captured
