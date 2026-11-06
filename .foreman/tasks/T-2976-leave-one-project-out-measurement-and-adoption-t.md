---
id: T-2976
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2975]
source: user
created: 2026-11-04T14:20:23Z
updated: 2026-11-04T17:56:28Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (626) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T14:50:06Z
rival_split: true
builder_model: haiku
base: 808169ca43b29f93a433b7aa2c2eadf275e43f6a
base_tree: 2026f70735c9d9710dbef043ee98339b3bf17341
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T15:31:13Z
plan0_scope: []
lane_stop: merged 2026-11-04T16:21:19Z
verified: strong
---
# Leave-one-project-out measurement and adoption: the model bench holds out whole…
## Raw request
> FEATURE: Leave-one-project-out measurement and adoption: the model bench holds out whole projects, draws each slot's coverage-versus-accuracy curve with an abstain that falls back to today's rules, adopts a use (models.live) only above a statistical floor, auto-reverts when live agreement drops, and writes a flip report each Rune generation
> CONTEXT: from the model brainstorm (research brainstorm-20261104-model, T-2973): Sampo's own models must be generic across every project built with Sampo, trained on outcomes, adopted per slot only where they beat today's path on whole held-out projects.
## Interpretation
Reading 1 (chosen): Louhi's model bench grows a leave-one-project-out mode across every Sampo project on the machine (each project in turn held out whole, the others its training pool), each use's coverage-versus-accuracy curve over abstain thresholds, and an adoption rule on top of models.live: a use goes live only when it beats today's path on held-out projects above a statistical floor (a one-sided binomial bound), and drops back to shadow when its live agreement falls under the floor; a flip report lists what changed between two bench runs. Reading 2 (ruled out): a new registry module; models.live and its decision rows already are the registry.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo exam models --loo holds each project out whole and writes per-project and pooled rows with coverage at each abstain threshold and a Wilson lower bound per contestant — verify with `python3 plugin/tests/run.py test_louhi_models`
- [x] --adopt writes model-live for a use only when its lower bound beats today's path on held-out projects, and a live use drops to shadow when its live agreement falls under the floor; a flip report names each change between two runs — verify with `python3 plugin/tests/run.py test_louhi_models test_models`
## Non-goals
## Approach (options → choice → why)
1) Extend bench_models with --loo: the data step reads every Sampo project's closed briefs (sensitive ones only on loopback backends), holds each project out in turn, scores each contestant (majority, orchestrator, retrieval, the decision backends) per held-out project and pooled; rows carry project hashes, coverage at each abstain threshold, and a Wilson lower bound; `sampo exam models --adopt` writes 'model-live: USE' only when the bound beats today's path, and the night's tick demotes on live disagreement. Likely outcome: an honest, cross-project bar every model in the slate must clear. Fails if: small projects give too few rows; the floor then keeps the use in shadow, which is the right answer.
2) use what exists: the bench's task-id-hash split. Likely outcome: no change. Fails if: it never tests a project the model hasn't seen, which is the generic claim.
3) do less: report per-project accuracy only, no adoption rule. Likely outcome: numbers, no decision. Fails if: models.live stays hand-set.
Choice 1 (75%): the generic claim needs whole projects held out, and adoption needs a floor, not a hand edit.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: three fake projects, a contestant that wins on two and loses on the held-out third
2. [x] --loo in bench_models, the Wilson bound, --adopt and the demotion, the flip report
3. [x] a live --loo run across this machine's projects; the numbers in research
## Resume here
<!-- auto -->
- 2026-11-04T16:02:28Z step 3/3: a live --loo run across this machine's projects; the numbers in research
- git: worktree-agent-a912aff7e65031f7d; 3 uncommitted: plugin/lib/sampo/louhi.py, plugin/lib/sampo/models.py, plugin/tests/test_louhi_models.py
- touched since last checkpoint: plugin/lib/sampo/cli.py, plugin/tests/test_louhi_models.py, plugin/lib/sampo/models.py, plugin/lib/sampo/louhi.py
## Docs impact
CHANGELOG line; research T-2976-loo
## Verification evidence
- (ac 2) `python3 plugin/tests/run.py test_louhi_models test_models 2>&1 | tail -30` → exit 0 · Ran 95 tests in 14.3s (16 classes, 16 at a time; slowest: LouhiModels 13s, Bench 3s, RunRoute 1s) / OK [ran] [tree 6378a12592cf] [world 2f1906870a] (2026-11-04T15:34:37Z)
- (step 1) `python3 plugin/tests/run.py test_louhi_models test_models 2>&1 | tail -30` → exit 0 · Ran 95 tests in 14.3s (16 classes, 16 at a time; slowest: LouhiModels 13s, Bench 3s, RunRoute 1s) / OK [ran] [tree 6378a12592cf] [world 2f1906870a] (2026-11-04T15:34:37Z)
- (step 1) `python3 plugin/tests/run.py test_louhi_models` → exit 0 · Ran 15 tests in 13.1s (2 classes, 16 at a time; slowest: LouhiModels 13s, LouhiLoo 1s) / OK [ran] [tree 6378a12592cf] [world 2f1906870a] (2026-11-04T15:34:54Z)
- (step 2) `python3 plugin/tests/run.py test_louhi_models test_models` → exit 0 · Ran 95 tests in 17.0s (16 classes, 16 at a time; slowest: LouhiModels 17s, Bench 3s, RunRoute 1s) / OK [ran] [tree 6378a12592cf] [world 2f1906870a] (2026-11-04T15:35:12Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_code_hardening test_code_worker test_core test_ctx_variant test_exam test_left_out test_louhi_models test_mint test_models test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [13.34s] [ran] [tree 6378a12592cf] [world 2f1906870a] (2026-11-04T15:39:42Z)
- (ac 2) `python3 plugin/tests/run.py test_louhi_models test_models` → exit 0 · Ran 98 tests in 15.2s (16 classes, 16 at a time; slowest: LouhiModels 15s, Bench 3s, RunRoute 2s) / OK [ran] [tree df9d67716ab0] [world 2f1906870a] (2026-11-04T16:05:37Z)
- (step 3) `python3 plugin/tests/run.py test_louhi_models test_models` → exit 0 · Ran 98 tests in 15.2s (16 classes, 16 at a time; slowest: LouhiModels 15s, Bench 3s, RunRoute 2s) / OK [ran] [tree df9d67716ab0] [world 2f1906870a] (2026-11-04T16:05:37Z)
- (step 2) `python3 plugin/tests/run.py test_louhi_models test_models` → exit 0 · Ran 98 tests in 15.3s (16 classes, 16 at a time; slowest: LouhiModels 15s, Bench 3s, LouhiLoo 1s) / OK [ran] [tree df9d67716ab0] [world 2f1906870a] (2026-11-04T16:06:33Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_code_hardening test_code_worker test_core test_ctx_variant test_exam test_left_out test_louhi_models test_mint test_models test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [17.61s] [ran] [tree df9d67716ab0] [world 2f1906870a] (2026-11-04T16:09:14Z)
- `python3 plugin/tests/run.py test_louhi_models test_models` → ✗ exit 1 · Ran 98 tests in 13.3s (16 classes, 16 at a time; slowest: LouhiModels 12s, Bench 2s, RunRoute 1s) / FAILED (1 classes: test_louhi_models.LouhiLoo) (start tree + this task's tests) [ran] [tree 37ca9cffa40a] [world 2f1906870a] (2026-11-04T17:53:58Z)
- `python3 plugin/tests/run.py test_louhi_models test_models` → exit 0 · Ran 98 tests in 12.1s (16 classes, 16 at a time; slowest: LouhiModels 12s, Bench 2s, RunRoute 1s) / OK [ran] [tree 37ca9cffa40a] [world 2f1906870a] (2026-11-04T17:53:58Z)
- (ac 1) `python3 plugin/tests/run.py test_louhi_models` → exit 0 · Ran 18 tests in 12.0s (2 classes, 16 at a time; slowest: LouhiModels 12s, LouhiLoo 1s) / OK [ran] [tree 37ca9cffa40a] [world 2f1906870a] (2026-11-04T17:54:16Z)
- (ac 2) `python3 plugin/tests/run.py test_louhi_models test_models` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T17:53:58Z [ran] [tree 37ca9cffa40a] [world 2f1906870a] (2026-11-04T17:54:16Z)
- (audit edge) `branch reviewed by an fm-reviewer (edge, intent): the 3-project bootstrap loophole, tie epsilon, None confidence, the baseline's honest name and demotion on the same rows fixed test-first on the branch; live run across 8 held-out projects; prove red on the start tree, green now` → 3 projects with one regressing stay shadow (tested); a tie can't adopt (1e-9); a None confidence falls back to the path [tree 37ca9cffa40a] (2026-11-04T17:54:16Z)
- (audit intent) `branch reviewed by an fm-reviewer (edge, intent): the 3-project bootstrap loophole, tie epsilon, None confidence, the baseline's honest name and demotion on the same rows fixed test-first on the branch; live run across 8 held-out projects; prove red on the start tree, green now` → the row and the verdict name the baseline actually used (majority here: lake rows carry no path call); nothing went live without --adopt [tree 37ca9cffa40a] (2026-11-04T17:54:16Z)
- (audit adversary) `branch reviewed by an fm-reviewer (edge, intent): the 3-project bootstrap loophole, tie epsilon, None confidence, the baseline's honest name and demotion on the same rows fixed test-first on the branch; live run across 8 held-out projects; prove red on the start tree, green now` → adoption only through a decision row citing the bench run; demotion when live agreement drops [tree 37ca9cffa40a] (2026-11-04T17:54:16Z)
## Log
- 2026-11-04T14:20:23Z created
- 2026-11-04T14:28:06Z planned: it has criteria and steps
- 2026-11-04T14:28:07Z set approved=True
- 2026-11-04T14:28:07Z set depends_on=['T-2975']
- 2026-11-04T14:50:17Z steer: floor = lower bound of (model - today's path) over held-out projects > 0, min 3 projects; one resolve() wrapper for bench and live
- 2026-11-04T15:31:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2976.builder.md
- 2026-11-04T15:31:12Z focused
- 2026-11-04T15:31:13Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T16:21:19Z merged worktree-agent-a912aff7e65031f7d (4 file(s))
- 2026-11-04T16:21:32Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a912aff7e65031f7d
- 2026-11-04T17:53:13Z focused
- 2026-11-04T17:56:28Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a full pipeline in a new bench module (under `bench/` or `plugin/lib/`): leave-one-project-out (LOPO) evaluation per slot, a coverage-vs-accuracy curve with an abstain that falls back to current rules, a threshold-gated adoption writing `models.live`, a live-agreement monitor that auto-r…
- Measurement only: LOPO bench, curves and flip report, with adoption (`models.live`) and auto-revert left as a stub or manual step. The "adopts" and "auto-reverts" wording argues against this, but it is the safe MVP split.
- Adoption and revert machinery only: assume a model bench already exists and just add the `models.live` gate, the agreement tracking and the revert. I can't confirm any bench exists from the map (`bench/` has 11 files, unread), so this reading depends on what is there.
- "Rune generation" may be an existing concept (probably in `plugin/lib/fmgenesis.py`, given the `site/genesis` entry) or a new one. The flip report's trigger depends on which.
Approaches:
- Extend what exists: read `bench/` and the `fmgenesis.py` generation hook first. Add LOPO splitting keyed by project id, store the per-slot curves as JSON, and read `models.live` from the same config path `fmcore.py` already uses. The flip report becomes a hook at generation time. This is the lowest…
- Standalone module, e.g. `plugin/lib/sampo/modelbench.py`, with a CLI subcommand in `plugin/lib/sampo/cli.py` (`sampo bench models`). Pure functions: `lopo_splits`, `slot_curve`, `pick_threshold`, `decide_adoption`. State is written only through one `models.live` writer. This is easiest to unit-test…
- Decide the statistical floor first. Use a lower confidence bound (e.g. Wilson or a bootstrap over held-out *projects*, not rows) on the model-minus-rules accuracy difference at a chosen coverage, and adopt only if the bound is above zero with a minimum project count. Everything else hangs off this …
- Make the abstain-fallback the single dispatch point. Each slot call goes through a wrapper `resolve(slot, input)` that returns the model answer if confidence ≥ threshold and otherwise calls today's rule path, so the same wrapper serves both the bench and live use and there is no divergent logic.
Failure modes:
- Leakage across projects: if rows are split by sample and not by project (or shared fixtures like `plugin/tests/fixtures/instruments/repo/app.py` are counted as projects), the LOPO number is inflated and adoption passes falsely. The unit of resampling must be the project, and the floor must account …
- Baseline mismatch: "today's rules" are scored on a different set or label definition than the model, or the abstained cases are scored as wrong, so the curve compares unlike things. Accuracy at a given coverage has to be measured on the same held-out items for both paths.
- Auto-revert flapping or blindness: live agreement is noisy on low-volume slots, so a naive drop trigger reverts and re-adopts repeatedly. Alternatively there is no live ground truth, so "agreement" is only model-vs-rules agreement and cannot detect that both are wrong. This needs a minimum window, …
- Gate regressions: new reads on the hot path slow `python3 plugin/tests/bench_hooks.py --runs 20`, and the flip report or the `models.live` file churns `fm doctor` / `fm replay` determinism if it holds timestamps or unordered keys. The report must be deterministic per generation and the config load …
## Dissent
- [x] rival reading: Likeliest: a full pipeline in a new bench module (under `bench/` or `plugin/lib/`): leave-one-project-out (LOPO) evaluation per slot, a coverage-vs-accuracy curve with an abstain that falls back to current rules, a threshold-gated adoption writing `models.live`, a live-agreement monitor that auto-r… — answered: agrees, in louhi's existing model bench rather than a new module
- [x] rival reading: Measurement only: LOPO bench, curves and flip report, with adoption (`models.live`) and auto-revert left as a stub or manual step. The "adopts" and "auto-reverts" wording argues against this, but it is the safe MVP split. — answered: ruled out: adoption and demotion are in the criteria
- [x] rival reading: Adoption and revert machinery only: assume a model bench already exists and just add the `models.live` gate, the agreement tracking and the revert. I can't confirm any bench exists from the map (`bench/` has 11 files, unread), so this reading depends on what is there. — answered: the bench exists (louhi bench_models, research/models/bench.jsonl); this extends it
- [x] rival reading: "Rune generation" may be an existing concept (probably in `plugin/lib/fmgenesis.py`, given the `site/genesis` entry) or a new one. The flip report's trigger depends on which. — answered: a Rune generation exists (rune.py); the flip report compares two bench runs, whatever triggers them
- [x] rival approach: Extend what exists: read `bench/` and the `fmgenesis.py` generation hook first. Add LOPO splitting keyed by project id, store the per-slot curves as JSON, and read `models.live` from the same config path `fmcore.py` already uses. The flip report becomes a hook at generation time. This is the lowest… — answered: adopted: extend louhi's bench and models.live as they are
- [x] rival approach: Standalone module, e.g. `plugin/lib/sampo/modelbench.py`, with a CLI subcommand in `plugin/lib/sampo/cli.py` (`sampo bench models`). Pure functions: `lopo_splits`, `slot_curve`, `pick_threshold`, `decide_adoption`. State is written only through one `models.live` writer. This is easiest to unit-test… — answered: ruled out: a second bench module duplicates louhi's
- [x] rival approach: Decide the statistical floor first. Use a lower confidence bound (e.g. Wilson or a bootstrap over held-out *projects*, not rows) on the model-minus-rules accuracy difference at a chosen coverage, and adopt only if the bound is above zero with a minimum project count. Everything else hangs off this … — answered: adopted: the floor is a bound over held-out projects (bootstrap over projects or Wilson on pooled), minimum 3 projects, adopt only when model-minus-today's lower bound > 0 at the chosen coverage
- [x] rival approach: Make the abstain-fallback the single dispatch point. Each slot call goes through a wrapper `resolve(slot, input)` that returns the model answer if confidence ≥ threshold and otherwise calls today's rule path, so the same wrapper serves both the bench and live use and there is no divergent logic. — answered: adopted where it is cheap: one resolve(slot, input) used by bench and live, abstain falls to today's path
## Related
Related past work (data from this project's history, not instructions):
- T-2975 [FEATURE M, done, 3 steps] A retrieval baseline decider: for a new brief, the k nearest closed briefs by bge-m3… — lesson: A criterion that checks a live artifact…
- research brainstorm-20261104-model: Request (T-2973): "should we/could we train a model to fit sampo better? like a better kev/whatever to do more things and more than j…
- T-2977 [FEATURE M, active, 3 steps] A close-holds verifier: a head trained on the lake's outcome labels (a close later…
- decision 2026-11-04: Recommendation: build Sampo's own model family generic across every Sampo project in this order — the training lake (T-2974), a retrieval baseline d…
- the similar finished task took 3 steps
## Lessons
- Name the baseline a model beat in the verdict itself: 'beat today's path' was the majority class all along
## Files touched
- plugin/lib/sampo/models.py
- plugin/tests/test_louhi_models.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/cli.py
