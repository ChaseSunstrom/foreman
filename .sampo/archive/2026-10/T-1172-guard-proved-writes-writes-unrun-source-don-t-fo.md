---
id: T-1172
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-16T10:48:15Z
updated: 2026-10-16T11:38:47Z
---
# Guard: _proved_writes / _writes_unrun_source don't follow a variable assigned a literal pa
## Raw request
> Guard: _proved_writes / _writes_unrun_source don't follow a variable assigned a literal path (p='CHANGELOG.md'; open(p,'w')), so 19+7 interpreter writes are refused as unknown or tree-wide; accept a single literal assignment, and name the unresolved variable in the block detail
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
- 2026-10-16T10:48:15Z created
- 2026-10-16T11:38:47Z dropped: premise false on replay: 33 mined refusals (4 days, all sessions) replayed with fm guard try: S=/literal; … $S already resolves (_track_vars); the rest are real protections (git reset/stash/merge/checkout on Foreman's tree, .env, installed_plugins.json) or an assignment after 'cd … &&', which can be unset and already carries the 'set its variable once before any branch' hint
## Follow-ups captured
