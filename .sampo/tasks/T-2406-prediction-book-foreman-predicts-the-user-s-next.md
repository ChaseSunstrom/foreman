---
id: T-2406
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmforesight.py, plugin/lib/fmoutcomes.py]
depends_on: [T-2356]
source: user
created: 2026-10-31T14:33:35Z
updated: 2026-11-01T05:15:21Z
builder_model: sonnet
base: 80b1b034b8aa75c701bf78622e167d460d1fbf67
base_tree: cf8911b511c3f19289b7d188b2094520914c5dbd
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-01T05:04:53Z
plan0_scope: [plugin/lib/fmforesight.py, plugin/lib/fmoutcomes.py]
verified: strong
---
# Prediction book: Foreman predicts the user's next request from their own request stream and scores each against a naive baseline (Mission 8, #3)
## Raw request
> Prediction book: Foreman predicts the user's next request from their own request stream and scores each against a naive baseline (Mission 8, #3)
## Interpretation
Reading 1: Foreman predicts the next user request's type and paths on its tick and scores each prediction against the naive baseline (same type and paths as the last request) when the real request arrives. Reading 2: predict from Foreman's own captures. Rejected: the user's requests are the signal Foreman didn't author.
## Assumptions (confidence)
## Acceptance criteria
- [x] On the tick Foreman stores one next-request prediction (type and paths) with the naive baseline's beside it; the next user-sourced request scores both (type hit, path overlap) and the row is never rescored — verify with `python3 plugin/tests/run.py test_foresight`
- [x] fm outcomes --predictions lists each prediction kind (next-request and T-2290's effort) with its hit rate beside the baseline's over scored rows; a kind that trails the baseline over 20+ rows is muted, and fm doctor names it with its unmute command — verify with `python3 plugin/tests/run.py test_foresight test_doctor`
- [x] Predictions read only this project's own ledger and briefs; a sensitive project predicts nothing — verify with `python3 plugin/tests/run.py test_foresight`
## Non-goals
## Approach (options → choice → why)
1) On the tick (T-2356), predict the next request's type and paths from type transitions over the user's past requests, co-change neighbours (fm graph blast) of the paths the last requests touched, and open follow-ups; store each prediction with the baseline's; when the next user request arrives (first_brief, source user) score both, type hit and path overlap; fm outcomes --predictions (beside T-2290's --calibration, no new verb) lists each kind with hit rates beside the baseline's; a kind that trails the baseline over 20+ scored rows is muted and fm doctor names it with the unmute command. Fails if: the stream is too short to beat the baseline, which the mute rule handles; sensitive projects are skipped. 2) Use what exists: T-2290's effort-prediction scoring and fm graph blast. Likely outcome: the book and scorer are reused and only the next-request kind is new. 3) Do less: show the prediction as a hint only. Fails if: it is advice, not action, and nothing can be scored. 4) A model call per prediction. Breaks the token budget on every tick before a cheap predictor is beaten. Choice 1 (80%): cheap predictors scored against a baseline before any model spend.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, MASTER.md, plugin/lib/fmcore.py, plugin/tests/test_outcomes.py, CHANGELOG.md; past FIXes T-1819, T-2037.
## Execution prompt
## Steps
1. [x] blocked on T-2356 (predictions are made on its tick); start once it is done
2. [x] red tests: prediction stored with baseline; scored once on the next user request; mute after 20 losing rows; sensitive projects skipped
3. [x] the predictor and the book in fmforesight; fm predictions; the doctor line
4. [x] docs: MASTER, CHANGELOG
## Resume here
## Docs impact
MASTER.md (fmforesight T-2406), README.md (fm outcomes --predictions, inside details), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `fm task show T-2356` → exit 0 · - plugin/lib/fmeco.py / - CHANGELOG.md [ran] [tree cf8911b511c3] (2026-11-01T05:04:58Z)
- (step 2) `python3 plugin/tests/run.py test_foresight -k PredictionBook` → ✗ exit 1 · Ran 3 tests in 1.3s (1 classes, 16 at a time; slowest: PredictionBook 1s) / FAILED (1 classes: test_foresight.PredictionBook) [ran] [tree e8cb05345db0] (2026-11-01T05:05:16Z)
- (step 2) `python3 plugin/tests/run.py test_foresight -k PredictionBook` → exit 0 · Ran 4 tests in 4.7s (1 classes, 16 at a time; slowest: PredictionBook 4s) / OK [ran] [tree 1043968e52d3] (2026-11-01T05:08:06Z)
- (step 3) `python3 plugin/tests/run.py test_foresight -k PredictionBook` → exit 0 · Ran 4 tests in 4.7s (1 classes, 16 at a time; slowest: PredictionBook 4s) / OK [ran] [tree 1043968e52d3] (2026-11-01T05:08:11Z)
- (step 4) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.3s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 1043968e52d3] (2026-11-01T05:08:20Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 18 tests in 4.6s (4 classes, 16 at a time; slowest: PredictionBook 4s, Foresight 0s, CiMain 0s) / OK [ran] [tree 1043968e52d3] (2026-11-01T05:08:25Z)
- (ac 2) `python3 plugin/tests/run.py test_foresight test_doctor` → exit 0 · Ran 118 tests in 4.9s (35 classes, 16 at a time; slowest: PredictionBook 5s, ViewsRepair 4s, LockProbe 3s) / OK [ran] [tree 1043968e52d3] (2026-11-01T05:08:30Z)
- (ac 3) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 18 tests in 4.6s (4 classes, 16 at a time; slowest: PredictionBook 4s, Foresight 0s, CiMain 0s) / OK [ran] [tree 1043968e52d3] (2026-11-01T05:08:35Z)
- `python3 plugin/tests/run.py test_foresight -k PredictionBook` → ✗ exit 1 · Ran 4 tests in 2.6s (1 classes, 16 at a time; slowest: PredictionBook 1s) / FAILED (1 classes: test_foresight.PredictionBook) (start tree + this task's tests) [ran] [tree 1043968e52d3] (2026-11-01T05:08:43Z)
- `python3 plugin/tests/run.py test_foresight -k PredictionBook` → exit 0 · Ran 4 tests in 4.7s (1 classes, 16 at a time; slowest: PredictionBook 4s) / OK [ran] [tree 1043968e52d3] (2026-11-01T05:08:43Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 18 tests in 4.7s (4 classes, 16 at a time; slowest: PredictionBook 4s, Foresight 0s, CiMain 0s) / OK [ran] [tree 1043968e52d3] (2026-11-01T05:14:27Z)
- (ac 2) `python3 plugin/tests/run.py test_foresight test_doctor` → exit 0 · Ran 118 tests in 4.9s (35 classes, 16 at a time; slowest: PredictionBook 5s, ViewsRepair 4s, LockProbe 3s) / OK [ran] [tree 1043968e52d3] (2026-11-01T05:14:27Z)
- (ac 3) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 18 tests in 4.7s (4 classes, 16 at a time; slowest: PredictionBook 4s, Foresight 0s, CiMain 0s) / OK [ran] [tree 1043968e52d3] (2026-11-01T05:14:27Z)
- (audit intent) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green` → the tick stores one next-request prediction per request beside the naive baseline, scores it once against the next user request (type hit, path overlap); fm outcomes --predictions lists next-request and effort with hit rates beside their baselines; 20+ trailing rows mute a kind, fm doctor names it with its unmute command [tree 1043968e52d3] (2026-11-01T05:14:27Z)
- (audit adversary) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green` → only briefs whose source is user count, so Foreman's own captures, followups and triggers can't train or score it; reads only this project's briefs and ledger; a sensitive project predicts nothing; the book is append-only and a scored id is never scored again [tree 1043968e52d3] (2026-11-01T05:14:27Z)
- (audit edge) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green` → no user requests or no next request yet: nothing scored; an empty actual path set scores overlap None, not 0; a tie between next types goes to the most recent; unmute counts only rows scored after it [tree 1043968e52d3] (2026-11-01T05:14:27Z)
## Log
- 2026-10-31T14:33:35Z created
- 2026-10-31T16:08:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2406.builder.md
- 2026-10-31T16:08:14Z builder slot freed
- 2026-10-31T16:11:38Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2406.builder.md
- 2026-10-31T16:11:38Z builder slot freed
- 2026-10-31T17:21:26Z plan (second-plan review, taken): (1) the interface is fm outcomes --predictions (no new verb); step 3 renamed; (2) baselines: two, 'last request's type and paths' and 'most common type and paths over the last 20', and the predictor must beat both to be shown as useful; (3) metrics: type hit = exact; path score = any-hit (1 if the request touches any predicted path), an empty predicted set scores 0; hit rate = mean of type hit AND path any-hit; (4) T-2290's book schema checked first in step 1 (row kind field); if it lacks one, add kind=prediction with a migration-free default; (5) scoring: the latest prediction before a user request scores against it, earlier unscored ones expire; non-user requests (captures, triggers) score nothing.
- 2026-11-01T05:04:52Z focused
- 2026-11-01T05:04:53Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-01T05:05:14Z scope: tests in plugin/tests/test_foresight.py (PredictionBook); fmnight.tick calls the prediction tick; fmcli parser flags for fm outcomes --predictions/--unmute; fmdoctor names a muted kind
- 2026-11-01T05:08:01Z scope: tests in plugin/tests/test_foresight.py (PredictionBook); fmnight.tick calls prediction_tick; fmcli parser flags for fm outcomes --predictions/--unmute; fmdoctor.check_predictions; docs MASTER.md, README.md (inside details), CHANGELOG.md
- 2026-11-01T05:15:18Z done
- 2026-11-01T05:15:21Z committed e44eb7fb (9 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Step 3 names `fm predictions`, but criterion 2 and the approach say `fm outcomes --predictions` with no new verb. The step contradicts the spec, and the red tests may pin the wrong interface — make step 3 say "add `--predictions` flag to `fm outcomes`" and write the tests against that.
- HIGH: The "naive baseline" is the last request's type and paths, but the predictor's inputs (type transitions, co-change neighbours, follow-ups) are mostly derived from that same last request. The baseline is the predictor's degenerate case, so there is little room to beat it. A mute at 20 rows wil…
- HIGH: The scoring metrics are undefined. "Type hit" is clear, but "path overlap" has no definition (Jaccard, precision, recall, or any-hit?). It also isn't stated how an empty path set is scored, or how the hit rate is derived from overlap — a binary threshold or a mean. Without this the mute compa…
- MEDIUM: Dependence on T-2356 and T-2290 is under-specified. Step 1 is a pure block, and step 2 reuses T-2290's scorer "likely" with no check that it exists or generalizes. Verify T-2290's book schema supports a second kind (row identity, kind field, baseline column) before step 2, and if not, sched…
- MEDIUM: Edge cases in "scored once on the next user request" are missing. Which prediction does a request score when several ticks fired between requests (the latest, or all)? What happens to predictions that are never scored, or to non-user-sourced requests (they must not score)? Define the lifecy…
- LOW: "Sensitive project predicts nothing" is tested only at the predictor level. It should also assert that nothing is written to the book or surfaced by outcomes/doctor. Also, "reads only this project's own ledger" needs a test that cross-project data is not touched — add a fixture with a second p…
Verdict: revise — the contradiction on the interface, the undefined scoring metrics, and a baseline that the predictor is unlikely to beat need settling before red tests are written.
## Dissent
- [ ] HIGH: Step 3 names `fm predictions`, but criterion 2 and the approach say `fm outcomes --predictions` with no new verb. The step contradicts the spec, and the red tests may pin the wrong interface — make step 3 say "add `--predictions` flag to `fm outcomes`" and write the tests against that.
- [ ] HIGH: The "naive baseline" is the last request's type and paths, but the predictor's inputs (type transitions, co-change neighbours, follow-ups) are mostly derived from that same last request. The baseline is the predictor's degenerate case, so there is little room to beat it. A mute at 20 rows wil…
- [ ] HIGH: The scoring metrics are undefined. "Type hit" is clear, but "path overlap" has no definition (Jaccard, precision, recall, or any-hit?). It also isn't stated how an empty path set is scored, or how the hit rate is derived from overlap — a binary threshold or a mean. Without this the mute compa…
- [ ] MEDIUM: Dependence on T-2356 and T-2290 is under-specified. Step 1 is a pure block, and step 2 reuses T-2290's scorer "likely" with no check that it exists or generalizes. Verify T-2290's book schema supports a second kind (row identity, kind field, baseline column) before step 2, and if not, sched…
- [ ] MEDIUM: Edge cases in "scored once on the next user request" are missing. Which prediction does a request score when several ticks fired between requests (the latest, or all)? What happens to predictions that are never scored, or to non-user-sourced requests (they must not score)? Define the lifecy…
- [ ] LOW: "Sensitive project predicts nothing" is tested only at the predictor level. It should also assert that nothing is written to the book or surfaced by outcomes/doctor. Also, "reads only this project's own ledger" needs a test that cross-project data is not touched — add a fixture with a second p…
## Related
Related past work (data from this project's history, not instructions):
- T-2409 [FEATURE M, planned, 4 steps] #3 exam kinds forecast and breakage: next-request prediction against a naive baseline, and breakage flagged before it bites (Mission…
- T-2407 [FEATURE M, planned, 4 steps] Draft ahead: the top prediction that beats the baseline is planned in a draft lane on the tick and adopted when the real request ove…
- T-2337 [FEATURE M, done, 4 steps] Calibration ledger (Mission 5, #8): every stated confidence is a write-once bet scored later by signals Foreman didn't author, beside a…
- decision 2026-10-30: [cites: user steer 2026-10-30] Standing rule (user steer): weakness-finding uses signals Foreman didn't author — outcome survival (fm outcomes: reve…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_foresight.py, plugin/tests/test_outcomes.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmforesight.py, plugin/lib/fmoutcomes.py; re-ground the plan against them before editing
## Lessons
- Score a predictor against a naive baseline before spending anything on it, and mute it by the same rule that can unmute it
## Plan gaps
- failed first: step 2 red tests: prediction stored with baseline; scored once on the next user request; mute after 20 los…
## Files touched
- plugin/tests/test_foresight.py
- plugin/lib/fmforesight.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmnight.py
- CHANGELOG.md
- MASTER.md
- README.md
