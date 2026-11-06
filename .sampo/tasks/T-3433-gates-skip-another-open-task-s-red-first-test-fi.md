---
id: T-3433
type: FIX
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T12:03:19Z
updated: 2026-11-06T12:25:33Z
base_note: 
lane_branch: worktree-agent-ad340b9890a48f17c
base: 26077fb83c0e892ff609b074873efcbde342a5c1
base_tree: c11bd8133d07df494ae2aeaf248c592aa2db09bb
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-06T12:05:27Z
plan0_scope: []
builder_returned: 2026-11-06T12:14:08Z
---
# Gates skip another open task's red-first test FILES whole (T-1101), so a regression in…
## Raw request
> FIX: gates skip another open task's red-first test FILES whole (T-1101), so a regression in an existing test of that file lands unseen: T-3398 broke test_claims.Claims (T-2870's test) while T-3371's red-first edit to test_claims kept the whole file out of every close's gates, and only sampo ship's unskipped run caught it; skip only the red-first test ids that open task added or changed (its diff), and run the rest of the file
## Interpretation
Reading 1: skip only the changed test ids of a committed file. Reading 2: keep whole-file skipping but only for new files (already so; ruled out, it does not address the reported hidden break).
## Assumptions (confidence)
## Acceptance criteria
- [ ] a red-first lane that added one test to a committed file: the gate runs the file's other tests, skips only the new one — verify with `python3 plugin/tests/run.py test_check_paths.CheckSkip`
- [ ] an existing test of that file broken by the change under test fails the gate — verify with `python3 plugin/tests/run.py test_check_paths.CheckSkip`
## Non-goals
## Approach (options → choice → why)
1) skip whole file (today); fails if: a regression in the file's other tests lands unseen. 2) skip ids from HEAD-vs-working AST diff, run.py skips ids in parent and child; likely outcome: only the new tests skipped. 3) use what exists: read ids from the evidence run's output; fails if: output cut or ids not named. Choice 2 (95%): deterministic, no extra state.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] tests red first: ids skipped, existing broken fails  <- CURRENT
2. [x] implement cli + run.py id skip
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_check_paths.CheckSkip` → ✗ exit 1 · Ran 3 tests in 9.5s (1 jobs, 16 at a time; slowest: CheckSkip 7s) / FAILED (1 classes: test_check_paths.CheckSkip) [ran] [tree 27b316e19988] [world 2f1906870a] (2026-11-06T12:05:49Z)
- (step 2) `python3 plugin/tests/run.py test_check_paths.CheckSkip` → ✗ exit 1 · Ran 11 tests in 1.3s (10 jobs, 16 at a time; slowest: CheckSkip.test_a_red_test_in_this_tasks_scope_still_runs 1s, CheckSkip.test_a_pass_with_tests_left_out_isnt_reused_once_they_count_again 1s, Check [ran] [tree d1e68e0620ed] [world 2f1906870a] (2026-11-06T12:06:18Z)
- (step 2) `python3 plugin/tests/run.py test_check_paths.CheckSkip` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 335.1s (1 jobs, 16 at a time; slowest: CheckSkip 335s) / FAILED (1 classes: test_check_paths.CheckSkip) [ran] [tree fcb05eaab141] [world 2f1906870a] (2026-11-06T12:12:08Z)
- (step 2) `python3 plugin/tests/run.py test_check_paths.CheckSkip` → exit 0 · Ran 10 tests in 4.7s (10 jobs, 16 at a time; slowest: CheckSkip.test_a_committed_test_file_is_shared_and_still_runs 4s, CheckSkip.test_run_py_leaves_out_the_named_modules 3s, CheckSkip.test_only_the_t [ran] [tree 1de837202d21] [world 2f1906870a] (2026-11-06T12:12:54Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_check_paths test_ci_annotations test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_run test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [12.16s] [ran] [tree 1de837202d21] [world 2f1906870a] (2026-11-06T12:13:53Z)
## Log
- 2026-11-06T12:03:19Z created
- 2026-11-06T12:05:03Z planned: it has criteria and steps
- 2026-11-06T12:05:26Z focused
- 2026-11-06T12:05:27Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-06T12:25:33Z dropped: premise refuted by review: base never skipped a committed test file (red_first_tests filters path not in tracked), so test_claims was not skipped; the real gap was that closes run only criteria plus affected tests and the post-merge full suite was paused (decision 2026-11-06); the lane's change widened skipping to committed files, so it is not landed
- 2026-11-06T12:25:33Z work at drop saved: b73ad1d4c7fb (restore: git -C ~/.claude/foreman restore --source=b73ad1d4c7fb --worktree -- :/)
- 2026-11-06T12:25:33Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad340b9890a48f17c (branch worktree-agent-ad340b9890a48f17c kept: not merged)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-3119 [PERFORMANCE M, planned, 2 steps] Merge trains: land several green lanes with one self-change gate run and one suite run, bisecting a red train to the lane that b…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Long-horizon tier is the deciding end-of-run score for every ca…
