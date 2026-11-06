---
id: T-2465
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-01T09:27:07Z
updated: 2026-11-01T17:56:30Z
done_in: T-2493
---
# fm decide refuses a row that cites a user steer without --check, naming --check and --revisited
## Raw request
> FIX: fm decide accepts a --cites 'user steer …' row with no --check, and fm doctor's steer-checks line fails only later (hit twice this session: 2026-10-31 and T-2462's row); refuse it at record time, naming --check
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm decide --cites 'user steer …' with no --check exits non-zero and names --check; with --check it records — verify with `python3 plugin/tests/run.py test_judgment`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red test, then the refusal in fm decide  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-01T09:27:07Z created
- 2026-11-01T16:56:28Z planned from capture
- 2026-11-01T17:47:17Z batched into T-2493
- 2026-11-01T17:56:30Z done in T-2493 (batch)
## Follow-ups captured
