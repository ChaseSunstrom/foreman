---
id: T-3420
type: FIX
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/cli.py, plugin/tests/test_cli.py, plugin/tests/test_visibility.py]
depends_on: []
source: discovered
created: 2026-11-06T09:57:37Z
updated: 2026-11-07T00:42:47Z
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T09:58:31Z
plan0_scope: []
builder_returned: 2026-11-06T10:43:11Z
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: f997eb98c8d4be4238b3699f7edc2ec5717a28e2
lane_stop: merged 2026-11-06T21:46:50Z
verified: strong
unproven: [meaning]
---
# Sampo task set depends_on= (and depends_on+=) accepts ids that don't exist and the…
## Raw request
> FIX: sampo task set depends_on= (and depends_on+=) accepts ids that don't exist and the task's own id; refuse both with a hint (T-3377 review)
## Interpretation
Validate depends_on ids via one helper in task_set and task_new.
## Assumptions (confidence)
## Acceptance criteria
- [x] refusals and archived dep tested — verify with `python3 plugin/tests/run.py test_cli.SetLists`
## Non-goals
## Approach (options → choice → why)
_check_deps helper using brief_paths incl. archive; called from task_set and task_new.
## Risks and rollback
## Execution prompt
## Steps
1. [x] implement and test
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli.SetLists` → ✗ exit 1 · Ran 3 tests in 16.4s (1 jobs, 16 at a time; slowest: SetLists 1s) / FAILED (1 classes: test_cli.SetLists) [ran] [tree ad2913d51fe6] [world 2f1906870a] (2026-11-06T09:59:04Z)
- (step 1) `python3 plugin/tests/run.py test_cli.SetLists` → exit 0 · Ran 3 tests in 41.0s (1 jobs, 16 at a time; slowest: SetLists 1s) / OK [ran] [tree 6523b8407c61] [world 2f1906870a] (2026-11-06T10:00:08Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 526 tests in 159.5s (128 jobs, 16 at a time; slowest: AffectedPairs 109s, TaskLifecycle 13s, KalevalaStep 9s) / FAILED (2 classes: test_cli.AffectedPairs, test_cli.StateViews) [ran] [tree 6523b8407c61] [world 2f1906870a] (2026-11-06T10:03:01Z)
- (step 1) `python3 plugin/tests/run.py test_cli.StateViews` → ✗ exit 1 · Ran 4 tests in 13.7s (1 jobs, 16 at a time; slowest: StateViews 7s) / FAILED (1 classes: test_cli.StateViews) [ran] [tree 6523b8407c61] [world 2f1906870a] (2026-11-06T10:03:18Z)
- (step 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 52.1s (5 jobs, 16 at a time; slowest: AffectedPairs.test_an_affected_run_with_evidence_records_it 32s, AffectedPairs.test_every_linked_test_skipped_is_said_so 25s, AffectedPairs.test_a_ [ran] [tree 6523b8407c61] [world 2f1906870a] (2026-11-06T10:04:11Z)
- (step 1) `python3 plugin/tests/run.py test_cli.StateViews test_cli.SetLists` → exit 0 · Ran 7 tests in 164.9s (5 jobs, 16 at a time; slowest: StateViews.test_state_md_is_bounded 6s, SetLists 1s, StateViews.test_queue_json_with_cycle 1s) / OK [ran] [tree ff7f4492b6f5] [world 2f1906870a] (2026-11-06T10:07:06Z)
- (step 1) `python3 plugin/tests/run.py test_cli.SetLists` → exit 0 · Ran 3 tests in 1.0s (1 jobs, 16 at a time; slowest: SetLists 1s) / OK [ran] [tree 24d2f8433f12] [world 2f1906870a] (2026-11-06T10:43:04Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 8d82ac7ab389] (2026-11-06T22:26:11Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.SetLists` → exit 0 · Ran 3 tests in 1.0s (1 jobs, 16 at a time; slowest: SetLists 1s) / OK [ran] [tree 8d82ac7ab389] [world 2f1906870a] (2026-11-06T22:26:14Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 8d82ac7ab389] (2026-11-06T22:26:14Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 8d82ac7ab389] (2026-11-06T22:26:14Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 8d82ac7ab389] (2026-11-06T22:26:14Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 8d82ac7ab389] (2026-11-06T22:26:14Z)
## Log
- 2026-11-06T09:57:37Z created
- 2026-11-06T09:58:26Z set tier=S
- 2026-11-06T09:58:29Z planned: it has criteria and steps
- 2026-11-06T09:58:30Z focused
- 2026-11-06T09:58:31Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T17:37:53Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a06c837b176fc2e41 (branch worktree-agent-a06c837b176fc2e41 kept: not merged)
- 2026-11-06T17:37:54Z lane: ~/.claude/foreman.lanes/T-3420 on foreman/T-3420
- 2026-11-06T17:38:33Z focused
- 2026-11-06T21:46:50Z merged foreman/T-3420 in merge train
- 2026-11-06T22:26:10Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_cli.py', 'plugin/tests/test_visibility.py']
- 2026-11-06T22:26:11Z scope: widened at merge to the reviewed lane's own diff (2ecb40734), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T22:26:47Z done
- 2026-11-06T22:26:50Z committed 483ea8c99 (1 file)
- 2026-11-07T00:42:47Z lane removed: ~/.claude/foreman.lanes/T-3420; dropped: merged and closed; the train merge path never removed it
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-2845 [FEATURE M, done, 2 steps] Every parser that reads typed commands or goals accepts sampo as well as fm (cost, repeats, friction, bench, long, smithtui, smith, man…
- playbook Schema and data migrations (fm playbooks show fix/migration)
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–3 steps
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 implement and test
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/sampo/cli.py
- CHANGELOG.md
- plugin/tests/test_visibility.py
