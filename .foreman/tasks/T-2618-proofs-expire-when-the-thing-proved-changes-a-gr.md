---
id: T-2618
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-02T14:30:06Z
updated: 2026-11-02T14:31:30Z
---
# Proofs expire when the thing proved changes: a green proof run on a done task is marked…
## Raw request
> proofs expire when the thing proved changes: a green proof run on a done task is marked stale once a later commit changes the files it proved, and the rollup lists it again (gen-3 #6 brainstorm; kill test: find a stale proof in the last 10 tasks)
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
- 2026-11-02T14:30:06Z created
- 2026-11-02T14:30:07Z deferred: no stale proof is on record in the last 10 tasks; its kill test needs one (revisit 2026-12-01)
- 2026-11-02T14:31:30Z dropped: carried in genesis not-yet.md (Proofs expire when the thing proved changes); its kill test ran and found no stale proof
## Follow-ups captured
