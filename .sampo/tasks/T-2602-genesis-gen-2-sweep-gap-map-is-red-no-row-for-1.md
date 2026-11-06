---
id: T-2602
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T10:54:32Z
updated: 2026-11-02T10:57:02Z
genesis_sweep: 2:gap map
---
# Genesis gen-2 sweep: gap map is red — no row for #1 Initiative; no row for #2 Exhaustive thinking; no row for #3 Antici…
## Raw request
> fm genesis sweep 2: ✗ gap map: no row for #1 Initiative; no row for #2 Exhaustive thinking; no row for #3 Anticipation; no row for #4 Goal to finish; no row for #5 Getting the tools it lacks; no row for #6 Verifying anything; no row for #7 Self-repair and self-improvement; no row for #8 Calibrated judgment; … 5 more
> Done when the rerun's gap map line is ✓.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the sweep's gap map line is ✓ — verify with `fm genesis sweep 2`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] fix what the sweep's gap map line names, then rerun fm genesis sweep 2  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-02T10:54:32Z created
- 2026-11-02T10:57:02Z dropped: done in the tower: gen-2/gap-map.md now carries the 13-row Area/Tier/Evidence/Missing table the sweep reads (filed after its cold read)
## Follow-ups captured
## Regression test
The sweep's gap map row: every fm genesis sweep reruns it, so this can't come back unseen.
