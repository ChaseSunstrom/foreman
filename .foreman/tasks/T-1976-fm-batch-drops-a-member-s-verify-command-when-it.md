---
id: T-1976
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T11:46:57Z
updated: 2026-10-29T12:25:19Z
done_in: T-1980
---
# Fm batch drops a member's verify command when its criteria come from the DONE-WHEN fallbac
## Raw request
> FIX: fm batch drops a member's verify command when its criteria come from the DONE-WHEN fallback: "x :: cmd" stays in the text with no verify, so fm focus on the batch is refused until each criterion is re-edited (T-1974 needed three fm task ac edits). _make_batch splits the fallback with rpartition(" :: ") as the other DONE-WHEN readers do (fmcli _make_batch).
> DONE-WHEN: a batch of intake tasks whose criteria live only in DONE-WHEN lines keeps their verify commands and focuses at once :: python3 plugin/tests/run.py test_batch
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
- 2026-10-29T11:46:57Z created
- 2026-10-29T12:10:05Z batched into T-1980
- 2026-10-29T12:25:19Z done in T-1980 (batch)
## Follow-ups captured
