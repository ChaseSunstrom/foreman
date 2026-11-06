---
id: T-2485
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T17:10:19Z
updated: 2026-11-01T17:33:53Z
base: 96aa091d2a2b0a7d6de2af58e34648dd6a3383c4
base_tree: 0267db5199f929ab03fd4887cbd4e956f960b5a8
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-01T17:20:09Z
plan0_scope: []
verified: strong
---
# decide() on fmmodels: a kind and an input return choice, score and probability from a…
## Raw request
> FEATURE: decide() on fmmodels: a kind and an input return choice, score and probability from a backend registry (cost, latency, sensitive_ok), cheapest first, each answer in the prediction book
## Interpretation
Readings: (a) one library call, fmmodels.decide(p, kind, prompt, choices, rule=None, bar=0.8), that tries a caller's deterministic rule first, then each registered backend cheapest first (local before cloud, cloud never for a sensitive project), stops at the first answer whose probability clears the bar, validates the reply (a choice from the list, a probability in [0, 1]) and writes every answer to the prediction book for scoring; (b) a new service process. (a): the user's rules are per call (sensitive, cheapest first, probabilities scored), and nothing needs a process.
## Assumptions (confidence)
## Acceptance criteria
- [x] decide() tries the rule, then local, then cloud, stops at the first answer clearing the bar, skips cloud for a sensitive project, rejects a malformed reply and books every answer — verify with `python3 plugin/tests/run.py test_models`
## Non-goals
## Approach (options → choice → why)
1) decide() in fmmodels with a registry built from profiles() (cost and sensitive_ok from where the backend runs, latency measured on each call), the cascade, reply validation and a prediction-book row per answer. Fails if: no backend answers (it returns the rule's answer or None with why, never raises into a caller). 2) A new fmdecide module. Fails if: it duplicates fmmodels' profile and call code. 3) Use what exists: fmmodels.profiles/resolve/complete call every backend; fmforesight's predictions.jsonl and its scoring rows; c.read_meta's sensitive flag. Likely outcome: ~80 lines plus tests. 4) Do less: decide() calls one configured model. Fails if: it ignores the cheapest-first and sensitive rules the user set. Choice 1 on 3 (85%): the smallest change that meets the user's rules, on what exists.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests
2. [x] decide(), the registry, validation and booking
## Resume here
## Docs impact
MASTER (fmmodels entry), CHANGELOG Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k Decide test_models` → ✗ exit 1 · Ran 5 tests in 0.4s (1 classes, 16 at a time; slowest: Decide 0s) / FAILED (1 classes: test_models.Decide) [ran] [tree cedfa497b13f] (2026-11-01T17:21:19Z)
- `python3 plugin/tests/run.py -k Decide test_models` → ✗ exit 1 · Ran 5 tests in 1.4s (1 classes, 16 at a time; slowest: Decide 0s) / FAILED (1 classes: test_models.Decide) (start tree + this task's tests) [ran] [tree e7d4c53f64bf] (2026-11-01T17:21:53Z)
- `python3 plugin/tests/run.py -k Decide test_models` → exit 0 · Ran 5 tests in 0.5s (1 classes, 16 at a time; slowest: Decide 0s) / OK [ran] [tree e7d4c53f64bf] (2026-11-01T17:21:53Z)
- (step 2) `python3 plugin/tests/run.py test_models test_foresight test_outcomes test_code` → exit 0 · Ran 595 tests in 69.0s (125 classes, 16 at a time; slowest: Worker 69s, Fakes 42s, Survival 20s) / OK [ran] [tree e7d4c53f64bf] (2026-11-01T17:23:03Z)
- (ac 1) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 60 tests in 2.2s (9 classes, 16 at a time; slowest: Bench 2s, RunRoute 1s, OpenAIShape 1s) / OK [ran] [tree f11fe5a0cdce] (2026-11-01T17:23:19Z)
- (ac 1) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 60 tests in 2.3s (9 classes, 16 at a time; slowest: Bench 2s, RunRoute 1s, OpenAIShape 1s) / OK [ran] [tree f11fe5a0cdce] (2026-11-01T17:28:43Z)
- (audit intent) `main-thread lens pass over decide(), registry() and _answer/_booked with the five tests` → decide() follows the user's order (rule, local, cloud), stops at the first valid answer clearing the bar, keeps a sensitive project local, and books each answer for calibration scoring [tree f11fe5a0cdce] (2026-11-01T17:28:43Z)
- (audit adversary) `main-thread lens pass over decide(), registry() and _answer/_booked with the five tests` → the reply is untrusted: only a listed choice and a non-bool number in [0, 1] are taken; the prompt is labelled data in the system text; keys stay inside complete(), which already refuses plain http to a remote host [tree f11fe5a0cdce] (2026-11-01T17:28:43Z)
- (audit edge) `main-thread lens pass over decide(), registry() and _answer/_booked with the five tests` → no usable reply returns None and books nothing; a rule returning anything but a (choice, probability) pair counts as no answer; a backend error is logged in tried and the next backend runs [tree f11fe5a0cdce] (2026-11-01T17:28:43Z)
- (audit operator) `main-thread lens pass over decide(), registry() and _answer/_booked with the five tests` → tried lists each backend with ok, malformed or its error and the latency [tree f11fe5a0cdce] (2026-11-01T17:28:43Z)
- (audit maintainer) `main-thread lens pass over decide(), registry() and _answer/_booked with the five tests` → lives in fmmodels beside complete(); fmcore and fmforesight are imported lazily, so fmmodels stays stdlib-only for fm code [tree f11fe5a0cdce] (2026-11-01T17:28:43Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree f11fe5a0cdce] (2026-11-01T17:29:35Z)
## Log
- 2026-11-01T17:10:19Z created
- 2026-11-01T17:11:07Z planned: it has criteria and steps
- 2026-11-01T17:11:08Z set approved=True
- 2026-11-01T17:20:09Z focused
- 2026-11-01T17:20:09Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-01T17:23:16Z scope: plugin/lib/fmmodels.py (decide, registry), plugin/tests/test_models.py, MASTER.md, CHANGELOG.md
- 2026-11-01T17:29:05Z done
- 2026-11-01T17:29:08Z committed 5e4f5355 (4 files)
- 2026-11-01T17:29:35Z guard authorization added: publish
- 2026-11-01T17:33:53Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2437 [FEATURE L, done, 5 steps] Gen 2: a model layer (user steer 2026-10-31, start after round 1). (1) A… — lesson: A user's next-generation request has to reach the n…
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- T-1838 [FEATURE M, done, 3 steps] Fm playbooks route: top-1 missed on 3 of 3 real task titles (e.g. a stop-hook bug → strate — lesson: bm25 in FTS5 scores 0 for a word i…
- decision 2026-10-31: Standing rule (user steer 2026-10-31): gen 2 builds a model layer, small specialist models wherever a decision, ranking or lookup is the job, backen…
## Lessons
- A model call returns data, not decisions: validate the answer against the caller's own choices before anything uses it
## Plan gaps
- failed first: step 1 red tests
## Files touched
- plugin/tests/test_models.py
- plugin/lib/fmmodels.py
- CHANGELOG.md
- MASTER.md
