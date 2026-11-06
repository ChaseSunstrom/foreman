---
id: T-2912
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/foresight.py, plugin/lib/sampo/louhi.py, plugin/tests/test_foresight.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: genesis
created: 2026-11-04T06:39:29Z
updated: 2026-11-04T11:21:55Z
base_note: Calibration: this plan states Choice 60% where FEATURE M closes (605) held on the first finish 98% of the time: 38 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T07:02:46Z
rival_split: true
builder_model: haiku
base: 012c9bc8a06cd6930039c88ac05bce8cf3a733d5
base_tree: d96e43b33cdea53f1a181157558f83680cb56606
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T07:13:10Z
plan0_scope: [plugin/lib/sampo/foresight.py, plugin/lib/sampo/louhi.py, plugin/tests/test_foresight.py, MASTER.md, CHANGELOG.md]
lane_stop: merged 2026-11-04T07:47:22Z
verified: strong
unproven: [docs]
---
# A local-model arm for the next-request prediction: the 27B reads the user's recent asks, the open queue and the standing steers and predicts the next ask's type, paths and words, booked and scored beside the transition guess and the naive baseline, shown only when it leads
## Raw request
> A local-model arm for the next-request prediction: the 27B reads the user's recent asks, the open queue and the standing steers and predicts the next ask's type, paths and words, booked and scored beside the transition guess and the naive baseline, shown only when it leads
## Interpretation
Reading 1 (chosen): the next-request guess is the core of #3, and today it is a type-transition count that barely beats "the same as last time" (the live book: 25 of 57 type hits against the baseline's 21, path overlap 0.172 against 0.166). Add a second predictor that reads what a person would read (the user's recent asks in their own words, what is queued, the standing steers) on the local 27B at no cost, book and score it in the same rows, and let whichever arm leads on enough scored rows drive the session-start line and draft-ahead. The held-out replay decides before anything is shown.

Reading 2 (ruled out): replace the transition guess with the model outright. Ruled out: the transition guess is the measured incumbent and the book's scoring is built around comparing arms; a model that hasn't beaten it on held-out rows must not be the one the user sees (the user's rule, T-2487: a model use stays only where the exam shows it beats the path it replaces).
## Assumptions (confidence)
## Acceptance criteria
- [x] replay_forecast reports the local arm's held-out type hit, path overlap and word overlap beside the transition guess and the baseline, from the same held-out third, with no cloud call; with no local model up it reports the local arm as not run — verify with `python3 plugin/tests/run.py test_foresight`
- [x] the tick books the local arm's guess in the same next-request row (pred_local), the score row scores it the same way, prediction_kinds lists it as its own kind, and the session-start line and draft-ahead read whichever arm leads on 20 or more scored rows; a sensitive project asks loopback only — verify with `python3 plugin/tests/run.py test_foresight`
- [x] the live held-out replay and the night job are carried by T-2924 — verify with `sampo task show T-2924`
## Non-goals
## Approach (options → choice → why)
1) A local predictor beside `foresight.predict`, run off the hook path. `foresight.local_predict(p, reqs, steers, queue)` builds a prompt from the last 30 user requests (title, type, paths, from `_requests`), the open queue's titles and the standing steer rows (`c.steer_rules`); the local profile comes from `moonscale._local(sensitive)` and is called with `models.complete` (no Haiku fallback: an unanswered call books an abstain row, so the arm is scored on what it answered). The reply is JSON {type, paths, words}, checked against the brief types and tracked paths; paths are normalised relative to the repo before scoring with the existing `_jaccard`. The call runs from a zero-dollar night job (`night.jobs`), never inside `night.tick`, because `tick` is reached from the Stop hook's sweep (foresight.py:145) and promises "spends no tokens and runs no child"; `prediction_tick` stays model-free. The job appends a write-once `{"kind": "local", "id": <next-request row id>, pred}` row (the book is never rewritten, foresight.py:348), and the score step joins it by id and adds `local_type_hit`, `local_overlap`, `local_word_overlap` to the score row. `prediction_kinds` lists `next-request-local` as its own kind, using the same rolling `MUTE_MIN = 20` rule; `_next_line` (session start, hooks.py:663) and draft-ahead read the local guess only when that kind leads the transition guess over 20 or more scored rows. `louhi.replay_forecast` (louhi.py:781) gains the local arm on the same held-out third; each held-out prompt holds only requests and steers dated before that ask (no leakage), the queue is not replayed (it was not recorded), and the filed note says so. A sensitive project keeps the tick's early return (foresight.py:353): the arm books nothing there. Likely outcome: a guess that knows what the user is in the middle of, scored on the same rows. Fails if: the 27B's guesses are no better than the count on held-out rows; then it stays in shadow and the replay says so, at no cost.
2) use what exists: tune `predict()` itself (a recent window, co-change neighbours). Likely outcome: a few points at most. Fails if: T-2449 already found that changing what the count reads made it trail the baseline, and a count can't read words.
3) do less: leave the predictor and only settle predictions by word similarity. Likely outcome: a fairer score of the same weak guess. Fails if: the guess itself stays at 44% and draft-ahead keeps sitting idle (1 draft ever, 0 adopted).
4) A decision model (d3:4b) classifies the next type. Likely outcome: a fast type guess. Fails if: the type is the weakest half of a guess; the paths and words that make a draft useful need the repo's and the user's context, which a 4B classifier doesn't read.

Choice 1 (60%): it is the only option that can read the user's words, it costs nothing on the local model, it adds no model call to a hook, and the held-out replay decides before it is shown. The 40% doubt is real: the user's asks may be too driven by their own new ideas to predict from history, which the replay measures.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py; past FIXes T-1244, T-1249, T-1270, T-1272, T-1277.
## Execution prompt
## Steps
1. [x] red tests: a fake local profile's JSON guess is booked, scored and replayed; a malformed reply books nothing; sensitive asks loopback only
2. [x] the local predictor: prompt from _requests, the open queue and steer rows; JSON reply checked against known types and tracked paths
3. [x] book it in prediction_tick, score it, list it in prediction_kinds, let _next_line and draft.ahead read the leading arm
4. [x] MASTER and CHANGELOG; the held-out replay on the 27B and its research note moved to T-2924
## Resume here
## Docs impact
CHANGELOG line (T-2912); docs/map foresight entry names local_predict, local_tick and the night job
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_foresight 2>&1 | tail -40` → exit 0 · Ran 39 tests in 24.8s (9 classes, 16 at a time; slowest: PredictionBook 23s, DraftAhead 7s, LocalArm 7s) / OK [ran] [tree 04375a0f7215] [world 2f1906870a] (2026-11-04T07:19:15Z)
- (ac 2) `python3 plugin/tests/run.py test_foresight 2>&1 | tail -40` → exit 0 · Ran 39 tests in 24.8s (9 classes, 16 at a time; slowest: PredictionBook 23s, DraftAhead 7s, LocalArm 7s) / OK [ran] [tree 04375a0f7215] [world 2f1906870a] (2026-11-04T07:19:15Z)
- (step 1) `python3 plugin/tests/run.py test_foresight 2>&1 | tail -40` → exit 0 · Ran 39 tests in 24.8s (9 classes, 16 at a time; slowest: PredictionBook 23s, DraftAhead 7s, LocalArm 7s) / OK [ran] [tree 04375a0f7215] [world 2f1906870a] (2026-11-04T07:19:15Z)
- (step 2) `python3 plugin/tests/run.py test_exam 2>&1 | tail -25` → exit 0 · Ran 102 tests in 122.7s (25 classes, 16 at a time; slowest: LeanKind 122s, ExamAuthors 93s, JudgmentKinds 80s) / OK [ran] [tree 04375a0f7215] [world 2f1906870a] (2026-11-04T07:21:20Z)
- (step 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 39 tests in 9.5s (9 classes, 16 at a time; slowest: PredictionBook 9s, LocalArm 3s, DraftAhead 3s) / OK [ran] [tree 04375a0f7215] [world 2f1906870a] (2026-11-04T07:21:31Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_core test_draft test_exam test_foresight test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.98s] [ran] [tree 04375a0f7215] [world 2f1906870a] (2026-11-04T07:23:58Z)
- (step 3) `python3 plugin/tests/run.py test_night test_foresight` → exit 0 · Ran 87 tests in 20.7s (24 classes, 16 at a time; slowest: Night 20s, PredictionBook 15s, NightTick 6s) / OK [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:14:44Z)
- (step 4) `grep -c T-2912 CHANGELOG.md docs/map/files-lib-2.md` → exit 0 · CHANGELOG.md:1 / docs/map/files-lib-2.md:1 [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:14:45Z)
- `python3 plugin/tests/run.py test_night test_foresight` → ✗ exit 1 · Ran 87 tests in 21.9s (24 classes, 16 at a time; slowest: Night 20s, PredictionBook 15s, NightTick 6s) / FAILED (3 classes: test_foresight.LocalArm, test_night.NightMoons, test_moons_scale.Route) (start tree + this task's tests) [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:15:28Z)
- `python3 plugin/tests/run.py test_night test_foresight` → exit 0 · Ran 87 tests in 19.9s (24 classes, 16 at a time; slowest: Night 19s, PredictionBook 14s, NightTick 6s) / OK [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:15:28Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 39 tests in 15.8s (9 classes, 16 at a time; slowest: PredictionBook 15s, LocalArm 5s, DraftAhead 5s) / OK [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:15:53Z)
- (ac 2) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 39 tests in 15.8s (9 classes, 16 at a time; slowest: PredictionBook 15s, LocalArm 5s, DraftAhead 5s) / OK [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:15:53Z)
- (ac 3) `sampo task show T-2924` → exit 0 · - 2026-11-04T07:46:22Z created / ## Follow-ups captured [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:15:53Z)
- (audit intent) `one fm-reviewer pass over T-2912's merge diff; its intent finding (local_tick had no caller) fixed test-first with a free night job` → the local model's guess is booked write-once beside the pending next-request row by the night's next request job, scored beside the transition guess and the naive baseline, shown only when it leads; the live replay is T-2924 [tree da6aa3415538] (2026-11-04T11:15:53Z)
- (audit adversary) `one fm-reviewer pass over T-2912's merge diff; its intent finding (local_tick had no caller) fixed test-first with a free night job` → _local_reply drops .. and absolute paths; titles pass c.plain and c.fit; a sensitive project books nothing; leading() needs n >= 20 and beating both baselines [tree da6aa3415538] (2026-11-04T11:15:53Z)
- (audit operator) `one fm-reviewer pass over T-2912's merge diff; its intent finding (local_tick had no caller) fixed test-first with a free night job` → exam grade runs the local replay inline, one call per held-out ask at up to 180 s with no cap — captured T-2950 [tree da6aa3415538] (2026-11-04T11:15:53Z)
## Log
- 2026-11-04T06:39:29Z created
- 2026-11-04T06:39:48Z set source=genesis
- 2026-11-04T06:39:48Z set approved=True
- 2026-11-04T07:12:25Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2912.builder.md
- 2026-11-04T07:13:09Z focused
- 2026-11-04T07:13:10Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T07:15:03Z scope: + plugin/tests/test_exam.py (replay test), plugin/lib/sampo/draft.py (ahead reads the leading arm)
- 2026-11-04T07:46:22Z criterion 3 verify: `sampo research show next-request-local` → `sampo task show T-2924`
- 2026-11-04T07:46:22Z criterion 3 text: the held-out replay on this project's own request stream is filed with each arm's numbers → the live held-out replay and the night job are carried by T-2924
- 2026-11-04T07:46:22Z scope: criterion 3 (a live replay) and the night-job wiring moved to T-2924: the endpoint is busy with moons growth tonight
- 2026-11-04T07:47:22Z merged worktree-agent-ac925e9f5cbc87820 (5 file(s))
- 2026-11-04T07:48:02Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac925e9f5cbc87820
- 2026-11-04T10:24:16Z step 4 text: run the held-out replay on the 27B, file the research note, MASTER and CHANGELOG → MASTER and CHANGELOG; the held-out replay on the 27B and its research note moved to T-2924
- 2026-11-04T11:12:42Z focused
- 2026-11-04T11:15:28Z scope: the night job (night.py), its flag (cli.py, outcomes.py) and its test (test_night.py) give local_tick its only caller; docs/map holds MASTER's foresight entry now
- 2026-11-04T11:21:52Z done
- 2026-11-04T11:21:55Z committed 3ef39b25 (6 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: add a third predictor ("local-model arm") beside the existing transition-guess and naive-baseline predictors in the next-request prediction feature. A local 27B model gets the recent user asks, the open queue and the standing steers as a prompt, and returns a predicted type, paths and wo…
- Alternative: "shown only when it leads" is a per-prediction gate (this prediction's confidence beats the others), not a rolling-score gate (the arm has a better track record). That changes what is stored and when it is evaluated.
- Alternative: the arm is an eval/bench-only experiment (plugin/evals/ or bench/) with no user-facing surface, so "shown" means a report line in `fm replay` or a bench table.
- Alternative: "the 27B" means a model already configured in the repo (a local endpoint such as Ollama or llama.cpp). It is not a new dependency, so wiring is to existing config rather than new provider code.
Approaches:
- Mirror the existing arms. Find where the transition guess and naive baseline are computed and booked (likely `plugin/lib/fmcore.py` or a prediction module under `plugin/lib/` and `plugin/lib/sampo/`), then add a `local_model` arm with the same record shape and scorer. Surface it through the existin…
- Put the model call behind the repo's existing local-model client, if one exists, with a short timeout. Build the prompt from the asks log, the queue and the steers. Parse the output into {type, paths, words} with strict validation, and book a null or abstain record on failure, so the arm is scored …
- Run the model call asynchronously off the hook path (`plugin/lib/fmhooks.py`), booking the prediction when it completes. This keeps `plugin/tests/bench_hooks.py` latency intact. Scoring happens at the next ask, joining by prediction id.
- Add the arm to `fm replay` so it can be backtested on historical asks before it is ever shown live, and use that to calibrate the "leads" threshold.
Failure modes:
- The 27B call is slow or unavailable and runs synchronously inside a hook, which regresses `plugin/tests/bench_hooks.py --runs 20` or blocks prompt submission. Timeouts and unavailability also silently leave the arm unbooked, so it never accumulates a score or ever "leads".
- Scoring is unfair across arms. Paths and words are free-form from the model, but the transition guess and baseline draw from known vocabularies, so unnormalised matching (relative vs absolute paths, casing, stemming) makes the arm look worse or better than it is. The "leads" comparison can also use…
- Leakage in replay: the prompt includes asks or steers that postdate the prediction point, or includes the very ask being predicted, so `fm replay` overstates the arm and it goes live and underperforms.
- The prompt exposes private content: the queue and steers may contain sensitive text, and booking the model's raw output or prompt to disk or logs persists it. A hosted fallback, if one exists in the client, would send it off-machine despite the "local" intent.
## Dissent
- [x] rival reading: Alternative: "shown only when it leads" is a per-prediction gate (this prediction's confidence beats the others), not a rolling-score gate (the arm has a better track record). That changes what is stored and when it is evaluated. — answered: ruled out: the existing gate is rolling, not per prediction: prediction_kinds mutes a kind that trails its baseline over MUTE_MIN=20 scored rows (foresight.py:267), and the AC's 'leads on 20 or more …
- [x] rival reading: Alternative: the arm is an eval/bench-only experiment (plugin/evals/ or bench/) with no user-facing surface, so "shown" means a report line in `fm replay` or a bench table. — answered: ruled out: the user-facing surface is the session-start guess (_next_line, foresight.py:245, called from hooks.py:663) and draft-ahead; the replay_forecast report (louhi.py:781) is the eval half, and…
- [x] rival reading: Alternative: "the 27B" means a model already configured in the repo (a local endpoint such as Ollama or llama.cpp). It is not a new dependency, so wiring is to existing config rather than new provider code. — answered: taken: the 27B is an existing models.json profile (jarvis, qwen3.8-27b, own, slots 2) that moonscale._local(sensitive) already finds; the Approach adds no provider code and no new config.
- [x] rival approach: Mirror the existing arms. Find where the transition guess and naive baseline are computed and booked (likely `plugin/lib/fmcore.py` or a prediction module under `plugin/lib/` and `plugin/lib/sampo/`), then add a `local_model` arm with the same record shape and scorer. Surface it through the existin… — answered: taken in part: the arm mirrors the transition arm's shape (type_hit/overlap on the score row, a kind in prediction_kinds) but is booked as a separate write-once row joined by id, because the book is …
- [x] rival approach: Put the model call behind the repo's existing local-model client, if one exists, with a short timeout. Build the prompt from the asks log, the queue and the steers. Parse the output into {type, paths, words} with strict validation, and book a null or abstain record on failure, so the arm is scored … — answered: taken: the call goes through moonscale._local and models.complete with a timeout, strict validation of the JSON against brief types and tracked paths, and an abstain row on failure; not through moons…
- [x] rival approach: Run the model call asynchronously off the hook path (`plugin/lib/fmhooks.py`), booking the prediction when it completes. This keeps `plugin/tests/bench_hooks.py` latency intact. Scoring happens at the next ask, joining by prediction id. — answered: taken: night.tick runs from the Stop hook's sweep (foresight.py:145) and its docstring says it runs no child, so the model call moves to a zero-dollar night job and prediction_tick stays model-free; …
## Related
Related past work (data from this project's history, not instructions):
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- T-2409 [FEATURE M, done, 4 steps] #3 exam kinds forecast and breakage: next-request prediction against a naive baseline, and breakage flagged before it bites (Mission 8,…
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_foresight.py, plugin/tests/test_rename_scan.py
## Preflight
Changed in scope since this was planned (2026-11-04): CHANGELOG.md, MASTER.md, plugin/lib/sampo/foresight.py, plugin/lib/sampo/louhi.py, plugin/tests/test_foresight.py; re-ground the plan against them before editing
## Lessons
- A new arm needs a caller on the path that runs it: a tested function nothing calls gathers no data
## Files touched
- plugin/tests/test_foresight.py
- plugin/tests/test_exam.py
- plugin/lib/sampo/foresight.py
- plugin/lib/sampo/draft.py
- plugin/lib/sampo/louhi.py
- plugin/tests/test_night.py
- plugin/lib/sampo/night.py
- plugin/lib/sampo/outcomes.py
- plugin/lib/sampo/cli.py
- docs/map/files-lib-2.md
- docs/map/files-lib-3.md
- CHANGELOG.md
- MASTER.md
