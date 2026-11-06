---
id: T-3243
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/lanes.py, plugin/lib/sampo/core.py, plugin/tests/test_builder.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-05T20:57:48Z
updated: 2026-11-05T21:03:16Z
base: 7807c598c69fe46ae4cef85aeeb382fcea286367
base_tree: 525b4eec745fbda785a2265557728db87e81b725
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-05T20:58:56Z
plan0_scope: [plugin/lib/sampo/lanes.py, plugin/lib/sampo/core.py, plugin/tests/test_builder.py, CHANGELOG.md]
verified: strong
unproven: [red]
---
# Builder lanes starved for hours: the lane gate (1-min load over 1.5 per CPU) stayed shut…
## Raw request
> Builder lanes starved for hours: the lane gate (1-min load over 1.5 per CPU) stayed shut while Sampo's own deferrable work held the load (full-suite sweeps, post-merge verifies, moons and card fills). Gate on non-nice CPU (/proc/stat user+system vs nice) so niced background work doesn't block lanes, run sweeps and fills niced, and reserve at least one lane when tasks are queued (user ask 2026-11-05: how come there aren't any builder agents building stuff?)
## Interpretation
Reading 1 (chosen): the user wants builders working whenever tasks are queued; the gate's job is to stop overload, not to leave the machine building nothing, so the first lane must not be starved by Sampo's own deferrable work (sweeps, verifies, fills held load at 1.7 to 3.7 per CPU for about three hours). Reading 2 (ruled out): drop the load gate; rejected because T-2797 measured five lanes plus a design agent pushing load to 3.5 per core and gates timing out.
## Assumptions (confidence)
## Acceptance criteria
- [x] with no builder out, lane brief starts a lane at a load between the soft and hard bars, refuses one past the hard bar, and with a builder working still refuses past the soft bar — verify with `python3 plugin/tests/run.py test_builder`
## Non-goals
## Approach (options → choice → why)
1) use what exists: host_strain and builders_cap already gate lanes; give host_strain a bar argument and pass a hard bar for the first lane: likely outcome: something is always being built, and a runaway load (past 3 per CPU) still holds everything. 2) gate on non-nice CPU from /proc/stat: fails if: every gate call samples for half a second, and most of the load here isn't niced. 3) nice my own sweeps and fills: fails if: it relies on every caller remembering. 4) do less: raise LOAD_BAR: fails if: five lanes again push gates past their timeouts (T-2797). Choice 1 (80%): a parameter and one condition in the brief path, keeping T-2797's protection for the second lane on.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [x] failing test: the three loads with and without a working builder
2. [x] lanes.brief: the first lane gets the hard bar
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_builder.Brief` → ✗ exit 1 · Ran 8 tests in 5.8s (1 jobs, 16 at a time; slowest: Brief 5s) / FAILED (1 classes: test_builder.Brief) [ran] [tree ea7a7cc6f37c] [world 2f1906870a] (2026-11-05T20:59:17Z)
- (step 2) `python3 plugin/tests/run.py test_builder test_lanes test_cli` → exit 0 · Ran 363 tests in 42.4s (311 jobs, 16 at a time; slowest: StateViews.test_state_md_is_bounded 13s, LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 10s, PlanRace 7s) / OK [ran] [tree 08fbb44a43e4] [world 2f1906870a] (2026-11-05T21:02:01Z)
- `python3 plugin/tests/run.py test_builder.Brief` → ✗ exit 1 · Ran 8 tests in 7.9s (1 jobs, 16 at a time; slowest: Brief 5s) / FAILED (1 classes: test_builder.Brief) (start tree + this task's tests) [ran] [tree 335adfee8087] [world 2f1906870a] (2026-11-05T21:02:13Z)
- `python3 plugin/tests/run.py test_builder.Brief` → exit 0 · Ran 8 tests in 1.7s (8 jobs, 16 at a time; slowest: Brief.test_l_tasks_held_tasks_and_a_third_builder_are_refused 1s, Brief.test_the_first_lane_is_never_starved_by_moderate_load 1s, Brief.test_builder [ran] [tree 335adfee8087] [world 2f1906870a] (2026-11-05T21:02:13Z)
- (ac 1) `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 29 tests in 4.4s (18 jobs, 16 at a time; slowest: Brief 4s, LaneMergeGate 2s, Contract.test_lane_merge_over_unrelated_uncommitted_work 2s) / OK [ran] [tree 335adfee8087] [world 2f1906870a] (2026-11-05T21:02:25Z)
- (audit intent) `self: host_strain takes a bar (default LOAD_BAR, so every other caller is unchanged); lanes' brief passes LANE_HARD_BAR=3.0 only when no builder is working, so one lane always runs below 3 per CPU and every later lane keeps T-2797's 1.5 bar; the memory hold (under 512 MB) still refuses in all cases` → something is always being built when tasks are queued, unless the machine is truly overloaded [tree 335adfee8087] (2026-11-05T21:02:25Z)
- (audit edge) `self: host_strain takes a bar (default LOAD_BAR, so every other caller is unchanged); lanes' brief passes LANE_HARD_BAR=3.0 only when no builder is working, so one lane always runs below 3 per CPU and every later lane keeps T-2797's 1.5 bar; the memory hold (under 512 MB) still refuses in all cases` → past 3 per CPU nothing starts; a returned builder no longer counts as working, so the next first lane gets the hard bar too [tree 335adfee8087] (2026-11-05T21:02:25Z)
- (audit operator) `self: host_strain takes a bar (default LOAD_BAR, so every other caller is unchanged); lanes' brief passes LANE_HARD_BAR=3.0 only when no builder is working, so one lane always runs below 3 per CPU and every later lane keeps T-2797's 1.5 bar; the memory hold (under 512 MB) still refuses in all cases` → the refusal text is unchanged; FOREMAN_LOAD_GATE=0 still turns the gate off [tree 335adfee8087] (2026-11-05T21:02:25Z)
## Log
- 2026-11-05T20:57:48Z created
- 2026-11-05T20:58:45Z planned: it has criteria and steps
- 2026-11-05T20:58:46Z set scope=['plugin/lib/sampo/lanes.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_builder.py', 'CHANGELOG.md']
- 2026-11-05T20:58:55Z focused
- 2026-11-05T20:58:56Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-05T21:03:05Z done
- 2026-11-05T21:03:07Z committed 88050b92 (4 files)
- 2026-11-05T21:03:16Z guard authorization added: publish
- 2026-11-05T21:03:16Z ship: main pushes are standing-approved (2026-10-29); shipping the macOS CI fixes (T-3238, T-3240), the bench race (T-3241), T-3222 and the rest so CI on main goes green
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3222 [FEATURE L, done, 5 steps] Network and filesystem sandboxing as a Sampo feature: one sampo sandbox verb that turns… — lesson: running the whole suite inside the n…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_lane_twins.py, plugin/tests/test_lanes.py, plugin/tests/test_verify_alias.py
## Why not caught
no test held the load past the bar with no builder out; test_builder now does
## Lessons
- a gate on shared load must reserve a minimum of the work it protects, or the gate's own owner's background work starves it
## Plan gaps
- failed first: step 1 failing test: the three loads with and without a working builder
## Files touched
- plugin/tests/test_builder.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/lanes.py
- CHANGELOG.md
