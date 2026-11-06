---
id: T-0080
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-09-30T11:28:09Z
updated: 2026-10-02T19:01:08Z
done_in: T-0088
---
# fm task set --section resolves template headings and keeps criterion ticks
## Raw request
> fm task set --section 'Approach' creates a new section instead of filling 'Approach (options → choice → why)', and scope='["a","b"]' is stored as one string; accept the short name and JSON lists — evidence: T-0059/T-0060 focus refused, scope malformed
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] --section Approach fills 'Approach (options → choice → why)' and rewriting Acceptance criteria keeps ticks of unchanged criteria — verify with `python3 -m unittest discover -s plugin/tests -p test_round_i.py -q`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red tests for alias + tick keep  <- CURRENT
2. [ ] resolve heading prefix in set_section path; keep [x] for identical criteria
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-09-30T11:28:09Z created
- 2026-10-02T18:34:51Z planned from capture
- 2026-10-02T19:01:08Z done in T-0088
## Follow-ups captured
