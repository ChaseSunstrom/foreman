---
id: T-2857
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T00:02:59Z
updated: 2026-11-04T00:32:37Z
steer_method_rate: 0.218
group: no mid-run questions, keep working
base: 1a723cfba7e521b7d61443b7b60c4b80bafab00c
base_tree: 40b1625ea729f4e039bf731f211f72bc582fac0a
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T00:31:18Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# **Work autonomously.** Don't ask the user for input, preferences, confirmation or…
## Raw request
> stop asking me for stuff, keep going, and then continue working on the tower/moons, and the moons you had come up with aren't even that "moon"y, theyre not that wild of ideas, I want wild.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
Reading 1 (chosen): 'stop asking me for stuff' covers every way a run interrupts the user: an AskUserQuestion and a permission prompt raised by fm ask (approval_granted via prompt, logged at 00:01:02Z, two minutes before the steer). The steer gets a runnable check: fm outcomes --questions counts both, and --none fails on either since the steer. Reading 2 (ruled out): only AskUserQuestion; the steer came right after an fm ask prompt, so that reading misses the very ask that prompted it.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm outcomes --questions also counts permission prompts (approval_granted via prompt) and --none fails on one since TS; the steer is recorded with that check — verify with `python3 plugin/tests/run.py test_question_answers`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: the --questions report (T-2840) reads question_answered rows; add approval_granted rows whose via is prompt as 'prompts'; --none fails when calls or prompts > 0. Likely outcome: 4 lines plus a test. Fails if a grant through a standing yes logs via prompt too; those log via standing, so they don't count.
2. A separate --prompts flag. Fails: two checks for one steer; one --none should mean nobody was interrupted.
Choice 1 (85%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then prompts in the --questions count; record the steer's decision with the check
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_question_answers` → ✗ exit 1 · Ran 5 tests in 2.1s (1 classes, 16 at a time; slowest: QuestionAnswers 1s) / FAILED (1 classes: test_question_answers.QuestionAnswers) (start tree + this task's tests) [ran] [tree 1017f9673a48] [world 2f1906870a] (2026-11-04T00:31:35Z)
- `python3 plugin/tests/run.py test_question_answers` → ✗ exit 1 · Ran 5 tests in 0.9s (1 classes, 16 at a time; slowest: QuestionAnswers 1s) / FAILED (1 classes: test_question_answers.QuestionAnswers) [ran] [tree 1017f9673a48] [world 2f1906870a] (2026-11-04T00:31:35Z)
- (step 1) `python3 plugin/tests/run.py test_question_answers` → exit 0 · Ran 5 tests in 1.0s (1 classes, 16 at a time; slowest: QuestionAnswers 1s) / OK [ran] [tree e18b060ef90e] [world 2f1906870a] (2026-11-04T00:31:55Z)
- `python3 plugin/tests/run.py test_question_answers` → ✗ exit 1 · Ran 5 tests in 2.1s (1 classes, 16 at a time; slowest: QuestionAnswers 1s) / FAILED (1 classes: test_question_answers.QuestionAnswers) (start tree + this task's tests) [ran] [tree e18b060ef90e] [world 2f1906870a] (2026-11-04T00:32:05Z)
- `python3 plugin/tests/run.py test_question_answers` → exit 0 · Ran 5 tests in 1.0s (1 classes, 16 at a time; slowest: QuestionAnswers 1s) / OK [ran] [tree e18b060ef90e] [world 2f1906870a] (2026-11-04T00:32:05Z)
- (ac 1) `python3 plugin/tests/run.py test_question_answers` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T00:32:05Z [ran] [tree e18b060ef90e] [world 2f1906870a] (2026-11-04T00:32:05Z)
- (audit edge) `self-review: --questions adds approval_granted and approval_declined rows since TS as prompts; --none fails on any question or prompt; the steer's decision carries the check with the steer's time` → a grant before --since doesn't count (tested via the real ledger: the 00:01:02Z prompt counts for the 14:55 steer, not the 00:02 one) [tree e18b060ef90e] (2026-11-04T00:32:05Z)
- (audit self) `self-review: --questions adds approval_granted and approval_declined rows since TS as prompts; --none fails on any question or prompt; the steer's decision carries the check with the steer's time` → no findings [tree e18b060ef90e] (2026-11-04T00:32:05Z)
## Log
- 2026-11-04T00:02:59Z created
- 2026-11-04T00:31:16Z planned: it has criteria and steps
- 2026-11-04T00:31:17Z focused
- 2026-11-04T00:31:18Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T00:32:35Z done
- 2026-11-04T00:32:37Z committed 1c5eb344 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2805 [FEATURE S, done, 0 steps] Work autonomously by default: when the next step is clear, take it instead of pausing to…
- T-2771 [FEATURE S, done, 0 steps] When the current task is finished, do not stop or wait for further prompting:…
- decision 2026-11-04: [cites: user steer 2026-11-03: the moons you had come up with aren't even that moony, theyre not that wild of ideas, I want wild] [check: python3 pl…
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- similar finished tasks took 0–1 steps
## Why not caught
T-2840 counted AskUserQuestion only; an fm ask permission prompt interrupts the user the same way
## Files touched
- plugin/tests/test_question_answers.py
- plugin/lib/sampo/outcomes.py
