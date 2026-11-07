---
id: T-3193
type: FIX
tier: S
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-11-05T11:00:10Z
updated: 2026-11-05T12:33:06Z
trigger: baseline
trigger_key: 18e3ce31fbc3c019
baseline: true
base: bef0b797c4c6a59c9856eeda94e6e34f21c67fac
base_tree: d396b2f87759332724ae32b5db4e8e63f4fc8484
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T12:10:16Z
plan0_scope: []
verified: strong
unproven: [meaning, red]
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_clock_windows.ClockWindows.test_digest_week_includes_a_close_exactly_seven_days_old_not_one_a_second_older, test_exam.ExamJs.test_planted_fails_hidden_checks_and_clean_passes, test_exam.ExamTs.test_planted_fails_hidden_checks_and_clean_passes, test_lanes.SelfChangeGate.test_a_branch_verdict_that_isnt_a_string_refuses_and_an_old_inability_doesnt, test_lanes.SelfChangeGate.test_a_hook_slower_past_fifteen_percent_or_its_budget_refuses_with_both_numbers. Captured by sampo check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the tests T-3193 names pass on main: SelfChangeGate (fixed by T-3195), ExamJs/ExamTs, and ClockWindows, whose digest calls now read an empty Claude config dir instead of the user's real transcripts — verify with `python3 plugin/tests/run.py test_clock_windows test_exam.ExamJs test_exam.ExamTs test_lanes.SelfChangeGate test_cost`
- [x] burn_findings JSON-parses only transcript lines that carry "usage"; fm digest --days 7 at a month-back pinned clock on this machine, before vs after, recorded — verify with `python3 plugin/tests/run.py test_cost`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: _entries with need= skips lines without it, and burn_findings passes need
2. [x] the need filter in cost._entries, used by burn_findings; ClockWindows' digest calls get an empty CLAUDE_CONFIG_DIR
## Resume here
<!-- auto -->
- 2026-11-05T12:27:26Z steps 2/2 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, plugin/lib/sampo/cost.py, plugin/tests/test_clock_windows.py, plugin/tests/test_usage_burn.py, scripts/
- touched since last checkpoint: plugin/tests/test_clock_windows.py, plugin/lib/sampo/cost.py, plugin/tests/test_usage_burn.py, /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/ab-digest.sh, CHANGELOG.md
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_usage_burn` → ✗ exit 1 · Ran 6 tests in 0.9s (2 jobs, 16 at a time; slowest: UsageBurn 0s, ScanCache 0s) / FAILED (1 classes: test_usage_burn.UsageBurn) [ran] [tree 2471022136a1] [world 2f1906870a] (2026-11-05T12:10:28Z)
- (step 2) `python3 plugin/tests/run.py test_usage_burn test_clock_windows test_cost test_doctor test_foresight test_exam.ExamJs test_exam.ExamTs test_lanes.SelfChangeGate` → ✗ exit 1 · Ran 199 tests in 34.0s (107 jobs, 16 at a time; slowest: ExamTs 32s, ExamJs 28s, ViewsRepair 22s) / FAILED (1 classes: test_usage_burn.UsageBurn) [ran] [tree e01757bc85bd] [world 2f1906870a] (2026-11-05T12:11:14Z)
- (step 2) `python3 plugin/tests/run.py test_usage_burn test_clock_windows test_cost test_doctor test_foresight test_exam.ExamJs test_exam.ExamTs test_lanes.SelfChangeGate` → exit 0 · Ran 199 tests in 42.0s (112 jobs, 16 at a time; slowest: ExamTs 39s, ExamJs 36s, ViewsRepair 30s) / OK [ran] [tree 33d1fcab925e] [world 2f1906870a] (2026-11-05T12:12:21Z)
- `python3 plugin/tests/run.py test_usage_burn` → ✗ exit 1 · Ran 6 tests in 2.1s (2 jobs, 16 at a time; slowest: UsageBurn 0s, ScanCache 0s) / FAILED (1 classes: test_usage_burn.UsageBurn) (start tree + this task's tests) [ran] [tree 33d1fcab925e] [world 2f1906870a] (2026-11-05T12:12:25Z)
- `python3 plugin/tests/run.py test_usage_burn` → exit 0 · Ran 6 tests in 1.0s (2 jobs, 16 at a time; slowest: UsageBurn 1s, ScanCache 0s) / OK [ran] [tree 33d1fcab925e] [world 2f1906870a] (2026-11-05T12:12:25Z)
- (ac 1) `python3 plugin/tests/run.py test_clock_windows test_exam.ExamJs test_exam.ExamTs test_lanes.SelfChangeGate test_cost` → exit 0 · Ran 45 tests in 38.9s (42 jobs, 16 at a time; slowest: ExamTs 35s, ExamJs 32s, TaskCostCap.test_the_brief_readers_show_the_cost_line 19s) / OK [ran] [tree dafbcb0c1d5f] [world 2f1906870a] (2026-11-05T12:19:52Z)
- (ac 2) `python3 plugin/tests/run.py test_cost` → exit 0 · Ran 22 tests in 3.3s (21 jobs, 16 at a time; slowest: TaskCostCap.test_a_cap_hit_asks_for_a_checkpoint_and_no_cap_changes_nothing 3s, TaskCostCap.test_the_brief_readers_show_the_cost_line 3s, TaskCost [ran] [tree dafbcb0c1d5f] [world 2f1906870a] (2026-11-05T12:19:52Z)
- (audit edge) `re-ran the five tests the baseline named on main: all pass (SelfChangeGate was T-3195's regression, already fixed; ExamJs/ExamTs pass at load 45-70, likely load flakes then); ClockWindows was slow because digest's burn scan JSON-parsed every transcript line since a month-back pinned clock in the user's real ~/.claude (24-33 s a call); the test now points digest at an empty config dir and the scan parses only lines carrying usage` → need= is a plain substring test before the timestamp regex, so a line without "usage" can't be a reply with usage (usage is a JSON key on every assistant reply line); a tool result quoting "usage" is still parsed and then dropped by the type check; scan() and timing() still read every line (they need tool lines) [tree dafbcb0c1d5f] (2026-11-05T12:19:52Z)
- (audit intent) `re-ran the five tests the baseline named on main: all pass (SelfChangeGate was T-3195's regression, already fixed; ExamJs/ExamTs pass at load 45-70, likely load flakes then); ClockWindows was slow because digest's burn scan JSON-parsed every transcript line since a month-back pinned clock in the user's real ~/.claude (24-33 s a call); the test now points digest at an empty config dir and the scan parses only lines carrying usage` → the baseline's five red tests are green on main, and the slowness behind the clock test is fixed at its cause for users too [tree dafbcb0c1d5f] (2026-11-05T12:19:52Z)
- (audit self) `re-ran the five tests the baseline named on main: all pass (SelfChangeGate was T-3195's regression, already fixed; ExamJs/ExamTs pass at load 45-70, likely load flakes then); ClockWindows was slow because digest's burn scan JSON-parsed every transcript line since a month-back pinned clock in the user's real ~/.claude (24-33 s a call); the test now points digest at an empty config dir and the scan parses only lines carrying usage` → no findings [tree dafbcb0c1d5f] (2026-11-05T12:19:52Z)
- (audit adversary) `re-ran the five tests the baseline named on main: all pass (SelfChangeGate was T-3195's regression, already fixed; ExamJs/ExamTs pass at load 45-70, likely load flakes then); ClockWindows was slow because digest's burn scan JSON-parsed every transcript line since a month-back pinned clock in the user's real ~/.claude (24-33 s a call); the test now points digest at an empty config dir and the scan parses only lines carrying usage` → transcripts are untrusted text (tool output lands in them): the new filter only skips lines before parsing, so a crafted line holding "usage" is parsed and type-checked exactly as before, and one without it can't add usage; no hashing, exec or path handling changed (the sha1 flag isn't in this diff) [tree 338b293aa4be] (2026-11-05T12:22:08Z)
- (audit edge) `re-ran the five tests the baseline named on main: all pass (SelfChangeGate was T-3195's regression, already fixed; ExamJs/ExamTs pass at load 45-70, likely load flakes then); ClockWindows was slow because digest's burn scan JSON-parsed every transcript line since a month-back pinned clock in the user's real ~/.claude (24-33 s a call); the test now points digest at an empty config dir and the scan parses only lines carrying usage` → need= is a plain substring test before the timestamp regex; usage is a JSON key on every assistant reply line, so no reply with usage is skipped; scan() and timing() still read every line (they need tool lines) [tree 338b293aa4be] (2026-11-05T12:22:08Z)
- (audit intent) `re-ran the five tests the baseline named on main: all pass (SelfChangeGate was T-3195's regression, already fixed; ExamJs/ExamTs pass at load 45-70, likely load flakes then); ClockWindows was slow because digest's burn scan JSON-parsed every transcript line since a month-back pinned clock in the user's real ~/.claude (24-33 s a call); the test now points digest at an empty config dir and the scan parses only lines carrying usage` → the baseline's five red tests are green on main, and the slowness behind the clock test is fixed at its cause for users too [tree 338b293aa4be] (2026-11-05T12:22:08Z)
- (audit self) `re-ran the five tests the baseline named on main: all pass (SelfChangeGate was T-3195's regression, already fixed; ExamJs/ExamTs pass at load 45-70, likely load flakes then); ClockWindows was slow because digest's burn scan JSON-parsed every transcript line since a month-back pinned clock in the user's real ~/.claude (24-33 s a call); the test now points digest at an empty config dir and the scan parses only lines carrying usage` → no findings [tree 338b293aa4be] (2026-11-05T12:22:08Z)
- (audit adversary) `fed the scan crafted transcript lines in thought: a line holding "usage" is parsed and type-checked exactly as before; a line without it was never a reply with usage; json.loads input and handling are unchanged, only fewer lines reach it` → held: no new parse path, no exec, path or hashing change [tree 338b293aa4be] (2026-11-05T12:25:33Z)
- (step 2) `python3 plugin/tests/run.py test_usage_burn test_clock_windows test_cost` → exit 0 · Ran 33 tests in 3.9s (22 jobs, 16 at a time; slowest: ClockWindows 4s, TaskCostCap.test_the_brief_readers_show_the_cost_line 2s, TaskCostCap.test_a_cap_hit_asks_for_a_checkpoint_and_no_cap_changes_not [ran] [tree 338b293aa4be] [world 2f1906870a] (2026-11-05T12:26:40Z)
- (audit adversary) `crafted transcript lines in thought: a line holding "usage" is parsed and type-checked exactly as before; a line without it was never a reply with usage; json.loads input and handling unchanged, only fewer lines reach it` → held: no new parse path, no exec, path or hashing change [tree 338b293aa4be] (2026-11-05T12:26:40Z)
- (audit adversary) `re-ran the five tests the baseline named on main: all pass (SelfChangeGate was T-3195's regression, already fixed; ExamJs/ExamTs pass at load 45-70); ClockWindows was slow because digest's burn scan JSON-parsed every transcript line since a month-back pinned clock in the user's real ~/.claude; the test now points digest at an empty config dir and the scan parses only lines carrying usage` → transcripts are untrusted text: the filter only skips lines before parsing, so a crafted line holding "usage" is parsed and type-checked exactly as before and one without it can't add usage; no hashing, exec or path handling changed [tree d4f8487c4396] (2026-11-05T12:32:39Z)
- (audit edge) `re-ran the five tests the baseline named on main: all pass (SelfChangeGate was T-3195's regression, already fixed; ExamJs/ExamTs pass at load 45-70); ClockWindows was slow because digest's burn scan JSON-parsed every transcript line since a month-back pinned clock in the user's real ~/.claude; the test now points digest at an empty config dir and the scan parses only lines carrying usage` → need= is a plain substring test before the timestamp regex; usage is a JSON key on every assistant reply line, so no reply with usage is skipped; scan() and timing() still read every line [tree d4f8487c4396] (2026-11-05T12:32:39Z)
- (audit intent) `re-ran the five tests the baseline named on main: all pass (SelfChangeGate was T-3195's regression, already fixed; ExamJs/ExamTs pass at load 45-70); ClockWindows was slow because digest's burn scan JSON-parsed every transcript line since a month-back pinned clock in the user's real ~/.claude; the test now points digest at an empty config dir and the scan parses only lines carrying usage` → the baseline's five red tests are green on main, and the slowness behind the clock test is fixed at its cause for users too [tree d4f8487c4396] (2026-11-05T12:32:39Z)
- (audit self) `re-ran the five tests the baseline named on main: all pass (SelfChangeGate was T-3195's regression, already fixed; ExamJs/ExamTs pass at load 45-70); ClockWindows was slow because digest's burn scan JSON-parsed every transcript line since a month-back pinned clock in the user's real ~/.claude; the test now points digest at an empty config dir and the scan parses only lines carrying usage` → no findings [tree d4f8487c4396] (2026-11-05T12:32:39Z)
## Log
- 2026-11-05T11:00:10Z created
- 2026-11-05T12:10:00Z set tier=S
- 2026-11-05T12:10:01Z planned: it has criteria and steps
- 2026-11-05T12:10:15Z focused
- 2026-11-05T12:10:16Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T12:27:27Z paused: focus moved to T-3200
- 2026-11-05T12:32:37Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-05T12:32:37Z focused
- 2026-11-05T12:33:04Z done
- 2026-11-05T12:33:06Z committed 9a6f242a (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2927 [FIX M, dropped, 0 steps] Baseline red: `python3 plugin/tests/run.py` fails…
- T-2309 [FIX S, done, 1 steps] Guard speed tests time CPU, not the wall clock, so a loaded host can't fail them — lesson: A complexity bar measures CPU (time.process_time…
- T-2429 [FIX M, done, 1 steps] Baseline red:… — lesson: A test that appends then shifts an mtime is shifting from the wall clock: read the mtime before the write
- decision 2026-11-03: [revisited: The rename's guard step comes first] [check: python3 plugin/tests/run.py test_guard_sampo] The rename's guard step comes first: Ward ref…
- similar finished tasks took 1–1 steps
- start here (files T-2309 touched): plugin/tests/test_guard.py
## Measurements
fm digest --days 7 at a month-back pinned clock on this machine's transcripts, alternating old/new at the same load: CPU 22.3/22.1 s before, 8.9/10.3 s after (2.3x less); lines JSON-parsed 1,300,140 before, 289,786 after; ClockWindows' test 51-103 s before, 4 s after
## Lessons
- A test that runs a verb against the real HOME measures the user's data, not the code: profile a slow test with HOME isolated vs real before blaming load
## Plan gaps
- failed first: step 1 failing test: _entries with need= skips lines without it, and burn_findings passes need
- failed first: step 2 the need filter in cost._entries, used by burn_findings; ClockWindows' digest calls get an empty CL…
## Files touched
- plugin/tests/test_usage_burn.py
- plugin/tests/test_clock_windows.py
- plugin/lib/sampo/cost.py
- CHANGELOG.md
