---
id: T-3501
type: FEATURE
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T19:05:58Z
updated: 2026-11-06T19:26:55Z
lane: ~/.claude/foreman.lanes/T-3501
lane_branch: foreman/T-3501
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T19:08:18Z
plan0_scope: []
---
# Auto-evidence matches the same check run another way: a cd, nice, timeout or env prefix, or a superset of the criterion's test modules
## Raw request
> Auto-evidence matches the same check run another way: a cd, nice, timeout or env prefix, or a superset of the criterion's test modules
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a Bash run of a criterion's verify command with a cd, nice, timeout or env prefix, or a run.py run naming a superset of its test modules, records that criterion's evidence as an exact run does, and a run of fewer modules does not — verify with `python3 plugin/tests/run.py test_auto_evidence`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] normalize the run and match by module superset, test-first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_auto_evidence` → ✗ exit 1 · Ran 5 tests in 3.1s (1 jobs, 16 at a time; slowest: SameCheckRunAnotherWay 2s) / FAILED (1 classes: test_auto_evidence.SameCheckRunAnotherWay) [ran] [tree 2e0008f85077] [world 2f1906870a] (2026-11-06T19:12:14Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_auto_evidence test_bookkeeping` → exit 0 · Ran 28 tests in 44.8s (28 jobs, 16 at a time; slowest: SessionTrailer 4s, CommitAfterFocus.test_a_file_another_task_edited_before_this_one_started_is_still_committed 4s, CommitOwnFiles.test_a_commit_w [ran] [tree 69e52a9e1ce6] [world 2f1906870a] (2026-11-06T19:20:10Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_auto_evidence test_hooks.AutoEvidence` → exit 0 · Ran 10 tests in 8.7s (2 jobs, 16 at a time; slowest: SameCheckRunAnotherWay 8s, AutoEvidence 3s) / OK [ran] [tree 1db2a72148e9] [world 2f1906870a] (2026-11-06T19:26:55Z)
## Log
- 2026-11-06T19:05:58Z created
- 2026-11-06T19:06:16Z lane: ~/.claude/foreman.lanes/T-3501 on foreman/T-3501
- 2026-11-06T19:08:17Z focused
- 2026-11-06T19:08:18Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2606 [FIX S, done, 2 steps] A criterion whose every recorded run matched no test can have its verify command edited: a command that measured nothing weakens no check —…
- T-1937 [SECURITY M, blocked, 2 steps] Guard reads wrapper flags by each wrapper's own table: command -p, time -p, setsid -c, exec -a, stdbuf -o L and time -o hid rm -rf ~
- research T-0270-review-1: Verdict: changes needed.** The new code has one regression and several ways around it. I read the code only. I could not run commands, so every…
- decision 2026-09-27: Recursion bound for T-0063: after R5, one more round (R6: auto-evidence from Bash results matching a criterion's verify command) from the existing R…
