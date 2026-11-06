---
id: T-3153
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T05:56:15Z
updated: 2026-11-05T05:59:18Z
---
# Bulk card writing ran on Haiku (661 calls at 23:58, 87 at 03:01) instead of local…
## Raw request
> Bulk card writing ran on Haiku (661 calls at 23:58, 87 at 03:01) instead of local models: cards grow should default to local profiles (Jarvis, then the GPU's gemma or mimo), use Haiku only when asked, and say which ran
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
- 2026-11-05T05:56:15Z created
- 2026-11-05T05:59:18Z dropped: user 2026-11-05 allows Haiku for moons and cards when local models fall short; Haiku fallback is the intended behaviour
## Follow-ups captured
