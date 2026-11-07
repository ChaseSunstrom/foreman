---
id: T-3332
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/kalevala.py, plugin/tests/test_kalevala.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: discovered
created: 2026-11-06T04:32:01Z
updated: 2026-11-06T21:59:35Z
base: 81de6117ebb5eb92339e29c572d44667cd4faca5
base_tree: 4292d2cb372e7e78d517e0b86024e6a8727f7921
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T06:27:01Z
plan0_scope: [plugin/lib/sampo/kalevala.py, plugin/tests/test_kalevala.py]
builder_returned: 2026-11-06T06:57:14Z
lane_stop: merged 2026-11-06T18:26:22Z
verified: ok
unproven: [typed]
---
# Kalevala: _decide and the restarted check run outside the project lock, so two concurrent steps can snapshot a tower twice and log an act twice
## Raw request
> Kalevala: _decide and the restarted check run outside the project lock, so two concurrent steps can snapshot a tower twice and log an act twice
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] two concurrent kalevala.step calls on one project log each act once and snapshot a stalled tower once — verify with `python3 plugin/tests/run.py test_kalevala`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] concurrency test, red
2. [x] take c.lock around _decide and the restarted check (kalevala.py:228-230, :584)
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_kalevala.KalevalaWatch.test_two_concurrent_steps_snapshot_a_stalled_tower_and_log_its_restart_once` → ✗ exit 1 · Ran 1 tests in 91.6s (1 jobs, 16 at a time; slowest: KalevalaWatch 1s) / FAILED (1 classes: test_kalevala.KalevalaWatch) (ran] (tree 066f746bb15e] (world 2f1906870a] (2026-11-06T06:29:11Z)
- (step 2) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 71 tests in 203.7s (9 jobs, 16 at a time; slowest: KalevalaStep 12s, KalevalaWatch 4s, Kalevala 2s) / OK (ran] (tree 95ccfd8ea349] (world 2f1906870a] (2026-11-06T06:32:50Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala` → ✗ exit 1 · Ran 72 tests in 37.0s (9 jobs, 16 at a time; slowest: KalevalaStep 12s, KalevalaWatch 5s, Kalevala 2s) / FAILED (1 classes: test_kalevala.KalevalaWatch) (ran] (tree 309c26711f19] (world 2f1906870a] (2026-11-06T06:54:16Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 72 tests in 131.3s (9 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, KalevalaGen 2s) / OK (ran] (tree e63f8e020e33] (world 2f1906870a] (2026-11-06T06:56:44Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 785256972ee0] (2026-11-06T18:33:06Z)
- `python3 plugin/tests/run.py test_kalevala` → ✗ exit 1 · Ran 74 tests in 14.5s (9 jobs, 16 at a time; slowest: KalevalaWatch 13s, KalevalaStep 9s, Kalevala 1s) / FAILED (1 classes: test_kalevala.KalevalaWatch) (start tree + this task's tests) [ran] [tree 785256972ee0] [world 2f1906870a] (2026-11-06T18:33:33Z)
- `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 74 tests in 9.4s (9 jobs, 16 at a time; slowest: KalevalaStep 9s, KalevalaWatch 3s, Kalevala 1s) / OK [ran] [tree 785256972ee0] [world 2f1906870a] (2026-11-06T18:33:33Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T18:33:33Z [ran] [tree 785256972ee0] [world 2f1906870a] (2026-11-06T18:33:35Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 785256972ee0] (2026-11-06T18:33:35Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 785256972ee0] (2026-11-06T18:33:35Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 785256972ee0] (2026-11-06T18:33:35Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 785256972ee0] (2026-11-06T18:33:35Z)
## Log
- 2026-11-06T04:32:01Z created
- 2026-11-06T06:26:58Z focused
- 2026-11-06T06:27:01Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T06:53:30Z focused
- 2026-11-06T18:26:22Z merged worktree-agent-acd1b9b94054d0907 in merge train
- 2026-11-06T18:33:06Z set scope=['plugin/lib/sampo/kalevala.py', 'plugin/tests/test_kalevala.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T18:33:06Z scope: widened at merge to the reviewed lane's own diff (20fe4aaf5), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T18:34:01Z done
- 2026-11-06T18:34:04Z committed a0ce5a83b (1 file)
- 2026-11-06T21:59:35Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-acd1b9b94054d0907; dropped: its task is closed; the lane was left behind after the merge
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3326 [FEATURE M, planned, 3 steps] Headroom part 2: Kalevala opens towers for new Frame areas, at most 2 a generation, each an act with an undo
- T-2555 [FEATURE S, done, 2 steps] fm ship retries its push when main moved between the last check and the push, through the same re-pick check, up to 3 tries — lesson: a…
- T-3081 [FEATURE M, done, 4 steps] Kalevala part 2: the towers per aspect, seeded and sealed, run at once as jobs; Kalevala's own generations and the capability registry …
- decision 2026-11-06: Recommendation: none to act on; route to plugin/lib/sampo/ rather than the fm*.py aliases, and drop the aliases when their two releases end (T-2742)…
- similar finished tasks took 2–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_kalevala.py
## Preflight
Changed in scope since this was planned (2026-11-06): plugin/lib/sampo/kalevala.py, plugin/tests/test_kalevala.py; re-ground the plan against them before editing
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 concurrency test, red
## Files touched
- plugin/tests/test_kalevala.py
- plugin/lib/sampo/kalevala.py
- CHANGELOG.md
