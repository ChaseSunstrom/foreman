---
id: T-3329
type: FEATURE
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/core.py, plugin/tests/test_id_blocks.py]
depends_on: [T-3321]
source: followup
created: 2026-11-06T04:31:56Z
updated: 2026-11-06T04:31:56Z
lane: ~/.claude/foreman/.claude/worktrees/agent-aeb5a77060abc43f5
lane_branch: worktree-agent-aeb5a77060abc43f5
---
# Fleet: id blocks: next_id reserves blocks of 32 T-numbers through a claims ref so two machines never mint the same id
## Raw request
> Fleet: id blocks: next_id reserves blocks of 32 T-numbers through a claims ref so two machines never mint the same id
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] two clones each mint 40 ids against one bare remote with no overlap; offline, a machine keeps minting inside its current block and says when the block runs out; ids stay T-\d{4,} — verify with `python3 plugin/tests/run.py test_id_blocks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] two-clone test, red  <- CURRENT
2. [ ] block reservation in next_id (core.py:2360)
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:31:56Z created
## Follow-ups captured
