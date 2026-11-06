---
id: T-2944
type: FIX
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/reverify.py, plugin/tests/run.py, plugin/tests/test_run.py, plugin/tests/test_backlog.py, CHANGELOG.md]
depends_on: [T-2779]
source: discovered
created: 2026-11-04T08:52:47Z
updated: 2026-11-06T09:48:02Z
group: timeouts under parallel load
lane: ~/.claude/foreman/.claude/worktrees/agent-ac6eb2d8ea2991cff
lane_branch: worktree-agent-ac6eb2d8ea2991cff
base: 19cf45dc02be51d02cca75532c0a953687420bda
base_tree: f7e92771539040aa709b2972758be9d5f52b3845
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T08:44:55Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/tests/test_backlog.py, CHANGELOG.md]
builder_returned: 2026-11-06T09:48:02Z
---
# A re-verify that times out is reported as inconclusive, not filed as a failed check
## Raw request
> Re-verify failed for T-2779 (b35fa5): python3 plugin/tests/run.py (now ✗ exit 124 (timed out after 120s) · timed out after 120s; queued by 3d1776cae… FEATURE: fm lane merge names changed text still found elsewhere, readers first, so a producer/reader split reaches the …)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo sentinel files a 'Re-verify failed' FIX only for a check that exits non-zero within its timeout; a check that times out (exit 124) is printed as timed out (inconclusive) with its cap and filed as nothing — verify with `python3 plugin/tests/run.py test_backlog`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test in test_backlog's Reverify: a queued check that times out files no FIX and prints timed out
2. [ ] skip exit 124 in the queued re-verify filing (cmd_sentinel), say it in the output  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_backlog` → ✗ exit 1 · Ran 24 tests in 23.0s (4 jobs, 16 at a time; slowest: Reverify 4s, Extras 4s, Capture 3s) / FAILED (1 classes: test_backlog.Reverify) [ran] [tree 363a3b2a9f25] [world 2f1906870a] (2026-11-06T08:45:35Z)
- (step 2) `python3 plugin/tests/run.py test_backlog` → exit 0 · Ran 24 tests in 4.4s (4 jobs, 16 at a time; slowest: Reverify 4s, Extras 3s, Capture 2s) / OK [ran] [tree afd8d71e5930] [world 2f1906870a] (2026-11-06T08:46:00Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_backlog test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [12.67s] [ran] [tree afd8d71e5930] [world 2f1906870a] (2026-11-06T08:47:51Z)
- (step 1) `python3 plugin/tests/run.py test_backlog test_run` → ✗ exit 1 · Ran 108 tests in 689.8s (53 jobs, 16 at a time; slowest: PerTestJobs 662s, CheckSkip 370s, UnknownNames 164s) / FAILED (1 classes: test_run.PerTestJobs) [ran] [tree a49dfc7aea59] [world 2f1906870a] (2026-11-06T09:10:01Z)
- (step 2) `python3 plugin/tests/run.py test_backlog test_run` → ✗ exit 1 · Ran 108 tests in 759.5s (53 jobs, 16 at a time; slowest: PerTestJobs 481s, UnknownNames 211s, CheckSkip 144s) / FAILED (2 classes: test_run.PerTestJobs, test_diff_gates.DiffGates) [ran] [tree a49dfc7aea59] [world 2f1906870a] (2026-11-06T09:13:54Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_backlog test_ci_annotations test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_run test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 642 tests in 332.1s (281 jobs, 16 at a time; slowest: PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 197s, PerTestJobs.test_a_k_run_keeps_a_whole_class_time_and_a_full_run_records_it [ran] [tree 3e6ebd67d383] [world 2f1906870a] (2026-11-06T09:28:44Z)
## Log
- 2026-11-04T08:52:47Z created
- 2026-11-05T02:39:20Z planned from capture
- 2026-11-05T02:39:21Z set approved=True
- 2026-11-05T02:39:21Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_backlog.py', 'CHANGELOG.md']
- 2026-11-05T02:39:27Z blocked: after T-3087's lane merges (it also changes cli.py; an uncommitted cli.py would stop that merge)
- 2026-11-06T03:53:18Z unblocked
- 2026-11-06T08:44:54Z focused
- 2026-11-06T08:44:55Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T08:58:29Z set scope=['plugin/lib/sampo/cli.py', 'plugin/lib/sampo/reverify.py', 'plugin/tests/run.py', 'plugin/tests/test_run.py', 'plugin/tests/test_backlog.py', 'CHANGELOG.md']
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2943 [FIX S, done, 1 steps] The fmmint and fmtraces shims match the exact old-path shim, so the rename alias test passes — lesson: A new sampo module's old-path shim m…
- T-2861 [FEATURE M, done, 3 steps] A rename-twin check for respelled literals: for each string fragment a branch respelled… — lesson: rank by either side: the changed sit…
- T-2822 [FIX M, done, 3 steps] CI failed on this branch: run 41676727022 — lesson: A gate that reads the machine must be off inside the harness's own sandboxes: route eve…
- decision 2026-11-03: [revisited: The rename's guard step comes first] [check: python3 plugin/tests/run.py test_guard_sampo] The rename's guard step comes first: Ward ref…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_affected_hubs.py, plugin/tests/test_affected_symbols.py, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_sca…
## Preflight
Changed in scope since this was planned (2026-11-04): CHANGELOG.md, plugin/lib/sampo/cli.py; re-ground the plan against them before editing
