---
id: T-2523
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: [T-2522]
source: discovered
created: 2026-11-02T01:40:10Z
updated: 2026-11-02T01:56:12Z
---
# Exam of the exam drops a child-authored proof or beyond item whose claim the base can't…
## Raw request
> Exam of the exam drops a child-authored proof or beyond item whose claim the base can't check (an unprovable claim kept would score every agent wrong) (from T-2442)
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
- 2026-11-02T01:40:10Z created
- 2026-11-02T01:45:51Z set depends_on=['T-2522']
- 2026-11-02T01:45:51Z waits on T-2522: there are no child-authored proof or beyond items to drop until T-2522 builds the authoring
- 2026-11-02T01:56:12Z dropped: covered by T-2453's design: the proof and beyond authors only reword the request (PARAPHRASE), the hidden check stays ours, and REWORD_MUST rejects a reword that drops what the check needs (fmexam ~1488 raises), so no child-written claim the base can't check reaches the exam
## Follow-ups captured
