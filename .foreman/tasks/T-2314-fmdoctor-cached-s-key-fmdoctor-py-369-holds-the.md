---
id: T-2314
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T10:45:49Z
updated: 2026-10-31T11:39:27Z
done_in: T-2316
---
# fmdoctor._cached's key (fmdoctor.py ~369) holds the inputs' stats and the day but not…
## Raw request
> fmdoctor._cached's key (fmdoctor.py ~369) holds the inputs' stats and the day but not the check's own code, so an edited check returns its stale cached result until tomorrow (someone tried rm state/doctor-cache.json): add fmdoctor's file mtime_ns to the key; test a patched stamp recomputes
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
- 2026-10-31T10:45:49Z created
- 2026-10-31T10:46:05Z batched into T-2316
- 2026-10-31T10:57:26Z blocked: member of batch T-2316 (in a builder lane); closes done with it
- 2026-10-31T11:39:27Z done in T-2316 (batch)
## Follow-ups captured
