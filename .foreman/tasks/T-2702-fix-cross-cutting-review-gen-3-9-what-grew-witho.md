---
id: T-2702
type: FIX
tier: L
status: captured
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T23:14:41Z
updated: 2026-11-06T03:53:53Z
trigger: genesis-review
trigger_key: b20aadabfb612457
---
# FIX: cross-cutting review gen-3 #9 (what grew without earning it): 449 lines of a run…
## Raw request
> FIX: cross-cutting review gen-3 #9 (what grew without earning it): 449 lines of a run the authors themselves label confounded ("sampling 'held' from closes whose window has ended picked only the oldest tasks") are committed beside the result; a discarded run is repo growth, not evidence. [bench/moonshot/m12-run1-confounded.json]
> genesis-review 3:9
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
- 2026-11-02T23:14:41Z created
- 2026-11-02T23:16:29Z batched into T-2719
- 2026-11-02T23:17:16Z blocked: needs the user: deleting a committed file in Foreman's tree (git rm bench/moonshot/m12-run1-confounded.json) is a core tree write the guard refuses without the user's yes; fm edit and Edit can't delete; the file stays, described as such in moonshot.md, until then (final report)
- 2026-11-02T23:17:49Z unbatched: T-2719 was dropped
- 2026-11-06T03:53:53Z unblocked
## Follow-ups captured
