---
id: T-2300
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T09:04:24Z
updated: 2026-10-31T09:26:07Z
---
# fmcore.global_events builds its event-file list inline and fmdoctor's T-2298 cache key…
## Raw request
> fmcore.global_events builds its event-file list inline and fmdoctor's T-2298 cache key repeats that list: share one global_event_files() so the cache key can't drift from what global_events reads
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
- 2026-10-31T09:04:24Z created
- 2026-10-31T09:05:02Z blocked: waits on T-2298 (the cache key it shares lives on T-2298's unmerged branch); folded into T-2298's review fixes, closed with it
- 2026-10-31T09:26:07Z dropped: done inside T-2298 (commit b6557ebb): fmcore.global_event_files shared by global_events and the doctor cache key
## Follow-ups captured
