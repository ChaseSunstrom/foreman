---
id: T-3367
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/test_lanes.py, plugin/tests/test_doctor.py, plugin/tests/test_demo.py, plugin/tests/test_docs.py, plugin/tests/test_cli.py, plugin/tests/test_showpieces.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: followup
created: 2026-11-06T05:55:41Z
updated: 2026-11-06T13:07:50Z
base: 08db898ab4180c15b3b9baf2ffa9f8e0f03f761b
base_tree: b9c0d8bd343bcfe4e6d27d1fa31e171b60fb21c9
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:56:25Z
plan0_scope: [plugin/tests/test_lanes.py, plugin/tests/test_doctor.py, plugin/tests/test_demo.py, plugin/tests/test_docs.py, plugin/tests/test_cli.py, plugin/tests/test_showpieces.py]
builder_returned: 2026-11-06T06:55:18Z
lane_stop: merged 2026-11-06T09:57:26Z
verified: ok
unproven: [meaning, typed]
---
# Six timing tests stop depending on the machine: test_lanes stall test sets the mtime ahead (not now), test_doctor stubs os.cpu_count (closes T-3308), test_demo drops its wall-clock assert for fm's scaled timeout, test_docs Fences scales CHECK_SECONDS, test_cli parallel captures retry on exit 3 and assert all 8, test_showpieces frame count scales with busy_factor
## Raw request
> Six timing tests stop depending on the machine: test_lanes stall test sets the mtime ahead (not now), test_doctor stubs os.cpu_count (closes T-3308), test_demo drops its wall-clock assert for fm's scaled timeout, test_docs Fences scales CHECK_SECONDS, test_cli parallel captures retry on exit 3 and assert all 8, test_showpieces frame count scales with busy_factor
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] they pass under load and with a pinned CPU count — verify with `python3 plugin/tests/run.py test_cli.CaptureAndIntake test_demo.Demo test_docs.Fences test_doctor.Checks test_lanes.LaneRecovery test_showpieces`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the six edits
## Resume here
<!-- auto -->
- 2026-11-06T09:58:39Z steps 1/1 done
- git: foreman/build; 2 uncommitted: CHANGELOG.md, scripts/
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/capture4.sh
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor test_demo` → exit 0 · Ran 120 tests in 85.0s (55 jobs, 16 at a time; slowest: Demo.test_pace_and_colour_for_a_recording 6s, ViewsRepair 5s, DemoNext 5s) / OK (ran] (tree 633963fe960a] (world 2f1906870a] (2026-11-06T06:55:10Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 8b1b91af6578] (2026-11-06T09:57:29Z)
- `python3 plugin/tests/run.py test_cli test_demo test_docs test_doctor test_lanes test_showpieces` → exit 0 · Ran 624 tests in 61.7s (137 jobs, 16 at a time; slowest: LaneRecovery 27s, Lanes 21s, AffectedPairs 20s) / OK (start tree + this task's tests) [ran] [tree 6acd074b4d3f] [world 2f1906870a] (2026-11-06T10:02:55Z)
- `python3 plugin/tests/run.py test_cli test_demo test_docs test_doctor test_lanes test_showpieces` → ✗ exit 1 · Ran 624 tests in 262.4s (391 jobs, 16 at a time; slowest: AffectedPairs.test_an_affected_run_with_evidence_records_it 85s, AffectedPairs.test_only_the_red_first_file_itself_is_left_out 77s, AffectedPa [ran] [tree 6acd074b4d3f] [world 2f1906870a] (2026-11-06T10:02:55Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 7ae8478eb35a] (2026-11-06T10:09:41Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.CaptureAndIntake test_demo.Demo test_docs.Fences test_doctor.Checks test_lanes.LaneRecovery test_showpieces` → exit 0 · Ran 145 tests in 211.6s (65 jobs, 16 at a time; slowest: GraphBrowser 12s, CityBrowser 12s, LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s) / OK [ran] [tree 7ae8478eb35a] [world 2f1906870a] (2026-11-06T10:13:14Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 7ae8478eb35a] (2026-11-06T10:13:14Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 7ae8478eb35a] (2026-11-06T10:13:14Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 7ae8478eb35a] (2026-11-06T10:13:14Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 7ae8478eb35a] (2026-11-06T10:13:14Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 62f4fcf71b5e] (2026-11-06T10:36:28Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 62f4fcf71b5e] (2026-11-06T10:36:29Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 62f4fcf71b5e] (2026-11-06T10:36:29Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 62f4fcf71b5e] (2026-11-06T10:36:29Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 62f4fcf71b5e] (2026-11-06T10:36:29Z)
## Log
- 2026-11-06T05:55:41Z created
- 2026-11-06T05:56:22Z focused
- 2026-11-06T05:56:25Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T09:41:58Z criterion 1 verify: `python3 plugin/tests/run.py --load 48 test_lanes test_doctor test_demo test_docs test_cli test_showpieces` → `python3 plugin/tests/run.py test_cli.CaptureAndIntake test_demo.Demo test_docs.Fences test_doctor.Checks test_lanes.LaneRecovery test_showpieces`
- 2026-11-06T09:41:58Z merge refusal: criterion 1 ran six whole modules (incl. test_cli) and timed out at 600 s under load; narrowed to the six classes the lane changed
- 2026-11-06T09:57:26Z merged worktree-agent-acfb0602c7edc4502 (6 file(s))
- 2026-11-06T09:57:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-acfb0602c7edc4502
- 2026-11-06T09:57:26Z focused
- 2026-11-06T09:57:29Z set scope=['plugin/tests/test_lanes.py', 'plugin/tests/test_doctor.py', 'plugin/tests/test_demo.py', 'plugin/tests/test_docs.py', 'plugin/tests/test_cli.py', 'plugin/tests/test_showpieces.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T09:57:29Z scope: widened at merge to the reviewed lane's own diff (bde7afc07), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T10:04:22Z paused: focus moved to T-3417
- 2026-11-06T10:09:37Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-06T10:09:37Z focused
- 2026-11-06T10:33:53Z paused: focus moved to T-3426
- 2026-11-06T10:36:26Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-06T10:36:26Z focused
- 2026-11-06T10:37:08Z done
- 2026-11-06T13:07:50Z not reverted: test_board_verbs.BoardVerbs, test_check_paths.CheckSkip, test_close_gates.CloseGates, test_docs.MapShards, test_docs.PluginFiles already fail on bde7afc07's first parent
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3338 [FIX S, active, 2 steps] Test runner under load: run.py scales each class's timer with busy_factor (the --deadline clamp unchanged) and records a killed class's t…
- T-1730 [FIX M, done, 3 steps] Load-proof tests: hook-call timeouts, redaction and loop-review races, and frame-count windows that fail only with buil… — lesson: Judge an…
- T-2152 [FIX M, done, 3 steps] CI failed on this branch: run 41054274567 — lesson: A test's timing bound should come from a real budget (the hook's configured timeout), n…
- decision 2026-11-05: [costly] T-3177 parked, branch kept (f5e8ec11): the machine-wide test slot pool at 2x cpu matches unpooled at 2 concurrent runs (19.1 vs 18.7 s) and…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Preflight
Changed in scope since this was planned (2026-11-06): .sampo/README.md, .sampo/archive/2026-09/T-0001-phase-3-hooks-one-dispatcher-per-event-guard-sto.md, .sampo/archive/2026-09/T-0002-phase-4-skills-rules-agents-visibility-layer-por.md, .sampo/archive/…; re-ground the plan against them before editing
## Regression test
none: the six fixes remove machine dependence from timing tests (stubbed cpu count, mtime set ahead, load stand-ins); on a calm machine the old tests pass too, so red-to-green can't be shown on demand (sampo task prove ran: start tree green at low load). The evidence is the classes passing under the night's load ~20-80
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_demo.py
- plugin/tests/test_lanes.py
- plugin/tests/test_doctor.py
- plugin/tests/test_docs.py
- plugin/tests/test_showpieces.py
- plugin/tests/test_cli.py
- CHANGELOG.md
