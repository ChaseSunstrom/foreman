---
id: T-2338
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/lib/fmoutcomes.py, plugin/lib/fmsecond.py, plugin/tests, plugin/skills/intake/references/planning.md, MASTER.md]
depends_on: [T-2337]
source: user
created: 2026-10-31T13:58:35Z
updated: 2026-10-31T16:41:52Z
builder_model: sonnet
base: 29838df1224c78cb4bc23af46456bc6d31e53196
base_tree: e7e6af292a2a964bee606054b72f4308dcf4231e
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T15:35:48Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_core.py, plugin/tests/test_reasoning.py, plugin/tests/test_judgment.py]
lane_stop: merged 2026-10-31T16:30:21Z
verified: strong
---
# Confidence routes the next step (Mission 5, #8): an M/L choice states a confidence; an assumption under the research bar needs research, a spike or a verified check before focus; a choice under the race bar with a runner-up sends fm next to a race before any edit; fm decide takes --confidence
## Raw request
> Confidence routes the next step (Mission 5, #8): an M/L choice states a confidence; an assumption under the research bar needs research, a spike or a verified check before focus; a choice under the race bar with a runner-up sends fm next to a race before any edit; fm decide takes --confidence
## Interpretation
Reading 1: gen-0 #8's 'states confidence, researches when unsure' as a routing rule: one number per M/L choice (and any assumption) decides the next action: act, research, or race. Reading 2: keep T-2269's '(low)' tag and wait for the model to use it. It fired 0 times: 5 briefs ever wrote an assumption, none '(low)'. Reading 1.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm focus refuses an unstarted M/L brief whose Approach choice states no confidence ('Choice 2 (70%): why'); an assumption marked '(NN%)' under the research bar (default 60 until the ledger raises it) or '(low)' needs evidence first: an answer copied onto its line from a research note or a closed spike, or fm task assume ID verify N --run CMD exiting 0 where fmcore.lint_verify finds nothing wrong with CMD, its output recorded; then a cold tool-less child (fmsecond's reader) that sees only the assumption and that evidence must agree it holds, and a disagreement or a failed child keeps it open; typed evidence and an open spike don't count; each cleared assumption stays a ledger row scored later; each gap names its fix; S is untouched; the stated numbers go to the ledger once at first focus — verify with `python3 plugin/tests/run.py test_core -k ConfidenceRoutes`
- [x] fm next on an S/M task with no edits yet whose choice confidence is under the race bar (default 70) and whose Approach names a runner-up names fm lane race ID before any edit, once per task (raced or race_of tasks are never asked again), and on an L task names the design race (brief 6); the stuck rung (T-2271) and this trigger share one function; fm decide --confidence N writes the number into decisions.md and the ledger — verify with `python3 plugin/tests/run.py test_reasoning test_judgment -k Confidence`
## Non-goals
## Approach (options → choice → why)
1) a required number on the M/L choice plus optional numbers on assumptions, routed by bars from the ledger (brief 3); fails if: the model writes 90% on everything, which the ledger scores against the base rate, and a flat 90% that holds 60% moves the bar. 2) use what exists: '(low)' only; fails if: a free tag is never written (0 in 2332 briefs). 3) do less: research only, no race trigger; fails if: #2's 'choose by evidence' stays stuck-only. 4) Foreman's own base-rate forecast in place of the model's number; fails if: it can't tell a hard task from an easy one of the same tier. Choice 1 (75%): one cheap number connects #8's research trigger and #2's race; S pays nothing, so depth scales with risk.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, MASTER.md, plugin/tests/test_cli.py, plugin/lib/fmhooks.py, plugin/tests/test_hooks.py; past FIXes T-0875, T-0876, T-0880, T-0907, T-0908.
## Execution prompt
## Steps
1. [x] red tests (test_core ConfidenceRoutes; test_reasoning and test_judgment Confidence): no confidence refused; a 50% assumption refused until research/spike/verified; an 85% one passes; a 60% choice with a runner-up makes fm next name the race; a raced task isn't asked twice; fm decide --confidence recorded
2. [x] one confidence parser (Choice and assumption lines, '(low)' kept as an alias) feeding _content_gaps
3. [x] the race trigger in fm next, merged with stuck_rung's race rung; fm decide --confidence
4. [x] docs: planning.md, MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T16:22:53Z step 1/4: red tests (test_core ConfidenceRoutes; test_reasoning and test_judgment Confidence): no confidence refused; a 50% assumption refused until research/spike/verified; an 85% one passes; a 60% choice with a runner-up makes fm next name the race; a raced task isn't asked twice; fm decide --confidence recorded
- git: worktree-agent-a2ee2c5c192a38336; 2 uncommitted: plugin/lib/fmcli.py, plugin/tests/test_core.py
- touched since last checkpoint: plugin/tests/test_core.py, plugin/lib/fmcli.py
## Docs impact
CHANGELOG.md, MASTER.md (builder)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core -k ConfidenceRoutes` → ✗ exit 1 · Ran 12 tests in 16.3s (1 classes, 16 at a time; slowest: ConfidenceRoutes 13s) / FAILED (1 classes: test_core.ConfidenceRoutes) [ran] [tree 8ccd9f4b2ea3] (2026-10-31T15:45:28Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k ConfidenceRoutes 2>&1 | tail -40` → exit 0 · Ran 12 tests in 4.5s (1 classes, 16 at a time; slowest: ConfidenceRoutes 4s) / OK [ran] [tree a815e3f82808] (2026-10-31T15:52:29Z)
- (step 2) `python3 plugin/tests/run.py test_core -k ConfidenceRoutes` → exit 0 · Ran 12 tests in 4.4s (1 classes, 16 at a time; slowest: ConfidenceRoutes 4s) / OK [ran] [tree a815e3f82808] (2026-10-31T15:52:36Z)
- (ac 2) `python3 plugin/tests/run.py test_reasoning test_judgment -k Confidence 2>&1 | tail -20` → ✗ exit 1 · Ran 14 tests in 6.0s (2 classes, 16 at a time; slowest: Confidence 5s, Confidence 1s) / FAILED (1 classes: test_reasoning.Confidence) [ran] [tree 374bf7c7e53b] (2026-10-31T15:55:01Z)
- (ac 2) `python3 plugin/tests/run.py test_reasoning test_judgment -k Confidence 2>&1 | tail -20` → ✗ exit 1 · Ran 14 tests in 5.9s (2 classes, 16 at a time; slowest: Confidence 5s, Confidence 1s) / FAILED (1 classes: test_reasoning.Confidence) [ran] [tree 9809d42e74fc] (2026-10-31T15:55:15Z)
- (ac 2) `python3 plugin/tests/run.py test_reasoning test_judgment -k Confidence 2>&1 | tail -20` → exit 0 · Ran 14 tests in 8.6s (2 classes, 16 at a time; slowest: Confidence 8s, Confidence 1s) / OK [ran] [tree 9bd85e31766d] (2026-10-31T15:55:28Z)
- (step 3) `python3 plugin/tests/run.py test_reasoning test_judgment -k Confidence 2>&1 | tail -20` → exit 0 · Ran 14 tests in 8.6s (2 classes, 16 at a time; slowest: Confidence 8s, Confidence 1s) / OK [ran] [tree 9bd85e31766d] (2026-10-31T15:55:28Z)
- (step 3) `python3 plugin/tests/run.py test_reasoning test_judgment -k Confidence` → exit 0 · Ran 14 tests in 7.6s (2 classes, 16 at a time; slowest: Confidence 7s, Confidence 1s) / OK [ran] [tree 9bd85e31766d] (2026-10-31T15:55:38Z)
- (step 4) `python3 plugin/tests/run.py test_core 2>&1 | grep -E "^(FAIL|ERROR)|Ran |OK|FAILED" | head -30` → exit 0 · Ran 127 tests in 7.8s (26 classes, 16 at a time; slowest: ConfidenceRoutes 7s, BriefIndex 4s, WritesAndLocks 2s) / OK [ran] [tree 27ed118d9c56] (2026-10-31T15:57:43Z)
- (step 4) `grep -c T-2338 plugin/skills/intake/references/planning.md` → exit 0 · 1 [ran] [tree 559e5972e15c] (2026-10-31T16:01:12Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_backlog test_board_surfaces test_board_verbs test_builder test_clean_helpers test_cli test_compact test_conflict_history test_core test_cost test_defect_classes test_deliberation test_design_surfaces test_design_tokens test_diagnosis test_docs test_doctor test_edit_cards test_evidence_quality test_extras test_followups test_graph test_guard test_guard_cases test_hooks test_ideation test_judgment test_lane_stall test_lanes test_lib_hostile test_lib_source_kill test_library test_metacog test_nudges test_onwrite test_outcomes test_pass4 test_paused test_playbook_use test_plugin_parity test_plugins test_reasoning test_recall test_replan test_robustness test_round_i test_runtime test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_splits test_steering test_supply_delta test_taste_ledger test_tidy test_trust test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2057 tests in 278.1s (483 classes, 16 at a time; slowest: Stop 191s, Recall 100s, Scout 87s) / FAILED (1 classes: test_outcomes.CalibrationLedgerBets) [ran] [tree 559e5972e15c] (2026-10-31T16:06:22Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_backlog test_board_surfaces test_board_verbs test_builder test_clean_helpers test_cli test_compact test_conflict_history test_core test_cost test_defect_classes test_deliberation test_design_surfaces test_design_tokens test_diagnosis test_docs test_doctor test_edit_cards test_evidence_quality test_extras test_followups test_graph test_guard test_guard_cases test_hooks test_ideation test_judgment test_lane_stall test_lanes test_lib_hostile test_lib_source_kill test_library test_metacog test_nudges test_onwrite test_outcomes test_pass4 test_paused test_playbook_use test_plugin_parity test_plugins test_reasoning test_recall test_replan test_robustness test_round_i test_runtime test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_splits test_steering test_supply_delta test_taste_ledger test_tidy test_trust test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [25.45s] [ran] [tree 05662881ae7c] (2026-10-31T16:13:11Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k ConfidenceRoutes 2>&1 | grep -E "^(FAIL|ERROR):|^OK|FAILED|Error" | head` → exit 0 · OK [ran] [tree 665f9196b277] (2026-10-31T16:22:46Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_away test_backlog test_board_surfaces test_board_verbs test_builder test_clean_helpers test_cli test_compact test_conflict_history test_core test_cost test_defect_classes test_deliberation test_design_surfaces test_design_tokens test_diagnosis test_docs test_doctor test_drive_side test_edit_cards test_evidence_quality test_exam test_extras test_find test_followups test_goal test_graph test_guard test_guard_cases test_guard_evasions test_hooks test_ideation test_judgment test_lane_stall test_lanes test_lib_hostile test_lib_source_kill test_library test_memory test_metacog test_nudges test_onwrite test_outcomes test_pass4 test_paused test_playbook_use test_plugin_parity test_plugins test_prove test_reasoning test_recall test_replan test_robustness test_round_i test_runtime test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_splits test_statusline_ui test_steering test_supply_delta test_taste_ledger test_tidy test_tool_loop test_tool_taint test_trust test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [22.99s] [ran] [tree c46cc1152754] (2026-10-31T16:29:01Z)
- (step 1) `python3 plugin/tests/run.py test_core test_reasoning test_judgment test_outcomes test_second test_lanes` → exit 0 · Ran 323 tests in 25.6s (71 classes, 16 at a time; slowest: LaneRecovery 25s, Lanes 21s, Survival 18s) / OK [ran] [tree c7dd60c5055b] (2026-10-31T16:30:59Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k ConfidenceRoutes` → exit 0 · Ran 15 tests in 21.2s (1 classes, 16 at a time; slowest: ConfidenceRoutes 20s) / OK [ran] [tree 246325a57026] (2026-10-31T16:32:02Z)
- (ac 2) `python3 plugin/tests/run.py test_reasoning test_judgment -k Confidence` → exit 0 · Ran 15 tests in 15.4s (2 classes, 16 at a time; slowest: Confidence 15s, Confidence 2s) / OK [ran] [tree 246325a57026] (2026-10-31T16:32:02Z)
- (audit intent) `fm-reviewer pass (intent, adversary, edge, operator, maintainer) on the lane diff; HIGH forged-mark and 4 LOW fixed test-first in b6fa01bf before merge` → Choice N (NN%) gap, research/race bars from fmoutcomes.bars(), race_ask for S/M and L [tree 246325a57026] (2026-10-31T16:32:02Z)
- (audit adversary) `fm-reviewer pass (intent, adversary, edge, operator, maintainer) on the lane diff; HIGH forged-mark and 4 LOW fixed test-first in b6fa01bf before merge` → cold-read mark stripped under both section names; evidence fenced as data, verdict from the last line only [tree 246325a57026] (2026-10-31T16:32:02Z)
- (audit edge) `fm-reviewer pass (intent, adversary, edge, operator, maintainer) on the lane diff; HIGH forged-mark and 4 LOW fixed test-first in b6fa01bf before merge` → a race that can't start gives the released task back focused (mocked builder_brief failure) [tree 246325a57026] (2026-10-31T16:32:02Z)
- (audit maintainer) `fm-reviewer pass (intent, adversary, edge, operator, maintainer) on the lane diff; HIGH forged-mark and 4 LOW fixed test-first in b6fa01bf before merge` → stated_confidence shared by the plan gate and ledger; duplicate _CONF_RE captured as T-2427 [tree 246325a57026] (2026-10-31T16:32:02Z)
- (audit intent) `fm-reviewer pass (intent, adversary, edge, operator, maintainer) on the lane diff; HIGH forged-mark and 4 LOW fixed test-first in b6fa01bf before merge` → Choice N (NN%) gap, research/race bars from fmoutcomes.bars(), race_ask for S/M and L [tree 246325a57026] (2026-10-31T16:37:56Z)
- (audit adversary) `fm-reviewer pass (intent, adversary, edge, operator, maintainer) on the lane diff; HIGH forged-mark and 4 LOW fixed test-first in b6fa01bf before merge` → cold-read mark stripped under both section names; evidence fenced as data, verdict from the last line only [tree 246325a57026] (2026-10-31T16:37:56Z)
- (audit edge) `fm-reviewer pass (intent, adversary, edge, operator, maintainer) on the lane diff; HIGH forged-mark and 4 LOW fixed test-first in b6fa01bf before merge` → a race that can't start gives the released task back focused (mocked builder_brief failure) [tree 246325a57026] (2026-10-31T16:37:56Z)
- (audit maintainer) `fm-reviewer pass (intent, adversary, edge, operator, maintainer) on the lane diff; HIGH forged-mark and 4 LOW fixed test-first in b6fa01bf before merge` → stated_confidence shared by the plan gate and ledger; duplicate _CONF_RE captured as T-2427 [tree 246325a57026] (2026-10-31T16:37:56Z)
## Log
- 2026-10-31T13:58:35Z created
- 2026-10-31T14:06:08Z criterion 1 text: fm focus refuses an unstarted M/L brief whose Approach choice states no confidence ('Choice 2 (70%): why'); an assumption marked '(NN%)' under the research bar (default 60 until the ledger sets it) or '(low)' needs research/NAME, 'spike T-NNNN' or [verified: …] first; each gap names its fix; S is untouched; the stated numbers go to the ledger once at first focus → fm focus refuses an unstarted M/L brief whose Approach choice states no confidence ('Choice 2 (70%): why'); an assumption marked '(NN%)' under the research bar (default 60 until the ledger raises it) or '(low)' is cleared only by a research note that exists (research/NAME), a spike task that exists ('spike T-NNNN'), or a ran check (fm task assume ID verify N --run CMD exiting 0); typed evidence (--evidence) doesn't clear it; each gap names its fix; S is untouched; the stated numbers go to the ledger once at first focus
- 2026-10-31T14:11:41Z criterion 1 text: fm focus refuses an unstarted M/L brief whose Approach choice states no confidence ('Choice 2 (70%): why'); an assumption marked '(NN%)' under the research bar (default 60 until the ledger raises it) or '(low)' is cleared only by a research note that exists (research/NAME), a spike task that exists ('spike T-NNNN'), or a ran check (fm task assume ID verify N --run CMD exiting 0); typed evidence (--evidence) doesn't clear it; each gap names its fix; S is untouched; the stated numbers go to the ledger once at first focus → fm focus refuses an unstarted M/L brief whose Approach choice states no confidence ('Choice 2 (70%): why'); an assumption marked '(NN%)' under the research bar (default 60 until the ledger raises it) or '(low)' is cleared only by a research note that names the assumption's subject with its answer copied onto the line ([verified|false: research/NAME: …]; false sends the plan back), a spike task that exists, or fm task assume ID verify N --run CMD exiting 0 where fmcore.lint_verify finds nothing wrong with CMD (true, echo or a pipe that hides the exit don't clear it); typed evidence doesn't clear it; each cleared assumption stays a ledger row scored later; each gap names its fix; S is untouched; the stated numbers go to the ledger once at first focus
- 2026-10-31T14:17:15Z criterion 1 text: fm focus refuses an unstarted M/L brief whose Approach choice states no confidence ('Choice 2 (70%): why'); an assumption marked '(NN%)' under the research bar (default 60 until the ledger raises it) or '(low)' is cleared only by a research note that names the assumption's subject with its answer copied onto the line ([verified|false: research/NAME: …]; false sends the plan back), a spike task that exists, or fm task assume ID verify N --run CMD exiting 0 where fmcore.lint_verify finds nothing wrong with CMD (true, echo or a pipe that hides the exit don't clear it); typed evidence doesn't clear it; each cleared assumption stays a ledger row scored later; each gap names its fix; S is untouched; the stated numbers go to the ledger once at first focus → fm focus refuses an unstarted M/L brief whose Approach choice states no confidence ('Choice 2 (70%): why'); an assumption marked '(NN%)' under the research bar (default 60 until the ledger raises it) or '(low)' is cleared only by an answer copied onto its line from a research note that names the assumption's subject or from a closed spike task ([verified|false: research/NAME or T-NNNN: …]; false sends the plan back), or by fm task assume ID verify N --run CMD exiting 0 where fmcore.lint_verify finds nothing wrong with CMD (true, echo or a pipe that hides the exit don't clear it); typed evidence and an open spike don't clear it; each cleared assumption stays a ledger row scored later; each gap names its fix; S is untouched; the stated numbers go to the ledger once at first focus
- 2026-10-31T14:22:27Z criterion 1 text: fm focus refuses an unstarted M/L brief whose Approach choice states no confidence ('Choice 2 (70%): why'); an assumption marked '(NN%)' under the research bar (default 60 until the ledger raises it) or '(low)' is cleared only by an answer copied onto its line from a research note that names the assumption's subject or from a closed spike task ([verified|false: research/NAME or T-NNNN: …]; false sends the plan back), or by fm task assume ID verify N --run CMD exiting 0 where fmcore.lint_verify finds nothing wrong with CMD (true, echo or a pipe that hides the exit don't clear it); typed evidence and an open spike don't clear it; each cleared assumption stays a ledger row scored later; each gap names its fix; S is untouched; the stated numbers go to the ledger once at first focus → fm focus refuses an unstarted M/L brief whose Approach choice states no confidence ('Choice 2 (70%): why'); an assumption marked '(NN%)' under the research bar (default 60 until the ledger raises it) or '(low)' needs evidence first: an answer copied onto its line from a research note or a closed spike, or fm task assume ID verify N --run CMD exiting 0 where fmcore.lint_verify finds nothing wrong with CMD, its output recorded; then a cold tool-less child (fmsecond's reader) that sees only the assumption and that evidence must agree it holds, and a disagreement or a failed child keeps it open; typed evidence and an open spike don't count; each cleared assumption stays a ledger row scored later; each gap names its fix; S is untouched; the stated numbers go to the ledger once at first focus
- 2026-10-31T15:35:27Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2338.builder.md
- 2026-10-31T15:35:45Z focused
- 2026-10-31T15:35:48Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T15:43:36Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmlanes.py', 'plugin/lib/fmoutcomes.py', 'plugin/lib/fmsecond.py', 'plugin/tests', 'plugin/skills/intake/references/planning.md', 'MASTER.md']
- 2026-10-31T16:02:35Z bars: read from fmoutcomes.bars() (research 70, race 55 as merged), not the brief's 60/70
- 2026-10-31T16:22:01Z steer: bars are fmoutcomes.bars() research 70, race 55 (T-2337); the AC's 60/70 defaults are superseded
- 2026-10-31T16:30:21Z merged worktree-agent-a2ee2c5c192a38336 (34 file(s))
- 2026-10-31T16:30:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2ee2c5c192a38336
- 2026-10-31T16:30:32Z focused
- 2026-10-31T16:37:54Z scope: files outside the globs came from the branch's merge of foreman/build (T-2354, T-2341, T-2385, T-2371, T-2333 work) and the changelog line; ANDON.md was created then deleted by the builder
- 2026-10-31T16:41:52Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2337-review: Changes needed.** Two acceptance criteria are not met: no bar check runs at finish, and Foreman's own evidence can still move a bar. I read the c…
- T-2337 [FEATURE M, done, 4 steps] Calibration ledger (Mission 5, #8): every stated confidence is a write-once bet scored later by signals Foreman didn't author, beside a…
- research mission-20261031-083832: Request: Mission 5, Genesis gen 1: 2. Exhaustive thinking. Before acting on anything non-trivial: list the readings of the request, eve…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-31): MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmlanes.py, plugin/lib/fmoutcomes.py, plugin/lib/fmsecond.py, plugin/skills/intake/references/planning.md, plugin/tests/bench_hooks.py…; re-ground the plan against them before editing
## Lessons
- A strip that keys on a section's full heading misses its short alias: normalize the name before any security check on it
## Plan gaps
- failed first: step 1 red tests (test_core ConfidenceRoutes; test_reasoning and test_judgment Confidence): no confidence …
## Files touched
- plugin/tests/helpers.py
- plugin/tests/test_core.py
- plugin/tests/test_reasoning.py
- plugin/tests/test_judgment.py
- plugin/lib/fmcore.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmcli.py
- plugin/lib/fmlanes.py
- plugin/tests/test_backlog.py
- plugin/tests/test_builder.py
- plugin/tests/test_clean_helpers.py
- plugin/tests/test_cli.py
- plugin/tests/test_conflict_history.py
- plugin/tests/test_defect_classes.py
- plugin/tests/test_deliberation.py
- plugin/tests/test_diagnosis.py
- plugin/tests/test_edit_cards.py
- plugin/tests/test_evidence_quality.py
- plugin/tests/test_graph.py
- plugin/tests/test_hooks.py
- plugin/tests/test_lane_stall.py
- plugin/tests/test_lanes.py
- plugin/tests/test_metacog.py
- plugin/tests/test_outcomes.py
- plugin/tests/test_pass4.py
- plugin/tests/test_recall.py
- plugin/tests/test_replan.py
- plugin/tests/test_round_i.py
- plugin/tests/test_runtime.py
- plugin/tests/test_second.py
