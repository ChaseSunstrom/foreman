---
id: T-2193
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T17:06:34Z
updated: 2026-10-30T17:07:50Z
---
# Exam session note (s31-006 rank-rust, Haiku, untrusted): fm task done reported criterion…
## Raw request
> exam session note (s31-006 rank-rust, Haiku, untrusted): fm task done reported criterion 1 unverified after fm task ac --evidence recorded it; reproduce with a temp project before trusting
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
- 2026-10-30T17:06:34Z created
- 2026-10-30T17:07:50Z repro in a throwaway repo (scratchpad toy2193, own FOREMAN_STATE): task new with an AC, fm task ac check 1 --evidence, step evidence, fm task done → the refusal names red→green and the self audit, never criterion 1; the session's note didn't reproduce
- 2026-10-30T17:07:50Z dropped: not reproduced: fm task done lists red→green and audit after fm task ac --evidence, not the criterion
## Follow-ups captured
