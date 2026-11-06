---
id: T-2945
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T09:26:50Z
updated: 2026-11-04T12:09:43Z
base_note: Calibration: this plan states Choice 65% where FEATURE M closes (621) held on the first finish 98% of the time: 33 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T11:29:12Z
rival_split: true
builder_model: haiku
base: e6c9d8cdb7f9f70fd9718f886d32d8ebac644ec8
base_tree: 02646e3feb7bbed33f0458ae4473def5bca6d303
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T11:51:31Z
plan0_scope: []
lane_stop: merged 2026-11-04T12:01:36Z
verified: strong
---
# Smith splits planning from acting: fm code --planner NAME asks the plan (readings,…
## Raw request
> Smith splits planning from acting: fm code --planner NAME asks the plan (readings, approach, criteria) and the close notes from a stronger profile and runs every step and fix round on --model, so a 4B-9B model that loops or never produces a valid M plan (uplift exp 1: qwen3.5:4b 0/8) still acts on a plan it can follow; the exam's smith arm takes --planner too and scores both split and solo
## Interpretation
Reading 1 (chosen): `fm code --planner NAME` sends only the plan slot (and its one re-plan) and the close-notes slots to the planner profile; the task, every step, every fix round and the escalation stay on `--model`. The journal's start event names both, and the exam's smith arm passes `--planner` through so a run can score split and solo on the same scenarios.
Reading 2 (ruled out): the planner also supervises each step (reviews every action). That doubles the strong model's calls per step and is a different feature (a step critic); the uplift data says small models fail at the plan, not at single actions.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code --planner P --model A sends the plan and close-note slots to P and every step and fix round to A; the start event names both — verify with `python3 plugin/tests/run.py test_code_planner`
- [x] without --planner every slot goes to --model as today, and a bad planner name fails before the first call — verify with `python3 plugin/tests/run.py test_code_planner test_code`
- [x] sampo exam run RUN --agent smith --model A --planner P passes it through and the answer records the planner — verify with `python3 plugin/tests/run.py test_code_planner test_exam`
## Non-goals
## Approach (options → choice → why)
1) A `run.planner` profile, resolved and offsite-checked like `run.escalate`; `_plan` and the close slots (`_finish`'s M notes and T-2937's gap slot) call `slot(run, run.planner or profile, …)`; served context and the cap stay the actor's. Likely outcome: qwen3.5:4b acts on a 27B or 12B plan and closes some scenarios. Fails if: the small model can't follow a plan's steps either, which the exam will then show.
2) use what exists: run `fm code --dry-plan` on the big model, then `fm code --task ID` on the small one (the task already holds the plan). Likely outcome: works today by hand, two commands. Fails if: the exam's smith arm makes one fm code call per scenario, so it can't measure the split without arm changes anyway, and the close notes still come from the small model.
3) do less: tell users below 9B to pick a bigger model (a note when the profile is small). Likely outcome: honest, no code. Fails if: the standing steer is to make small models match frontier results, not to refuse them.
Choice 1 (65%): one flag, reuses the escalate pattern, and the exam can score it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test first: a fake two-server run proves the plan and close slots hit P and the steps hit A
2. [x] the flag in cli.py, run.planner resolved like escalate, slot calls in _plan and the close slots
3. [x] the exam's smith arm passes --planner; docs in Smith's docstring and MASTER
## Resume here
## Docs impact
CHANGELOG line (T-2945); Smith's docstring and --help name --planner
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_code_planner 2>&1 | tail -8` → exit 0 · Ran 4 tests in 12.5s (2 classes, 16 at a time; slowest: CodePlanner 10s, ExamArm 1s) / OK [ran] [tree 326efd582d87] [world 2f1906870a] (2026-11-04T11:55:59Z)
- (step 2) `python3 plugin/tests/run.py test_code_planner 2>&1 | tail -8` → exit 0 · Ran 4 tests in 12.5s (2 classes, 16 at a time; slowest: CodePlanner 10s, ExamArm 1s) / OK [ran] [tree 326efd582d87] [world 2f1906870a] (2026-11-04T11:55:59Z)
- (step 3) `python3 plugin/tests/run.py test_code_planner test_exam_smith_findings 2>&1 | tail -4` → exit 0 · Ran 8 tests in 5.0s (3 classes, 16 at a time; slowest: CodePlanner 4s, SmithFindings 0s, ExamArm 0s) / OK [ran] [tree 326efd582d87] [world 2f1906870a] (2026-11-04T11:56:27Z)
- (step 1) `python3 plugin/tests/run.py test_code_planner` → exit 0 · Ran 4 tests in 8.4s (2 classes, 16 at a time; slowest: CodePlanner 7s, ExamArm 0s) / OK [ran] [tree 326efd582d87] [world 2f1906870a] (2026-11-04T11:57:45Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_code_hardening test_code_planner test_code_worker test_core test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [26.67s] [ran] [tree 326efd582d87] [world 2f1906870a] (2026-11-04T11:59:42Z)
- (step 2) `python3 plugin/tests/run.py test_code_planner test_exam_smith_findings` → exit 0 · Ran 8 tests in 2.8s (3 classes, 16 at a time; slowest: CodePlanner 2s, SmithFindings 0s, ExamArm 0s) / OK [ran] [tree f2b53f21cdad] [world 2f1906870a] (2026-11-04T12:03:05Z)
- (step 3) `python3 plugin/tests/run.py test_code_planner test_exam_smith_findings` → exit 0 · Ran 8 tests in 2.8s (3 classes, 16 at a time; slowest: CodePlanner 3s, SmithFindings 0s, ExamArm 0s) / OK [ran] [tree f2b53f21cdad] [world 2f1906870a] (2026-11-04T12:03:08Z)
- `python3 plugin/tests/run.py test_code_planner` → ✗ exit 1 · Ran 4 tests in 2.8s (2 classes, 16 at a time; slowest: CodePlanner 1s, ExamArm 0s) / FAILED (2 classes: test_code_planner.CodePlanner, test_code_planner.ExamArm) (start tree + this task's tests) [ran] [tree f2b53f21cdad] [world 2f1906870a] (2026-11-04T12:03:15Z)
- `python3 plugin/tests/run.py test_code_planner` → exit 0 · Ran 4 tests in 2.9s (2 classes, 16 at a time; slowest: CodePlanner 3s, ExamArm 0s) / OK [ran] [tree f2b53f21cdad] [world 2f1906870a] (2026-11-04T12:03:15Z)
- (ac 1) `python3 plugin/tests/run.py test_code_planner` → exit 0 · Ran 4 tests in 2.9s (2 classes, 16 at a time; slowest: CodePlanner 3s, ExamArm 0s) / OK [ran] [tree b4fa2d896f4d] [world 2f1906870a] (2026-11-04T12:06:52Z)
- (ac 2) `python3 plugin/tests/run.py test_code_planner test_code` → exit 0 · Ran 481 tests in 86.1s (104 classes, 16 at a time; slowest: Worker 86s, CodeFakes 37s, OutcomeEscalation 32s) / OK [ran] [tree b4fa2d896f4d] [world 2f1906870a] (2026-11-04T12:06:52Z)
- (ac 3) `python3 plugin/tests/run.py test_code_planner test_exam` → exit 0 · Ran 113 tests in 118.4s (29 classes, 16 at a time; slowest: LeanKind 118s, ExamAuthors 86s, JudgmentKinds 76s) / OK [ran] [tree b4fa2d896f4d] [world 2f1906870a] (2026-11-04T12:06:52Z)
- (audit intent) `self-review of the lane diff: run.planner is resolved and offsite-checked like run.escalate before any call; only _plan, the M close notes and the gap slot use it; a resume reads it back from the journal` → --planner P --model A sends the plan and close slots to P and every step and fix round to A; the start event and journal name both; without it every slot goes to --model [tree b4fa2d896f4d] (2026-11-04T12:06:52Z)
- (audit adversary) `self-review of the lane diff: run.planner is resolved and offsite-checked like run.escalate before any call; only _plan, the M close notes and the gap slot use it; a resume reads it back from the journal` → a planner profile goes through offsite_ok like --escalate, so a sensitive repo can't send its plan to a cloud planner; a bad name fails in m.resolve before any call [tree b4fa2d896f4d] (2026-11-04T12:06:52Z)
- (audit edge) `self-review of the lane diff: run.planner is resolved and offsite-checked like run.escalate before any call; only _plan, the M close notes and the gap slot use it; a resume reads it back from the journal` → --worker and --verify runs have no profile, so run.planner or profile stays None there and _plan returns early on --verify; the exam CLI's --planner path has no end-to-end test, only the arm function [tree b4fa2d896f4d] (2026-11-04T12:06:52Z)
## Log
- 2026-11-04T09:26:50Z created
- 2026-11-04T09:27:49Z planned: it has criteria and steps
- 2026-11-04T09:27:56Z criterion 1 text: fm code --planner P --model A sends the plan and close-note slots to P and every step and fix round to A; the start event names both — verify → fm code --planner P --model A sends the plan and close-note slots to P and every step and fix round to A; the start event names both
- 2026-11-04T11:51:11Z set approved=True
- 2026-11-04T11:51:12Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2945.builder.md
- 2026-11-04T11:51:30Z focused
- 2026-11-04T11:51:31Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T12:01:36Z merged worktree-agent-a4565db6e61fe7313 (4 file(s))
- 2026-11-04T12:03:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4565db6e61fe7313
- 2026-11-04T12:03:01Z focused
- 2026-11-04T12:03:23Z scope: smith.py (planner slots), cli.py (--planner on fm code and exam), louhi.py (the arm passes it), test_code_planner.py, CHANGELOG
- 2026-11-04T12:09:39Z done
- 2026-11-04T12:09:43Z committed 726d9eed (1 file)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: add a `--planner NAME` flag to the `fm code` smith command (likely `plugin/lib/fmcli.py` plus the smith implementation) that makes a planning call on the stronger profile NAME (readings, approach, criteria, and later the close notes) while every step and fix round still runs on `--model`…
- The "exam" half: the smith arm of the exam takes `--planner` too and reports split and solo scores side by side, so the exam harness (probably under `plugin/evals/` or `bench/`) must pass the flag through and label results by mode.
- Narrower: only the plan's shape changes. The planner emits the existing "M plan" structure and the small model consumes it, with no change to the close-notes path or the exam.
- Alternative: "planner" is a generic role/profile slot in the profile config (resolved like `--model`), not a smith-only flag, so other commands could reuse it later.
Approaches:
- Add `--planner` to the argparse for `fm code` in `plugin/lib/fmcli.py`. Resolve NAME through the same profile lookup as `--model`. In smith, run one planner call before the step loop, parse the result into the existing plan structure, then feed that to the step and fix rounds on `--model`. Call the…
- Introduce a small `Planner` seam inside the smith module (`plan()` and `close()`). A solo implementation delegates to `--model` and a split implementation delegates to NAME, so the step loop never branches on mode.
- Build the exam by looping the smith arm over {solo, split}. The arm forwards `--planner` from the exam CLI, and results carry a `mode` field so scores stay separable in the report.
- Make the planner's output validated against the plan schema. On invalid output, retry the planner (never the small model) and fail loudly after N tries, so the 4B model never has to produce the plan.
Failure modes:
- The planner profile leaks into step or fix calls. For example, a shared client or default-model global gets set by the planner call and is reused, so "split" silently runs everything on the strong model and the exam scores look inflated.
- The plan is rendered into the step prompt in a form the 4B-9B model still can't follow, for example too long for its context or nested criteria. The split then scores no better than solo, and the tests only check that the plan was passed, not that it was usable.
- Cost and budget accounting attribute planner tokens to `--model`, or skip them. The exam then compares split and solo unfairly, and any budget guard in `plugin/lib/fmguard.py` can be bypassed or tripped wrongly.
- Resume, replay, or `fm replay` and any recorded run state don't persist the planner name or the plan. A replayed or resumed run then re-plans with a different planner or none, and a solo run is mistaken for a split run in the exam results.
## Dissent
- [x] rival reading: Likeliest: add a `--planner NAME` flag to the `fm code` smith command (likely `plugin/lib/fmcli.py` plus the smith implementation) that makes a planning call on the stronger profile NAME (readings, approach, criteria, and later the close notes) while every step and fix round still runs on `--model`… — answered: adopted: Reading 1 — --planner on fm code resolves like --escalate; plan and close slots go to it, steps and fix rounds to --model — answered: adopted: criterion 3 — the exam's smith arm passes --planner and the answer records it, so split and solo score side by side — answered: ruled out: the close notes come from the same planner, since the close slots (T-2937) are where small models were refused at finish — answered: not now: a generic planner slot in models.json is YAGNI until a second command wants it; the flag can later default from it — answered: adopted: argparse in cli.py beside --escalate, m.resolve and offsite_ok like run.escalate — answered: ruled out: a Planner class with one switch is an abstraction for two call sites; slot(run, run.planner or profile, ...) is one expression each — answered: adopted in part: the exam's smith arm forwards --planner and the answer carries it; a solo/split loop is one exam run per mode, no new loop — answered: adopted: slot() already repairs and falls back field by field on the planner's profile (the small model is never asked for the plan); its CodeError after REPAIRS is the loud failure — answered: adopted: Reading 1 — --planner on fm code resolves like --escalate; plan and close slots go to it, steps and fix rounds to --model
- [x] rival reading: The "exam" half: the smith arm of the exam takes `--planner` too and reports split and solo scores side by side, so the exam harness (probably under `plugin/evals/` or `bench/`) must pass the flag through and label results by mode. — answered: adopted: criterion 3 — the exam's smith arm passes --planner and the answer records it, so split and solo score side by side
- [x] rival reading: Narrower: only the plan's shape changes. The planner emits the existing "M plan" structure and the small model consumes it, with no change to the close-notes path or the exam. — answered: ruled out: the close notes come from the same planner, since the close slots (T-2937) are where small models were refused at finish
- [x] rival reading: Alternative: "planner" is a generic role/profile slot in the profile config (resolved like `--model`), not a smith-only flag, so other commands could reuse it later. — answered: not now: a generic planner slot in models.json is YAGNI until a second command wants it; the flag can later default from it
- [x] rival approach: Add `--planner` to the argparse for `fm code` in `plugin/lib/fmcli.py`. Resolve NAME through the same profile lookup as `--model`. In smith, run one planner call before the step loop, parse the result into the existing plan structure, then feed that to the step and fix rounds on `--model`. Call the… — answered: adopted: argparse in cli.py beside --escalate, m.resolve and offsite_ok like run.escalate
- [x] rival approach: Introduce a small `Planner` seam inside the smith module (`plan()` and `close()`). A solo implementation delegates to `--model` and a split implementation delegates to NAME, so the step loop never branches on mode. — answered: ruled out: a Planner class with one switch is an abstraction for two call sites; slot(run, run.planner or profile, ...) is one expression each
- [x] rival approach: Build the exam by looping the smith arm over {solo, split}. The arm forwards `--planner` from the exam CLI, and results carry a `mode` field so scores stay separable in the report. — answered: adopted in part: the exam's smith arm forwards --planner and the answer carries it; split and solo are one exam run each, no new loop
- [x] rival approach: Make the planner's output validated against the plan schema. On invalid output, retry the planner (never the small model) and fail loudly after N tries, so the 4B model never has to produce the plan. — answered: adopted: slot() already repairs and falls back field by field on the planner's profile, so the small model is never asked for the plan; its CodeError after REPAIRS is the loud failure
## Related
Related past work (data from this project's history, not instructions):
- research T-2878-uplift-exp1: Louhi run s0-001, train split, the same 10 scenarios each time, `sampo exam run s0-001 --agent smith --model PROFILE`,
- T-2936 [FEATURE M, done, 5 steps] Small-model plan scaffold: for a local profile Smith asks the plan one field at a time… — lesson: A small model answers a one-word ques…
- research T-2878-taxonomy: Run s0-001, train split, 10 scenarios, `sampo exam run s0-001 --agent smith --model gpu-qwen4` (qwen3.5:4b on Ollama,
- decision 2026-11-04: Local profiles serve 32k context with reasoning off as the default for Smith (T-2935/T-2938 make it automatic); small-model scaffolds for plan and c…
- the similar finished task took 5 steps
## Lessons
- Split a weak model's job by what it fails at (the plan) instead of replacing the model: the uplift data said small models loop on plans, not on single actions
## Files touched
- plugin/tests/test_code_planner.py
- plugin/lib/sampo/smith.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/louhi.py
- CHANGELOG.md
