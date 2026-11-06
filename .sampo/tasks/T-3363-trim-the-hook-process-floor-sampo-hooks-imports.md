---
id: T-3363
type: PERFORMANCE
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/hooks/hook, plugin/tests/test_bench_hooks.py]
depends_on: []
source: followup
created: 2026-11-06T05:54:53Z
updated: 2026-11-06T05:54:55Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a519553639925a6b6
lane_branch: worktree-agent-a519553639925a6b6
---
# Trim the hook process floor: sampo.hooks imports its stdlib extras lazily (tempfile/random, shutil/bz2, hashlib) and hooks/hook runs python3 -I, so the floor (TaskCompleted p50, 37.5 ms) drops to 30 ms or less with every gate green
## Raw request
> Trim the hook process floor: sampo.hooks imports its stdlib extras lazily (tempfile/random, shutil/bz2, hashlib) and hooks/hook runs python3 -I, so the floor (TaskCompleted p50, 37.5 ms) drops to 30 ms or less with every gate green
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] bench_hooks floor (TaskCompleted p50) is 30 ms or less and the gates still pass — verify with `python3 plugin/tests/run.py test_bench_hooks test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] measure the floor before (bench_hooks --runs 30)  <- CURRENT
2. [ ] lazy imports and -I; measure after
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:54:53Z created
## Follow-ups captured
