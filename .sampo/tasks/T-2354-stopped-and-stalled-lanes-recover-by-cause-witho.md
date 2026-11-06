---
id: T-2354
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/tests/test_lanes.py, plugin/tests/test_lane_stall.py, plugin/skills/intake/references/delegate.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-31T14:00:59Z
updated: 2026-10-31T16:14:10Z
builder_model: sonnet
base: c9f6b96c90c46b172342e0165939a862ab17d7ec
base_tree: ad8c70119d9576a2c150106f20c8c2023c351ae3
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T15:00:04Z
plan0_scope: [plugin/lib/fmlanes.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py]
verified: strong
---
# Stopped and stalled lanes recover by cause without being told (Mission 8, #9)
## Raw request
> Stopped and stalled lanes recover by cause without being told (Mission 8, #9)
## Interpretation
Gap map #9 'auto-recovery of Agent lanes'. fm next appends 'fm lane resume ID' for a stopped builder and a check-and-force note for a stalled one; nothing acts. Here: 401 builder lanes, 39 merge conflicts, 11 unverified merges and not one lane_resume event ever: stopped lanes are removed and redone, not recovered.
## Assumptions (confidence)
## Acceptance criteria
- [x] A stop-cause table maps each recorded cause (process ended with work uncommitted, ended with a commit and no report, usage limit, stalled 15+ min, merge conflict, red after merge) to one recovery; a table test covers every cause — verify with `python3 plugin/tests/run.py test_lanes`
- [x] Resume runs only once the builder's process is known to have ended: a stalled builder that is still live is first stopped through its own agent (the main session's stop of that background agent), never resumed with --force over a process that may be alive — verify with `python3 plugin/tests/run.py test_lanes`
- [x] In full autonomy fm next's required action is the recovery with fm lane brief's Agent line and the Stop drive continues on it; standard autonomy names it; the two old trailing lane notes are gone — verify with `python3 plugin/tests/run.py test_lanes test_orchestration`
- [x] A lane gets two recoveries at most; a third stop blocks its task with the cause and both attempts — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
1) one stop-cause table from what's recorded (builder process ended with work uncommitted or committed and no report; a usage-limit message or fm budget's window; stalled 15+ min; merge conflict; red after merge), each mapped to one recovery (resume from its branch with no --force when the process is known ended; wait for the window's reset; the conflict brief back to the builder; the failing output back to the builder); in full autonomy it is fm next's required action, with fm lane brief's Agent line, and the drive continues on it; two recoveries per lane, then a block with the diagnosis. 2) fm run's headless stall-kill for Agent lanes too - rejected: Agent lanes belong to the main session, which must launch the new builder. 3) a watchdog process - rejected: a new install for what the drive already sees each turn. Choice 1; fm next's two trailing lane notes go.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, MASTER.md, plugin/tests/test_hooks.py, plugin/lib/fmcore.py, plugin/tests/test_cli.py; past FIXes T-0875, T-0877, T-0880, T-0907, T-0908.
## Execution prompt
## Steps
1. [x] red tests: the cause table; next's action in full autonomy; the cap of two
2. [x] the classifier and recoveries in fmlanes; fm next and the drive use it; old notes removed
3. [x] docs: MASTER lanes line, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T15:36:06Z step 1/3: red tests: the cause table; next's action in full autonomy; the cap of two
- git: worktree-agent-a21900020778a1907; 2 uncommitted: plugin/lib/fmlanes.py, plugin/tests/test_lanes.py
- touched since last checkpoint: plugin/tests/test_lanes.py, plugin/lib/fmlanes.py
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/intake/references/delegate.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -25` → ✗ exit 1 · Ran 60 tests in 74.2s (5 classes, 16 at a time; slowest: Lanes 71s, BoardLanes 4s, SafeGitFailsClosed 1s) / FAILED (2 classes: test_lanes.Lanes, test_lanes.SafeGitFailsClosed) [ran] [tree 5129b50d710c] (2026-10-31T15:11:14Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -25` → ✗ exit 1 · Ran 60 tests in 74.2s (5 classes, 16 at a time; slowest: Lanes 71s, BoardLanes 4s, SafeGitFailsClosed 1s) / FAILED (2 classes: test_lanes.Lanes, test_lanes.SafeGitFailsClosed) [ran] [tree 5129b50d710c] (2026-10-31T15:11:14Z)
- (ac 4) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -25` → ✗ exit 1 · Ran 60 tests in 74.2s (5 classes, 16 at a time; slowest: Lanes 71s, BoardLanes 4s, SafeGitFailsClosed 1s) / FAILED (2 classes: test_lanes.Lanes, test_lanes.SafeGitFailsClosed) [ran] [tree 5129b50d710c] (2026-10-31T15:11:14Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.LaneRecovery` → ✗ exit 1 · Ran 14 tests in 23.0s (1 classes, 16 at a time; slowest: LaneRecovery 22s) / FAILED (1 classes: test_lanes.LaneRecovery) [ran] [tree fb2fc8a66301] (2026-10-31T15:12:20Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_lane_stall test_orchestration test_which 2>&1 | tail -30` → exit 0 · Ran 88 tests in 24.4s (14 classes, 16 at a time; slowest: Lanes 24s, LaneRecovery 16s, LaneStall 16s) / OK [ran] [tree 43cdcf89bc6c] (2026-10-31T15:17:45Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -20` → exit 0 · Ran 61 tests in 25.9s (6 classes, 16 at a time; slowest: Lanes 25s, LaneRecovery 17s, BoardLanes 2s) / OK [ran] [tree e8b1af79d640] (2026-10-31T15:18:49Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -20` → exit 0 · Ran 61 tests in 25.9s (6 classes, 16 at a time; slowest: Lanes 25s, LaneRecovery 17s, BoardLanes 2s) / OK [ran] [tree e8b1af79d640] (2026-10-31T15:18:49Z)
- (ac 4) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -20` → exit 0 · Ran 61 tests in 25.9s (6 classes, 16 at a time; slowest: Lanes 25s, LaneRecovery 17s, BoardLanes 2s) / OK [ran] [tree e8b1af79d640] (2026-10-31T15:18:49Z)
- (step 3) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -20` → exit 0 · Ran 61 tests in 25.9s (6 classes, 16 at a time; slowest: Lanes 25s, LaneRecovery 17s, BoardLanes 2s) / OK [ran] [tree e8b1af79d640] (2026-10-31T15:18:49Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_lane_stall test_orchestration` → exit 0 · Ran 72 tests in 33.1s (11 classes, 16 at a time; slowest: Lanes 33s, LaneRecovery 23s, LaneStall 18s) / OK [ran] [tree e8b1af79d640] (2026-10-31T15:19:24Z)
- (step 3) `python3 plugin/tests/run.py test_lanes test_orchestration test_which` → exit 0 · Ran 84 tests in 14.6s (13 classes, 16 at a time; slowest: Lanes 14s, LaneRecovery 12s, Stall 9s) / OK [ran] [tree 55afe9934789] (2026-10-31T15:19:56Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_away test_board_surfaces test_board_verbs test_builder test_cli test_core test_cost test_design_surfaces test_design_tokens test_docs test_doctor test_drive_side test_edit_cards test_extras test_followups test_guard test_guard_cases test_guard_evasions test_hooks test_ideation test_judgment test_lane_stall test_lanes test_lib_hostile test_lib_source_kill test_library test_memory test_nudges test_onwrite test_paused test_playbook_use test_plugin_parity test_plugins test_replan test_robustness test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_steering test_supply_delta test_taste_ledger test_tidy test_tool_taint test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1824 tests in 68.2s (411 classes, 16 at a time; slowest: Stop 61s, NoTaskGate 33s, PreToolUse 28s) / FAILED (1 classes: test_docs.MasterShape) [ran] [tree 55afe9934789] (2026-10-31T15:21:04Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_away test_board_surfaces test_board_verbs test_builder test_cli test_core test_cost test_design_surfaces test_design_tokens test_docs test_doctor test_drive_side test_edit_cards test_extras test_followups test_guard test_guard_cases test_guard_evasions test_hooks test_ideation test_judgment test_lane_stall test_lanes test_lib_hostile test_lib_source_kill test_library test_memory test_nudges test_onwrite test_paused test_playbook_use test_plugin_parity test_plugins test_replan test_robustness test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_steering test_supply_delta test_taste_ledger test_tidy test_tool_taint test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.54s] [ran] [tree 9e009fee592e] (2026-10-31T15:23:15Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -40` → ✗ exit 1 · Ran 69 tests in 37.1s (6 classes, 16 at a time; slowest: Lanes 36s, LaneRecovery 35s, BoardLanes 2s) / FAILED (1 classes: test_lanes.LaneRecovery) [ran] [tree 98e709d1aa69] (2026-10-31T15:34:26Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -40` → ✗ exit 1 · Ran 69 tests in 37.1s (6 classes, 16 at a time; slowest: Lanes 36s, LaneRecovery 35s, BoardLanes 2s) / FAILED (1 classes: test_lanes.LaneRecovery) [ran] [tree 98e709d1aa69] (2026-10-31T15:34:26Z)
- (ac 4) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -40` → ✗ exit 1 · Ran 69 tests in 37.1s (6 classes, 16 at a time; slowest: Lanes 36s, LaneRecovery 35s, BoardLanes 2s) / FAILED (1 classes: test_lanes.LaneRecovery) [ran] [tree 98e709d1aa69] (2026-10-31T15:34:26Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_away test_backlog test_batch test_board_surfaces test_board_verbs test_builder test_clean_helpers test_cli test_code test_code_envelope test_code_hardening test_code_worker test_compact test_conflict_history test_core test_cost test_cost_forecast test_crash_hygiene test_defect_classes test_deliberation test_design_surfaces test_design_tokens test_diagnosis test_docs test_doctor test_drive_side test_economics test_edit_cards test_evidence_quality test_export test_extras test_followups test_genesis test_graph test_guard test_guard_cases test_guard_evasions test_hooks test_ideation test_judge_home test_judgment test_lane_stall test_lanes test_lib_hostile test_lib_source_kill test_library test_memory test_metacog test_nudges test_onwrite test_outcomes test_parallel test_pass4 test_paused test_planning test_playbook_use test_plugin_parity test_plugins test_queue_preview test_reasoning test_recall test_replan test_robustness test_round_g test_round_i test_runner_lint test_runtime test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_splits test_steering test_supply_delta test_taste_ledger test_tidy test_tool_taint test_trials test_trust test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [35.22s] [ran] [tree 1bbf1d439811] (2026-10-31T15:44:50Z)
- (step 1) `python3 plugin/tests/run.py test_lanes test_lane_stall test_orchestration test_hooks` → exit 0 · Ran 311 tests in 107.2s (41 classes, 16 at a time; slowest: Stop 107s, NoTaskGate 59s, PreToolUse 54s) / OK [ran] [tree 1bbf1d439811] (2026-10-31T15:46:44Z)
- (step 1) `python3 plugin/tests/run.py test_lanes test_lane_stall test_orchestration test_hooks` → exit 0 · Ran 315 tests in 63.5s (41 classes, 16 at a time; slowest: Stop 63s, NoTaskGate 40s, PreToolUse 34s) / OK [ran] [tree d239b3657b16] (2026-10-31T15:56:18Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 69 tests in 27.7s (6 classes, 16 at a time; slowest: LaneRecovery 27s, Lanes 24s, BoardLanes 1s) / OK [ran] [tree bc7cf222347e] (2026-10-31T15:57:42Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 69 tests in 27.7s (6 classes, 16 at a time; slowest: LaneRecovery 27s, Lanes 24s, BoardLanes 1s) / OK [ran] [tree bc7cf222347e] (2026-10-31T15:57:42Z)
- (ac 3) `python3 plugin/tests/run.py test_lanes test_orchestration` → exit 0 · Ran 75 tests in 28.1s (10 classes, 16 at a time; slowest: LaneRecovery 28s, Lanes 24s, Stall 9s) / OK [ran] [tree bc7cf222347e] (2026-10-31T15:57:42Z)
- (ac 4) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 69 tests in 27.7s (6 classes, 16 at a time; slowest: LaneRecovery 27s, Lanes 24s, BoardLanes 1s) / OK [ran] [tree bc7cf222347e] (2026-10-31T15:57:42Z)
- (audit intent) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 3 MEDIUM), all fixed on the branch: a conflict or red merge on a live builder counts only once the marker is _stall_limit() old with no lane work since (stop_causes, so fm next never orders it early), the cap block runs after the live-builder guards, the drive clears its recover key so a repeat stop drives, a guard refusal is its own cause naming the grant, the marker and recovery count live on the brief, unblock resets them, finished_lanes gets the full list; 315 tests OK after merge` → six (now seven) stop causes each with one recovery; never resumes over a live builder; a third stop blocks (tested) [tree bc7cf222347e] (2026-10-31T15:57:42Z)
- (audit adversary) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 3 MEDIUM), all fixed on the branch: a conflict or red merge on a live builder counts only once the marker is _stall_limit() old with no lane work since (stop_causes, so fm next never orders it early), the cap block runs after the live-builder guards, the drive clears its recover key so a repeat stop drives, a guard refusal is its own cause naming the grant, the marker and recovery count live on the brief, unblock resets them, finished_lanes gets the full list; 315 tests OK after merge` → no path removes or resumes a worktree under a live builder: fresh conflicts on live lanes are left alone (tested) [tree bc7cf222347e] (2026-10-31T15:57:42Z)
- (audit edge) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 3 MEDIUM), all fixed on the branch: a conflict or red merge on a live builder counts only once the marker is _stall_limit() old with no lane work since (stop_causes, so fm next never orders it early), the cap block runs after the live-builder guards, the drive clears its recover key so a repeat stop drives, a guard refusal is its own cause naming the grant, the marker and recovery count live on the brief, unblock resets them, finished_lanes gets the full list; 315 tests OK after merge` → the old-and-quiet rule rests on mtimes with a 2 s slack and an indirect timing test (weakest link, noted) [tree bc7cf222347e] (2026-10-31T15:57:42Z)
- (audit operator) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 3 MEDIUM), all fixed on the branch: a conflict or red merge on a live builder counts only once the marker is _stall_limit() old with no lane work since (stop_causes, so fm next never orders it early), the cap block runs after the live-builder guards, the drive clears its recover key so a repeat stop drives, a guard refusal is its own cause naming the grant, the marker and recovery count live on the brief, unblock resets them, finished_lanes gets the full list; 315 tests OK after merge` → recoveries come from brief meta, not a ledger scan per prompt; one finished_lanes call [tree bc7cf222347e] (2026-10-31T15:57:42Z)
- (audit maintainer) `one fm-reviewer pass (all five lenses): changes needed (1 HIGH, 3 MEDIUM), all fixed on the branch: a conflict or red merge on a live builder counts only once the marker is _stall_limit() old with no lane work since (stop_causes, so fm next never orders it early), the cap block runs after the live-builder guards, the drive clears its recover key so a repeat stop drives, a guard refusal is its own cause naming the grant, the marker and recovery count live on the brief, unblock resets them, finished_lanes gets the full list; 315 tests OK after merge` → the cause table is one place [tree bc7cf222347e] (2026-10-31T15:57:42Z)
## Log
- 2026-10-31T14:00:59Z created
- 2026-10-31T14:59:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2354.builder.md
- 2026-10-31T15:00:03Z focused
- 2026-10-31T15:00:04Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T15:09:42Z set scope=['plugin/lib/fmlanes.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_lanes.py', 'plugin/tests/test_lane_stall.py', 'plugin/skills/intake/references/delegate.md', 'MASTER.md']
- 2026-10-31T15:09:42Z scope widened: next_for lives in fmcore; the tests and docs the criteria name
- 2026-10-31T15:55:11Z merged worktree-agent-a21900020778a1907 (8 file(s))
- 2026-10-31T15:55:11Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a21900020778a1907
- 2026-10-31T15:55:12Z focused
- 2026-10-31T15:56:45Z scope: plugin/lib/fmlanes.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/skills/intake/references/delegate.md, plugin/tests/test_lanes.py, plugin/tests/test_lane_stall.py, plugin/tests/test_orchestration.py, MASTER.md, CHANGELOG.md
- 2026-10-31T16:01:39Z done
- 2026-10-31T16:01:43Z committed 6c18fc51 (1 file)
- 2026-10-31T16:02:44Z guard authorization added: publish
- 2026-10-31T16:14:10Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2038-review: Verdict: approve with nits.** The acceptance tests cover the two stated behaviours: a clean, quiet lane that is ahead gets a merge line, and a di…
- research brainstorm-20261016-round2: Format per cluster: ideas, grounding (code or fm command), Status (queued / done / partial / new / false), Score (value 1-5, effort …
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- decision 2026-10-31: Mission-order merging (user steer 2026-10-31): ready lanes merge lowest Mission first (5, 6, 7, 8); a later Mission's lane waits only for earlier-Mi…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_hooks.py, plugin/tests/test_lanes.py
## Preflight
Changed in scope since this was planned (2026-10-31): MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmlanes.py, plugin/skills/intake/references/delegate.md, plugin/tests/test_lane_stall.py, plugin/tests/test_lan…; re-ground the plan against them before editing
## Lessons
- Liveness read from the wrong process makes every recovery unsafe: wait for old-and-quiet before touching a lane
## Plan gaps
- failed first: step 1 red tests: the cause table; next's action in full autonomy; the cap of two
## Files touched
- plugin/tests/test_lanes.py
- plugin/tests/test_lane_stall.py
- plugin/lib/fmlanes.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/skills/intake/references/delegate.md
- MASTER.md
- CHANGELOG.md
