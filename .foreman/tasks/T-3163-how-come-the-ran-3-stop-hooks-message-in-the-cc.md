---
id: T-3163
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T06:15:17Z
updated: 2026-11-06T05:35:48Z
builder: 2026-11-05T20:57:15Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|431015|12747818
lane: ~/.claude/foreman/.claude/worktrees/agent-a532ee8d8689c0873
lane_branch: worktree-agent-a532ee8d8689c0873
base: 7807c598c69fe46ae4cef85aeeb382fcea286367
base_tree: d1cca40401eaa4973321367ac891d91d2d9cf9d6
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-05T20:57:41Z
plan0_scope: []
---
# The Sampo UI mod styles every row kind Claude Code lets a mod draw that it skips today (AskUserQuestion, CommandOutput, ToolProgress, InfoNotice, SessionMode), and the unstylable hook rows get quieter by sending less through them
## Raw request
> how come the 'ran 3 stop hooks' message in the CC terminal here isn't being rendered like the rest of the mod text in your output, and a few other things arent either
## Interpretation
Reading 1 (chosen): this build raises ui.render for 17 row kinds; the mod handles 10. The hook summary ('Ran N stop hooks'), Stop-hook feedback and hook error lines are not among the 17, so no mod can style them on this build (an upstream gap; filed). Fix what can be fixed: style the 5 skipped kinds in Sampo's look, and cut how often Sampo's own Stop hook blocks with feedback (one short line, and only when there is a real next action). Reading 2: draw a replacement for the hook rows from another hook; rejected, the engine draws those rows itself.
## Assumptions (confidence)
## Acceptance criteria
- [ ] The mod draws AskUserQuestion, CommandOutput, ToolProgress, InfoNotice and SessionMode in Sampo's style, keeping each row's information and the engine's behaviour (answers, commands, ctrl+b) — verify with `claude plugin test mods/foreman-ui`
- [ ] The drive's Stop-hook feedback is one line of at most 160 characters naming the one next action, and it blocks only when that action exists — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
1) Use what exists: register.tsx's row helpers and palette for the 5 kinds, one ui.render hook each; the drive's Stop feedback trimmed to one line in hooks.py; likely outcome: every row a mod can reach looks like Sampo. 2) Do less: only CommandOutput; fails if: questions and the progress pill stay off-style. 3) Hide the engine's rows (return nothing); fails if: the person loses information. Choice 1 (80%).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing mod tests for the five row kinds  <- CURRENT
2. [x] the five ui.render hooks
3. [x] the shorter Stop feedback (test first)
4. [x] a terminal shot of each row kind
## Resume here
<!-- auto -->
- 2026-11-06T05:01:12Z step 1/4: failing mod tests for the five row kinds
- git: worktree-agent-a532ee8d8689c0873; 5 uncommitted: mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py
- touched since last checkpoint: mods/foreman-ui/hooks/rows.tsx, plugin/tests/test_hooks.py, plugin/lib/sampo/hooks.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx
## Docs impact
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 175 tests across 6 files. [28.03s] [ran] [tree f1f29917b243] [world 2f1906870a] (2026-11-05T21:08:19Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 175 tests across 6 files. [25.88s] [ran] [tree d0b5e93dbbc4] [world 2f1906870a] (2026-11-05T21:14:08Z)
- (step 3) `python3 plugin/tests/run.py test_hooks -k drive 2>&1 | tail -25` → exit 0 · Ran 28 tests in 5.6s (28 jobs, 16 at a time; slowest: Stop.test_drive_offers_queued_work_while_background_runs 4s, Stop.test_drive_skips_work_already_under_way 3s, Stop.test_a_oneoff_headless_session_ [ran] [tree 9285e606eeff] [world 2f1906870a] (2026-11-05T21:21:43Z)
- (step 4) `python3 plugin/tests/run.py test_hooks test_perf_cost test_lanes test_tool_queue test_todo 2>&1 | tail -8` → exit 0 · Ran 491 tests in 55.2s (445 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 23s, LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 11s, NoTaskGateMulti.t [ran] [tree a9e1518d13b7] [world 2f1906870a] (2026-11-05T21:24:20Z)
- (step 3) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 260 tests in 39.1s (217 jobs, 16 at a time; slowest: Approvals 31s, UserPromptSubmit 23s, SessionStart.test_budget_holds_with_large_queue 22s) / OK [ran] [tree a9e1518d13b7] [world 2f1906870a] (2026-11-05T21:25:59Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 175 tests across 6 files. [23.50s] [ran] [tree 49c83f0d86f3] [world 2f1906870a] (2026-11-06T00:08:11Z)
- (step 3) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 260 tests in 34.5s (250 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 24s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_take [ran] [tree 49c83f0d86f3] [world 2f1906870a] (2026-11-06T00:08:49Z)
- (step 4) `grep -c '▸ /focus\|▸ /context\|↧ ctrl+b ctrl+b (twice) to run in background\|? Claude asks Colour 1 question\|You picked Red' .fm-scratch/shot/7.txt .fm-scratch/shot/3-progress.txt .fm-scratch/shot/4-ask.txt .fm-scratch/shot/5-answer.txt` → exit 0 · .fm-scratch/shot/4-ask.txt:2 / .fm-scratch/shot/5-answer.txt:3 [ran] [tree f3985c61f2cf] [world 2f1906870a] (2026-11-06T00:13:47Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_claims test_cli test_code_tui test_compact test_core test_design_surfaces test_docsdrift test_doctor test_hooks test_left_out test_models test_plugins test_rename_scan test_settings test_shot test_suite_hygiene test_supply_delta test_ui test_ui_replay && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 175 tests across 6 files. [13.63s] [ran] [tree f3985c61f2cf] [world 2f1906870a] (2026-11-06T00:15:11Z)
## Log
- 2026-11-05T06:15:17Z created
- 2026-11-05T06:15:36Z planned from capture
- 2026-11-05T06:15:37Z blocked: after T-3113 (the crest, also in register.tsx) merges, to avoid a conflict
- 2026-11-05T17:52:09Z unblocked
- 2026-11-05T20:57:15Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3163.builder.md
- 2026-11-05T20:57:40Z focused
- 2026-11-05T20:57:41Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-05T23:56:33Z focused
- 2026-11-06T04:35:00Z steer: also throttle the drive's background-running push to once per active task per WAIT_REPUSH_S; with ~20 agents the 'new running set' test (hooks.py ~4283) fired on almost every Stop
- 2026-11-06T04:46:52Z scope: the background-wait push comes at most once per active task per WAIT_REPUSH_S (600 s), not once per running set (coordinator: ~8 repeats in a row with ~20 agents)
- 2026-11-06T05:04:05Z scope: wait push once per task per WAIT_REPUSH_S (600 s); once-pushes skip while the project lock is busy so their record can't be lost; UI rows guard empty props (coordinator review)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-2774 [CLEAN M, done, 3 steps] Rune's anticipation gaps are consumed, not dropped: the next generation's predict action lists the last generation's missed steers, and s…
- decision 2026-11-04: The gen-4 Mission brainstorms ran without their --deepen rounds: sampo ideas dropped them on its own because today's risk budget is spent (8 of 6: 6…
