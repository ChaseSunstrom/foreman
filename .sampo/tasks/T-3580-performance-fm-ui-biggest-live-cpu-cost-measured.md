---
id: T-3580
type: FEATURE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-07T02:46:34Z
updated: 2026-11-07T03:37:18Z
lane: ~/.claude/foreman.lanes/T-3580
base_note: 
lane_branch: foreman/T-3580
base: 123067af9e790bad2e6ef8331983b3d466b387d8
base_tree: a4685f25e586e55356a14627c95de924ad6cbe2d
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T02:48:28Z
plan0_scope: []
---
# PERFORMANCE fm ui (biggest live CPU cost, measured 2026-11-06): the UI pane runs fm ui…
## Raw request
> PERFORMANCE fm ui (biggest live CPU cost, measured 2026-11-06): the UI pane runs fm ui --json ~1,665 times an hour at ~486 ms CPU (≈809 CPU-s/h, more than all hooks together); it reruns on almost every 2 s tick because it watches the project folder and ledger.jsonl, which change constantly, and each run starts ~20 git processes and reads ~130 MB. Narrow the watch list to what the view shows, refresh at most every 10 s unless a user-visible state (focus, pause, trust, an ask) changed, cache git answers keyed on .git HEAD/index stats, and read the logs by seeking from a stored offset; target ≤150 CPU-s/h
## Interpretation
Reading 1 (chosen): cut both how often the pane reruns fm ui (at most one rebuild per 10 s unless a user-visible state moved: focus, pause/PANIC, trust, an ask, drive) and what each rerun costs (git answers cached on .git stats, ledger/events tails read by seeking), keeping what the pane shows. Reading 2 (ruled out): port fm ui to Rust (DESIGN.md's native slice): the cost is cadence and re-reading, not the interpreter, and a port doubles the view's code.
## Assumptions (confidence)
## Acceptance criteria
- [ ] The pane reruns fm ui at most once per 10 s on busy-file moves and at once on a focus/pause/trust/ask/drive move — verify with `claude plugin test mods/foreman-ui`
- [ ] fm ui serves git answers from a cache keyed on .git stats (a commit invalidates it) and its view is unchanged — verify with `nice -n 10 python3 plugin/tests/run.py test_ui_cache test_ui_signals`
- [ ] At the same activity fm ui costs at most 150 CPU-s/h (calls/h x CPU per call, from a 5-minute process sample before and after) — verify with `nice -n 10 python3 plugin/tests/run.py test_ui_cache`
- [ ] It no longer reruns on almost every 2 s tick because it watches the project folder and ledger.jsonl: those moves rerun fm ui at most every 10 s; target ≤150 CPU-s/h measured — verify with `claude plugin test mods/foreman-ui`
## Non-goals
A Rust port of fm ui (DESIGN.md's native slice) and the hook-side index (T-3573).
## Approach (options → choice → why)
1) do less: mod-side throttle only (10 s floor on every refresh). Likely outcome: 360 calls/h x ~486 ms = 175 CPU-s/h, misses the 150 target, and a pause or trust change waits up to 10 s. 2) use what exists: T-3542's ui.json cache plus its 'cached' re-poll; fails if: the key includes ledger.jsonl and tasks/, which move per tool call, so it misses nearly always under load (the measured 1,665/h). 3) a view-stamp file writers touch on view-relevant changes; fails if: one of dozens of writers forgets the touch and the pane freezes stale. 4) both, narrowly: fm ui names 'now' paths (meta, trust, PANIC, asks, drive) beside its 'slow' watch list; the mod reruns at once on a 'now' move, else at most every 10 s; fm ui memoizes git answers keyed on .git HEAD/index/refs stats and reads ledger/events tails by seeking from a stored offset. Likely outcome: ~360 calls/h x ~250 ms ≈ 90 CPU-s/h. Choice 4 (85%): the only one that meets the target without touching every writer, and it builds on T-3542's cache.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing tests: mod cadence (10 s floor, urgent paths at once) and Python git cache / view watch split  <- CURRENT
2. [x] Mod: split watch into now/slow paths with a 10 s floor; fm ui names them
3. [x] Python: git answer cache on .git stats, ledger/events offset reads, other profile hot spots
4. [x] Measure calls/h and CPU per call before and after
## Resume here
## Docs impact
docs/map/files-lib-3.md (fmwatch line): watch vs watch_now, the 10 s pane gap, the git answer cache, the offset scans and the 15 min band lines. mods/foreman-ui/types/index.d.ts documents watch_now.
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_ui_cache.UiCadence` → ✗ exit 1 · Ran 4 tests in 6.7s (1 jobs, 16 at a time; slowest: UiCadence 1s) / FAILED (1 classes: test_ui_cache.UiCadence) [ran] [tree a7a840c6d77f] [world 2f1906870a] (2026-11-07T03:04:01Z)
- (step 1) `cd mods/foreman-ui && timeout 600 nice -n 10 claude plugin test .` → ✗ exit 1 · 2 fail / Ran 178 tests across 6 files. [37.27s] [ran] [tree a7a840c6d77f] [world 2f1906870a] (2026-11-07T03:06:01Z)
- (step 2) `cd mods/foreman-ui && timeout 600 nice -n 10 claude plugin test .` → exit 0 · 0 fail / Ran 178 tests across 6 files. [27.82s] [ran] [tree 79ff7ecdf333] [world 2f1906870a] (2026-11-07T03:21:44Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_ui_cache test_ui test_ui_signals test_board_surfaces test_budget test_friction test_bus test_cockpit test_roles test_live` → exit 0 · Ran 241 tests in 82.8s (172 jobs, 16 at a time; slowest: Page.test_the_network_view_draws_three_columns_and_pulses_on_a_new_flow_at_both_widths 23s, Page.test_the_charts_are_drawn_from_one_kit_labelle [ran] [tree 79ff7ecdf333] [world 2f1906870a] (2026-11-07T03:23:19Z)
- (step 4) `nice -n 10 python3 /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3580/ab.py ~/.claude/foreman/plugin/bin/fm ~/.claude/foreman.lanes/T-3580/plugin/bin/fm ~/.claude/foreman 8` → exit 0 · {"before": {"median_ms": 498, "runs_ms": [494, 519, 520, 502, 513, 468, 480, 494]}, "after": {"median_ms": 266, "runs_ms": [316, 287, 264, 275, 253, 248, 268, 258]}} [ran] [tree 79ff7ecdf333] [world 2f1906870a] (2026-11-07T03:23:56Z)
- (ac 2) `nice -n 10 python3 plugin/tests/run.py test_ui_cache test_ui_signals` → exit 0 · Ran 18 tests in 1.5s (8 jobs, 16 at a time; slowest: UiCadence 1s, UiCache 1s, CloseOut 1s) / OK [ran] [tree 79ff7ecdf333] [world 2f1906870a] (2026-11-07T03:24:13Z)
- (ac 3) `nice -n 10 python3 plugin/tests/run.py test_ui_cache test_ui_signals` → exit 0 · Ran 18 tests in 1.4s (8 jobs, 16 at a time; slowest: UiCadence 1s, UiCache 1s, CloseOut 1s) / OK [ran] [tree 79ff7ecdf333] [world 2f1906870a] (2026-11-07T03:24:15Z)
- (ac 1) `cd mods/foreman-ui && timeout 600 nice -n 10 claude plugin test .` → exit 0 · 0 fail / Ran 178 tests across 6 files. [14.24s] [ran] [tree 79ff7ecdf333] [world 2f1906870a] (2026-11-07T03:24:30Z)
- (ac 4) `cd mods/foreman-ui && timeout 600 nice -n 10 claude plugin test .` → exit 0 · 0 fail / Ran 178 tests across 6 files. [13.87s] [ran] [tree 79ff7ecdf333] [world 2f1906870a] (2026-11-07T03:24:44Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_ui_cache test_ui test_ui_signals test_board_surfaces test_budget test_friction test_bus test_cockpit test_roles test_live` → exit 0 · Ran 245 tests in 35.2s (158 jobs, 16 at a time; slowest: Page.test_the_network_view_draws_three_columns_and_pulses_on_a_new_flow_at_both_widths 23s, Page.test_the_charts_are_drawn_from_one_kit_labelle [ran] [tree 8685e507ec51] [world 2f1906870a] (2026-11-07T03:36:46Z)
- (step 2) `cd mods/foreman-ui && timeout 600 nice -n 10 claude plugin test .` → exit 0 · 0 fail / Ran 180 tests across 6 files. [63.95s] [ran] [tree 8685e507ec51] [world 2f1906870a] (2026-11-07T03:37:18Z)
## Log
- 2026-11-07T02:46:34Z created
- 2026-11-07T02:47:56Z planned: it has criteria and steps
- 2026-11-07T02:48:00Z lane: ~/.claude/foreman.lanes/T-3580 on foreman/T-3580
- 2026-11-07T02:48:26Z focused
- 2026-11-07T02:48:28Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T03:20:02Z scope: core._git (GIT_KEPT seam), budget.ledger (seek), friction.due (task_done-only parse) and bus.rows (active_brief_fast) are on fm ui's per-call path; mods/foreman-ui for the poll cadence
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rust-fast-path-design: Measured 2026-11-06 on this box (16 cores, load 5-18), niced, against a copy of the state
- T-3542 [PERFORMANCE M, active, 3 steps] The Sampo UI's fm ui --json starts about every 3 s and uses most of a core each time…
- T-3577 [PERFORMANCE M, active, 3 steps] PERFORMANCE hooks hot path (user 2026-11-06: fast-track the Python CPU fixes): every…
- decision 2026-11-07: [costly] T-3571: speed Sampo up with a native Rust fast path for the per-call hot paths (hook dispatch, guard, statusline, ui, next) plus a state in…
