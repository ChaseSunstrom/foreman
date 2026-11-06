---
id: T-3420
type: FIX
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T09:57:37Z
updated: 2026-11-06T10:43:11Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a06c837b176fc2e41
lane_branch: worktree-agent-a06c837b176fc2e41
base: bde7afc07e1a546532ad97af95448441a0b9df0d
base_tree: 2d4ad93f64d5a5c0129271fa648fc6aa01d9471f
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T09:58:31Z
plan0_scope: []
builder_returned: 2026-11-06T10:43:11Z
---
# Sampo task set depends_on= (and depends_on+=) accepts ids that don't exist and the…
## Raw request
> FIX: sampo task set depends_on= (and depends_on+=) accepts ids that don't exist and the task's own id; refuse both with a hint (T-3377 review)
## Interpretation
Validate depends_on ids via one helper in task_set and task_new.
## Assumptions (confidence)
## Acceptance criteria
- [ ] refusals and archived dep tested — verify with `python3 plugin/tests/run.py test_cli.SetLists`
## Non-goals
## Approach (options → choice → why)
_check_deps helper using brief_paths incl. archive; called from task_set and task_new.
## Risks and rollback
## Execution prompt
## Steps
1. [x] implement and test
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli.SetLists` → ✗ exit 1 · Ran 3 tests in 16.4s (1 jobs, 16 at a time; slowest: SetLists 1s) / FAILED (1 classes: test_cli.SetLists) [ran] [tree ad2913d51fe6] [world 2f1906870a] (2026-11-06T09:59:04Z)
- (step 1) `python3 plugin/tests/run.py test_cli.SetLists` → exit 0 · Ran 3 tests in 41.0s (1 jobs, 16 at a time; slowest: SetLists 1s) / OK [ran] [tree 6523b8407c61] [world 2f1906870a] (2026-11-06T10:00:08Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 526 tests in 159.5s (128 jobs, 16 at a time; slowest: AffectedPairs 109s, TaskLifecycle 13s, KalevalaStep 9s) / FAILED (2 classes: test_cli.AffectedPairs, test_cli.StateViews) [ran] [tree 6523b8407c61] [world 2f1906870a] (2026-11-06T10:03:01Z)
- (step 1) `python3 plugin/tests/run.py test_cli.StateViews` → ✗ exit 1 · Ran 4 tests in 13.7s (1 jobs, 16 at a time; slowest: StateViews 7s) / FAILED (1 classes: test_cli.StateViews) [ran] [tree 6523b8407c61] [world 2f1906870a] (2026-11-06T10:03:18Z)
- (step 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 52.1s (5 jobs, 16 at a time; slowest: AffectedPairs.test_an_affected_run_with_evidence_records_it 32s, AffectedPairs.test_every_linked_test_skipped_is_said_so 25s, AffectedPairs.test_a_ [ran] [tree 6523b8407c61] [world 2f1906870a] (2026-11-06T10:04:11Z)
- (step 1) `python3 plugin/tests/run.py test_cli.StateViews test_cli.SetLists` → exit 0 · Ran 7 tests in 164.9s (5 jobs, 16 at a time; slowest: StateViews.test_state_md_is_bounded 6s, SetLists 1s, StateViews.test_queue_json_with_cycle 1s) / OK [ran] [tree ff7f4492b6f5] [world 2f1906870a] (2026-11-06T10:07:06Z)
- (step 1) `python3 plugin/tests/run.py test_cli.SetLists` → exit 0 · Ran 3 tests in 1.0s (1 jobs, 16 at a time; slowest: SetLists 1s) / OK [ran] [tree 24d2f8433f12] [world 2f1906870a] (2026-11-06T10:43:04Z)
## Log
- 2026-11-06T09:57:37Z created
- 2026-11-06T09:58:26Z set tier=S
- 2026-11-06T09:58:29Z planned: it has criteria and steps
- 2026-11-06T09:58:30Z focused
- 2026-11-06T09:58:31Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-2845 [FEATURE M, done, 2 steps] Every parser that reads typed commands or goals accepts sampo as well as fm (cost, repeats, friction, bench, long, smithtui, smith, man…
- playbook Schema and data migrations (fm playbooks show fix/migration)
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–3 steps
