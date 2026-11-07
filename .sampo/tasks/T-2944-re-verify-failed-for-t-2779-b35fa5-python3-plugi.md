---
id: T-2944
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/reverify.py, plugin/tests/run.py, plugin/tests/test_run.py, plugin/tests/test_backlog.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: [T-2779]
source: discovered
created: 2026-11-04T08:52:47Z
updated: 2026-11-06T21:59:34Z
group: timeouts under parallel load
base: 81de6117ebb5eb92339e29c572d44667cd4faca5
base_tree: 4292d2cb372e7e78d517e0b86024e6a8727f7921
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T08:44:55Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/tests/test_backlog.py, CHANGELOG.md]
builder_returned: 2026-11-06T09:48:02Z
lane_stop: merged 2026-11-06T18:26:22Z
verified: strong
unproven: [meaning]
---
# A re-verify that times out is reported as inconclusive, not filed as a failed check
## Raw request
> Re-verify failed for T-2779 (b35fa5): python3 plugin/tests/run.py (now ✗ exit 124 (timed out after 120s) · timed out after 120s; queued by 3d1776cae… FEATURE: fm lane merge names changed text still found elsewhere, readers first, so a producer/reader split reaches the …)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo sentinel files a 'Re-verify failed' FIX only for a check that exits non-zero within its timeout; a check that times out (exit 124) is printed as timed out (inconclusive) with its cap and filed as nothing — verify with `python3 plugin/tests/run.py test_backlog`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test in test_backlog's Reverify: a queued check that times out files no FIX and prints timed out
2. [x] skip exit 124 in the queued re-verify filing (cmd_sentinel), say it in the output
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_backlog` → ✗ exit 1 · Ran 24 tests in 23.0s (4 jobs, 16 at a time; slowest: Reverify 4s, Extras 4s, Capture 3s) / FAILED (1 classes: test_backlog.Reverify) [ran] [tree 363a3b2a9f25] [world 2f1906870a] (2026-11-06T08:45:35Z)
- (step 2) `python3 plugin/tests/run.py test_backlog` → exit 0 · Ran 24 tests in 4.4s (4 jobs, 16 at a time; slowest: Reverify 4s, Extras 3s, Capture 2s) / OK [ran] [tree afd8d71e5930] [world 2f1906870a] (2026-11-06T08:46:00Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_backlog test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [12.67s] [ran] [tree afd8d71e5930] [world 2f1906870a] (2026-11-06T08:47:51Z)
- (step 1) `python3 plugin/tests/run.py test_backlog test_run` → ✗ exit 1 · Ran 108 tests in 689.8s (53 jobs, 16 at a time; slowest: PerTestJobs 662s, CheckSkip 370s, UnknownNames 164s) / FAILED (1 classes: test_run.PerTestJobs) [ran] [tree a49dfc7aea59] [world 2f1906870a] (2026-11-06T09:10:01Z)
- (step 2) `python3 plugin/tests/run.py test_backlog test_run` → ✗ exit 1 · Ran 108 tests in 759.5s (53 jobs, 16 at a time; slowest: PerTestJobs 481s, UnknownNames 211s, CheckSkip 144s) / FAILED (2 classes: test_run.PerTestJobs, test_diff_gates.DiffGates) [ran] [tree a49dfc7aea59] [world 2f1906870a] (2026-11-06T09:13:54Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_backlog test_ci_annotations test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_run test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 642 tests in 332.1s (281 jobs, 16 at a time; slowest: PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 197s, PerTestJobs.test_a_k_run_keeps_a_whole_class_time_and_a_full_run_records_it [ran] [tree 3e6ebd67d383] [world 2f1906870a] (2026-11-06T09:28:44Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 9b757399c14a] (2026-11-06T18:35:07Z)
- (ac 1) `python3 plugin/tests/run.py test_backlog` → exit 0 · Ran 27 tests in 3.1s (12 jobs, 16 at a time; slowest: Reverify.test_a_timed_out_reverify_is_inconclusive_files_nothing_and_stays_queued 3s, Extras 2s, Capture 2s) / OK [ran] [tree 9b757399c14a] [world 2f1906870a] (2026-11-06T18:35:19Z)
- (step 1) `python3 plugin/tests/run.py test_backlog test_run` → exit 0 · Ran 126 tests in 5.9s (80 jobs, 16 at a time; slowest: PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 5s, UnknownNames 4s, PerTestJobs.test_a_deadline_kill_is_not_recorded_as_slow_and_the [ran] [tree 9b757399c14a] [world 2f1906870a] (2026-11-06T18:35:19Z)
- (step 2) `python3 plugin/tests/run.py test_backlog test_run` → exit 0 · Ran 126 tests in 5.9s (80 jobs, 16 at a time; slowest: PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 5s, UnknownNames 4s, PerTestJobs.test_a_deadline_kill_is_not_recorded_as_slow_and_the [ran] [tree 9b757399c14a] [world 2f1906870a] (2026-11-06T18:35:19Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 9b757399c14a] (2026-11-06T18:35:19Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 9b757399c14a] (2026-11-06T18:35:19Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 9b757399c14a] (2026-11-06T18:35:19Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 9b757399c14a] (2026-11-06T18:35:19Z)
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
- 2026-11-06T18:26:22Z merged worktree-agent-ac6eb2d8ea2991cff in merge train
- 2026-11-06T18:35:07Z set scope=['plugin/lib/sampo/cli.py', 'plugin/lib/sampo/reverify.py', 'plugin/tests/run.py', 'plugin/tests/test_run.py', 'plugin/tests/test_backlog.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T18:35:07Z scope: widened at merge to the reviewed lane's own diff (4f33ca9db), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T18:35:53Z done
- 2026-11-06T18:35:55Z committed 89d0d3468 (1 file)
- 2026-11-06T21:59:34Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac6eb2d8ea2991cff; dropped: its task is closed; the lane was left behind after the merge
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
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 failing test in test_backlog's Reverify: a queued check that times out files no FIX and prints time…
## Files touched
- plugin/tests/test_backlog.py
- .fm-scratch/e.json
- plugin/lib/sampo/cli.py
- plugin/tests/test_run.py
- plugin/tests/run.py
- plugin/lib/sampo/reverify.py
- .fm-scratch/e2.json
- CHANGELOG.md
