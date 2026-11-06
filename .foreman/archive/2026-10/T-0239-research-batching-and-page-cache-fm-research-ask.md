---
id: T-0239
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T05:27:19Z
updated: 2026-10-04T07:46:18Z
done_in: T-0277
---
# Research batching and page cache — fm research ask --file runs a queue of questions in one
## Raw request
> FEATURE: research batching and page cache — fm research ask --file runs a queue of questions in one batch, and fetched pages are cached by URL and day so verification and repeat asks don't refetch
> CONTEXT: fmresearch.fetch/verify
> DONE-WHEN: a second verify of the same URL the same day reads the cache; a two-question file yields two notes
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
- 2026-10-04T05:27:19Z created
- 2026-10-04T05:27:29Z set tier=S
- 2026-10-04T07:35:44Z batched into T-0277
- 2026-10-04T07:46:18Z done in T-0277 (batch)
## Follow-ups captured
