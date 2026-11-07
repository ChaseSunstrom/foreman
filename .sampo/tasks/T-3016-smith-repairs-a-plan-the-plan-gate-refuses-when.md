---
id: T-3016
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/smith.py, plugin/tests/test_code.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-04T20:24:05Z
updated: 2026-11-05T02:34:59Z
base: 1a8ef8df177cff00415f016dd9e1cbab1e38e870
base_tree: f9d1a1a6b4cffdf92a8f5fa264cfd5bc419f4eda
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T22:04:04Z
plan0_scope: []
inferred_deps: [T-2878]
inferred_why: T-2878: named in its request
verified: strong
unproven: [docs, infra, meaning, tui-unshot, ui-unshot]
---
# Smith repairs a plan the plan gate refuses: when fm focus refuses the planner's plan (a…
## Raw request
> Smith repairs a plan the plan gate refuses: when fm focus refuses the planner's plan (a request clause with no criterion), the refusal goes back to the planner for one repair instead of ending the run; 3 of 15 local exam runs ended this way (research T-2878-taxonomy)
## Interpretation
When fm code's planner (a local model) writes a plan the plan gate refuses (fm task new, or fm focus for an M plan: e.g. a request clause with no criterion), the run ends today (3 of 15 local exam runs). Instead the refusal text goes back to the planner once, as the re-plan for a weak verify already does; the refused task is dropped with the reason, the corrected plan is checked like any plan and filed; a second refusal ends the run as today.
## Assumptions (confidence)
## Acceptance criteria
- [x] a plan fm focus refuses (an M plan missing a criterion for a request clause) goes back to the planner once with the refusal; the corrected plan is filed and the run finishes, and the refused task is dropped with the reason; a second refusal ends the run with the refusal as today — verify with `python3 plugin/tests/run.py test_code`
## Non-goals
## Approach (options → choice → why)
1) In _make_task: on a refusal, drop the task it made (if any), send the refusal to the planner with the plan conversation for one corrected plan, re-check it (_plan_problem) and file it again; a second refusal raises as today. Likely outcome: the clause-coverage refusals get a criterion or non-goal and the run goes on. Fails if: the planner returns the same plan (then it ends as today, one model call later).
2) Use what exists: fill the gap mechanically (name each uncovered clause under Non-goals). Likely outcome: the gate passes. Fails if: a clause is a real requirement: the run would silently drop it, which the gate exists to stop.
3) Do less: leave the run ending, and only name the refusal in the taxonomy (already done). Likely outcome: no change in fix rate. Fails if: the goal is fewer dead runs.
Choice 1 (80%): the same one-repair pattern the plan's verify check uses, through the existing slot and drop verbs.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: an M plan refused by fm focus for an uncovered clause, then a corrected plan, finishes; refused twice ends with the refusal
2. [x] the one repair in smith._make_task (drop, re-plan with the refusal, re-check, file again)
3. [x] rerun the local exam scenario that ended plan_refused (s4-018-m04, jarvis) and record how it ends
## Resume here
<!-- auto -->
- 2026-11-04T22:33:56Z step 3/3: rerun the local exam scenario that ended plan_refused (s4-018-m04, jarvis) and record how it ends
- git: foreman/build; 14 uncommitted: plugin/lib/sampo/jeffexport.py, plugin/lib/sampo/smith.py, plugin/lib/sampo/smithtui.py, plugin/tests/fixtures/golden/demo-00.0s.txt, plugin/tests/fixtures/golden/demo-03.4s.txt, plugin/tests/fixtures/golden/demo-09.1s.txt, plugin/tests/fixtures/golden/demo-30.0s.txt, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, plugin/tests/test_jeff_export.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3006-arms.sh, plugin/tests/test_code.py, plugin/lib/sampo/smith.py, /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/quiet-merge.sh, mods/foreman-ui/tests/palette-baseline.test.tsx, mods/foreman-ui/tests/fixtures/baseline-palettes.ts, plugin/tests/fixtures/tui-baseline.json, plugin/lib/sampo/smithtui.py, plugin/tests/test_code_tui.py, plugin/tests/fixtures/golden/demo-00.0s.txt, plugin/tests/fixtures/golden/demo-03.4s.txt, plugin/tests/fixtures/golden/demo-09.1s.txt, plugin/tests/fixtures/golden/demo-30.0s.txt, mods/foreman-ui/tests/forge.test.tsx
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_code.Review.test_a_plan_focus_refuses_goes_back_to_the_planner_once` → ✗ exit 1 · Ran 1 tests in 3.2s (1 classes, 16 at a time; slowest: Review 1s) / FAILED (1 classes: test_code.Review) (start tree + this task's tests) [ran] [tree 3c294a6924f8] [world 2f1906870a] (2026-11-04T22:04:50Z)
- `python3 plugin/tests/run.py test_code.Review.test_a_plan_focus_refuses_goes_back_to_the_planner_once` → ✗ exit 1 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Review 0s) / FAILED (1 classes: test_code.Review) [ran] [tree 3c294a6924f8] [world 2f1906870a] (2026-11-04T22:04:50Z)
- `python3 plugin/tests/run.py test_code.Review.test_a_plan_focus_refuses_goes_back_to_the_planner_once` → ✗ exit 1 · Ran 1 tests in 2.3s (1 classes, 16 at a time; slowest: Review 1s) / FAILED (1 classes: test_code.Review) (start tree + this task's tests) [ran] [tree bb617924a0d9] [world 2f1906870a] (2026-11-04T22:06:25Z)
- `python3 plugin/tests/run.py test_code.Review.test_a_plan_focus_refuses_goes_back_to_the_planner_once` → exit 0 · Ran 1 tests in 2.8s (1 classes, 16 at a time; slowest: Review 2s) / OK [ran] [tree bb617924a0d9] [world 2f1906870a] (2026-11-04T22:06:25Z)
- (step 1) `python3 plugin/tests/run.py test_code.Review.test_a_plan_focus_refuses_goes_back_to_the_planner_once test_code.Review.test_a_plan_refused_twice_ends_the_run_with_the_refusal` → exit 0 · Ran 2 tests in 3.2s (1 classes, 16 at a time; slowest: Review 3s) / OK [ran] [tree bb617924a0d9] [world 2f1906870a] (2026-11-04T22:06:29Z)
- (step 2) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 507 tests in 141.1s (107 classes, 16 at a time; slowest: Worker 141s, CodeFakes 39s, OutcomeEscalation 35s) / OK [ran] [tree bb617924a0d9] [world 2f1906870a] (2026-11-04T22:08:57Z)
- `python3 plugin/tests/run.py test_code.Review.test_a_re_plan_that_cannot_stand_keeps_the_refused_task` → ✗ exit 1 · Ran 1 tests in 4.4s (1 classes, 16 at a time; slowest: Review 1s) / FAILED (1 classes: test_code.Review) (start tree + this task's tests) [ran] [tree 31e5d33cb122] [world 2f1906870a] (2026-11-04T22:25:49Z)
- `python3 plugin/tests/run.py test_code.Review.test_a_re_plan_that_cannot_stand_keeps_the_refused_task` → exit 0 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: Review 1s) / OK [ran] [tree 31e5d33cb122] [world 2f1906870a] (2026-11-04T22:25:49Z)
- (step 2) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 508 tests in 101.0s (107 classes, 16 at a time; slowest: Worker 100s, OutcomeEscalation 52s, CodeFakes 46s) / OK [ran] [tree 31e5d33cb122] [world 2f1906870a] (2026-11-04T22:28:28Z)
- (step 3) `grep -q 're-plan: Criterion 3' state/projects/foreman-4a056f/exam/s4-018/answers/smith/s4-018-m02.events.jsonl` → exit 0 · (no output) [ran] [tree 9b2a47d0a4b1] [world 2f1906870a] (2026-11-05T02:27:21Z)
- `python3 plugin/tests/run.py test_code` → ✗ exit 1 · Ran 516 tests in 80.3s (108 classes, 16 at a time; slowest: Worker 79s, CodeFakes 36s, OutcomeEscalation 30s) / FAILED (3 classes: test_code.Review, test_code_tui.Core, test_code_tui.Forge) (start tree + this task's tests) [ran] [tree 246d3ae54904] [world 2f1906870a] (2026-11-05T02:30:14Z)
- `python3 plugin/tests/run.py test_code` → exit 0 · Ran 516 tests in 91.2s (108 classes, 16 at a time; slowest: Worker 91s, CodeFakes 36s, OutcomeEscalation 30s) / OK [ran] [tree 246d3ae54904] [world 2f1906870a] (2026-11-05T02:30:14Z)
- (ac 1) `python3 plugin/tests/run.py test_code` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T02:30:14Z [ran] [tree 246d3ae54904] [world 2f1906870a] (2026-11-05T02:30:39Z)
- (audit intent) `self: _replan sends a gate refusal back to the planner once, re-checks the corrected plan with the same checks, drops the refused task only after the new plan stands; a repaired (field-by-field) plan, a timeout (124) or a non-gate failure end the run as before` → the live s4-018-m02 run shows the re-plan firing and the second refusal ending the run with both reasons, T-0001 kept [tree 246d3ae54904] (2026-11-05T02:30:39Z)
- (audit edge) `self: _replan sends a gate refusal back to the planner once, re-checks the corrected plan with the same checks, drops the refused task only after the new plan stands; a repaired (field-by-field) plan, a timeout (124) or a non-gate failure end the run as before` → a drop that fails is noted and the run continues beside it; a plan from --verify has no planner conversation and raises as before; the clause hint is added only for an uncovered-clause refusal [tree 246d3ae54904] (2026-11-05T02:30:39Z)
- (audit adversary) `self: _replan sends a gate refusal back to the planner once, re-checks the corrected plan with the same checks, drops the refused task only after the new plan stands; a repaired (field-by-field) plan, a timeout (124) or a non-gate failure end the run as before` → the text fed back is Sampo's own gate output, and the model's corrected plan passes check_plan, _plan_problem and the plan gate again before anything runs; no new network, exec or HTML path; the drop reason is one line capped at 200 chars [tree 246d3ae54904] (2026-11-05T02:30:39Z)
- (audit self) `self: _replan sends a gate refusal back to the planner once, re-checks the corrected plan with the same checks, drops the refused task only after the new plan stands; a repaired (field-by-field) plan, a timeout (124) or a non-gate failure end the run as before` → no findings [tree 246d3ae54904] (2026-11-05T02:30:39Z)
## Log
- 2026-11-04T20:24:05Z created
- 2026-11-04T22:04:00Z planned: it has criteria and steps
- 2026-11-04T22:04:03Z set approved=True
- 2026-11-04T22:04:04Z focused
- 2026-11-04T22:04:04Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T22:06:19Z hypothesis confirmed: the refusal reaches the planner (re-plan event) and the corrected plan passes the gate when its criterion shares 2+ words with the clause (recall.bind); rules out a matcher change
- 2026-11-04T22:07:30Z paused: focus moved to T-2995
- 2026-11-04T22:24:15Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-04T22:24:15Z focused
- 2026-11-04T22:25:42Z review fixes (fm-reviewer intent/edge): the refused task is dropped only after the re-plan passes its checks; a timeout (124) or a failure without 'refused' raises as before (no duplicate after a timed-out task new); the criterion hint only for a clause gap; a failed drop is a note; extract_json guarded to a dict; tests pin the twice-refused state and a re-plan that can't stand
- 2026-11-04T22:33:56Z paused: focus moved to T-2876
- 2026-11-04T22:34:11Z scope: smithtui.py, test_code_tui.py, the TUI baseline/golden fixtures and the mod's baseline/forge tests were T-2876's edits made while T-3016 held the focus; T-2876 commits them before T-3016 closes
- 2026-11-05T02:26:32Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-05T02:26:32Z focused
- 2026-11-05T02:26:33Z set scope=['plugin/lib/sampo/smith.py', 'plugin/tests/test_code.py', 'CHANGELOG.md']
- 2026-11-05T02:27:21Z step 3: s4-018-m02 on jarvis-nothink (19:09): the plan gate refused for two uncovered clauses and a missing Undo line; the re-plan fired, the 27B's corrected plan added criteria but its keep-the-tests check passed on the start tree, so the run ended on the second refusal with both reasons and kept T-0001, as criterion 1 says
- 2026-11-05T02:30:28Z scope: CHANGELOG.md (the user-visible line)
- 2026-11-05T02:34:52Z done
- 2026-11-05T02:34:59Z committed 15a2ce42 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2878-taxonomy: Source: the 15 Smith exam runs on local or self-hosted models kept in this project's exam answers (s0-001 seeded across 6 languages, s4-018 and…
- research T-2878-smithbench-gpu: `fm code bench --model PROFILE --seed-timeout 600` on an RTX 5070 Ti (16 GB) through Ollama 0.40.11, one model at a time,
- T-2908 [FEATURE M, done, 4 steps] Uplift part 1: Louhi's exam runs Smith on a local model (sampo exam run RUN --agent smith --model PROFILE) in every scenario, graded li…
- decision 2026-11-04: Local profiles serve 32k context with reasoning off as the default for Smith (T-2935/T-2938 make it automatic); small-model scaffolds for plan and c…
- similar past tasks were M: consider --tier M
## Lessons
- A loop that ends on a gate's refusal should hand the refusal back once before giving up: the 27B fixed the named gaps but introduced a vacuous check, so the second pass's reason must be shown with the first.
## Files touched
- plugin/tests/test_code.py
- plugin/lib/sampo/smith.py
- mods/foreman-ui/tests/fixtures/baseline-palettes.ts
- mods/foreman-ui/tests/palette-baseline.test.tsx
- plugin/tests/fixtures/tui-baseline.json
- plugin/tests/test_code_tui.py
- plugin/lib/sampo/smithtui.py
- plugin/tests/fixtures/golden/demo-00.0s.txt
- plugin/tests/fixtures/golden/demo-03.4s.txt
- plugin/tests/fixtures/golden/demo-09.1s.txt
- plugin/tests/fixtures/golden/demo-30.0s.txt
- mods/foreman-ui/tests/forge.test.tsx
- CHANGELOG.md
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
