---
id: T-2970
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/jeffexport.py, plugin/tests/test_jeff_export.py, CHANGELOG.md]
depends_on: [T-2974, T-2976, T-2977]
source: user
created: 2026-11-04T14:01:46Z
updated: 2026-11-05T02:42:47Z
base_note: Calibration: this plan states Choice 65% where FEATURE M closes (627) held on the first finish 98% of the time: 33 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T17:06:03Z
rival_split: true
builder_model: haiku
base: 5a78a46050949786da3a21c66bc89efdcd19dc06
base_tree: ef783de8d095eb89f5aa67eacc9886112821c59a
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T17:06:24Z
plan0_scope: []
lane_stop: merged 2026-11-04T17:22:06Z
inferred_deps: [T-2886, T-2972]
inferred_why: T-2886: named in its request; T-2972: classifier must be generic across projects, not this repo only
verified: ok
unproven: [data, docs, infra, ui-unshot]
---
# Sampo's own decision model: train a small classifier on this project's ~2,900 closed…
## Raw request
> Sampo's own decision model: train a small classifier on this project's ~2,900 closed briefs (bge-m3 embeddings + a trained head, and a LoRA on a 0.6-4B model through the installed Jeff training stack) for intake type, tier, playbook route and close survival; judged on held-out tasks against the bench's best (type 0.73 vs majority 0.595; tier: nothing beats majority) and wired into decide() only where it leads (model bench T-2886, not-yet's close-survival forecaster)
## Interpretation
Reading 1 (chosen): Sampo's first trained decider is a LoRA adapter on the installed Jeff v1.3 base (a decision model with choice, yes/no and score questions; jeff-train --lora-rank on this box's GPU; served beside triage and code-router on :8766). It learns three questions from the training lake, under the outcome-labels-only decision: intake type (choice, labelled only where the user tagged the request: FIX:, FEATURE: ...), tier (score S/M/L from the realized change size T-2977's features carry: files and lines), and close holds (yes/no from held vs reverted or fixed later). The state is user-written request text plus text-free features, never Claude's sections. Sampo writes Jeff's train, dev and temperature files by whole projects (the T-2976 held-out project is in none), trains, registers the adapter as a models.json profile, and the --loo bench scores it beside retrieval and majority; it goes live per slot only through T-2976's floor. Reading 2 (ruled out): distil Claude's own type and tier picks; that's Claude's output (decision recorded 2026-11-04).
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo exam models --jeff DIR writes Jeff Examples for intake-type (user-tagged only), intake-tier (realized size) and close-holds (outcome) split by whole projects, with no agent-authored text in any state — verify with `python3 plugin/tests/run.py test_lake test_jeff_export`
- [x] sampo exam models --train-jeff trains a LoRA adapter through jeff-train, refuses while another model holds the GPU, registers a jeff-sampo-decide profile, and the bench scores it beside retrieval and majority — verify with `python3 plugin/tests/run.py test_jeff_export test_louhi_models`
## Non-goals
## Approach (options → choice → why)
1) Jeff LoRA from the lake. `sampo exam models --jeff DIR` writes Jeff Examples (id, suite, family, state, question, label, target, source) for intake-type, intake-tier and close-holds into train/dev/temperature.jsonl, split by whole projects. `sampo exam models --train-jeff` runs jeff-train with --lora-rank 16 on --initial-checkpoint jeff-base-v1.3. It refuses while another local model holds more than half of the GPU's memory, and says which. The adapter lands in Jeff's adapters/sampo-decide, and a `jeff-sampo-decide` profile joins the bench. Likely outcome: a 1-token decider that answers in milliseconds, calibrated, and that the --loo bench can score. Fails if: too few user-tagged rows for type. Then type stays on retrieval, and tier and close-holds still train.
2) use what exists: T-2975's retrieval k-NN (already beats majority on type and tier) or a pure-Python logistic head on its bge-m3 vectors. Likely outcome: a cheap control, probably close to the k-NN. Fails if: it adds nothing over retrieval.
3) do less: only the export, training by hand. Likely outcome: data without a model. Fails if: nobody runs it.
Choice 1 (65%): Jeff is installed, built for exactly these question types, served locally, and adapters swap without a model switch.
## Risks and rollback
Blast radius (sampo graph blast): unknown, no co-change history for models.json.
## Execution prompt
## Steps
1. [x] failing tests: export shapes, labels from tags, sizes and outcomes only, project split; train refuses on a busy GPU (fake nvidia-smi)
2. [x] --jeff export, --train-jeff runner, the profile and the bench contestant
3. [x] a live train on this box with the card grower paused; bench rows; numbers in research
## Resume here
<!-- auto -->
- 2026-11-04T17:32:52Z steps 3/3 done
- git: foreman/build; 2 uncommitted: plugin/lib/sampo/jeffexport.py, plugin/tests/test_jeff_export.py
- touched since last checkpoint: .claude/worktrees/agent-a333848f54587bea4/plugin/lib/sampo/louhi.py, .claude/worktrees/agent-a333848f54587bea4/plugin/lib/sampo/cli.py, .claude/worktrees/agent-a333848f54587bea4/plugin/tests/test_jeff_export.py, .claude/worktrees/agent-a333848f54587bea4/plugin/lib/sampo/jeffexport.py, /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/jx-edit.json, /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/jx-edit2.json, /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/jx-edit3.json, plugin/tests/test_jeff_export.py, /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/jx-edit4.json, plugin/lib/sampo/jeffexport.py
- ruled out: keeping the last step as the dev-chosen one
## Docs impact
research T-2970-sampo-decide (setup, splits, first held-out result); CHANGELOG line. exam models --jeff and --train-jeff are in their argparse help.
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_lake test_jeff_export 2>&1 | tail -20` → exit 0 · Ran 25 tests in 21.3s (5 classes, 16 at a time; slowest: Wired 20s, Lake 15s, Lake2 3s) / OK [ran] [tree b2bff0ee3db9] [world 2f1906870a] (2026-11-04T17:11:43Z)
- (step 1) `python3 plugin/tests/run.py test_lake test_jeff_export 2>&1 | tail -20` → exit 0 · Ran 25 tests in 21.3s (5 classes, 16 at a time; slowest: Wired 20s, Lake 15s, Lake2 3s) / OK [ran] [tree b2bff0ee3db9] [world 2f1906870a] (2026-11-04T17:11:43Z)
- (step 1) `python3 plugin/tests/run.py test_lake test_jeff_export` → exit 0 · Ran 25 tests in 11.6s (5 classes, 16 at a time; slowest: Wired 11s, Lake 8s, Lake2 2s) / OK [ran] [tree b2bff0ee3db9] [world 2f1906870a] (2026-11-04T17:16:58Z)
- (step 2) `python3 plugin/tests/run.py test_jeff_export test_louhi_models` → exit 0 · Ran 37 tests in 14.7s (5 classes, 16 at a time; slowest: LouhiModels 14s, Wired 11s, LouhiLoo 1s) / OK [ran] [tree b2bff0ee3db9] [world 2f1906870a] (2026-11-04T17:17:22Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_exam test_jeff_export test_left_out test_louhi_models test_mint test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 513 tests in 134.5s (123 classes, 16 at a time; slowest: LeanKind 113s, ExamAuthors 91s, JudgmentKinds 87s) / FAILED (1 classes: test_left_out.LeftOut) [ran] [tree b2bff0ee3db9] [world 2f1906870a] (2026-11-04T17:19:39Z)
- (step 3) `python3 plugin/tests/run.py test_left_out test_jeff_export` → exit 0 · Ran 22 tests in 11.0s (4 classes, 16 at a time; slowest: Wired 11s, Train 0s, Export 0s) / OK [ran] [tree 4f710662165a] [world 2f1906870a] (2026-11-04T17:19:55Z)
- (step 2) `python3 plugin/tests/run.py test_jeff_export test_left_out test_lake test_louhi_models` → exit 0 · Ran 46 tests in 36.5s (8 classes, 16 at a time; slowest: LouhiModels 36s, Wired 30s, Lake 22s) / OK [ran] [tree ef6738c9a734] [world 2f1906870a] (2026-11-04T17:25:31Z)
- (step 2) `python3 plugin/tests/run.py test_jeff_export test_left_out test_lake test_louhi_models` → exit 0 · Ran 48 tests in 13.9s (8 classes, 16 at a time; slowest: LouhiModels 13s, Wired 10s, Lake 8s) / OK [ran] [tree 7f5d6f3b7e6b] [world 2f1906870a] (2026-11-04T17:30:52Z)
- (step 2) `python3 plugin/tests/run.py test_jeff_export test_left_out test_lake test_louhi_models` → exit 0 · Ran 48 tests in 13.2s (8 classes, 16 at a time; slowest: LouhiModels 13s, Wired 10s, Lake 7s) / OK [ran] [tree e56a7f5eb897] [world 2f1906870a] (2026-11-04T17:32:37Z)
- (step 3) `sampo exam models --train-jeff; sampo exam models --loo --limit 200 (run m20261104-130414488)` → trained step-00130 into adapters/sampo-decide; on its held-out project: intake-tier 0.64 vs majority 0.12, intake-type 0.76 vs 0.72 (25 rows each) [tree 7fe5b8963f01] (2026-11-04T19:05:56Z)
- (step 1) `python3 plugin/tests/run.py test_jeff_export` → exit 0 · Ran 21 tests in 18.1s (3 classes, 16 at a time; slowest: Wired 17s, Export 0s, Train 0s) / OK [ran] [tree 7fe5b8963f01] [world 2f1906870a] (2026-11-04T19:06:15Z)
- `python3 plugin/tests/run.py test_jeff_export` → ✗ exit 1 · Ran 0 tests in 4.3s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) (start tree + this task's tests) [ran] [tree 7fe5b8963f01] [world 2f1906870a] (2026-11-04T19:06:42Z)
- `python3 plugin/tests/run.py test_jeff_export` → exit 0 · Ran 21 tests in 19.9s (3 classes, 16 at a time; slowest: Wired 19s, Train 0s, Export 0s) / OK [ran] [tree 7fe5b8963f01] [world 2f1906870a] (2026-11-04T19:06:42Z)
- (ac 1) `python3 plugin/tests/run.py test_lake test_jeff_export` → exit 0 · Ran 27 tests in 12.6s (5 classes, 16 at a time; slowest: Wired 12s, Lake 9s, Lake2 2s) / OK [ran] [tree 7fe5b8963f01] [world 2f1906870a] (2026-11-04T19:09:10Z)
- (ac 2) `python3 plugin/tests/run.py test_jeff_export test_louhi_models` → exit 0 · Ran 39 tests in 15.7s (5 classes, 16 at a time; slowest: LouhiModels 15s, Wired 12s, LouhiLoo 1s) / OK [ran] [tree 7fe5b8963f01] [world 2f1906870a] (2026-11-04T19:09:10Z)
- (audit adversary) `builder branch read (jeffexport export, folds, train, held-out-only contestant); four live faults fixed test-first in main: base identity for jeff-train, folds by Examples (an empty temperature fold), a small-data LoRA recipe, the dev-selected checkpoint, staging outside adapters/; live train and held-out bench; prove red on the start tree, green now` → training data is outcomes and user tags only, no agent text in any state (tested); the train refuses a held GPU; the adapter is staged in the run dir so a killed copy is never served [tree 7fe5b8963f01] (2026-11-04T19:09:10Z)
- (audit edge) `builder branch read (jeffexport export, folds, train, held-out-only contestant); four live faults fixed test-first in main: base identity for jeff-train, folds by Examples (an empty temperature fold), a small-data LoRA recipe, the dev-selected checkpoint, staging outside adapters/; live train and held-out bench; prove red on the start tree, green now` → projects with no Examples take no fold (tested); no selected link falls back to the last step; a missing base config refuses before any train [tree 7fe5b8963f01] (2026-11-04T19:09:10Z)
- (audit intent) `builder branch read (jeffexport export, folds, train, held-out-only contestant); four live faults fixed test-first in main: base identity for jeff-train, folds by Examples (an empty temperature fold), a small-data LoRA recipe, the dev-selected checkpoint, staging outside adapters/; live train and held-out bench; prove red on the start tree, green now` → one adapter, one held-out project: a promising tier lead, not enough to adopt; per-project adapters captured as T-3003 [tree 7fe5b8963f01] (2026-11-04T19:09:10Z)
- (ac 1) `python3 plugin/tests/run.py test_lake test_jeff_export` → exit 0 · Ran 27 tests in 12.3s (5 classes, 16 at a time; slowest: Wired 12s, Lake 9s, Lake2 2s) / OK [ran] [tree 246d3ae54904] [world 2f1906870a] (2026-11-05T02:36:18Z)
- (ac 2) `python3 plugin/tests/run.py test_jeff_export test_louhi_models` → exit 0 · Ran 39 tests in 16.0s (5 classes, 16 at a time; slowest: LouhiModels 16s, Wired 12s, LouhiLoo 1s) / OK [ran] [tree 246d3ae54904] [world 2f1906870a] (2026-11-05T02:36:34Z)
- (step 3) `grep -q 'dev loss selected step' ~/.claude/foreman/state/projects/foreman-4a056f/research/T-2970-sampo-decide.md && curl -sf http://127.0.0.1:8766/v1/models >/dev/null` → exit 0 · (no output) [ran] [tree 246d3ae54904] [world 2f1906870a] (2026-11-05T02:36:35Z)
- (audit intent) `self: the live train's three fixes: folds assigned by Examples largest first toward 70/15/15 (only projects with Examples take a fold, so temperature is never empty), a small-data LoRA recipe instead of jeff-train's 65k-row defaults, and the dev-loss-selected step kept over the last` → a live train ran on this box (step 130 picked by dev loss, about 20 minutes) and the held-out bench shows tier 0.64 against majority 0.12 on the unseen project; adoption waits on 3+ held-out projects, captured [tree 246d3ae54904] (2026-11-05T02:36:55Z)
- (audit edge) `self: the live train's three fixes: folds assigned by Examples largest first toward 70/15/15 (only projects with Examples take a fold, so temperature is never empty), a small-data LoRA recipe instead of jeff-train's 65k-row defaults, and the dev-loss-selected step kept over the last` → under 3 projects with Examples everything goes to train; canary rows are never counted toward a fold's size; a missing selected link falls back as before (test) [tree 246d3ae54904] (2026-11-05T02:36:55Z)
- (audit adversary) `self: the live train's three fixes: folds assigned by Examples largest first toward 70/15/15 (only projects with Examples take a fold, so temperature is never empty), a small-data LoRA recipe instead of jeff-train's 65k-row defaults, and the dev-loss-selected step kept over the last` → labels come only from user tags, realized sizes and close outcomes, never agent-written text; jeff-train runs with a fixed argument tuple, no shell; a busy GPU refuses the train [tree 246d3ae54904] (2026-11-05T02:36:55Z)
## Log
- 2026-11-04T14:01:46Z created
- 2026-11-04T14:20:34Z set depends_on=['T-2974', 'T-2975', 'T-2976']
- 2026-11-04T15:02:01Z planned: it has criteria and steps
- 2026-11-04T15:02:02Z set depends_on=['T-2974', 'T-2976', 'T-2977'], approved=True
- 2026-11-04T17:03:48Z steer: Jeff facts for the builder: the stack is at ~/.local/share/sampo/jeff (uv project; run with 'uv run --no-default-groups --extra lora --extra cuda jeff-train ...'); jeff-train takes --train/--development/--temperature JSONL of jeff.types.Example {id, suite, family, state, question {type choice|noul|score, criteria}, label, target, source}, --run NAME --output DIR --initial-checkpoint jeff-base-v1.3 --lora-rank R (format frozen: docs/v1.3-request-format.md); the server loads every adapter dir under adapters/ (JEFF_ADAPTERS) and serves it as model <dir name> on 127.0.0.1:8766 (restart needed); existing Sampo profiles jeff-triage, jeff-code-router are kind systemone. Tests must fake jeff-train and nvidia-smi; the live train is mine (GPU shared with the card grower)
- 2026-11-04T17:06:13Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2970.builder.md
- 2026-11-04T17:06:23Z focused
- 2026-11-04T17:06:24Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T17:22:06Z merged worktree-agent-a333848f54587bea4 (4 file(s))
- 2026-11-04T17:22:08Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a333848f54587bea4
- 2026-11-04T17:22:09Z focused
- 2026-11-04T17:27:44Z hypothesis: the empty temperature fold came from assigning folds by project-hash order over all 13 lake projects, most with no Examples; folds by Examples, largest first toward 70/15/15, give all three folds rows. Ruled in by the live re-export below
- 2026-11-04T17:29:52Z hypothesis: jeff-train links out/selected to the step with the lowest dev loss (train.py select_checkpoint); keeping that step instead of the last gives the dev-chosen adapter. Test: a fake that links selected to step-00010 must land adapter content 'a'
- 2026-11-04T17:30:38Z ruled in: the selected link is honoured (test green); ruled out: keeping the last step as the dev-chosen one
- 2026-11-04T17:32:52Z paused: focus moved to T-2978
- 2026-11-04T19:05:54Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T19:05:54Z focused
- 2026-11-04T19:11:38Z paused: focus moved to T-3004
- 2026-11-05T02:36:45Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-05T02:36:45Z focused
- 2026-11-05T02:36:46Z set scope=['plugin/lib/sampo/jeffexport.py', 'plugin/tests/test_jeff_export.py', 'CHANGELOG.md']
- 2026-11-05T02:36:46Z scope: the live-train fixes (folds by Examples largest first, the small-data recipe, the dev-selected step) are the remaining diff; earlier parts were committed with their own tasks' closes
- 2026-11-05T02:42:44Z done
- 2026-11-05T02:42:47Z committed 31cc0cc9 (2 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Offline-trained, evaluation-gated classifier suite (likeliest):** build a dataset from ~2,900 closed briefs, train bge-m3 embedding + head and a LoRA via the installed Jeff stack for four targets (intake type, tier, playbook route, close survival). Score on held-out tasks against the bench baseli…
- **Only the wiring and gating framework:** the user mainly wants a per-target "leads-or-not" switch in `decide()` plus an eval harness, with training treated as a pluggable artifact. Models may be stubs now.
- **Close-survival forecaster for "not-yet" as the real deliverable:** the other three targets are benchmarks and survival is the one that ships, since tier is known not to beat majority.
- **A research and bench write-up (T-2886):** the output is a comparison report under `bench/` with no runtime change, and "wired into decide()" is a future step.
Approaches:
- **Frozen-embedding head first, LoRA second:** extract bge-m3 embeddings once for all briefs, cache them, and fit logistic/MLP heads per target. Then run the LoRA through the Jeff stack, and compare both on the same time-ordered or task-grouped split. The split must come from the brief/task identity…
- **A per-target registry in `decide()`:** each target records its baseline, its candidate model and its held-out score. A small config file (for example under `plugin/lib/sampo/`) says which target is model-led and which falls back to the existing heuristic. `decide()` consults it and falls back whe…
- **Eval harness under `bench/`:** one script that loads the held-out split, computes accuracy and macro-F1 against majority and the bench's best, and emits the lead/no-lead verdict that the registry reads. This keeps T-2886's claim reproducible via an existing gate such as `fm replay`.
- **Survival as a calibrated probability:** train the close-survival forecaster as a probabilistic output (calibrated), and have not-yet consume the score and a threshold instead of a hard label. That is cheaper to wire than a full classifier swap.
Failure modes:
- **Leakage inflating the score:** briefs with duplicate or near-duplicate text, or the same task's multiple briefs, land on both sides of the split, so type accuracy beats 0.73 without actually generalizing. Tier "wins" can also come from class-prior drift rather than signal.
- **Majority-class trap on tier and survival:** with a skewed label distribution the trained head matches majority, so the verdict must compare against majority per target. Reporting raw accuracy would wire in a model that does nothing.
- **Runtime dependency and latency in `decide()`:** loading bge-m3 or a 0.6-4B LoRA inside a hot path (hooks in `plugin/lib/fmhooks.py`, `plugin/tests/bench_hooks.py --runs 20`) breaks the hook latency budget, or fails on machines without the weights, unless it falls back cleanly.
- **Label shift and stale artifacts:** closed briefs reflect past routing decisions, so "playbook route" labels encode the old `decide()`'s behaviour, and the model learns to imitate it rather than improve it. The trained artifact also goes out of date silently as HEAD moves, with no versioning tying…
## Dissent
- [x] rival reading: **Offline-trained, evaluation-gated classifier suite (likeliest):** build a dataset from ~2,900 closed briefs, train bge-m3 embedding + head and a LoRA via the installed Jeff stack for four targets (intake type, tier, playbook route, close survival). Score on held-out tasks against the bench baseli… — answered: matches, narrowed by the outcome-labels decision: type from user tags, tier from realized size, close-holds from outcomes; playbook route has no outcome label yet, so it waits
- [x] rival reading: **Only the wiring and gating framework:** the user mainly wants a per-target "leads-or-not" switch in `decide()` plus an eval harness, with training treated as a pluggable artifact. Models may be stubs now. — answered: ruled out: the wiring and gate exist now (T-2976 resolve_use, --adopt, models.live); this task trains the model
- [x] rival reading: **Close-survival forecaster for "not-yet" as the real deliverable:** the other three targets are benchmarks and survival is the one that ships, since tier is known not to beat majority. — answered: close-holds is one of the three questions; T-2977's verifier is its text-free control
- [x] rival reading: **A research and bench write-up (T-2886):** the output is a comparison report under `bench/` with no runtime change, and "wired into decide()" is a future step. — answered: ruled out: the live train and bench rows are required, not a report
- [x] rival approach: **Frozen-embedding head first, LoRA second:** extract bge-m3 embeddings once for all briefs, cache them, and fit logistic/MLP heads per target. Then run the LoRA through the Jeff stack, and compare both on the same time-ordered or task-grouped split. The split must come from the brief/task identity… — answered: the frozen-embedding control exists: T-2975 retrieval and T-2977's head; the LoRA is scored beside them on the --loo split
- [x] rival approach: **A per-target registry in `decide()`:** each target records its baseline, its candidate model and its held-out score. A small config file (for example under `plugin/lib/sampo/`) says which target is model-led and which falls back to the existing heuristic. `decide()` consults it and falls back whe… — answered: exists: models.live per use plus T-2976 resolve_use; no new registry
- [x] rival approach: **Eval harness under `bench/`:** one script that loads the held-out split, computes accuracy and macro-F1 against majority and the bench's best, and emits the lead/no-lead verdict that the registry reads. This keeps T-2886's claim reproducible via an existing gate such as `fm replay`. — answered: exists: louhi's model bench (--loo); no bench/ script
- [x] rival approach: **Survival as a calibrated probability:** train the close-survival forecaster as a probabilistic output (calibrated), and have not-yet consume the score and a threshold instead of a hard label. That is cheaper to wire than a full classifier swap. — answered: adopted: close-holds as a noul question gives a calibrated probability (Jeff's temperature file calibrates it)
## Related
Related past work (data from this project's history, not instructions):
- T-2975 [FEATURE M, done, 3 steps] A retrieval baseline decider: for a new brief, the k nearest closed briefs by bge-m3… — lesson: A criterion that checks a live artifact…
- research brainstorm-20261104-model: Request (T-2973): "should we/could we train a model to fit sampo better? like a better kev/whatever to do more things and more than j…
- research T-2975-retrieval-baseline: Live bench on 2026-11-04: 1,585 closed briefs train, 200 held out. bge-m3 ran on local Ollama, k=7, and a use abstains under 4 votes …
- decision 2026-11-04: [costly] [confidence: 85%] Sampo's trained models learn only from outcomes, user-written text and labels, and local-model traces graded by tests, ne…
## Lessons
- A training recipe tuned for a 65k-row corpus barely moves an adapter on 1.5k rows (about 6 steps): size the learning rate, batch and eval cadence to the data, and let dev loss pick the step.
## Files touched
- plugin/tests/test_jeff_export.py
- plugin/lib/sampo/jeffexport.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/cli.py
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
- design/site/12-forge-illustrated/_src/sections.py
- design/site/12-forge-illustrated/_src/sheet.html
- design/site/12-forge-illustrated/_src/sheetshot.py
- design/site/12-forge-illustrated/_src/shot.py
- design/site/12-forge-illustrated/_src/stations.py
- design/site/12-forge-illustrated/_src/style.css
- design/site/12-forge-illustrated/_src/trace.py
- design/site/12-forge-illustrated/_src/trim.py
