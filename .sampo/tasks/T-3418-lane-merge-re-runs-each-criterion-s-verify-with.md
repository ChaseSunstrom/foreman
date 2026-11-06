---
id: T-3418
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T09:42:06Z
updated: 2026-11-06T10:09:24Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a44768a190419fcfa
lane_branch: worktree-agent-a44768a190419fcfa
base: 9d9fa0fbb24df1b029200903120bfec2db40d1de
base_tree: 99dd50385e0908d624cbfe75a56d634f010a38bb
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T09:43:10Z
plan0_scope: []
builder_returned: 2026-11-06T10:09:24Z
---
# Lane merge re-runs each criterion's verify with a fixed 600 s cap, and builders write…
## Raw request
> FIX: lane merge re-runs each criterion's verify with a fixed 600 s cap, and builders write criteria naming whole modules (T-3367: test_lanes test_doctor test_demo test_docs test_cli test_showpieces → exit 124 at load ~20); scale the cap with load like the gates do, and have sampo task ac add/edit warn when a verify names a whole module whose last recorded run took over ~120 s, suggesting the touched classes
## Interpretation
Reading 1: scale the cap by load, tell timeout from red, warn on slow modules. Reading 2 (ruled out): change builders' criteria only, since the cap itself is the bug.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a verify that times out is reported as a timeout with seconds and load, not as red — verify with `python3 plugin/tests/run.py test_lanes.VerifyTimeout`
- [ ] ac add/edit notes a slow whole-module verify from check_run timing, silent without data — verify with `python3 plugin/tests/run.py test_cli.SlowVerifyNote`
## Non-goals
## Approach (options → choice → why)
1) Do less: only raise the base cap; fails if load stays high, no timeout/red distinction. 2) Use what exists: load_scaled with a larger base plus check_run timing already in the ledger; likely outcome: no new signal. 3) New absolute-load signal (ruled out, T-3391 unifies); fails by duplicating it. Choice 2 (80%): smallest change reusing load_scaled.
## Risks and rollback
Blast radius: lanes.py _verify and cli.py ac note only; revert the commit.
## Execution prompt
## Steps
1. [x] tests then code
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes.VerifyTimeout test_cli.SlowVerifyNote` → exit 0 · Ran 4 tests in 18.3s (2 jobs, 16 at a time; slowest: SlowVerifyNote 0s, VerifyTimeout 0s) / OK [ran] [tree b22d98cb8c0c] [world 2f1906870a] (2026-11-06T09:43:58Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_doctor test_kalevala test_lane_twins test_lanes test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 705 tests in 257.4s (143 jobs, 16 at a time; slowest: AffectedPairs 174s, LaneRecovery 29s, Lanes 19s) / FAILED (1 classes: test_cli.AffectedPairs) [ran] [tree b22d98cb8c0c] [world 2f1906870a] (2026-11-06T09:48:22Z)
- (step 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 69.9s (5 jobs, 16 at a time; slowest: AffectedPairs.test_a_skipped_red_first_module_isnt_named_to_run_py 46s, AffectedPairs.test_an_affected_run_with_evidence_records_it 31s, AffectedPa [ran] [tree b22d98cb8c0c] [world 2f1906870a] (2026-11-06T09:49:45Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.VerifyTimeout test_cli.SlowVerifyNote` → exit 0 · Ran 8 tests in 10.3s (2 jobs, 16 at a time; slowest: SlowVerifyNote 1s, VerifyTimeout 0s) / OK [ran] [tree b4f32e621853] [world 2f1906870a] (2026-11-06T10:04:12Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_doctor test_kalevala test_lane_twins test_lanes test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 709 tests in 254.4s (377 jobs, 16 at a time; slowest: AffectedPairs.test_a_skipped_red_first_module_isnt_named_to_run_py 40s, AffectedPairs.test_an_affected_run_with_evidence_records_it 32s, Affec [ran] [tree b4f32e621853] [world 2f1906870a] (2026-11-06T10:08:34Z)
- (step 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 19.7s (5 jobs, 16 at a time; slowest: AffectedPairs.test_an_affected_run_with_evidence_records_it 11s, AffectedPairs.test_only_the_red_first_file_itself_is_left_out 7s, AffectedPairs.te [ran] [tree b4f32e621853] [world 2f1906870a] (2026-11-06T10:09:12Z)
## Log
- 2026-11-06T09:42:06Z created
- 2026-11-06T09:42:57Z planned: it has criteria and steps
- 2026-11-06T09:43:09Z focused
- 2026-11-06T09:43:10Z predicted from its closes: 8 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-2797 [FIX M, done, 3 steps] Gates under machine load wait or stretch instead of failing: fm lane brief holds a new lane past 1.5 load per core, and fm task finish, fm …
- T-2606 [FIX S, done, 2 steps] A criterion whose every recorded run matched no test can have its verify command edited: a command that measured nothing weakens no check —…
- decision 2026-11-06: No new builder lanes until T-3252's slot pool lands
- similar finished tasks took 2–3 steps
