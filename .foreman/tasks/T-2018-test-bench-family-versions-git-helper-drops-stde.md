---
id: T-2018
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T17:09:04Z
updated: 2026-10-29T17:21:26Z
---
# test_bench_family Versions' git helper drops stderr, so a 128 from git add -A in the…
## Raw request
> FIX: test_bench_family Versions' git helper drops stderr, so a 128 from git add -A in the ship worktree (passes alone and in gates) can't be diagnosed; surface stderr and find the cause
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
- 2026-10-29T17:09:04Z created
- 2026-10-29T17:09:08Z set tier=S
- 2026-10-29T17:21:26Z dropped: folded into T-2019: the cause was /tmp out of inodes from leaked test temp dirs; the git helper now shows stderr
## Follow-ups captured
