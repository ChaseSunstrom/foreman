---
id: T-3340
type: FEATURE
tier: M
status: planned
priority: normal
scope: [bench/spec-suite, plugin/tests/test_bench.py]
depends_on: []
source: user
created: 2026-11-06T05:06:38Z
updated: 2026-11-06T05:55:13Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a4dde600af6ee6121
lane_branch: worktree-agent-a4dde600af6ee6121
---
# Benchmark queue fixture: bench/spec-suite/queue.py (make.py --suite queue) builds 12 candidate tasks on hard's invoicing package (keep-rule bugs, dense features, a flaky test, an API migration, one impossible task, one ambiguous-but-safe task), each with hidden fail-to-pass tests and a naive variant that must fail
## Raw request
> Measure what the user feels: Sampo vs plain Claude Code vs Sampo of a month ago. The only head-to-head on record is bench duel 2026-10-16 (Sonnet, 6 single-task cases): bare 1/6 passed, score 6, 1.46 USD; Foreman 0/6, score 4, 1.95 USD: too small to mean anything, and it measured single short tasks, not what Sampo is for. Build the duel the claim needs: ~10 realistic queued tasks in a fixture repo run unattended on a fixed time budget, three arms (plain CC, Sampo HEAD, Sampo tagged 30 days ago), same model, scored by held-out tests the agents can't see, plus user time needed (questions, stalls) and cost; 3 seeds each with noise bands (fm bench's gate). Publish the result on the site whatever it says. User: 'if sampo isn't better than regular CC or even older versions of itself, why does it feel increasingly better?'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] make.py --suite queue --check exits 0 with 12 fail-to-pass tasks and 12 failing naive variants — verify with `python3 bench/spec-suite/make.py --suite queue --check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] fixture tasks and hidden tests  <- CURRENT
2. [ ] naive variants and --check
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:06:38Z created
- 2026-11-06T05:55:11Z planned from capture
## Follow-ups captured
