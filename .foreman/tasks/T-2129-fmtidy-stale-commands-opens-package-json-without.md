---
id: T-2129
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T09:12:31Z
updated: 2026-10-30T09:12:44Z
---
# fmtidy.stale_commands` opens `package.json` without `encoding=` and calls `.get` on an…
## Raw request
> fmtidy.stale_commands` opens `package.json` without `encoding=` and calls `.get` on an unchecked type. It is a pre-existing crash for any `fm docs` scan
> (noticed by an agent; research T-2121-review)
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
- 2026-10-30T09:12:31Z created
- 2026-10-30T09:12:44Z dropped: fixed inside T-2121: stale_commands now reads package.json utf-8, skips links, catches odd JSON types (FindHostile covers it)
## Follow-ups captured
