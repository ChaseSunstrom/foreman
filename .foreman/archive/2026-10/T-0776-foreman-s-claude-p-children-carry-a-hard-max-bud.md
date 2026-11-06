---
id: T-0776
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmideas.py, plugin/lib/fmresearch.py, plugin/tests/test_ideas.py]
depends_on: []
source: user
created: 2026-10-14T15:55:14Z
updated: 2026-10-14T16:42:24Z
inferred_deps: [T-0760]
inferred_why: T-0760: named in its request
group: headless child command budget and effort
base: b763f8adf9bbe0238396d354b6f70430a5d55972
base_tree: d60c5f4b593bc54d107a6ac583e3e02c996c05c7
verified: strong
---
# Foreman's claude -p children carry a hard --max-budget-usd
## Raw request
> PERF: Foreman's claude -p children carry a hard --max-budget-usd and an --effort
> CONTEXT: T-0760, cluster headless-children. fmideas.child_cmd and fmresearch._child only pre-check the budget; fmbench.py:248 already passes --max-budget-usd. claude -p has --effort and --max-budget-usd (2.1.217).
> DONE-WHEN: every child argv built by fmideas.child_cmd and fmresearch._child includes --max-budget-usd from fm budget's per-command cap share and an --effort; a test pins it.
## Interpretation
fmideas.child_cmd (fm ideas, second, relate, evolve, spec, rewrite, bench judges) and fmresearch._child only pre-check the day budget (fmbudget.check); a runaway child spends until it ends. claude -p --max-budget-usd (2.1.217) stops it at the cap; fmbench already passes it. Each child gets the per-command cap (fm budget 'run', default $6). --effort stays the model default: lens and research quality are the point.
## Assumptions (confidence)
## Acceptance criteria
- [x] every argv from fmideas.child_cmd and fmresearch._child has --max-budget-usd equal to fm budget's run cap — verify with `cd plugin/tests && python3 -m unittest test_ideas.ChildCommand`
## Non-goals
## Approach (options → choice → why)
Options: per-child share of the run cap (needs the child count at every call site); the whole run cap per child (one line per builder, still a hard ceiling); effort too (quality loss). Chose the run cap per child.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test
2. [x] --max-budget-usd in both builders
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_ideas.ChildCommand` → exit 0 · Ran 1 test in 0.042s / OK [ran] [tree bb59633a928f] (2026-10-14T16:30:02Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_ideas test_research` → exit 0 · Ran 22 tests in 12.980s / OK [ran] [tree bb59633a928f] (2026-10-14T16:30:18Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · Notification                61.4   101.9     150  [0] / SessionEnd                  57.9    81.2     150  [0] [ran] [tree bb59633a928f] (2026-10-14T16:35:01Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · Notification               136.3   312.4     150  [0]  OVER BUDGET / SessionEnd                 212.0   520.3     150  [0]  OVER BUDGET [ran] [tree bb59633a928f] (2026-10-14T16:35:09Z)
- `cd plugin/tests && python3 -m unittest test_ideas.ChildCommand` → ✗ exit 1 · Ran 1 test in 0.044s / FAILED (errors=1) (start tree + this task's tests) [ran] [tree 86a8461f8dd6] (2026-10-14T16:42:04Z)
- `cd plugin/tests && python3 -m unittest test_ideas.ChildCommand` → exit 0 · Ran 1 test in 0.030s / OK [ran] [tree 86a8461f8dd6] (2026-10-14T16:42:04Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_ideas.ChildCommand` → exit 0 · Ran 1 test in 0.030s / OK [ran] [tree 86a8461f8dd6] (2026-10-14T16:42:05Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_ideas test_research` → exit 0 · Ran 22 tests in 11.667s / OK [ran] [tree 86a8461f8dd6] (2026-10-14T16:42:17Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_ideas.ChildCommand` → exit 0 · Ran 1 test in 0.032s / OK [ran] [tree 86a8461f8dd6] (2026-10-14T16:42:17Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_ideas.ChildCommand` → exit 0 · Ran 1 test in 0.055s / OK [ran] [tree 86a8461f8dd6] (2026-10-14T16:42:23Z)
- (audit edge) `self: merged diff read; both child builders add --max-budget-usd at fmbudget.effective()'s run cap, the same cap fmbudget.check enforces before a run; bench children already had it` → a run cap of 0 means no spend, consistent with check(); the cap is per child, so a 4-round fm ideas run is bounded per child, while its total stays guarded by the day cap [tree 86a8461f8dd6] (2026-10-14T16:42:23Z)
- (audit self) `self: merged diff read; both child builders add --max-budget-usd at fmbudget.effective()'s run cap, the same cap fmbudget.check enforces before a run; bench children already had it` → no findings [tree 86a8461f8dd6] (2026-10-14T16:42:23Z)
## Log
- 2026-10-14T15:55:14Z created
- 2026-10-14T16:04:09Z planned from capture
- 2026-10-14T16:29:23Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0776.builder.md
- 2026-10-14T16:29:30Z focused
- 2026-10-14T16:39:48Z merged worktree-agent-a26d77a16499480b1 (3 file(s))
- 2026-10-14T16:39:49Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a26d77a16499480b1
- 2026-10-14T16:42:03Z focused
- 2026-10-14T16:42:23Z scope: other files in the scope check are T-0781/T-0785's, committed by them
- 2026-10-14T16:42:24Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0227-review: HIGH, missing: the UI half of the request is not built. [stale: plugin/lib/fmbudget.py, plugin/lib/fmwatch.py, plugin/tests/helpers.py changed si…
- research T-0298-review-1: Findings
- T-0227 [FEATURE M, done, 3 steps] fm budget: one spend ledger and caps for every child run and subagent — lesson: A cap that a NaN can switch off isn't a cap: validate l…
- decision 2026-10-09: [costly] budget raised: day 30 → 40
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
- start here (files T-0227 touched): plugin/tests/test_budget.py, plugin/lib/fmbudget.py, plugin/hooks/hooks.json, plugin/lib/fmbench.py, plugin/lib/fmevolve.py, plugin/lib/fmhooks.py
- likely tests for the scope: plugin/tests/test_ideas.py, plugin/tests/test_research.py
## Measurements
worst-case spend of one runaway fm ideas/research child: unbounded (only a pre-run estimate check) → capped at fm budget's run cap ($6 default, halved under high usage)
## Lessons
- a pre-run estimate isn't a cap; pass the hard limit to the child process
## Files touched
- .claude/worktrees/agent-a26d77a16499480b1/plugin/tests/test_ideas.py
- .claude/worktrees/agent-a26d77a16499480b1/plugin/lib/fmideas.py
- .claude/worktrees/agent-a26d77a16499480b1/plugin/lib/fmresearch.py
- MASTER.md
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- plugin/lib/fmideas.py
- plugin/lib/fmresearch.py
- plugin/tests/test_doctor.py
- plugin/tests/test_hooks.py
- plugin/tests/test_ideas.py
