---
id: T-2339
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/tests/test_lanes.py, plugin/lib/fmcli.py, plugin/lib/fmoutcomes.py, plugin/tests/test_race.py, plugin/tests/test_outcomes.py, plugin/lib/fmcore.py, MASTER.md]
depends_on: [T-2338]
source: user
created: 2026-10-31T13:58:36Z
updated: 2026-10-31T16:44:39Z
rival_at: 2026-10-31T16:04:34Z
rival_split: true
builder_model: sonnet
base: 631a7682861b6384d1c04da80b3fdb428a068aff
base_tree: 246325a57026476ce789b28321d43b936b3b0ca6
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T16:12:37Z
plan0_scope: [plugin/lib/fmlanes.py, plugin/tests/test_lanes.py]
lane_stop: merged 2026-10-31T16:42:49Z
verified: strong
---
# Race at plan time, chosen by evidence (Mission 5, #2): fm lane race takes up to 3 sides from the Approach's options, refuses checks that already pass on the base, and ranks sides by the frozen checks, cross-examination (each side's new tests run on the other trees) and size; the pick is a ledger row
## Raw request
> Race at plan time, chosen by evidence (Mission 5, #2): fm lane race takes up to 3 sides from the Approach's options, refuses checks that already pass on the base, and ranks sides by the frozen checks, cross-examination (each side's new tests run on the other trees) and size; the pick is a ledger row
## Interpretation
Reading 1: gen-0 #2's 'generate several candidate fixes or designs, test them in parallel lanes, and choose by evidence' happens before work whenever the plan is unsure (brief 4's trigger), not only after 3 failed runs (T-2271). Reading 2: every M task races. Reading 2 doubles every M's cost against 'Scale the depth to the risk'. Reading 1. 0 races have started since fm lane race shipped (T-1069, 2026-10-16).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane race ID --sides 3 clones one side per named Approach option (2 by default, builder slots permitting) and each side's brief names the option it builds; a race whose frozen checks all pass on the base tree is refused with 'the checks can't tell the sides apart: add one that fails now' — verify with `python3 plugin/tests/run.py test_lanes -k PlanRace`
- [x] fm lane race ID --score ranks sides by frozen checks passed, then cross-examination (each side's added test files run against every other side's tree; a side whose tests fail another side while it passes theirs ranks up), then lines changed and files outside scope; identical diffs are reported as 'no real alternative'; fm lane pick records the pick as an fm decide row (winner, the evidence, the loser rejected), writes a race row (stated choice, winner, whether the first choice won) to the ledger, and puts the loser's option and reason into the winner's Approach — verify with `python3 plugin/tests/run.py test_lanes -k RaceEvidence`
## Non-goals
## Approach (options → choice → why)
1) widen fm lane race: N sides, base-tree refusal, cross-examination, ledger row; fails if: builders converge on one design, so each side's brief names its option and identical diffs are flagged. 2) use what exists: 2 sides scored on pass ratio then lines, add only the trigger; fails if: a tie on the task's own checks picks the smaller diff, not the better design. 3) do less: T-2271's stuck race only; fails if: it has never fired. 4) a judge model scores the designs; fails if: Foreman's model grading Foreman's work is an opinion, not evidence. Choice 1 (70%): evidence the sides produce themselves, deterministic, and Mission 4's lesson that a check that can't fail proves nothing becomes the base-tree refusal.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmhooks.py, plugin/tests/test_cli.py, README.md, plugin/tests/test_hooks.py; past FIXes T-0875, T-0876, T-0880, T-0907, T-0908.
## Execution prompt
## Steps
1. [x] red tests (test_lanes PlanRace, RaceEvidence): 3 sides from 3 options; base-passing checks refused; cross-examination ranks a side whose test catches the other's bug first; identical diffs flagged; pick writes the ledger row and the Approach note
2. [x] --sides N and the base-tree refusal in race()
3. [x] cross-examination in _side/score
4. [x] pick: ledger row, Approach note; docs: MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T16:31:05Z step 1/4: red tests (test_lanes PlanRace, RaceEvidence): 3 sides from 3 options; base-passing checks refused; cross-examination ranks a side whose test catches the other's bug first; identical diffs flagged; pick writes the ledger row and the Approach note
- git: worktree-agent-a0a779aa526da9d29; 2 uncommitted: plugin/lib/fmcore.py, plugin/lib/fmlanes.py
- touched since last checkpoint: plugin/lib/fmoutcomes.py, plugin/tests/test_lanes.py, plugin/tests/test_outcomes.py, MASTER.md, plugin/lib/fmcore.py, plugin/lib/fmlanes.py
## Docs impact
CHANGELOG.md, MASTER.md (builder)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes -k PlanRace` → ✗ exit 1 · Ran 5 tests in 1.5s (1 classes, 16 at a time; slowest: PlanRace 1s) / FAILED (1 classes: test_lanes.PlanRace) [ran] [tree 61ceeec3d1c2] (2026-10-31T16:14:49Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes -k PlanRace 2>&1 | tail -30` → ✗ exit 1 · Ran 5 tests in 3.1s (1 classes, 16 at a time; slowest: PlanRace 3s) / FAILED (1 classes: test_lanes.PlanRace) [ran] [tree 8f8c7343ea90] (2026-10-31T16:19:55Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes -k RaceEvidence 2>&1 | tail -40` → ✗ exit 1 · Ran 7 tests in 5.2s (1 classes, 16 at a time; slowest: RaceEvidence 5s) / FAILED (1 classes: test_lanes.RaceEvidence) [ran] [tree 304366630c93] (2026-10-31T16:20:13Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes -k RaceEvidence 2>&1 | tail -30` → exit 0 · Ran 7 tests in 8.9s (1 classes, 16 at a time; slowest: RaceEvidence 9s) / OK [ran] [tree 4f5addfd9fbd] (2026-10-31T16:20:26Z)
- (step 2) `python3 plugin/tests/run.py test_lanes -k PlanRace` → exit 0 · Ran 5 tests in 1.7s (1 classes, 16 at a time; slowest: PlanRace 1s) / OK [ran] [tree daf866aa8eab] (2026-10-31T16:21:59Z)
- (step 3) `python3 plugin/tests/run.py test_lanes -k RaceEvidence` → exit 0 · Ran 7 tests in 7.0s (1 classes, 16 at a time; slowest: RaceEvidence 7s) / OK [ran] [tree daf866aa8eab] (2026-10-31T16:22:06Z)
- (step 4) `python3 plugin/tests/run.py test_lanes test_race test_outcomes` → exit 0 · Ran 137 tests in 29.4s (22 classes, 16 at a time; slowest: LaneRecovery 29s, Lanes 26s, Survival 24s) / OK [ran] [tree daf866aa8eab] (2026-10-31T16:22:36Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_builder test_cli test_docs test_guard_cases test_lane_stall test_lanes test_outcomes test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [19.03s] [ran] [tree daf866aa8eab] (2026-10-31T16:23:35Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes -k PlanRace 2>&1 | tail -30` → ✗ exit 1 · Ran 9 tests in 14.9s (1 classes, 16 at a time; slowest: PlanRace 13s) / FAILED (1 classes: test_lanes.PlanRace) [ran] [tree 27ee3cb33401] (2026-10-31T16:34:42Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes -k PlanRace 2>&1 | tail -20` → exit 0 · Ran 9 tests in 11.9s (1 classes, 16 at a time; slowest: PlanRace 11s) / OK [ran] [tree 02ed6c8651c4] (2026-10-31T16:35:01Z)
- (step 1) `python3 plugin/tests/run.py test_lanes -k PlanRace` → exit 0 · Ran 10 tests in 10.6s (1 classes, 16 at a time; slowest: PlanRace 10s) / OK [ran] [tree 3bc289a0fb7f] (2026-10-31T16:39:36Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_backlog test_board_surfaces test_board_verbs test_builder test_clean_helpers test_cli test_compact test_conflict_history test_core test_cost test_defect_classes test_deliberation test_design_surfaces test_design_tokens test_diagnosis test_docs test_doctor test_edit_cards test_evidence_quality test_extras test_followups test_goal test_graph test_guard test_guard_cases test_hooks test_ideation test_judgment test_lane_stall test_lanes test_lib_hostile test_lib_source_kill test_library test_metacog test_nudges test_onwrite test_outcomes test_pass4 test_paused test_playbook_use test_plugin_parity test_plugins test_reasoning test_recall test_replan test_robustness test_round_i test_runtime test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_splits test_steering test_supply_delta test_taste_ledger test_tidy test_trust test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.43s] [ran] [tree 3bc289a0fb7f] (2026-10-31T16:42:03Z)
- (step 2) `python3 plugin/tests/run.py test_lanes -k RaceEvidence` → exit 0 · Ran 12 tests in 9.0s (1 classes, 16 at a time; slowest: RaceEvidence 9s) / OK [ran] [tree 3bc289a0fb7f] (2026-10-31T16:42:15Z)
- (step 1) `python3 plugin/tests/run.py test_lanes test_race test_reasoning test_outcomes` → exit 0 · Ran 168 tests in 21.8s (28 classes, 16 at a time; slowest: LaneRecovery 21s, Lanes 16s, Survival 14s) / OK [ran] [tree a504e4902264] (2026-10-31T16:43:17Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes -k PlanRace` → exit 0 · Ran 10 tests in 4.8s (1 classes, 16 at a time; slowest: PlanRace 4s) / OK [ran] [tree c3107e96427e] (2026-10-31T16:43:49Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes -k RaceEvidence` → exit 0 · Ran 12 tests in 11.3s (1 classes, 16 at a time; slowest: RaceEvidence 11s) / OK [ran] [tree c3107e96427e] (2026-10-31T16:43:49Z)
- (audit intent) `fm-reviewer pass (intent, adversary, edge, operator, maintainer) on the lane diff; 1 adversary MEDIUM, 6 MEDIUM and 3 LOW fixed with tests in 38503986 before merge` → one side per option, stated choice first; one-option default race stays open [tree c3107e96427e] (2026-10-31T16:43:49Z)
- (audit adversary) `fm-reviewer pass (intent, adversary, edge, operator, maintainer) on the lane diff; 1 adversary MEDIUM, 6 MEDIUM and 3 LOW fixed with tests in 38503986 before merge` → builder tests run guarded with a cut env (no tokens), \w-only ASCII names, archives extracted with the data filter, temp trees always removed [tree c3107e96427e] (2026-10-31T16:43:49Z)
- (audit edge) `fm-reviewer pass (intent, adversary, edge, operator, maintainer) on the lane diff; 1 adversary MEDIUM, 6 MEDIUM and 3 LOW fixed with tests in 38503986 before merge` → uncommitted side is an error row; write errors give no result; base refusal ignores 124/127 and can't-fail checks [tree c3107e96427e] (2026-10-31T16:43:49Z)
- (audit operator) `fm-reviewer pass (intent, adversary, edge, operator, maintainer) on the lane diff; 1 adversary MEDIUM, 6 MEDIUM and 3 LOW fixed with tests in 38503986 before merge` → 300 s cross deadline with a row note, stderr phase lines, pick reuses score rows [tree c3107e96427e] (2026-10-31T16:43:49Z)
## Log
- 2026-10-31T13:58:36Z created
- 2026-10-31T14:06:08Z criterion 2 text: fm lane race ID --score ranks sides by frozen checks passed, then cross-examination (each side's added test files run against every other side's tree; a side whose tests fail another side while it passes theirs ranks up), then lines changed and files outside scope; identical diffs are reported as 'no real alternative'; fm lane pick writes a race row (stated choice, winner, whether the first choice won) to the ledger and the loser's option and reason into the winner's Approach → fm lane race ID --score ranks sides by frozen checks passed, then cross-examination (each side's added test files run against every other side's tree; a side whose tests fail another side while it passes theirs ranks up), then lines changed and files outside scope; identical diffs are reported as 'no real alternative'; fm lane pick records the pick as an fm decide row (winner, the evidence, the loser rejected), writes a race row (stated choice, winner, whether the first choice won) to the ledger, and puts the loser's option and reason into the winner's Approach
- 2026-10-31T16:10:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2339.builder.md
- 2026-10-31T16:10:28Z builder slot freed
- 2026-10-31T16:10:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2339.builder.md
- 2026-10-31T16:10:45Z builder slot freed
- 2026-10-31T16:12:12Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2339.builder.md
- 2026-10-31T16:12:33Z focused
- 2026-10-31T16:12:37Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T16:14:59Z set scope=['plugin/lib/fmlanes.py', 'plugin/tests/test_lanes.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmoutcomes.py', 'plugin/tests/test_race.py', 'plugin/tests/test_outcomes.py', 'plugin/tests/test_reasoning.py', 'plugin/tests/test_genesis.py']
- 2026-10-31T16:29:58Z set scope=['plugin/lib/fmlanes.py', 'plugin/tests/test_lanes.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmoutcomes.py', 'plugin/tests/test_race.py', 'plugin/tests/test_outcomes.py', 'plugin/lib/fmcore.py', 'MASTER.md']
- 2026-10-31T16:42:49Z merged worktree-agent-a0a779aa526da9d29 (8 file(s))
- 2026-10-31T16:42:53Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0a779aa526da9d29
- 2026-10-31T16:42:54Z focused
- 2026-10-31T16:43:31Z scope: files outside the globs came from merging foreman/build (T-2338) and the changelog line
- 2026-10-31T16:44:39Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **New `fm lane race` subcommand (likeliest):** add it to `plugin/lib/fmcli.py` (dispatched from `plugin/bin/fm`). It takes ≤3 sides from the plan's Approach options, builds each in its own worktree/tree, refuses any frozen check that already passes on the base, scores each side on three signals (fr…
- **Ranking and ledger only:** sides are built by existing lane machinery, and the work here is the scorer (checks, cross-exam matrix, diff size) plus the ledger-row writer. The "race at plan time" hook-up is left for later.
- **Plan-stage integration:** `fm plan` or the Approach step calls the race automatically when Approach lists ≥2 options, so racing is part of planning rather than a separate command. "Plan time" supports this reading.
- **Evidence-only pick:** the ranking is advisory output, and a human or later step commits the winner. The "ledger row" would then be a recommendation and not a decision.
Approaches:
- **Thin orchestrator in `fmcli.py`:** reuse the existing lane create/run/check functions, loop over the sides, and call a new ranking function. Ledger writing goes through whatever `fmcore.py` already uses for rows. This is the smallest diff, but `fmcli.py` is one of the most-changed files and grows…
- **New module `plugin/lib/fmrace.py`:** it holds `refuse_passing`, `cross_examine`, `rank` and `record_pick`, with `fmcli.py` adding only the argparse wiring. It follows the existing `fmaway.py` / `fmbacktest.py` pattern and is testable in isolation as `plugin/tests/test_race.py`.
- **Cross-exam by test-file diff:** diff each side's tree against the base to find the new test files, copy them into the other trees, run them there, and build an N×N pass matrix. Ranking is lexicographic: frozen checks first, then cross-exam pass count, then diff size (lines changed).
- **Weighted score instead of lexicographic:** the three signals are combined into one number. It is simpler to display but hides why a side won, and it gives the ledger row less evidence to cite.
Failure modes:
- **Base-pass refusal checks the wrong tree:** if the frozen checks run in a dirty working tree, or on a side's tree instead of a clean checkout of base HEAD, a check that really fails on base can be refused, or one that passes can slip through. Everything in the race then ranks against a bad baselin…
- **Cross-exam contamination:** one side's new tests, copied into another tree, can overwrite same-named files (such as `test_*.py` in `plugin/tests/`) or depend on that side's new helpers. The resulting failure is an import error and not a real behavioural failure, which unfairly penalizes the other…
- **Ledger row is not append-safe or not replayable:** if the pick is written in a format that `fm replay` or `fm doctor` doesn't recognize, or without the evidence (check results, matrix, sizes), the gates fail. Concurrent races can also interleave rows.
- **Size as a tiebreaker rewards deletions:** counting raw diff lines favours a side that skips work or deletes tests. Sides with equal check and cross-exam results then get ranked by the least-effort change, and if generated files or lockfiles are counted, size becomes noise.
## Dissent
- [x] rival reading: **New `fm lane race` subcommand (likeliest):** add it to `plugin/lib/fmcli.py` (dispatched from `plugin/bin/fm`). It takes ≤3 sides from the plan's Approach options, builds each in its own worktree/tree, refuses any frozen check that already passes on the base, scores each side on three signals (fr… — answered: adopted: it is Reading 1 and steps 2 to 4
- [x] rival reading: **Ranking and ledger only:** sides are built by existing lane machinery, and the work here is the scorer (checks, cross-exam matrix, diff size) plus the ledger-row writer. The "race at plan time" hook-up is left for later. — answered: rejected: a scorer without the --sides path leaves race() unable to take 3 sides, and criterion 1 asks for both
- [x] rival reading: **Plan-stage integration:** `fm plan` or the Approach step calls the race automatically when Approach lists ≥2 options, so racing is part of planning rather than a separate command. "Plan time" supports this reading. — answered: rejected: racing on every plan with 2 options is Reading 2, every M racing; the plan-unsure trigger is brief 4's
- [x] rival reading: **Evidence-only pick:** the ranking is advisory output, and a human or later step commits the winner. The "ledger row" would then be a recommendation and not a decision. — answered: rejected: criterion 2 makes fm lane pick an fm decide row plus a ledger row, a decision with evidence, not advice
- [x] rival approach: **Thin orchestrator in `fmcli.py`:** reuse the existing lane create/run/check functions, loop over the sides, and call a new ranking function. Ledger writing goes through whatever `fmcore.py` already uses for rows. This is the smallest diff, but `fmcli.py` is one of the most-changed files and grows… — answered: adopted: extend the existing lane functions in fmlanes.py, the brief's own scope, with no new module
- [x] rival approach: **New module `plugin/lib/fmrace.py`:** it holds `refuse_passing`, `cross_examine`, `rank` and `record_pick`, with `fmcli.py` adding only the argparse wiring. It follows the existing `fmaway.py` / `fmbacktest.py` pattern and is testable in isolation as `plugin/tests/test_race.py`. — answered: rejected: a new fmrace.py is outside the brief's scope (fmlanes.py, test_lanes.py); race() already lives in fmlanes
- [x] rival approach: **Cross-exam by test-file diff:** diff each side's tree against the base to find the new test files, copy them into the other trees, run them there, and build an N×N pass matrix. Ranking is lexicographic: frozen checks first, then cross-exam pass count, then diff size (lines changed). — answered: adopted: criterion 2 is this, each side's added test files run on the other trees
- [x] rival approach: **Weighted score instead of lexicographic:** the three signals are combined into one number. It is simpler to display but hides why a side won, and it gives the ledger row less evidence to cite. — answered: rejected: criterion 2 states the order frozen checks, then cross-examination, then size, because a lexicographic rank shows why a side won
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261031-083832: Request: Mission 5, Genesis gen 1: 2. Exhaustive thinking. Before acting on anything non-trivial: list the readings of the request, eve…
- T-2340 [FEATURE M, planned, 3 steps] L plans race their design (Mission 5, #2): an L task under the race bar gets one throwaway S spike per top option, built by builder …
- research mission-20261031-083832.pack: Mission 5, Genesis gen 1: 2. Exhaustive thinking. Before acting on anything non-trivial: list the readings of the request, every a…
- decision 2026-10-31: [cites: user steer 2026-10-31: run the remaining independent missions in parallel lanes] Parallel Missions 5-8 (user steer 2026-10-31): fm lane refu…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_lanes.py
## Preflight
Changed in scope since this was planned (2026-10-31): MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmlanes.py, plugin/lib/fmoutcomes.py, plugin/tests/test_lanes.py, plugin/tests/test_outcomes.py; re-ground the plan against them before editing
## Lessons
- A cross-examination score rewards coupling unless it separates assertion failures from import errors: a test that can't load elsewhere says nothing about behaviour
## Plan gaps
- failed first: step 1 red tests (test_lanes PlanRace, RaceEvidence): 3 sides from 3 options; base-passing checks refused;…
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmcli.py
- plugin/lib/fmlanes.py
- plugin/lib/fmoutcomes.py
- plugin/tests/test_outcomes.py
- MASTER.md
- plugin/lib/fmcore.py
- CHANGELOG.md
- plugin/skills/intake/references/planning.md
- plugin/tests/helpers.py
- plugin/tests/test_backlog.py
- plugin/tests/test_builder.py
- plugin/tests/test_clean_helpers.py
- plugin/tests/test_cli.py
- plugin/tests/test_conflict_history.py
- plugin/tests/test_core.py
- plugin/tests/test_defect_classes.py
- plugin/tests/test_deliberation.py
- plugin/tests/test_diagnosis.py
- plugin/tests/test_edit_cards.py
- plugin/tests/test_evidence_quality.py
- plugin/tests/test_goal.py
- plugin/tests/test_graph.py
- plugin/tests/test_hooks.py
- plugin/tests/test_judgment.py
- plugin/tests/test_lane_stall.py
- plugin/tests/test_metacog.py
- plugin/tests/test_pass4.py
- plugin/tests/test_reasoning.py
- plugin/tests/test_recall.py
