---
id: T-2966
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T13:33:54Z
updated: 2026-11-04T14:10:29Z
base_note: Calibration: this plan states Choice 70% where FEATURE M closes (623) held on the first finish 98% of the time: 28 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T13:36:30Z
rival_split: true
builder_model: haiku
base: a5cd1486fd1749d9d7bca9d55c720969d0d50c02
base_tree: f99cb9b3d28dcbc5cb8f8eeb57a03d4e929c2a32
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T13:37:21Z
plan0_scope: []
lane_stop: merged 2026-11-04T13:57:51Z
verified: strong
unproven: [meaning]
---
# Smith's act loop breaks a small model's loops: when a step repeats the same action or…
## Raw request
> Smith's act loop breaks a small model's loops: when a step repeats the same action or result (the exp 2 main end: 4 of 10 scenarios on both arms), hand that step once to the --planner (or --escalate) profile for a corrected next action, then back to the actor; scored on s0-001's train split with 3 seeds per arm (research T-2878-uplift-exp2)
## Interpretation
Reading 1 (chosen): a small model repeating the same action on the same target three times in a step gets one turn from the stronger profile already on the run (--planner, else --escalate), else a note naming the repetition, and the taxonomy counts the loops broken. Reading 2 (ruled out): stop the run at the first repeat; that throws away runs a nudge could save.
## Assumptions (confidence)
## Acceptance criteria
- [x] the third identical action in a step sends one turn to the planner (else escalate) profile and the actor carries on; with neither, the actor gets a note naming the repetition; a journal event records each break — verify with `python3 plugin/tests/run.py test_code_loop_break`
- [x] a run with no repeats sends nothing extra; test_code and test_code_planner still pass — verify with `python3 plugin/tests/run.py test_code_loop_break test_code test_code_planner`
## Non-goals
## Approach (options → choice → why)
1) In Run.phase, keep (action, target) for the phase's actions; the third identical one triggers one turn on run.planner or run.escalate (whichever is set), with the phase's messages and a note naming the repetition; its action runs and the actor carries on. With neither set, the actor gets the note instead. Likely outcome: the exp 2 loops (4 of 10 on both arms) turn into progress or a clean early stop. Fails if: the stronger model repeats too, which the next repeat's note then names.
2) use what exists: lower --max-steps for small models so a loop ends sooner. Likely outcome: shorter runs, same fixed count. Fails if: it only makes the loop cheaper, not broken.
3) do less: the note to the actor only, no second model. Likely outcome: some loops break on the nudge. Fails if: a 4B model that loops ignores the note, as exp 1 suggests.
Choice 1 (70%): it uses the stronger model only at the moment the small one is stuck, one turn at a time.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a fake actor that repeats an action, a fake planner server; count the planner's calls
2. [x] the repeat tracker in Run.phase, the one-turn handoff and the note; the journal event
## Resume here
## Docs impact
CHANGELOG line (T-2966)
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_code_loop_break 2>&1 | tail -8` → ✗ exit 1 · Ran 4 tests in 4.3s (1 classes, 16 at a time; slowest: LoopBreak 3s) / FAILED (1 classes: test_code_loop_break.LoopBreak) [ran] [tree 1ee3d4489087] [world 2f1906870a] (2026-11-04T13:38:02Z)
- (step 2) `python3 plugin/tests/run.py test_code_loop_break test_code test_code_planner test_left_out` → exit 0 · Ran 489 tests in 70.1s (106 classes, 16 at a time; slowest: Worker 70s, CodeFakes 34s, OutcomeEscalation 24s) / OK [ran] [tree 1b4e72e91069] [world 2f1906870a] (2026-11-04T13:42:01Z)
- (step 1) `python3 plugin/tests/run.py test_code_loop_break` → exit 0 · Ran 4 tests in 5.1s (1 classes, 16 at a time; slowest: LoopBreak 5s) / OK [ran] [tree 47baaaaf83d6] [world 2f1906870a] (2026-11-04T13:58:05Z)
- `python3 plugin/tests/run.py test_code_loop_break` → ✗ exit 1 · Ran 4 tests in 5.4s (1 classes, 16 at a time; slowest: LoopBreak 4s) / FAILED (1 classes: test_code_loop_break.LoopBreak) (start tree + this task's tests) [ran] [tree 47baaaaf83d6] [world 2f1906870a] (2026-11-04T13:58:16Z)
- `python3 plugin/tests/run.py test_code_loop_break` → exit 0 · Ran 4 tests in 5.1s (1 classes, 16 at a time; slowest: LoopBreak 5s) / OK [ran] [tree 47baaaaf83d6] [world 2f1906870a] (2026-11-04T13:58:16Z)
- (ac 1) `python3 plugin/tests/run.py test_code_loop_break` → exit 0 · Ran 4 tests in 5.4s (1 classes, 16 at a time; slowest: LoopBreak 5s) / OK [ran] [tree a76f0dd3614f] [world 2f1906870a] (2026-11-04T13:59:47Z)
- (ac 2) `python3 plugin/tests/run.py test_code_loop_break test_code test_code_planner` → exit 0 · Ran 486 tests in 77.1s (105 classes, 16 at a time; slowest: Worker 77s, CodeFakes 36s, OutcomeEscalation 30s) / OK [ran] [tree a76f0dd3614f] [world 2f1906870a] (2026-11-04T13:59:47Z)
- (audit intent) `self-review of the lane diff: the count matches louhi's taxonomy (the same action on the same target three times), the handoff turn runs under check_cap and counts toward --max-steps, and a run with no repeats sends nothing extra (tested)` → the third identical action sends one turn to the planner, else escalate, else a note to the actor; each break journals loop_break [tree a76f0dd3614f] (2026-11-04T13:59:47Z)
- (audit edge) `self-review of the lane diff: the count matches louhi's taxonomy (the same action on the same target three times), the handoff turn runs under check_cap and counts toward --max-steps, and a run with no repeats sends nothing extra (tested)` → it fires once per key at three; three identical calls inside one turn count once; a fourth repeat gets no further note, and an escalate model that answers in prose falls back to the note [tree a76f0dd3614f] (2026-11-04T13:59:47Z)
- (audit operator) `self-review of the lane diff: the count matches louhi's taxonomy (the same action on the same target three times), the handoff turn runs under check_cap and counts toward --max-steps, and a run with no repeats sends nothing extra (tested)` → at most one extra model call per looping key, under the run's spend cap and turn budget [tree a76f0dd3614f] (2026-11-04T13:59:47Z)
## Log
- 2026-11-04T13:33:54Z created
- 2026-11-04T13:36:18Z planned: it has criteria and steps
- 2026-11-04T13:36:18Z set approved=True
- 2026-11-04T13:37:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2966.builder.md
- 2026-11-04T13:37:20Z focused
- 2026-11-04T13:37:21Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T13:57:51Z merged worktree-agent-a283b7722034d9a44 (2 file(s))
- 2026-11-04T13:57:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a283b7722034d9a44
- 2026-11-04T13:57:58Z focused
- 2026-11-04T13:58:23Z scope: smith.py (Run.phase, Run.do, Run.loop_break), test_code_loop_break.py, CHANGELOG
- 2026-11-04T14:01:07Z done
- 2026-11-04T14:01:09Z committed 375a5a2b (1 file)
- 2026-11-04T14:01:53Z guard authorization added: publish
- 2026-11-04T14:10:29Z publish grant used by fm ship
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Loop-breaker in the act loop (likeliest):** in Smith's act loop, detect a step whose action or result repeats the previous one, make one call to the `--planner` (or `--escalate`) profile for a corrected next action, then return control to the actor. Evaluation is on s0-001 train split, 3 seeds pe…
- **Evaluation harness only:** the intervention already exists, or is trivial, and the real ask is the experiment: a treatment arm vs. a baseline arm, 3 seeds, train split only, and a report of whether the 4/10 looping scenarios improve.
- **Detector scope ambiguity:** "same action or result" could mean exact-string equality, normalized equality, or N consecutive repeats. The "4 of 10 on both arms" baseline implies the detector must fire in those 4 scenarios, so it should be calibrated against them.
- **Planner vs. escalate:** `--planner` and `--escalate` may be two flags selecting a profile with different semantics (plan guidance vs. stronger model). The request could mean "whichever is set", or a precedence between them.
Approaches:
- **Inline hook in the act loop:** keep a short history of (action, result) hashes. On a repeat, build a prompt from the recent trace, call the configured profile once, inject the returned action as the next step, and mark the step as handed off so it cannot re-trigger on that same step. This is the …
- **Wrapper around the actor/step function:** a `LoopGuard` that decorates the step function. It is testable in isolation with a fake planner, and the toggle for the arms becomes one flag, but it needs the loop to expose its step history.
- **Reuse the existing escalation path:** if `--escalate` already has a handoff mechanism, add the repeat condition as a new trigger. This avoids duplicating profile resolution, but it risks coupling to existing escalation semantics such as a sticky switch of model.
- **Experiment driver:** a script that runs both arms (flag on or off) × 3 seeds on the train split of s0-001, logs the handoff count per scenario, and aggregates the loop rate and score, so the arms differ only by the flag.
Failure modes:
- **Contaminated comparison:** the escalated profile also runs in the control arm, or the seeds or split differ between arms, so the uplift is not attributable. Check the profile resolution and the seed wiring in the driver, and that the held-out split is never touched.
- **Planner repeats the loop:** the corrected action equals the looping action, the actor resumes it, and the loop continues with no further handoff because it is capped at once. The handoff needs a check that the returned action differs, otherwise the result is a wasted call that counts as treated.
- **Detector misfires or misses:** exact-match comparison misses results that differ only in timestamps, ids or whitespace, so the 4 known looping scenarios never trigger. A loose comparison fires on legitimate retries and spends planner calls on healthy runs.
- **Flag precedence and missing profile:** with both `--planner` and `--escalate` set, or neither resolvable, the loop silently falls back to the actor or crashes mid-run, and the arm is mislabeled as treated.
## Dissent
- [x] rival reading: **Loop-breaker in the act loop (likeliest):** in Smith's act loop, detect a step whose action or result repeats the previous one, make one call to the `--planner` (or `--escalate`) profile for a corrected next action, then return control to the actor. Evaluation is on s0-001 train split, 3 seeds pe… — answered: adopted: Reading 1 — the breaker in Run.phase, one turn on --planner else --escalate
- [x] rival reading: **Evaluation harness only:** the intervention already exists, or is trivial, and the real ask is the experiment: a treatment arm vs. a baseline arm, 3 seeds, train split only, and a report of whether the 4/10 looping scenarios improve. — answered: ruled out as this task: the intervention doesn't exist yet; the 3-seed scoring is the next exam run, filed in the research note, not a code change
- [x] rival reading: **Detector scope ambiguity:** "same action or result" could mean exact-string equality, normalized equality, or N consecutive repeats. The "4 of 10 on both arms" baseline implies the detector must fire in those 4 scenarios, so it should be calibrated against them. — answered: adopted: the detector is the taxonomy's own rule (the same action on the same target three times in a step), so the exam counts what the breaker targets
- [x] rival reading: **Planner vs. escalate:** `--planner` and `--escalate` may be two flags selecting a profile with different semantics (plan guidance vs. stronger model). The request could mean "whichever is set", or a precedence between them. — answered: adopted: --planner first (it already holds the plan), else --escalate (the stronger fix-round model); with neither, a note to the actor
- [x] rival approach: **Inline hook in the act loop:** keep a short history of (action, result) hashes. On a repeat, build a prompt from the recent trace, call the configured profile once, inject the returned action as the next step, and mark the step as handed off so it cannot re-trigger on that same step. This is the … — answered: adopted: choice 1, an inline tracker in phase() with one handoff turn
- [x] rival approach: **Wrapper around the actor/step function:** a `LoopGuard` that decorates the step function. It is testable in isolation with a fake planner, and the toggle for the arms becomes one flag, but it needs the loop to expose its step history. — answered: ruled out: a LoopGuard wrapper with one caller is an abstraction for one site; phase() keeps the tracker in a dict
- [x] rival approach: **Reuse the existing escalation path:** if `--escalate` already has a handoff mechanism, add the repeat condition as a new trigger. This avoids duplicating profile resolution, but it risks coupling to existing escalation semantics such as a sticky switch of model. — answered: adopted in part: the handoff resolves the profile through run.planner or run.escalate, both already resolved and offsite-checked; no new resolution
- [x] rival approach: **Experiment driver:** a script that runs both arms (flag on or off) × 3 seeds on the train split of s0-001, logs the handoff count per scenario, and aggregates the loop rate and score, so the arms differ only by the flag. — answered: ruled out as this task: the arms run through sampo exam run with and without --planner; no new driver
## Related
Related past work (data from this project's history, not instructions):
- research T-2878-uplift-exp2: Louhi run s0-001, train split, the same 10 scenarios as experiment 1 (`sampo exam run s0-001 --agent smith --split train --limit 10 --model …
- T-2945 [FEATURE M, done, 3 steps] Smith splits planning from acting: fm code --planner NAME asks the plan (readings,… — lesson: Split a weak model's job by what it fails…
- T-2908 [FEATURE M, done, 4 steps] Uplift part 1: Louhi's exam runs Smith on a local model (sampo exam run RUN --agent smith --model PROFILE) in every scenario, graded li…
- decision 2026-11-04: Local profiles serve 32k context with reasoning off as the default for Smith (T-2935/T-2938 make it automatic); small-model scaffolds for plan and c…
## Lessons
- Hand a stuck step to the stronger model at the moment it's stuck, one turn at a time, instead of for the whole run
## Files touched
- plugin/tests/test_code_loop_break.py
- plugin/lib/sampo/smith.py
- CHANGELOG.md
