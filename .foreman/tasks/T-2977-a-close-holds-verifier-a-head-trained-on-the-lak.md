---
id: T-2977
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2974]
source: user
created: 2026-11-04T14:20:23Z
updated: 2026-11-04T17:05:30Z
base_note: Calibration: this plan states Choice 65% where FEATURE M closes (626) held on the first finish 98% of the time: 33 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T14:49:09Z
rival_split: true
builder_model: haiku
base: 9dfdba475c25016b58829f96ab74f50cb807bdcb
base_tree: d0a36ff882d695c6c02e09cd5940001255b897fa
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T15:31:06Z
plan0_scope: []
lane_stop: merged 2026-11-04T16:49:11Z
verified: strong
unproven: [data, docs]
---
# A close-holds verifier: a head trained on the lake's outcome labels (a close later…
## Raw request
> FEATURE: A close-holds verifier: a head trained on the lake's outcome labels (a close later reverted or fixed counts as false) scores each close before fm task finish lands it, Smith's close and Louhi's grader read it, and a low score asks for the missing evidence instead of closing; measured on held-out projects against today's false-done rate (exp 2: 4 of gemma's 5 closes were false-done)
> CONTEXT: from the model brainstorm (research brainstorm-20261104-model, T-2973): Sampo's own models must be generic across every project built with Sampo, trained on outcomes, adopted per slot only where they beat today's path on whole held-out projects.
## Interpretation
Reading 1 (chosen): a close-holds verifier that learns only from outcomes and machine signals, never from Claude-written text (Anthropic's terms; the lake's agent text stays off): each lake row gains a features dict computed from the brief and git at close (criteria, steps and evidence counts, red-then-green proofs, tests run and passed parsed from evidence, audits and lenses, files and lines changed, minutes active, tier, type), and Louhi's exam closes add rows labelled by their verify (false_done = closed and red). A pure-Python logistic head (no numpy here) trains on rows of all projects but the held-out one, outputs P(holds), and runs in shadow: sampo task finish and Smith's close log the score; it only asks for the missing evidence when models.live adopts it per T-2976's floor. Reading 2 (ruled out): embed the briefs' text; most of that text is Claude's.
## Assumptions (confidence)
## Acceptance criteria
- [x] lake rows carry a text-free features dict; sampo exam models --verifier trains a logistic head with whole projects held out and writes per-project AUC and false-done-caught-at-10%-false-alarm to bench.jsonl and the weights to the project's state — verify with `python3 plugin/tests/run.py test_lake test_verifier`
- [x] task finish and Smith's close log a close_score event in shadow and change no outcome unless models.live names the verifier, which then asks for the missing evidence below the threshold — verify with `python3 plugin/tests/run.py test_verifier test_code_worker`
## Non-goals
## Approach (options → choice → why)
1) Structural features plus a logistic head. Add a `features` dict to lake rows: counts and parsed test totals only, no text. Add a `sampo exam models --verifier` that trains the head on lake rows and Louhi exam closes, with whole projects held out (the same split as T-2976). It writes the weights to the project's research/models/verifier.json, AUC per held-out project, and the false-done caught at a fixed 10% false-alarm rate. Then a shadow score: finish and Smith's close log `close_score` events. Likely outcome: a cheap, explainable scorer that can be compared against today's false-done rate. Fails if: 92 negatives are too few. The exam closes add test-graded negatives, and the measured AUC decides adoption; the head is not adopted on faith.
2) use what exists: louhi's retrieval k-NN (T-2975) pointed at the evidence text (tool output). Likely outcome: a near-duplicate detector of past failures. Fails if: evidence text is formulaic and every close looks the same.
3) do less: rules only (today's gates). Likely outcome: no change. Fails if: exp 2's 4 of 5 false-dones pass today's gates.
Choice 1 (65%): outcomes and machine signals only, explainable, cheap, measured per held-out project before any live use.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: features from a fixture brief; a head separates a planted signal on two projects and is scored on a third; shadow logs, live asks
2. [x] features in lake.py, the head and --verifier in a new verifier.py, the shadow hook at finish and Smith's close
3. [x] a live --verifier run across this machine's projects; the numbers in research
## Resume here
<!-- auto -->
- 2026-11-04T16:02:31Z step 3/3: a live --verifier run across this machine's projects; the numbers in research
- git: worktree-agent-a780bb85a43467278; 3 uncommitted: plugin/lib/sampo/louhi.py, plugin/lib/sampo/verifier.py, plugin/tests/test_verifier.py
- touched since last checkpoint: plugin/tests/test_code_worker.py, plugin/lib/sampo/lake.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/verifier.py, plugin/lib/sampo/louhi.py, plugin/tests/test_verifier.py
## Docs impact
CHANGELOG line; research T-2977-verifier; MASTER bullet and map line
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_verifier 2>&1 | tail -15` → exit 0 · Ran 12 tests in 8.9s (4 classes, 16 at a time; slowest: Lake2 9s, Shadow 1s, Head 0s) / OK [ran] [tree 74ec700f671c] [world 2f1906870a] (2026-11-04T15:35:02Z)
- (step 2) `python3 plugin/tests/run.py test_lake test_verifier test_code_worker` → exit 0 · Ran 97 tests in 245.1s (10 classes, 16 at a time; slowest: Worker 245s, Lake2 21s, Failover 17s) / OK [ran] [tree 74ec700f671c] [world 2f1906870a] (2026-11-04T15:39:09Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_code_worker test_core test_exam test_lake test_left_out test_louhi_models test_mint test_moons_scale test_rename_scan test_verifier test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [14.00s] [ran] [tree 74ec700f671c] [world 2f1906870a] (2026-11-04T15:44:39Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_code_worker test_core test_exam test_lake test_left_out test_louhi_models test_mint test_moons_scale test_rename_scan test_verifier test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 570 tests in 279.7s (128 classes, 16 at a time; slowest: Worker 261s, LeanKind 196s, ExamAuthors 181s) / FAILED (1 classes: test_exam.LeanKind) [ran] [tree 74ec700f671c] [world 2f1906870a] (2026-11-04T15:44:39Z)
- (step 2) `python3 plugin/tests/run.py test_verifier` → exit 0 · Ran 13 tests in 9.5s (4 classes, 16 at a time; slowest: Lake2 9s, Shadow 3s, Head 1s) / OK [ran] [tree fb83425acd3a] [world 2f1906870a] (2026-11-04T16:06:29Z)
- (step 3) `sampo exam models --verifier` → exit 0 · verifier: 590 closes, pooled held-out AUC 0.5547, false-done caught at 10% false alarms 0.2283 (today lets 0.1559 by); weights written [ran] [tree 39795cbbf611] [world 2f1906870a] (2026-11-04T16:49:39Z)
- (step 1) `python3 plugin/tests/run.py test_verifier test_lake` → exit 0 · Ran 18 tests in 9.7s (5 classes, 16 at a time; slowest: Lake2 9s, Lake 8s, Shadow 2s) / OK [ran] [tree 39795cbbf611] [world 2f1906870a] (2026-11-04T16:49:52Z)
- `python3 plugin/tests/run.py test_verifier` → ✗ exit 1 · Ran 0 tests in 1.8s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) (start tree + this task's tests) [ran] [tree 39795cbbf611] [world 2f1906870a] (2026-11-04T16:50:05Z)
- `python3 plugin/tests/run.py test_verifier` → exit 0 · Ran 13 tests in 9.6s (4 classes, 16 at a time; slowest: Lake2 9s, Shadow 2s, Head 0s) / OK [ran] [tree 39795cbbf611] [world 2f1906870a] (2026-11-04T16:50:05Z)
- (ac 1) `python3 plugin/tests/run.py test_lake test_verifier` → exit 0 · Ran 18 tests in 28.2s (5 classes, 16 at a time; slowest: Lake2 27s, Lake 24s, Shadow 7s) / OK [ran] [tree ef783de8d095] [world 2f1906870a] (2026-11-04T16:54:24Z)
- (ac 2) `python3 plugin/tests/run.py test_verifier test_code_worker` → exit 0 · Ran 93 tests in 164.2s (9 classes, 16 at a time; slowest: Worker 163s, Lake2 28s, Failover 21s) / OK [ran] [tree ef783de8d095] [world 2f1906870a] (2026-11-04T16:54:24Z)
- (audit adversary) `branch reviewed by an fm-reviewer (adversary, edge, intent); its 6 findings fixed test-first on the branch (typed evidence can't feed counts, retries can't raise a score, held-out threshold, stale weights removed, no-weights noise gone, run ids); merge conflict resolved on the branch; live run across 590 closes; prove red on the start tree, green now` → features are numbers parsed only from Sampo-run evidence after the arrow; a typed 'Ran 500 tests' line and repeated audits change nothing (tested); a corrupt or missing weights file never blocks a close [tree ef783de8d095] (2026-11-04T16:54:24Z)
- (audit edge) `branch reviewed by an fm-reviewer (adversary, edge, intent); its 6 findings fixed test-first on the branch (typed evidence can't feed counts, retries can't raise a score, held-out threshold, stale weights removed, no-weights noise gone, run ids); merge conflict resolved on the branch; live run across 590 closes; prove red on the start tree, green now` → one-class or empty folds return no AUC; a missing class deletes stale weights; the live threshold comes from pooled held-out scores [tree ef783de8d095] (2026-11-04T16:54:24Z)
- (audit intent) `branch reviewed by an fm-reviewer (adversary, edge, intent); its 6 findings fixed test-first on the branch (typed evidence can't feed counts, retries can't raise a score, held-out threshold, stale weights removed, no-weights noise gone, run ids); merge conflict resolved on the branch; live run across 590 closes; prove red on the start tree, green now` → shadow-only until T-2976's floor adopts it; the first live AUC (0.55 pooled) says it shouldn't be adopted yet, and it isn't [tree ef783de8d095] (2026-11-04T16:54:24Z)
## Log
- 2026-11-04T14:20:23Z created
- 2026-11-04T14:20:34Z set depends_on=['T-2974']
- 2026-11-04T14:48:51Z planned: it has criteria and steps
- 2026-11-04T14:48:51Z set approved=True
- 2026-11-04T14:49:15Z steer: below threshold the ask names the head's top-weighted missing features by template
- 2026-11-04T15:30:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2977.builder.md
- 2026-11-04T15:31:05Z focused
- 2026-11-04T15:31:06Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T16:49:11Z merged worktree-agent-a780bb85a43467278 (5 file(s))
- 2026-11-04T16:49:17Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a780bb85a43467278
- 2026-11-04T16:49:33Z focused
- 2026-11-04T16:50:52Z scope: fmverifier.py shim, MASTER.md bullet and files-lib-3 map line the builder left out (self docs gate)
- 2026-11-04T17:05:28Z done
- 2026-11-04T17:05:30Z committed 5a78a460 (5 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: an offline-trained classifier plus a runtime gate.** A scorer trained on lake outcome labels (close later reverted or fixed = false-done) is called inside `fm task finish` (likely `plugin/lib/fmcli.py` / `plugin/lib/fmcore.py`). A low score blocks the close and returns a "missing evide…
- **Evaluation-first reading: the deliverable is the measurement harness.** The head is a thin baseline and the real product is a held-out-by-project split and a comparison against today's path, in the style of `plugin/evals/`, `bench/` and `fm replay`. Adoption per slot depends on it beating today's…
- **Advisory-only reading.** The score is surfaced to Smith and Louhi as a signal and never blocks `fm task finish`. The "ask for missing evidence" part is a prompt or skill change under `plugin/skills/`, not a hard gate in `plugin/lib/fmguard.py` or `plugin/lib/fmhooks.py`.
- **Narrow reading: a rule-based or LLM-judge precursor.** There is no training yet. Features such as missing test output or no diff evidence are scored by rules and checked against the 5 exp-2 closes. The trained head comes later once the lake has enough labels.
Approaches:
- **Gradient-boosted or logistic head on structured close features.** Features are diff size, tests run, evidence artifacts attached, task type and claimed-vs-observed checks. Labels are derived from lake events where a close was later reverted or reopened by a fix. Train in a new `plugin/lib/` modul…
- **Embedding or LM head over the close transcript.** Frozen encoder features of the closing summary and evidence feed a linear head. This is more general across projects but heavier at runtime and harder to run inside the hook latency budget (`plugin/tests/bench_hooks.py --runs 20`).
- **Shadow mode first, then enforce per slot.** The scorer runs inside `fm task finish` and logs `score` and `decision` to the lake without blocking. Smith and Louhi read the logged value. A flag per slot turns on enforcement only after `fm replay` over held-out projects shows a lower false-done rate…
- **Evidence-request generation from feature attribution.** When the score is below threshold, map the top contributing missing features (for example no test run, or no verification of the claimed file) to a fixed message template. This avoids a free-text generation step and keeps the "missing eviden…
Failure modes:
- **Label leakage and delayed labels.** "Reverted or fixed later" labels only exist for old closes, so recent closes are censored and look true. If the split is by time or by task and not by whole project, or if the features include post-close signals, the held-out gain is inflated. The baseline of 4…
- **Gate deadlock or evidence gaming.** A low score blocks the close, the agent adds boilerplate evidence to raise the score, and the head learns surface features rather than truth. Or the gate loops forever with no escape hatch, so `fm task finish` needs a bounded retry and an explicit override reco…
- **Hook latency or availability regression.** Loading the model in `fm task finish` or inside `plugin/lib/fmhooks.py` breaks the `bench_hooks.py` budget, or a missing model file or version mismatch makes finishing fail closed. It should fail open with a logged "unscored" outcome.
- **Smith and Louhi disagree with the gate.** Louhi's grader reads the score and treats it as ground truth, so the grader's own errors correlate with the head's. Offline gains then do not transfer, and a per-slot adoption decision made on a mixed signal is unsound.
## Dissent
- [x] rival reading: **Likeliest: an offline-trained classifier plus a runtime gate.** A scorer trained on lake outcome labels (close later reverted or fixed = false-done) is called inside `fm task finish` (likely `plugin/lib/fmcli.py` / `plugin/lib/fmcore.py`). A low score blocks the close and returns a "missing evide… — answered: the gate is in the plan, behind models.live; shadow until the floor says live
- [x] rival reading: **Evaluation-first reading: the deliverable is the measurement harness.** The head is a thin baseline and the real product is a held-out-by-project split and a comparison against today's path, in the style of `plugin/evals/`, `bench/` and `fm replay`. Adoption per slot depends on it beating today's… — answered: adopted in part: per-project AUC and false-done-caught are the deliverable's numbers; T-2976 owns adoption
- [x] rival reading: **Advisory-only reading.** The score is surfaced to Smith and Louhi as a signal and never blocks `fm task finish`. The "ask for missing evidence" part is a prompt or skill change under `plugin/skills/`, not a hard gate in `plugin/lib/fmguard.py` or `plugin/lib/fmhooks.py`. — answered: shadow is the default; live asks only after adoption
- [x] rival reading: **Narrow reading: a rule-based or LLM-judge precursor.** There is no training yet. Features such as missing test output or no diff evidence are scored by rules and checked against the 5 exp-2 closes. The trained head comes later once the lake has enough labels. — answered: ruled out: rules are today's path, the head is measured against it
- [x] rival approach: **Gradient-boosted or logistic head on structured close features.** Features are diff size, tests run, evidence artifacts attached, task type and claimed-vs-observed checks. Labels are derived from lake events where a close was later reverted or reopened by a fix. Train in a new `plugin/lib/` modul… — answered: matches choice 1 (logistic, pure Python; no numpy on this box)
- [x] rival approach: **Embedding or LM head over the close transcript.** Frozen encoder features of the closing summary and evidence feed a linear head. This is more general across projects but heavier at runtime and harder to run inside the hook latency budget (`plugin/tests/bench_hooks.py --runs 20`). — answered: ruled out: the closing summary is Claude's text; hook latency too
- [x] rival approach: **Shadow mode first, then enforce per slot.** The scorer runs inside `fm task finish` and logs `score` and `decision` to the lake without blocking. Smith and Louhi read the logged value. A flag per slot turns on enforcement only after `fm replay` over held-out projects shows a lower false-done rate… — answered: matches the plan
- [x] rival approach: **Evidence-request generation from feature attribution.** When the score is below threshold, map the top contributing missing features (for example no test run, or no verification of the claimed file) to a fixed message template. This avoids a free-text generation step and keeps the "missing eviden… — answered: adopted: the ask names the top missing features from the weights via a fixed template, no generation
## Related
Related past work (data from this project's history, not instructions):
- T-2974 [FEATURE M, done, 3 steps] The training lake: `sampo models export` (under an existing verb, no new top-level verb)… — lesson: Grep a live export for the user's o…
- research brainstorm-20261104-model: Request (T-2973): "should we/could we train a model to fit sampo better? like a better kev/whatever to do more things and more than j…
- T-2975 [FEATURE M, done, 3 steps] A retrieval baseline decider: for a new brief, the k nearest closed briefs by bge-m3… — lesson: A criterion that checks a live artifact…
- decision 2026-11-04: [costly] [confidence: 85%] Sampo's trained models learn only from outcomes, user-written text and labels, and local-model traces graded by tests, ne…
## Lessons
- A verifier's honest first number can be weak; shipping it in shadow with a measured floor beats tuning it until it looks good
## Files touched
- plugin/tests/test_verifier.py
- plugin/tests/test_code_worker.py
- plugin/lib/sampo/verifier.py
- plugin/lib/sampo/lake.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/cli.py
- .fm-scratch-run.log
- CHANGELOG.md
- plugin/lib/sampo/core.py
- plugin/lib/sampo/foresight.py
- plugin/lib/sampo/mint.py
- plugin/lib/sampo/models.py
- plugin/tests/test_board_posture.py
- plugin/tests/test_exam.py
- plugin/tests/test_foresight.py
- plugin/tests/test_louhi_models.py
- plugin/tests/test_mint.py
- plugin/tests/test_planning.py
- research/models/bench.jsonl
- plugin/lib/fmverifier.py
- MASTER.md
- docs/map/files-lib-3.md
