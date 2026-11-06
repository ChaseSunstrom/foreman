---
id: T-3379
type: PERFORMANCE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:22:19Z
updated: 2026-11-06T06:22:19Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a62fa1ce1fdf8b5ac
lane_branch: worktree-agent-a62fa1ce1fdf8b5ac
---
# test_exam's GateGrowth classes (LeanKindGate*, one per louhi.GATE_MUTATIONS entry,…
## Raw request
> PERF: test_exam's GateGrowth classes (LeanKindGate*, one per louhi.GATE_MUTATIONS entry, T-3171) each run louhi.gate_mutations(runs=2) real hook benches: ~480 s per class under load, killed by run.py, and they keep every lane's affected check red on 2026-11-06 (T-3274, T-3287). Make the planted-growth proof cheap (bench a stub hook or a recorded baseline, runs=1 with a scaled band) or gate them to changes in louhi/bench/hooks, so the self-change gate keeps its proof without 8 min per class
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
- 2026-11-06T06:22:19Z created
## Follow-ups captured
