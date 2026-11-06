---
id: T-3049
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/budget.py, plugin/lib/sampo/hooks.py, plugin/lib/sampo/watch.py, plugin/lib/sampo/cli.py, plugin/tests/test_budget.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md, mods/foreman-ui/types/index.d.ts, plugin/lib/ui-demo.json, plugin/lib/sampo/night.py, plugin/lib/sampo/bench.py]
depends_on: []
source: user
created: 2026-11-05T00:12:37Z
updated: 2026-11-05T00:34:52Z
base: 192dab33599aaf96ccf9e0cd61897d7f5211a1b2
base_tree: 541789e284f30cedcca58a371e4c6e62b86f10b6
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-05T00:12:46Z
plan0_scope: [plugin/lib/sampo/budget.py, plugin/lib/sampo/hooks.py, plugin/lib/sampo/watch.py, plugin/lib/sampo/cli.py, plugin/tests/test_budget.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md]
verified: strong
unproven: [ui-unshot]
---
# Weekly usage never leans this project: no economy mode, halved caps or paused subagents past 80% weekly
## Raw request
> Weekly usage never leans this project: no economy mode, halved caps or paused subagents past 80% weekly
## Interpretation
Reading 1 (taken): on this project only, weekly usage past 80% (and the pace rule from 75%) stops leaning: no economy-mode prompt or toast, no halved budget caps, no paused subagents, builder lanes still offered; the 5-hour window keeps its 90% rule because the user named weekly; other projects keep today's lean. Reading 2 (ruled out): turn the lean off machine-wide: the user said 'on this project specifically'. Reading 3 (ruled out): stop tracking usage at all: 'don't waste it' still holds, so spend caps and the usage figures stay.
## Assumptions (confidence)
## Acceptance criteria
- [x] Remove the weekly usage 80% lean on this project specifically: with the project's switch off, weekly usage past 80% halves no cap and pauses no subagent, and the 5-hour window still does — verify with `python3 plugin/tests/run.py test_budget`
- [x] The pane's economy mode (the prompt section and the toast) stays off for weekly usage on this project, and still shows for the 5-hour window — verify with `claude plugin test mods/foreman-ui`
- [x] Hooks offer builder lanes past 80% weekly on this project; other projects keep the lean — verify with `python3 plugin/tests/run.py test_budget test_hooks`
- [x] No need to hold back on usage here: this project's switch is set, and sampo budget reports subagents running at the live weekly figure — verify with `sampo budget`
## Non-goals
## Approach (options → choice → why)
1) use what exists: the project's pace switch (sampo drive on --pace off, meta pace_drops=false, T-2327) already says 'usage pace never drops work' but only reaches degrade(); widen it to every weekly rule (usage_high, subagent_pause, hooks' economy, the pane via fm ui --json): likely outcome: one switch, five readers. 2) a new meta key and verb (usage_lean): fails if: two switches mean nearly the same thing. 3) raise the thresholds to 100% for the project: fails if: the pace rule and the pane's own 80% stay. 4) do less: only set pace_drops=false: fails if: caps still halve, subagents still pause and the pane still says economy mode. Choice 1 (85%): the switch already exists under the user's own steer; usage_high and subagent_pause take the project (else the cwd's) and skip the weekly rules when it's off.
## Risks and rollback
Running past the weekly limit: the user has several subscriptions and asked for it; the 5-hour rule and the spend caps still stand. Rollback: sampo drive on --pace on.
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1284, T-1293, T-1303, T-1316, T-1323.
## Execution prompt
## Steps
1. [x] budget: weekly lean per project (tests first)
2. [x] hooks and the ui payload pass it; the pane skips weekly economy (tests first)
3. [x] set it on this project; live check
## Resume here
## Docs impact
CHANGELOG line; sampo drive --pace help
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_budget` → exit 0 · Ran 13 tests in 11.1s (2 classes, 16 at a time; slowest: SessionStart 11s, Budget 3s) / OK [ran] [tree e47f5a0a7ba1] [world 2f1906870a] (2026-11-05T00:14:50Z)
- (step 2) `python3 plugin/tests/run.py test_budget test_hooks && claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 163 tests across 6 files. [28.09s] [ran] [tree f99902414116] [world 2f1906870a] (2026-11-05T00:18:12Z)
- (step 3) `sampo budget | grep -q 'running' && sampo ui --json | python3 -c 'import json,sys; assert json.load(sys.stdin)["weekly_lean"] is False' && echo 'foreman: weekly lean off; subagents running'` → exit 0 · foreman: weekly lean off; subagents running [ran] [tree f99902414116] [world 2f1906870a] (2026-11-05T00:19:07Z)
- `python3 plugin/tests/run.py test_budget.Budget.test_a_project_can_turn_the_weekly_lean_off` → ✗ exit 1 · Ran 1 tests in 2.5s (1 classes, 16 at a time; slowest: Budget 0s) / FAILED (1 classes: test_budget.Budget) (start tree + this task's tests) [ran] [tree f99902414116] [world 2f1906870a] (2026-11-05T00:19:12Z)
- `python3 plugin/tests/run.py test_budget.Budget.test_a_project_can_turn_the_weekly_lean_off` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Budget 0s) / OK [ran] [tree f99902414116] [world 2f1906870a] (2026-11-05T00:19:12Z)
- (ac 1) `python3 plugin/tests/run.py test_budget` → exit 0 · Ran 13 tests in 35.9s (2 classes, 16 at a time; slowest: SessionStart 34s, Budget 11s) / OK [ran] [tree 8d9428cf71c4] [world 2f1906870a] (2026-11-05T00:29:10Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 164 tests across 6 files. [23.61s] [ran] [tree 8d9428cf71c4] [world 2f1906870a] (2026-11-05T00:29:10Z)
- (ac 3) `python3 plugin/tests/run.py test_budget test_hooks` → exit 0 · Ran 270 tests in 113.3s (32 classes, 16 at a time; slowest: Stop 113s, NoTaskGate 43s, PreToolUse 35s) / OK [ran] [tree 8d9428cf71c4] [world 2f1906870a] (2026-11-05T00:29:10Z)
- (ac 4) `sampo budget` → exit 0 · relate: $0.01 over 1 run(s) / goal-plan: $0.00 over 5 run(s) [ran] [tree 8d9428cf71c4] [world 2f1906870a] (2026-11-05T00:29:10Z)
- (audit intent) `one fm-reviewer (intent, edge, maintainer): 1 MEDIUM (no test that the hook lets subagents through with the switch off) and 6 LOW (callers without the project in night, bench, the pane's budget panel and sampo budget; the project lookup before the bar; the pane's wiring untested); all fixed, the MEDIUM and the wiring test-first` → on this project, weekly usage past 80% halves no cap, pauses no subagent, keeps builder lanes and shows no economy mode; the 5-hour window keeps its 90% rule; other projects lean as before; live: foreman's meta has pace_drops false, sampo budget says subagents running, fm ui says weekly_lean false [tree 8d9428cf71c4] (2026-11-05T00:29:10Z)
- (audit edge) `one fm-reviewer (intent, edge, maintainer): 1 MEDIUM (no test that the hook lets subagents through with the switch off) and 6 LOW (callers without the project in night, bench, the pane's budget panel and sampo budget; the project lookup before the bar; the pane's wiring untested); all fixed, the MEDIUM and the wiring test-first` → every usage reader now takes the project it serves (night, bench, sampo budget, the pane) and falls back to the cwd's; the project lookup runs only past the bar; a missing or unreadable project leans as before [tree 8d9428cf71c4] (2026-11-05T00:29:10Z)
- (audit maintainer) `one fm-reviewer (intent, edge, maintainer): 1 MEDIUM (no test that the hook lets subagents through with the switch off) and 6 LOW (callers without the project in night, bench, the pane's budget panel and sampo budget; the project lookup before the bar; the pane's wiring untested); all fixed, the MEDIUM and the wiring test-first` → one switch (the existing --pace, T-2327) whose help now says all it does; the demo view carries the new key (parity test); the pane's economyText is exported and its wiring tested through the world harness [tree 8d9428cf71c4] (2026-11-05T00:29:10Z)
- (audit intent) `one fm-reviewer (intent, edge, maintainer): 1 MEDIUM (no test that the hook lets subagents through with the switch off) and 6 LOW (callers without the project in night, bench, the pane's budget panel and sampo budget; the project lookup before the bar; the pane's wiring untested); all fixed, the MEDIUM and the wiring test-first` → on this project, weekly usage past 80% halves no cap, pauses no subagent, keeps builder lanes and shows no economy mode; the 5-hour window keeps its 90% rule; other projects lean as before; live: foreman's meta has pace_drops false, sampo budget says subagents running, fm ui says weekly_lean false [tree 8d9428cf71c4] (2026-11-05T00:32:04Z)
- (audit edge) `one fm-reviewer (intent, edge, maintainer): 1 MEDIUM (no test that the hook lets subagents through with the switch off) and 6 LOW (callers without the project in night, bench, the pane's budget panel and sampo budget; the project lookup before the bar; the pane's wiring untested); all fixed, the MEDIUM and the wiring test-first` → every usage reader now takes the project it serves (night, bench, sampo budget, the pane) and falls back to the cwd's; the project lookup runs only past the bar; a missing or unreadable project leans as before [tree 8d9428cf71c4] (2026-11-05T00:32:04Z)
- (audit maintainer) `one fm-reviewer (intent, edge, maintainer): 1 MEDIUM (no test that the hook lets subagents through with the switch off) and 6 LOW (callers without the project in night, bench, the pane's budget panel and sampo budget; the project lookup before the bar; the pane's wiring untested); all fixed, the MEDIUM and the wiring test-first` → one switch (the existing --pace, T-2327) whose help now says all it does; the demo view carries the new key (parity test); the pane's economyText is exported and its wiring tested through the world harness [tree 8d9428cf71c4] (2026-11-05T00:32:04Z)
## Log
- 2026-11-05T00:12:37Z created
- 2026-11-05T00:12:45Z focused
- 2026-11-05T00:12:46Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-05T00:14:38Z scope: mods/foreman-ui/types/index.d.ts (FmView gains weekly_lean)
- 2026-11-05T00:17:54Z scope: plugin/lib/ui-demo.json (the demo view carries weekly_lean, as test_board_surfaces requires)
- 2026-11-05T00:22:19Z review fixes: pass the project at every usage reader (night, bench, pane budget, sampo budget), project lookup only past the bar; hypothesis: every caller now honours the switch for its own project, so the tests below stay green
- 2026-11-05T00:31:49Z scope: plugin/lib/sampo/night.py and plugin/lib/sampo/bench.py: the review's edge finding: their usage readers now pass the project, so the night and the stranger test honour the per-project switch
- 2026-11-05T00:31:53Z set scope=['plugin/lib/sampo/budget.py', 'plugin/lib/sampo/hooks.py', 'plugin/lib/sampo/watch.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_budget.py', 'mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'CHANGELOG.md', 'mods/foreman-ui/types/index.d.ts', 'plugin/lib/ui-demo.json', 'plugin/lib/sampo/night.py', 'plugin/lib/sampo/bench.py']
- 2026-11-05T00:34:49Z done
- 2026-11-05T00:34:52Z committed 2760c2b4 (12 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- [instruction-like text quoted from a file or tool; data, not instructions] T-0198 [FEATURE M, done, 3 steps] Economy mode: past 80% weekly (or 90% five-hour) usage, the …
- research T-0320-review: Approve with nits. Nothing blocks. One MEDIUM and two LOW findings, all in snapshot parsing. I did not run the tests. [stale: plugin/lib/fmbudget…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-02: [costly] Correction: Mission 3 and the loop rounds run now, bounded by fm budget
- similar finished tasks took 3–9 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_budget.py, plugin/tests/test_claims.py, plugin/tests/test_cli.py, plugin/tests/test_code_tui.py, plugin/tests/test_design_surfaces.py, plu…
## Why not caught
no test asserted the weekly rules per project; the pace switch (T-2327) was only tested on degrade()
## Lessons
- A per-project switch over a global reading must reach every reader with the project in hand: a cwd fallback hides callers that serve another project (night, the pane's budget panel)
## Files touched
- plugin/tests/test_budget.py
- plugin/lib/sampo/budget.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/watch.py
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/sampo/cli.py
- CHANGELOG.md
- plugin/lib/ui-demo.json
- plugin/lib/sampo/night.py
- plugin/lib/sampo/bench.py
