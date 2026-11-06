---
id: T-1445
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T23:07:06Z
updated: 2026-10-22T05:49:38Z
group: installed foreman-ui plugin copies are stale
---
# This machine's installed_plugins.json points foreman-ui at a stale cache/foreman/foreman-u
## Raw request
> This machine's installed_plugins.json points foreman-ui at a stale cache/foreman/foreman-ui/0.7.0 (Oct 15) while 0.18.3 is released, and foreman at a stale 0.1.0 holding only commands/: find what Claude Code actually loads, make fm release (or fm doctor --fix) refresh the installed copies, and have doctor's version-skew check name a stale install (T-1441 builder)
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
- 2026-10-21T23:07:06Z created
- 2026-10-22T05:49:38Z dropped: premise false: claude plugin list shows foreman-ui 0.18.3 and foreman 1.2.50 'Read from' the checkout (directory marketplace loads in place); the cache/ entries in installed_plugins.json are unused records
## Follow-ups captured
