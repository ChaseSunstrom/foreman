---
id: T-3337
type: FIX
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T05:02:35Z
updated: 2026-11-06T05:02:35Z
inferred_deps: [T-3248, T-3285, T-3287]
inferred_why: T-3248: named in its request; T-3285: named in its request; T-3287: named in its request
---
# Lane stall/recover hints misfire on resumed builders: after SendMessage resumes a…
## Raw request
> Lane stall/recover hints misfire on resumed builders: after SendMessage resumes a finished builder with review fixes, the Stop hook calls its lane 'stalled 15+ min' or 'process ended with work uncommitted' and says TaskStop + lane recover, while the agent is alive running a 20-min test under load (T-3248, T-3285, T-3287 tonight). A resume (bg_start agent=True event, T-2848) should reset the lane's stall clock, and a lane whose agent is in the session's running set is never stalled
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
- 2026-11-06T05:02:35Z created
## Follow-ups captured
