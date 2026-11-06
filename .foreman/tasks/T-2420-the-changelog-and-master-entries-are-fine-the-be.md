---
id: T-2420
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T15:09:28Z
updated: 2026-11-02T00:40:45Z
---
# The CHANGELOG and MASTER entries are fine. The bench has no fixture filter, so any…
## Raw request
> the CHANGELOG and MASTER entries are fine. The bench has no fixture filter, so any caller that wants only a few hooks pays for all 15
> (noticed by an agent; research T-2359-review)
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
- 2026-10-31T15:09:28Z created
- 2026-11-02T00:40:45Z dropped: already built: bench_hooks.run_bench(runs, only=PREDICATE) filters fixtures by name (T-2359, 1f2bb1dc, 2026-10-31), and fmdoctor.hook_p95 times only the PreToolUse fixtures with it; the review note predates it
## Follow-ups captured
