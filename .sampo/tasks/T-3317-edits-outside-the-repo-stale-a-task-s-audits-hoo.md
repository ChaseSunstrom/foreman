---
id: T-3317
type: FIX
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/core.py, plugin/tests/test_core.py]
depends_on: []
source: discovered
created: 2026-11-06T04:23:07Z
updated: 2026-11-06T06:12:57Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a55d20cd9c2a47474
lane_branch: worktree-agent-a55d20cd9c2a47474
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:52:14Z
plan0_scope: [plugin/lib/sampo/core.py, plugin/tests/test_core.py]
builder_returned: 2026-11-06T06:12:57Z
---
# Edits outside the repo don't stale a task's audits
## Raw request
> Edits outside the repo stale a task's audits: hooks.py:3129 attributes every Write/Edit to the active task, scratchpad and memory files included, and core.last_change (core.py:3424) counts them, so T-3297's five audits read 'predate the last change' after I wrote a diagram in the scratchpad and a memory note; no repo file had changed. last_change should count only files under p.root (the diff reviewers saw); test: an out-of-repo touched event leaves audits fresh
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] core.last_change ignores touched files outside p.root (scratchpad, memory), so an audit recorded before such an edit stays fresh, while a repo file edited after the audit still stales it; the out-of-repo touched events are still logged — verify with `python3 plugin/tests/run.py test_core`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] test: an out-of-repo touched event after an audit leaves it fresh; a repo one stales it (red)  <- CURRENT
2. [x] filter last_change by p.root
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core.Ledger.test_last_change_ignores_files_outside_the_repo` → ✗ exit 1 · Ran 1 tests in 5.0s (1 jobs, 16 at a time; slowest: Ledger 1s) / FAILED (1 classes: test_core.Ledger) (ran] (tree 0f69b9fabbbc] (world 2f1906870a] (2026-11-06T05:52:51Z)
- (step 2) `python3 plugin/tests/run.py test_core test_ledger_chain` → exit 0 · Ran 182 tests in 315.6s (56 jobs, 16 at a time; slowest: Migrate 13s, Chain 10s, ConfidenceRoutes.test_an_assumption_under_the_bar_is_refused_until_a_verified_check_a_cold_reader_agrees_with 4s) / OK (ran] (tree f15f9c92538c] (world 2f1906870a] (2026-11-06T06:12:34Z)
## Log
- 2026-11-06T04:23:07Z created
- 2026-11-06T05:51:42Z planned from capture
- 2026-11-06T05:52:13Z focused
- 2026-11-06T05:52:14Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2784 [FIX M, done, 3 steps] fm task finish answers only for the task's own changes when other lanes merge while it is focused: files a merge commit of another task's l…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-03: SAMPO_X moves into FOREMAN_X when sampo.core loads and leaves the environment (SAMPO wins); FOREMAN_X is not copied back to SAMPO_X
- similar past tasks were L: consider --tier L
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_verify_alias.py
## Preflight
Changed in scope since this was planned (2026-11-06): plugin/lib/sampo/core.py, plugin/tests/test_core.py; re-ground the plan against them before editing
