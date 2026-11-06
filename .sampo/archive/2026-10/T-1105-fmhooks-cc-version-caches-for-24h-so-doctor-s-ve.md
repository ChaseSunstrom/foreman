---
id: T-1105
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T05:04:24Z
updated: 2026-10-16T07:03:20Z
---
# Fmhooks._cc_version` caches for 24h, so doctor's version-dependent checks lag a `claude up
## Raw request
> fmhooks._cc_version` caches for 24h, so doctor's version-dependent checks lag a `claude update` by up to a day. A small task could invalidate the cache on mtime or on `--version` mismatch
> (noticed by an agent; research T-1076-review)
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
- 2026-10-16T05:04:24Z created
- 2026-10-16T07:03:20Z dropped: done by T-1109: the version cache refreshes when the claude binary is newer
## Follow-ups captured
