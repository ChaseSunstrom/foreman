---
id: T-2887
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T03:52:56Z
updated: 2026-11-04T04:06:51Z
builder_model: haiku
base: b48f5ec15ea1e14d5bbd8b3e2a717387ac257b8d
base_tree: b11e62a7f51040d2a7cbf12addf0463350ad66d1
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T03:53:59Z
plan0_scope: []
lane_stop: merged 2026-11-04T04:02:50Z
verified: strong
unproven: [data]
---
# Model bench part 1: a systemone backend kind (Jev's API: Ollama /v1/systemone, Jeff, SelfJev) in models.decide, and sampo louhi models with the decision arm (intake type and tier from held-out closed tasks) and the embedding arm (title-to-brief recall), results in research/models/bench.jsonl
## Raw request
> Model bench part 1: a systemone backend kind (Jev's API: Ollama /v1/systemone, Jeff, SelfJev) in models.decide, and sampo louhi models with the decision arm (intake type and tier from held-out closed tasks) and the embedding arm (title-to-brief recall), results in research/models/bench.jsonl
## Interpretation
Reading 1 (chosen): part 1 of T-2886: the plumbing and two arms, so the full lineup can be measured on Sampo's own labels. decide() gains a backend that speaks Jev's typed-decision API (POST {base}/systemone with a state and typed questions, per-option probabilities back), and sampo louhi models runs the decision and embedding arms, writing one metrics row per backend and use. Reading 2 (ruled out): route decision models through chat completions with a JSON prompt, as decide() does today. Ruled out because Ollama's decision models (kev, tev1, d3), Jeff and SelfJev write no text: they only answer the systemone shape.
## Assumptions (confidence)
## Acceptance criteria
- [x] decide() answers through a systemone backend, taking only listed choices and probabilities in [0,1] — verify with `python3 plugin/tests/run.py test_models_systemone`
- [x] sampo louhi models run writes accuracy, Brier, p50/p95 latency and n per backend and use, held out by task-id hash; sampo louhi models show prints the table — verify with `python3 plugin/tests/run.py test_louhi_models`
## Non-goals
## Approach (options → choice → why)
1) Add a 'systemone' profile kind to models (base_url, model, key_env as today). decide() sends one choice question whose criteria are the choices, and keeps only listed choices with probabilities in [0,1]. Ollama's decision models are found through /api/tags (capabilities include 'decision'); Jeff (:8765) and SelfJev (:8000) come from models.json or TYPESAFE_BASE_URL. sampo louhi models run takes closed tasks, holds out a third by a task-id hash as louhi's scenarios do, and asks each backend for intake-type and intake-tier from the raw request. It records accuracy, Brier score, p50/p95 latency, n and errors per backend and use. The 'without' row is the majority class, or core's own guess where one exists. The embedding arm records recall@1 and recall@10 from a title to its brief (first 600 chars). Rows go to research/models/bench.jsonl with a run id, and louhi models show prints the latest table. Likely outcome: the arm works against fakes in tests, plus a first real table for kev:4b and three embedders. Fails if the real systemone reply differs from the documented shape, so the builder probes localhost:11434 first. Choice 1 (80%). 2) A separate top-level verb outside louhi. Likely outcome: the same numbers, but a second held-out split and run-id scheme to keep in sync, and a new always-on verb the self-change gate must pay for. Fails if the two splits drift and leak labels. 3) Ask decision models through chat completions with a JSON prompt, as decide() does today. Likely outcome: kev, tev1, d3, Jeff and SelfJev return errors or nothing, because they write no text. Fails at once on every decision model. 4) use what exists: models.shadow_pass already answers shadow rows (intake-type, intake-tier) through decide() on local backends and books the answers in predictions.jsonl, and foresight scores the book. Likely outcome: numbers for the 184 shadow rows only, through chat completions, so decision models are still excluded and no embedding arm exists. Fails if the book lacks latency per backend (it has ms) and a held-out split (it has none). The new arm reuses shadow_uses() and the booking. 5) do less: only the systemone kind and a one-off script table. Likely outcome: the user's first numbers today, but nothing reruns per generation or feeds the site. Fails the user's 'keep improving on that'.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: a fake systemone server (state + questions in, per-option probabilities out) answers decide(); malformed or out-of-list answers are refused
2. [x] the systemone kind in models: profiles from models.json (kind systemone), Ollama decision models found through /api/tags capabilities
3. [x] test: louhi models on a fixture project with closed tasks and fake backends writes the metrics rows
4. [x] louhi models run/show: decision and embedding arms, the rules path as the 'without' row
## Resume here
## Docs impact
CHANGELOG line added at close of T-2886; MASTER's exam bullet gains models in part 2
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_models_systemone test_models 2>&1 | tail -15` → exit 0 · Ran 74 tests in 4.7s (13 classes, 16 at a time; slowest: Bench 4s, RunRoute 2s, ModelRules 1s) / OK [ran] [tree 355ec8b139d6] [world 2f1906870a] (2026-11-04T03:56:20Z)
- (step 2) `python3 plugin/tests/run.py test_louhi_models test_models_systemone test_models test_exam 2>&1 | tail -20` → exit 0 · Ran 176 tests in 82.2s (38 classes, 16 at a time; slowest: LeanKind 82s, ExamAuthors 77s, JudgmentKinds 73s) / OK [ran] [tree 52d5d27611c1] [world 2f1906870a] (2026-11-04T03:59:28Z)
- (step 1) `python3 plugin/tests/run.py test_models_systemone` → exit 0 · Ran 6 tests in 0.5s (1 classes, 16 at a time; slowest: Systemone 0s) / OK [ran] [tree 52d5d27611c1] [world 2f1906870a] (2026-11-04T03:59:31Z)
- (step 4) `python3 plugin/tests/run.py test_louhi_models` → exit 0 · Ran 4 tests in 6.2s (1 classes, 16 at a time; slowest: LouhiModels 6s) / OK [ran] [tree 52d5d27611c1] [world 2f1906870a] (2026-11-04T03:59:38Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_louhi_models test_models test_models_systemone test_moons_scale test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.70s] [ran] [tree 52d5d27611c1] [world 2f1906870a] (2026-11-04T04:00:15Z)
- `python3 plugin/tests/run.py test_models_systemone` → exit 0 · Ran 6 tests in 0.5s (1 classes, 16 at a time; slowest: Systemone 0s) / OK [ran] [tree 52d5d27611c1] [world 2f1906870a] (2026-11-04T04:04:35Z)
- `python3 plugin/tests/run.py test_louhi_models` → exit 0 · Ran 4 tests in 6.5s (1 classes, 16 at a time; slowest: LouhiModels 6s) / OK [ran] [tree 52d5d27611c1] [world 2f1906870a] (2026-11-04T04:04:42Z)
- (step 3) `python3 plugin/tests/run.py test_louhi_models` → exit 0 · Ran 4 tests in 6.4s (1 classes, 16 at a time; slowest: LouhiModels 6s) / OK [ran] [tree a9f612733c39] [world 2f1906870a] (2026-11-04T04:05:48Z)
- (step 1) `python3 plugin/tests/run.py test_models_systemone` → exit 0 · Ran 6 tests in 0.5s (1 classes, 16 at a time; slowest: Systemone 0s) / OK [ran] [tree a9f612733c39] [world 2f1906870a] (2026-11-04T04:05:49Z)
- `python3 plugin/tests/run.py test_louhi_models test_models_systemone` → ✗ exit 1 · Ran 10 tests in 7.5s (2 classes, 16 at a time; slowest: LouhiModels 6s, Systemone 0s) / FAILED (2 classes: test_models_systemone.Systemone, test_louhi_models.LouhiModels) (start tree + this task's tests) [ran] [tree a9f612733c39] [world 2f1906870a] (2026-11-04T04:06:04Z)
- `python3 plugin/tests/run.py test_louhi_models test_models_systemone` → exit 0 · Ran 10 tests in 6.2s (2 classes, 16 at a time; slowest: LouhiModels 6s, Systemone 0s) / OK [ran] [tree a9f612733c39] [world 2f1906870a] (2026-11-04T04:06:04Z)
- (ac 1) `python3 plugin/tests/run.py test_models_systemone` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T04:05:49Z [ran] [tree a9f612733c39] [world 2f1906870a] (2026-11-04T04:06:09Z)
- (ac 2) `python3 plugin/tests/run.py test_louhi_models` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T04:05:48Z [ran] [tree a9f612733c39] [world 2f1906870a] (2026-11-04T04:06:09Z)
- (audit intent) `lane diff read in the main thread; tests green; first live run m20261103-220442429 on 4 decision models and 3 embedders` → decide() speaks systemone and the exam's models arm records accuracy, Brier, latency per backend on held-out closed tasks; first table produced live [tree a9f612733c39] (2026-11-04T04:06:09Z)
- (audit edge) `lane diff read in the main thread; tests green; first live run m20261103-220442429 on 4 decision models and 3 embedders` → real /api/tags carries capabilities (verified live: decision, embedding), so discovery works; unknown or out-of-list choices and error replies are refused; a dead endpoint costs at most the timeout per call (noted: _post retries 3x, captured for part 2) [tree a9f612733c39] (2026-11-04T04:06:09Z)
- (audit adversary) `lane diff read in the main thread; tests green; first live run m20261103-220442429 on 4 decision models and 3 embedders` → a model reply is untrusted: only a listed choice and a probability in [0,1] are taken; the state is sent as data with an instruction saying so; no held-out label reaches a prompt [tree a9f612733c39] (2026-11-04T04:06:09Z)
- (audit operator) `lane diff read in the main thread; tests green; first live run m20261103-220442429 on 4 decision models and 3 embedders` → sampo exam models show prints the latest run, says how many held-out rows were left out [tree a9f612733c39] (2026-11-04T04:06:09Z)
- (audit maintainer) `lane diff read in the main thread; tests green; first live run m20261103-220442429 on 4 decision models and 3 embedders` → SERVING hardcodes one endpoint URL and the data comes from shadow rows only (48 per use); both are part 2's first fixes [tree a9f612733c39] (2026-11-04T04:06:09Z)
## Log
- 2026-11-04T03:52:56Z created
- 2026-11-04T03:53:16Z set approved=True
- 2026-11-04T03:53:42Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2887.builder.md
- 2026-11-04T03:53:58Z focused
- 2026-11-04T03:53:59Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T04:02:50Z merged worktree-agent-ae5e7d8636284da1b (6 file(s))
- 2026-11-04T04:02:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae5e7d8636284da1b
- 2026-11-04T04:02:59Z focused
- 2026-11-04T04:06:50Z done
- 2026-11-04T04:06:51Z committed cc964027 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2886 [FEATURE L, planned, 5 steps] Model bench: every local backend (Ollama decision models, Jeff, SelfJev, embedders, generators) measured on Sampo's own work with an…
- T-2437 [FEATURE L, done, 5 steps] Gen 2: a model layer (user steer 2026-10-31, start after round 1). (1) A… — lesson: A user's next-generation request has to reach the n…
- T-2742 [FEATURE L, active, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; …
- decision 2026-10-31: Standing rule (user steer 2026-10-31): gen 2 builds a model layer, small specialist models wherever a decision, ranking or lookup is the job, backen…
## Lessons
- give decision models option descriptions, not bare labels: kev/tev1/d3 scored 0.35-0.54 on type with criteria equal to the names
## Files touched
- plugin/tests/test_models_systemone.py
- plugin/lib/sampo/models.py
- plugin/tests/test_models.py
- plugin/tests/test_louhi_models.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/cli.py
- research/models/bench.jsonl
