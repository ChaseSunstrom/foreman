---
id: T-3576
type: PERFORMANCE
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-07T02:34:46Z
updated: 2026-11-07T04:24:26Z
lane: ~/.claude/foreman.lanes/T-3576
lane_branch: foreman/T-3576
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-07T02:39:22Z
plan0_scope: []
lane_stop: merged 2026-11-07T04:14:53Z
lane_verified: 1f5fc38dc5d59f019cfb4e19934273b50097eb1c
---
# PERFORMANCE (user 2026-11-06: fast-track the Python CPU fixes): the full suite runs…
## Raw request
> PERFORMANCE (user 2026-11-06: fast-track the Python CPU fixes): the full suite runs several times per merge batch: the train's affected gate (~181 modules), the post-merge full verify (pm_run, T-3544), and a sentinel full run after closes (cli._sentinel, T-1117) once no recent full check_run exists — the train's affected-only pass doesn't count as one. Make the sentinel skip while a post-merge verify is pending or running or has verified this code tree, and count a pm_run result as the last full run, so one full suite runs per batch
## Interpretation
After a train, the post-merge verify (lanes.pm_run) is the batch's one full suite run; the close sentinel (cli._sentinel) must not start another. It skips while a pm verify is pending (landed within SENTINEL_MIN) or running (live pid), or when the newest green pm verify ran on this code tree; a lane_verified event resets its age check like a check_run. Sessions without trains keep the sentinel.
## Assumptions (confidence)
## Acceptance criteria
- [ ] the sentinel skips with a pending/running post-merge verify and after a green one on this code tree, still runs when nothing verified this tree recently — verify with `nice -n 10 python3 plugin/tests/run.py test_close_gates`
## Non-goals
## Approach (options → choice → why)
Options: (1) the train logs a fake full check_run after pm_run ends - lies in the ledger, reused by _cached_pass as a full pass; (2) pm_verify logs a check_run - same problem, wrong tree/gates; (3) the sentinel reads pm records directly and counts lane_verified in its age scan. Choice: 3 - one helper next to _sentinel, no new state, pm records are already the source of truth.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing tests in test_close_gates: sentinel skips on a pending/running pm verify, on a green pm verify of this code tree, after a recent lane_verified; still runs on an older tree or a stale pending record  <- CURRENT
2. [x] cli._sentinel: _pm_covers helper and lane_verified in the age scan; tests green
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_close_gates` → ✗ exit 1 · Ran 20 tests in 73.3s (1 jobs, 16 at a time; slowest: CloseGates 57s) / FAILED (1 classes: test_close_gates.CloseGates) [ran] [tree e2313de9c3fe] [world 2f1906870a] (2026-11-07T02:41:12Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_close_gates test_close_affected test_train` → exit 0 · Ran 27 tests in 29.8s (22 jobs, 16 at a time; slowest: CloseAffectedReuse 9s, PrTrain 5s, CloseGates.test_a_close_starts_a_full_run_when_the_last_one_is_old 4s) / OK [ran] [tree d9a72e49b0c0] [world 2f1906870a] (2026-11-07T02:42:00Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_close_gates test_close_affected test_train test_docs` → exit 0 · Ran 142 tests in 38.8s (55 jobs, 16 at a time; slowest: Fences 15s, CloseGates.test_a_close_starts_a_full_run_when_the_last_one_is_old 6s, CloseGates.test_a_file_its_scope_log_names_is_committed_with_ [ran] [tree 089e0abf78dc] [world 2f1906870a] (2026-11-07T02:43:20Z)
- (ac 1) `nice -n 10 python3 plugin/tests/run.py test_close_gates` → exit 0 · Ran 20 tests in 25.7s (20 jobs, 16 at a time; slowest: CloseGates.test_a_sentinel_run_on_a_tree_edited_since_the_close_captures_nothing 5s, CloseGates.test_a_close_starts_a_full_run_when_the_last_one_ [ran] [tree 089e0abf78dc] [world 2f1906870a] (2026-11-07T02:43:51Z)
## Log
- 2026-11-07T02:34:46Z created
- 2026-11-07T02:39:13Z set type=PERFORMANCE, tier=S
- 2026-11-07T02:39:14Z planned: it has criteria and steps
- 2026-11-07T02:39:17Z lane: ~/.claude/foreman.lanes/T-3576 on foreman/T-3576
- 2026-11-07T02:39:21Z focused
- 2026-11-07T02:39:22Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-07T04:14:53Z merged foreman/T-3576 in merge train
- 2026-11-07T04:24:26Z verified: the full suite is green on 020346f6d, which contains 1f5fc38dc
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-3544 [PERFORMANCE M, done, 3 steps] Merge trains test only what changed: the gate runs the tests affected by the batch's merged changes (plus the rule tests), the full…
- T-3119 [PERFORMANCE M, planned, 2 steps] Merge trains: land several green lanes with one self-change gate run and one suite run, bisecting a red train to the lane that b…
- decision 2026-11-06: Post-merge suite paused for the serial landing run: its auto-revert reverted T-3410 (0cad059e5, a MASTER.md bullet) on load-only failures (CheckSkip…
