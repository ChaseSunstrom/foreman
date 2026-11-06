---
id: T-3364
type: FIX
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/bench.py, plugin/tests/test_bench.py]
depends_on: []
source: discovered
created: 2026-11-06T05:55:15Z
updated: 2026-11-06T05:58:04Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a930cb76c3efc3c84
lane_branch: worktree-agent-a930cb76c3efc3c84
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:58:04Z
plan0_scope: [plugin/lib/sampo/bench.py, plugin/tests/test_bench.py]
---
# fm bench leaks the answers: _worktree (bench.py:74) is a linked git worktree, so an agent can git show the case commit's hidden tests and reference fix; arms must run in a fresh git init of git archive base (long.py's _archive), and a transcript audit voids any run that touches spec-suite/, the source repo or cases.json
## Raw request
> fm bench leaks the answers: _worktree (bench.py:74) is a linked git worktree, so an agent can git show the case commit's hidden tests and reference fix; arms must run in a fresh git init of git archive base (long.py's _archive), and a transcript audit voids any run that touches spec-suite/, the source repo or cases.json
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] the case commit is unreachable from the arm's tree, and a fake transcript that reads cases.json is flagged as a leak — verify with `python3 plugin/tests/run.py test_bench`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] run_case(fresh=True) and the leak audit
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:55:15Z created
- 2026-11-06T05:57:55Z focused
- 2026-11-06T05:58:04Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2334 [FIX M, done, 2 steps] A task always gets a start point: a git timeout at focus or at finish is retried, never read as no start commit — lesson: A timeout is not …
- T-3340 [FEATURE M, planned, 2 steps] Benchmark queue fixture: bench/spec-suite/queue.py (make.py --suite queue) builds 12 candidate tasks on hard's invoicing package (ke…
- research wave1-plan-a4e57ddf98089606d: === T-1074 [stale: plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-31: End-of-run exam: one fresh child-authored draw (seed 70, 18 per kind, all six languages, 6 held out per kind), the zero-token arms on all, then the …
- similar past tasks were M: consider --tier M
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_bench.py, plugin/tests/test_core.py, plugin/tests/test_rename_scan.py
