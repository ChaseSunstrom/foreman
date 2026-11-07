---
id: T-3044
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-3054]
source: user
created: 2026-11-04T23:57:49Z
updated: 2026-11-05T15:15:20Z
group: website progress for long-running tasks
builder_model: haiku
base: 6f1244432a3107633e4a38fdf79581006f121e8b
base_tree: f607f1b7e9e52e4f7fade86c913ddeaf20891828
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T10:23:37Z
plan0_scope: []
builder_returned: 2026-11-05T11:46:20Z
lane_stop: merged 2026-11-05T14:08:32Z
lane_verified: 713c247da3cf917bb594b262fbfbb5c2e39c00bf
verified: strong
unproven: [docs, ui-unshot]
---
# The live page shows each running job's progress (training models, growing cards and moons, exams): done of total, rate and ETA
## Raw request
> also on the website i want to see progress of tasks, like training models, and such
## Interpretation
Reading 1 (taken): long-running jobs on the machine show real progress on the live page: a model training run (jeff-train: step of total steps, loss, eval), a cards or moons grow (rows toward its target, kept moons toward 10,000), a moons funnel (rows judged of those waiting), an exam run (scenario k of N), a genesis step; each with done of total, a bar, the rate and an ETA, in the modern look (T-3054). Reading 2 (also taken, cheap): tasks' own progress: each active task and builder lane shows its steps done of total and its stage. Reading 3 (ruled out): progress only as a log line: the user asked to see progress.
## Assumptions (confidence)
live.py's jobs() already finds these processes and leaves progress None (85%); jeff-train writes JEFF_EVENTS (events.jsonl: training_started with total_steps, training_step with step, evaluation), readable through /proc/PID/environ for the same user (85%); Sampo's own loops can write a small progress file per pid (90%).
## Acceptance criteria
- [x] Progress of tasks like training models: a jeff-train run shows step of total steps, its loss and an ETA on the live page — verify with `python3 plugin/tests/run.py test_live test_live_page`
- [x] And such: cards and moons grow, the moons funnel, exam runs and genesis steps write progress (done of total) that the page shows as a bar with rate and ETA — verify with `python3 plugin/tests/run.py test_live test_live_page`
- [x] Tasks' progress: every active task and builder lane shows its steps done of total and its stage — verify with `python3 plugin/tests/run.py test_live test_live_page`
## Non-goals
## Approach (options → choice → why)
1) use what exists: jobs() fills progress from a progress file each Sampo loop writes under state (done, total, unit, note, at), and from jeff-train's own events file found through the process's JEFF_EVENTS; the rate and ETA from the first and latest samples: likely outcome: one protocol, every Sampo job, training without touching jeff-train. 2) parse each job's log for 'N of M': fails if: logs go anywhere and each tool's format drifts. 3) ledger events per batch: fails if: coarse, and most have no total. 4) do less: show elapsed time only: fails if: no percent or ETA, the ask. Choice 1 (80%).
## Risks and rollback
A stale progress file outliving its job: keyed by pid and dropped when the pid is gone; reading another user's process: only the same uid's /proc entries are read; rollback: progress stays None, the panel shows elapsed time as today.
## Execution prompt
## Steps
1. [x] the progress protocol: a per-pid file Sampo's loops write, read by jobs() (tests first)
2. [x] training: jeff-train's events through JEFF_EVENTS (tests first)
3. [x] the page: bars with rate and ETA in the modern look, tasks' step progress (tests first)
4. [x] live: a real running job's bar moves between two shots
## Resume here
<!-- auto -->
- 2026-11-05T11:33:17Z steps 4/4 done
- git: worktree-agent-a29999a312ca53dde; 9 uncommitted: plugin/lib/sampo/core.py, plugin/lib/sampo/live.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/rune.py, plugin/tests/fixtures/live/snap-5.json, plugin/tests/test_live.py, plugin/tests/test_live_page.py, plugin/tests/test_moons_scale.py
- touched since last checkpoint: plugin/tests/test_moons_scale.py, plugin/tests/test_live_page.py, plugin/tests/fixtures/live/snap-5.json, plugin/tests/test_live.py, plugin/lib/sampo/core.py, plugin/lib/sampo/rune.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/live.py
## Docs impact
CHANGELOG line; live.py jobs() and core.progress docstrings name the per-pid progress protocol
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 90 tests in 142.6s (12 classes, 16 at a time; slowest: Page 142s, Serve 12s, Act 10s) / OK [ran] [tree 8d856e1fa008] [world 2f1906870a] (2026-11-05T10:46:01Z)
- (step 2) `python3 plugin/tests/run.py test_progress` → exit 0 · Ran 15 tests in 1.8s (2 classes, 16 at a time; slowest: Progress 1s, Progress 1s) / OK [ran] [tree 8d856e1fa008] [world 2f1906870a] (2026-11-05T10:46:10Z)
- (step 3) `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 34 tests in 146.7s (2 classes, 16 at a time; slowest: Page 146s, Files 0s) / OK [ran] [tree 8d856e1fa008] [world 2f1906870a] (2026-11-05T10:48:39Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_exam test_guard test_instruments test_left_out test_library test_live test_live_page test_louhi_models test_mint test_models test_moons_scale test_motion_verify test_playbook_check test_playbook_machinery test_rename_scan test_scaffold test_small_cards test_smoke test_smoke_profiles test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [60.23s] [ran] [tree 8d856e1fa008] [world 2f1906870a] (2026-11-05T10:57:46Z)
- (step 4) `python3 plugin/tests/run.py test_live.JobProgress test_progress test_moons_scale.KeepGrow` → exit 0 · Ran 26 tests in 2.9s (4 classes, 16 at a time; slowest: KeepGrow 2s, JobProgress 1s, Progress 1s) / OK [ran] [tree 860e4c9284a0] [world 2f1906870a] (2026-11-05T11:01:02Z)
- (step 2) `python3 plugin/tests/run.py test_live.JobProgress test_progress test_moons_scale.KeepGrow` → exit 0 · Ran 26 tests in 7.4s (4 classes, 16 at a time; slowest: KeepGrow 6s, JobProgress 2s, Progress 2s) / OK [ran] [tree 860e4c9284a0] [world 2f1906870a] (2026-11-05T11:03:36Z)
- (step 1) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 91 tests in 141.5s (12 classes, 16 at a time; slowest: Page 141s, Serve 16s, Act 13s) / OK [ran] [tree 860e4c9284a0] [world 2f1906870a] (2026-11-05T11:06:01Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_exam test_guard test_instruments test_left_out test_library test_live test_live_page test_louhi_models test_mint test_models test_moons_scale test_motion_verify test_playbook_check test_playbook_machinery test_rename_scan test_scaffold test_small_cards test_smoke test_smoke_profiles test_tool_taint test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [74.99s] [ran] [tree 860e4c9284a0] [world 2f1906870a] (2026-11-05T11:14:03Z)
- (ac 1) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 93 tests in 165.7s (12 classes, 16 at a time; slowest: Page 165s, Serve 13s, Act 11s) / OK [ran] [tree d24a5e71a488] [world 2f1906870a] (2026-11-05T11:38:00Z)
- (ac 2) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 93 tests in 165.7s (12 classes, 16 at a time; slowest: Page 165s, Serve 13s, Act 11s) / OK [ran] [tree d24a5e71a488] [world 2f1906870a] (2026-11-05T11:38:00Z)
- (ac 3) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 93 tests in 165.7s (12 classes, 16 at a time; slowest: Page 165s, Serve 13s, Act 11s) / OK [ran] [tree d24a5e71a488] [world 2f1906870a] (2026-11-05T11:38:00Z)
- (step 2) `python3 plugin/tests/run.py test_live.JobProgress test_live.Snapshot test_moons_scale.Yield test_moons_scale.KeepGrow test_progress` → exit 0 · Ran 61 tests in 4.7s (6 classes, 16 at a time; slowest: Yield 4s, Snapshot 4s, KeepGrow 4s) / OK [ran] [tree d24a5e71a488] [world 2f1906870a] (2026-11-05T11:38:11Z)
- (step 1) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 93 tests in 131.7s (12 classes, 16 at a time; slowest: Page 131s, Serve 11s, Act 9s) / OK [ran] [tree d24a5e71a488] [world 2f1906870a] (2026-11-05T11:40:25Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_exam test_guard test_instruments test_left_out test_library test_live test_live_page test_louhi_models test_mint test_models test_moons_scale test_motion_verify test_playbook_check test_playbook_machinery test_rename_scan test_scaffold test_small_cards test_smoke test_smoke_profiles test_tool_taint test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [14.57s] [ran] [tree d24a5e71a488] [world 2f1906870a] (2026-11-05T11:45:03Z)
- (step 4) `bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/jobs-twice.sh` → ✗ exit 1 · moons grow --keep 10000 --workers 2 | 15607 / 15867 moons | rate 0.5658077138432048 | eta_s 460 / read 2 08:42:34 [ran] [tree 7ea12c75962d] [world 2f1906870a] (2026-11-05T14:42:34Z)
- (step 3) `python3 plugin/tests/run.py test_live test_live_page test_progress test_exam test_genesis test_moons_scale` → exit 0 · Ran 562 tests in 205.3s (296 jobs, 16 at a time; slowest: LeanKindGateHookDelay 203s, LeanKindGateGuardAllow 194s, LeanKindGateSessionLine 192s) / OK [ran] [tree 7ea12c75962d] [world 2f1906870a] (2026-11-05T14:46:01Z)
- (step 4) `bash /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/jobs-twice.sh` → exit 0 · moons grow --keep 10000 --workers 2 | 15703 / 15867 moons | rate 0.5553038666490617 | eta_s 295 / read 2 08:46:20 [ran] [tree 7ea12c75962d] [world 2f1906870a] (2026-11-05T14:46:20Z)
- (ac 1) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 95 tests in 28.1s (80 jobs, 16 at a time; slowest: Page.test_the_network_view_draws_three_columns_and_pulses_on_a_new_flow_at_both_widths 27s, Page.test_the_charts_are_drawn_from_one_kit_labelled_ [ran] [tree 24aacb0727a1] [world 2f1906870a] (2026-11-05T14:47:00Z)
- (ac 2) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 95 tests in 28.1s (80 jobs, 16 at a time; slowest: Page.test_the_network_view_draws_three_columns_and_pulses_on_a_new_flow_at_both_widths 27s, Page.test_the_charts_are_drawn_from_one_kit_labelled_ [ran] [tree 24aacb0727a1] [world 2f1906870a] (2026-11-05T14:47:00Z)
- (ac 3) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 95 tests in 28.1s (80 jobs, 16 at a time; slowest: Page.test_the_network_view_draws_three_columns_and_pulses_on_a_new_flow_at_both_widths 27s, Page.test_the_charts_are_drawn_from_one_kit_labelled_ [ran] [tree 24aacb0727a1] [world 2f1906870a] (2026-11-05T14:47:00Z)
- (audit intent) `re-ran test_live test_live_page test_progress test_exam test_genesis test_moons_scale on main after the merge (562 OK); live: /api/state read twice 10 s apart shows the moons fill's bar moving (15,575 to 15,591 of 15,867 moons, rate ~0.57/s, ETA falling) and the card writer's (2,986 of 12,000); review's 6 findings fixed before merge; conflicts with T-3086 and T-3170 resolved in the lane (one exam count, one genesis bar, fixture fields combined)` → training, cards, moons, exams and genesis write done-of-total that the page draws with rate and ETA; task rows and lane benches show steps and stage in both themes [tree 24aacb0727a1] (2026-11-05T14:47:00Z)
- (audit edge) `re-ran test_live test_live_page test_progress test_exam test_genesis test_moons_scale on main after the merge (562 OK); live: /api/state read twice 10 s apart shows the moons fill's bar moving (15,575 to 15,591 of 15,867 moons, rate ~0.57/s, ETA falling) and the card writer's (2,986 of 12,000); review's 6 findings fixed before merge; conflicts with T-3086 and T-3170 resolved in the lane (one exam count, one genesis bar, fixture fields combined)` → a job that raises ends its bar (finally); an outer loop keeps its rate when a nested one ends; a command that only mentions jeff-train isn't a training job; a dead pid's progress file is dropped [tree 24aacb0727a1] (2026-11-05T14:47:00Z)
- (audit adversary) `re-ran test_live test_live_page test_progress test_exam test_genesis test_moons_scale on main after the merge (562 OK); live: /api/state read twice 10 s apart shows the moons fill's bar moving (15,575 to 15,591 of 15,867 moons, rate ~0.57/s, ETA falling) and the card writer's (2,986 of 12,000); review's 6 findings fixed before merge; conflicts with T-3086 and T-3170 resolved in the lane (one exam count, one genesis bar, fixture fields combined)` → progress files are per pid under state/progress, written by Sampo's own loops and read as numbers and a capped note; the page renders them as text, never HTML [tree 24aacb0727a1] (2026-11-05T14:47:00Z)
- (audit intent) `re-ran test_live test_live_page test_progress test_exam test_genesis test_moons_scale on main after the merge (562 OK); live: /api/state read twice 10 s apart shows the moons fill's bar moving (15,575 to 15,591 of 15,867 moons, rate ~0.57/s, ETA falling) and the card writer's (2,986 of 12,000); review's 6 findings fixed before merge; conflicts with T-3086 and T-3170 resolved in the lane (one exam count, one genesis bar, fixture fields combined)` → training, cards, moons, exams and genesis write done-of-total that the page draws with rate and ETA; task rows and lane benches show steps and stage in both themes [tree 32b0d10fb327] (2026-11-05T15:04:59Z)
- (audit edge) `re-ran test_live test_live_page test_progress test_exam test_genesis test_moons_scale on main after the merge (562 OK); live: /api/state read twice 10 s apart shows the moons fill's bar moving (15,575 to 15,591 of 15,867 moons, rate ~0.57/s, ETA falling) and the card writer's (2,986 of 12,000); review's 6 findings fixed before merge; conflicts with T-3086 and T-3170 resolved in the lane (one exam count, one genesis bar, fixture fields combined)` → a job that raises ends its bar (finally); an outer loop keeps its rate when a nested one ends; a command that only mentions jeff-train isn't a training job; a dead pid's progress file is dropped [tree 32b0d10fb327] (2026-11-05T15:04:59Z)
- (audit adversary) `re-ran test_live test_live_page test_progress test_exam test_genesis test_moons_scale on main after the merge (562 OK); live: /api/state read twice 10 s apart shows the moons fill's bar moving (15,575 to 15,591 of 15,867 moons, rate ~0.57/s, ETA falling) and the card writer's (2,986 of 12,000); review's 6 findings fixed before merge; conflicts with T-3086 and T-3170 resolved in the lane (one exam count, one genesis bar, fixture fields combined)` → progress files are per pid under state/progress, written by Sampo's own loops and read as numbers and a capped note; the page renders them as text, never HTML [tree 32b0d10fb327] (2026-11-05T15:04:59Z)
- (audit intent) `re-ran test_live test_live_page test_progress test_exam test_genesis test_moons_scale on main after the merge (562 OK); live: /api/state read twice 10 s apart shows the moons fill's bar moving (15,575 to 15,591 of 15,867 moons, rate ~0.57/s, ETA falling) and the card writer's (2,986 of 12,000); review's 6 findings fixed before merge; conflicts with T-3086 and T-3170 resolved in the lane` → training, cards, moons, exams and genesis write done-of-total that the page draws with rate and ETA; task rows and lane benches show steps and stage in both themes [tree 58813900910e] (2026-11-05T15:10:21Z)
- (audit edge) `re-ran test_live test_live_page test_progress test_exam test_genesis test_moons_scale on main after the merge (562 OK); live: /api/state read twice 10 s apart shows the moons fill's bar moving (15,575 to 15,591 of 15,867 moons, rate ~0.57/s, ETA falling) and the card writer's (2,986 of 12,000); review's 6 findings fixed before merge; conflicts with T-3086 and T-3170 resolved in the lane` → a job that raises ends its bar (finally); an outer loop keeps its rate when a nested one ends; a command that only mentions jeff-train isn't a training job; a dead pid's progress file is dropped [tree 58813900910e] (2026-11-05T15:10:21Z)
- (audit adversary) `re-ran test_live test_live_page test_progress test_exam test_genesis test_moons_scale on main after the merge (562 OK); live: /api/state read twice 10 s apart shows the moons fill's bar moving (15,575 to 15,591 of 15,867 moons, rate ~0.57/s, ETA falling) and the card writer's (2,986 of 12,000); review's 6 findings fixed before merge; conflicts with T-3086 and T-3170 resolved in the lane` → progress files are per pid under state/progress, written by Sampo's own loops and read as numbers and a capped note; the page renders them as text, never HTML; the guard files the gate names are T-3154's, merged inside this task's window [tree 58813900910e] (2026-11-05T15:10:21Z)
## Log
- 2026-11-04T23:57:49Z created
- 2026-11-05T00:27:25Z set title=The live page shows each running job's progress (training models, growing cards and moons, exams): done of total, rate and ETA, depends_on=['T-3054']
- 2026-11-05T00:27:27Z planned: it has criteria and steps
- 2026-11-05T00:27:28Z set approved=True
- 2026-11-05T10:23:12Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3044.builder.md
- 2026-11-05T10:23:35Z focused
- 2026-11-05T10:23:37Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T10:27:41Z focused
- 2026-11-05T11:55:52Z verified: jeff-train matched by the program's basename after python options (live.py:317-326); genesis progress_end in finally (rune.py ~1938); queued for merge; step 4 live screenshots after merge
- 2026-11-05T13:02:33Z focused
- 2026-11-05T13:08:59Z merged main (2b19d1a0) into the lane: louhi/rune conflicts with T-3086 resolved to T-3044's superset (outer bars, finally); T-3086's in-one() counter removed (counted() keeps it); T-3086's tests now expect the 0/N start; test_exam test_genesis test_live test_live_page test_progress test_moons_scale OK
- 2026-11-05T13:30:18Z focused
- 2026-11-05T13:34:13Z merged main (0b4ed540) into the lane again: snap-5.json fixture combined (T-3044's lane stage + T-3170's waiting flag); test_live test_live_page test_exam test_genesis test_progress test_moons_scale OK
- 2026-11-05T14:08:32Z merged worktree-agent-a29999a312ca53dde (14 file(s))
- 2026-11-05T14:08:36Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a29999a312ca53dde
- 2026-11-05T14:18:34Z verified: the full suite is green on 713c247da
- 2026-11-05T14:42:16Z focused
- 2026-11-05T15:00:14Z paused: focus moved to T-3189
- 2026-11-05T15:04:56Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-05T15:04:56Z focused
- 2026-11-05T15:05:20Z paused: focus moved to T-3126
- 2026-11-05T15:10:18Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-05T15:10:18Z focused
- 2026-11-05T15:15:20Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3083 [FEATURE M, done, 3 steps] Job progress, the data half: a per-pid progress file Sampo's long loops write, jeff-train's events read through JEFF_EVENTS, and live.p…
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- T-3054 [FEATURE L, planned, 4 steps] The live page goes modern: a clean dashboard with modern charts by default, the forge look as a setting
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- similar finished tasks took 3–5 steps
## Lessons
- Two lanes that instrument the same loops conflict at merge: merge the smaller first and fold its counter into the other
## Files touched
- plugin/tests/test_live.py
- plugin/lib/sampo/live.py
- plugin/web/live/charts.js
- plugin/web/live/live.js
- plugin/tests/fixtures/live/snap-5.json
- plugin/tests/test_live_page.py
- plugin/lib/sampo/moonscale.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/core.py
- plugin/tests/test_moons_scale.py
- plugin/web/live/live.css
- CHANGELOG.md
- MASTER.md
- docs/map/files-lib-2.md
- plugin/lib/fmguard.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/cost.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/lanes.py
- plugin/lib/sampo/selfgate.py
- plugin/lib/sampo/smallcards.py
- plugin/lib/sampo/smith.py
- plugin/lib/sampo/smithbench.py
- plugin/lib/sampo/steer.py
- plugin/skills/library/cards/claude-code/cc-mod-testing.md
- plugin/tests/helpers.py
- plugin/tests/run.py
- plugin/tests/test_clock_windows.py
- plugin/tests/test_code.py
