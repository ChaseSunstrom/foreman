---
id: T-3083
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/live.py, plugin/lib/sampo/core.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/smallcards.py, plugin/lib/sampo/louhi.py, plugin/tests/test_live.py, plugin/tests/test_progress.py]
depends_on: []
source: user
created: 2026-11-05T00:40:10Z
updated: 2026-11-05T07:36:41Z
builder_model: haiku
base: 7f5d1f67e0f36baf23d56dcf1dcf1297d560c50d
base_tree: 55becad92b1eb74e94a2a67c0a616b42a82d9144
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T00:40:23Z
plan0_scope: [plugin/lib/sampo/live.py, plugin/lib/sampo/core.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/smallcards.py, plugin/lib/sampo/louhi.py, plugin/tests/test_live.py, plugin/tests/test_progress.py]
lane_stop: merged 2026-11-05T04:49:44Z
verified: strong
unproven: [docs, infra, tui-unshot, ui-unshot]
---
# Job progress, the data half: a per-pid progress file Sampo's long loops write, jeff-train's events read through JEFF_EVENTS, and live.py's jobs() filling done, total, rate and ETA (T-3044 part 1)
## Raw request
> Job progress, the data half: a per-pid progress file Sampo's long loops write, jeff-train's events read through JEFF_EVENTS, and live.py's jobs() filling done, total, rate and ETA (T-3044 part 1)
## Interpretation
Reading 1 (taken): the data half of T-3044: real progress for running jobs (done of total, rate, ETA) and tasks' step progress, in the snapshot the live page reads; the page's drawing waits for the modern shell (T-3055). Reading 2 (ruled out): parse logs for 'N of M': brittle and per tool.
## Assumptions (confidence)
## Acceptance criteria
- [x] Training models: for a running jeff-train, jobs() reports step of total steps, the last loss and an ETA from its events file found through the process's JEFF_EVENTS (same uid only) — verify with `python3 plugin/tests/run.py test_live test_progress`
- [x] And such: cards grow, moons grow and funnel, exam runs and genesis steps write a progress file (done, total, unit, note) that jobs() reads by pid, with rate and ETA from the first and latest samples; a file whose pid is gone is ignored and cleaned — verify with `python3 plugin/tests/run.py test_live test_progress`
- [x] Tasks' progress: the snapshot carries each active task's and builder lane's steps done of total and stage — verify with `python3 plugin/tests/run.py test_live`
## Non-goals
## Approach (options → choice → why)
1) use what exists: a tiny c.progress(done, total, unit, note) writing state/progress/<pid>.json atomically, called from the loops that already count (moonscale grow/funnel, smallcards grow, louhi exam run, rune step); jeff-train's own events.jsonl via /proc/PID/environ's JEFF_EVENTS; jobs() reads both: likely outcome: one protocol, no change to jeff-train. 2) the ledger's batch events: fails if: coarse and no total. 3) a socket the page polls per job: fails if: a second channel beside the snapshot. 4) do less: elapsed only: fails if: no percent or ETA. Choice 1 (80%).
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/sampo/cli.py, plugin/tests/test_moons_scale.py, plugin/tests/test_louhi_models.py, plugin/tests/test_small_cards.py, plugin/tests/test_mint.py; past FIXes T-2839, T-2866, T-2940, T-2950, T-2951.
## Execution prompt
Read the parent's brief (state/projects/foreman-4a056f/tasks/T-3044-also-on-the-website-i-want-to-see-progress-of-ta.md). live.py jobs() already finds the processes (JOBS patterns; 'jeff-train' in cmd → train) and sets progress None: fill it. Write the helper in core.py (atomic write, throttled to one write a second), call it from the loops named, and read jeff-train events (kinds: training_started has total_steps; training_step has step; evaluation; final_checkpoint_saved) from the path in /proc/PID/environ's JEFF_EVENTS, only for processes owned by this uid. Do not touch plugin/web/live (another lane redesigns it) and do not edit jeffexport.py (uncommitted work of another task sits there). Tests in plugin/tests/test_progress.py and test_live.py.
## Steps
1. [x] the progress helper and its readers (tests first)
2. [x] the loops write it; jeff-train's events (tests first)
3. [x] tasks' and lanes' step progress in the snapshot (tests first)
## Resume here
## Docs impact
none: the live page shows it; CHANGELOG had its line at merge
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_live test_progress 2>&1 | tail -30` → ✗ exit 1 · Ran 74 tests in 44.1s (13 classes, 16 at a time; slowest: Page 43s, Serve 11s, Act 10s) / FAILED (1 classes: test_progress.Progress) [ran] [tree 000a75071d97] [world 2f1906870a] (2026-11-05T00:42:33Z)
- (ac 2) `python3 plugin/tests/run.py test_live test_progress 2>&1 | tail -30` → ✗ exit 1 · Ran 74 tests in 44.1s (13 classes, 16 at a time; slowest: Page 43s, Serve 11s, Act 10s) / FAILED (1 classes: test_progress.Progress) [ran] [tree 000a75071d97] [world 2f1906870a] (2026-11-05T00:42:33Z)
- (step 1) `python3 plugin/tests/run.py test_live test_progress` → exit 0 · Ran 74 tests in 43.0s (13 classes, 16 at a time; slowest: Page 43s, Serve 11s, Act 10s) / OK [ran] [tree dc58a46e5a77] [world 2f1906870a] (2026-11-05T00:44:06Z)
- (step 2) `python3 plugin/tests/run.py test_live test_progress` → exit 0 · Ran 74 tests in 42.8s (13 classes, 16 at a time; slowest: Page 42s, Serve 11s, Act 10s) / OK [ran] [tree dc58a46e5a77] [world 2f1906870a] (2026-11-05T00:44:49Z)
- (step 3) `python3 plugin/tests/run.py test_live test_progress` → exit 0 · Ran 74 tests in 42.8s (13 classes, 16 at a time; slowest: Page 42s, Serve 11s, Act 10s) / OK [ran] [tree dc58a46e5a77] [world 2f1906870a] (2026-11-05T00:45:32Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_core test_doctor test_left_out test_live test_models test_moons_scale test_progress test_rename_scan test_small_cards test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [23.60s] [ran] [tree dc58a46e5a77] [world 2f1906870a] (2026-11-05T00:46:41Z)
- (ac 1) `python3 plugin/tests/run.py test_live test_progress 2>&1 | tail -40` → ✗ exit 1 · Ran 81 tests in 44.4s (13 classes, 16 at a time; slowest: Page 44s, Act 11s, Serve 10s) / FAILED (1 classes: test_progress.Progress) [ran] [tree 46ff9b42d893] [world 2f1906870a] (2026-11-05T00:55:26Z)
- (ac 2) `python3 plugin/tests/run.py test_live test_progress 2>&1 | tail -40` → ✗ exit 1 · Ran 81 tests in 44.4s (13 classes, 16 at a time; slowest: Page 44s, Act 11s, Serve 10s) / FAILED (1 classes: test_progress.Progress) [ran] [tree 46ff9b42d893] [world 2f1906870a] (2026-11-05T00:55:26Z)
- `python3 plugin/tests/run.py test_live test_progress` → exit 0 · Ran 100 tests in 153.7s (13 classes, 16 at a time; slowest: Page 153s, Serve 13s, Act 11s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:18:23Z)
- `python3 plugin/tests/run.py test_progress` → ✗ exit 1 · Ran 15 tests in 3.0s (2 classes, 16 at a time; slowest: Progress 1s, Progress 0s) / FAILED (1 classes: test_progress.Progress) (start tree + this task's tests) [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:18:59Z)
- `python3 plugin/tests/run.py test_progress` → exit 0 · Ran 15 tests in 1.1s (2 classes, 16 at a time; slowest: Progress 1s, Progress 1s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:18:59Z)
- (ac 1) `python3 plugin/tests/run.py test_live test_progress` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T07:18:23Z [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:21:18Z)
- (ac 2) `python3 plugin/tests/run.py test_live test_progress` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T07:18:23Z [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:21:18Z)
- (ac 3) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 85 tests in 127.3s (11 classes, 16 at a time; slowest: Page 127s, Serve 10s, Act 10s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:21:18Z)
- (audit intent) `builder lane reviewed and merged (409b5588, a moonscale conflict resolved in its lane keeping both the progress line and _repair); criteria re-run on main green (100 tests); red→green proved (test_progress fails on the start tree, passes now)` → the ask was progress for long jobs on the website: the data half writes per-pid progress files the loops update, and live.py's jobs() fills done, total, rate and ETA [tree 9ff1569cf979] (2026-11-05T07:21:18Z)
- (audit edge) `builder lane reviewed and merged (409b5588, a moonscale conflict resolved in its lane keeping both the progress line and _repair); criteria re-run on main green (100 tests); red→green proved (test_progress fails on the start tree, passes now)` → a dead pid's progress file is ignored; a job with no total shows a rate without an ETA [tree 9ff1569cf979] (2026-11-05T07:21:18Z)
- (audit adversary) `builder lane reviewed and merged (409b5588, a moonscale conflict resolved in its lane keeping both the progress line and _repair); criteria re-run on main green (100 tests); red→green proved (test_progress fails on the start tree, passes now)` → progress and events files are opened with O_NOFOLLOW|O_NONBLOCK (no symlink or FIFO tricks), a line is read to at most 1 MiB, rows that aren't JSON objects are skipped, /proc/<pid>/environ is only readable for the same uid; the page's fetch is its own same-origin snapshot [tree 9ff1569cf979] (2026-11-05T07:21:18Z)
- (audit intent) `builder lane reviewed and merged (409b5588); criteria re-run on main green (100 tests); red→green proved` → progress for long jobs on the website: per-pid progress files the loops update, live.py's jobs() fills done, total, rate and ETA [tree 9ff1569cf979] (2026-11-05T07:27:11Z)
- (audit edge) `builder lane reviewed and merged (409b5588); criteria re-run on main green (100 tests); red→green proved` → a dead pid's progress file is ignored; a job with no total shows a rate without an ETA [tree 9ff1569cf979] (2026-11-05T07:27:11Z)
- (audit adversary) `builder lane reviewed and merged (409b5588); criteria re-run on main green (100 tests); red→green proved` → progress and events files open with O_NOFOLLOW|O_NONBLOCK, lines capped at 1 MiB, non-object rows skipped, /proc environ readable only for the same uid; the page fetches only its own snapshot [tree 9ff1569cf979] (2026-11-05T07:27:11Z)
## Log
- 2026-11-05T00:40:10Z created
- 2026-11-05T00:40:11Z set approved=True
- 2026-11-05T00:40:12Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3083.builder.md
- 2026-11-05T00:40:23Z focused
- 2026-11-05T00:40:23Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T03:42:01Z gate hold 2026-11-05 ~04:00 at load 16.7: PostToolUseFailure +27%, UserPromptSubmit 119 -> 161 ms (past its 150 ms budget), PreCompact +22%; the diff writes progress only inside long loops; held for T-3091's noise filter
- 2026-11-05T04:49:44Z merged worktree-agent-a1c0ca9caa07b2429 (6 file(s))
- 2026-11-05T06:10:55Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1c0ca9caa07b2429
- 2026-11-05T07:15:09Z focused
- 2026-11-05T07:27:09Z scope: the files outside its globs (CHANGELOG.md, MASTER.md, design/site/..., site/genesis/...) came from other tasks' merges and closes (T-3047's export, T-3093, T-3087, T-3151, T-3152) that landed between T-3083's merge and this close; T-3083's own change is the merge 409b5588 within its globs
- 2026-11-05T07:36:41Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3044 [FEATURE M, planned, 4 steps] The live page shows each running job's progress (training models, growing cards and moons, exams): done of total, rate and ETA
- research live-schema: Server: `sampo live [--port N]`
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- decision 2026-11-02: [revisited: steer-expansion exam. From a user's raw words] [cites: user steer 2026-11-02: MOONSHOT.md part B (start now)] [check: python3 plugin/tes…
- the similar finished task took 3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_live.py, plugin/tests/test_mint.py, plugin/tests/test_moons_scale.py, plugin/tests/test_rename_scan.py, plugin/…
## Preflight
Changed in scope since this was planned (2026-11-05): plugin/lib/sampo/core.py, plugin/lib/sampo/live.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/smallcards.py, plugin/tests/test_live.py, plugin/tests/test_progress.py; re-ground the plan against them before editing
## Lessons
- A long job is only visible when it writes its own progress; the page can't infer it
## Files touched
- plugin/tests/test_progress.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/live.py
- plugin/lib/sampo/moonscale.py
- plugin/lib/sampo/smallcards.py
- plugin/tests/test_live.py
- CHANGELOG.md
- MASTER.md
- design/site/12-forge-illustrated/NOTES.md
- design/site/12-forge-illustrated/_src/art.py
- design/site/12-forge-illustrated/_src/build.py
- design/site/12-forge-illustrated/_src/crops.py
- design/site/12-forge-illustrated/_src/final.sh
- design/site/12-forge-illustrated/_src/fonts/Archivo-normal.woff2
- design/site/12-forge-illustrated/_src/fonts/BodoniModa-italic.woff2
- design/site/12-forge-illustrated/_src/fonts/BodoniModa-normal.woff2
- design/site/12-forge-illustrated/_src/fonts/MartianMono-normal.woff2
- design/site/12-forge-illustrated/_src/frames.py
- design/site/12-forge-illustrated/_src/fullpage.py
- design/site/12-forge-illustrated/_src/hero.py
- design/site/12-forge-illustrated/_src/led2.png
- design/site/12-forge-illustrated/_src/marks.py
- design/site/12-forge-illustrated/_src/measure.py
- design/site/12-forge-illustrated/_src/page.html
- design/site/12-forge-illustrated/_src/page.js
- design/site/12-forge-illustrated/_src/sections.py
- design/site/12-forge-illustrated/_src/sheet.html
- design/site/12-forge-illustrated/_src/sheetshot.py
- design/site/12-forge-illustrated/_src/shot.py
- design/site/12-forge-illustrated/_src/stations.py
