---
id: T-2944
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/tests/test_backlog.py, CHANGELOG.md]
depends_on: [T-2779]
source: discovered
created: 2026-11-04T08:52:47Z
updated: 2026-11-06T03:53:18Z
group: timeouts under parallel load
---
# A re-verify that times out is reported as inconclusive, not filed as a failed check
## Raw request
> Re-verify failed for T-2779 (b35fa5): python3 plugin/tests/run.py (now ✗ exit 124 (timed out after 120s) · timed out after 120s; queued by 3d1776cae… FEATURE: fm lane merge names changed text still found elsewhere, readers first, so a producer/reader split reaches the …)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo sentinel files a 'Re-verify failed' FIX only for a check that exits non-zero within its timeout; a check that times out (exit 124) is printed as timed out (inconclusive) with its cap and filed as nothing — verify with `python3 plugin/tests/run.py test_backlog`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test in test_backlog's Reverify: a queued check that times out files no FIX and prints timed out  <- CURRENT
2. [ ] skip exit 124 in the queued re-verify filing (cmd_sentinel), say it in the output
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T08:52:47Z created
- 2026-11-05T02:39:20Z planned from capture
- 2026-11-05T02:39:21Z set approved=True
- 2026-11-05T02:39:21Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_backlog.py', 'CHANGELOG.md']
- 2026-11-05T02:39:27Z blocked: after T-3087's lane merges (it also changes cli.py; an uncommitted cli.py would stop that merge)
- 2026-11-06T03:53:18Z unblocked
## Follow-ups captured
