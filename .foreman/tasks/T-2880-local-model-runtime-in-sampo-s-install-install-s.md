---
id: T-2880
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T03:39:12Z
updated: 2026-11-04T10:51:20Z
builder_model: haiku
base: da18f15a1b5f3976e83a9436e045ce9770311d5b
base_tree: 567114cc7b86d4fa92653403ef3cc80bbb2f4eec
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T09:47:04Z
plan0_scope: []
lane_stop: merged 2026-11-04T10:26:55Z
verified: strong
unproven: [docs, infra]
---
# Local model runtime in Sampo's install: install.sh offers (opt-in) Ollama with pinned…
## Raw request
> FEATURE: Local model runtime in Sampo's install: install.sh offers (opt-in) Ollama with pinned embedding models (qwen3-embedding, bge-m3, nomic-embed-text) and a reranker where the runtime serves one, writes the models.json profiles, and sampo doctor checks them; the moons funnel and recall use the local embeddings (dedupe bars calibrated) and rerank when available
## Interpretation
Reading 1 (chosen): install.sh gains an opt-in `--local-models` (asked on a terminal, off with no terminal): when `ollama` is on PATH it pulls the pinned embedding models (bge-m3, the bench's best title-to-brief recall@1 0.85, plus nomic-embed-text as the small one); when it isn't, it prints Ollama's own install command and skips, never installing a runtime itself. Sampo already finds local embedders on its own (models.embedding_profiles, moonscale._embedder picks the bench's best), so no models.json profile is written for them. `sampo doctor`'s model-backends line names the local embedders and any pinned one missing, with the pull command.
Reading 2 (ruled out): also install Ollama, Jeff, SelfJev and rerankers. Installing a system runtime from Sampo's installer is outward and needs root; Ollama serves no reranker; the classifiers (Jeff, SelfJev) have their own installers and are reached as profiles (T-2886's bench already measures them). Recall's switch to embeddings is out until a recall miss needs synonyms (recall.py's ponytail note).
## Assumptions (confidence)
## Acceptance criteria
- [x] install.sh --local-models with a fake ollama on PATH pulls each pinned embedder; without ollama it prints the download URL, pulls nothing and the install still succeeds; with no terminal and no flag it does nothing — verify with `python3 plugin/tests/run.py test_setup`
- [x] sampo doctor's model-backends line names the local embedders and each pinned one missing with its pull command, and never fails the doctor — verify with `python3 plugin/tests/run.py test_doctor`
- [x] INSTALL.md and install.sh --help list --local-models and --no-local-models — verify with `python3 plugin/tests/run.py test_setup test_docs`
## Non-goals
## Approach (options → choice → why)
1) A LOCAL=ask flag in install.sh beside BYPASS (same terminal/no-terminal rule), a pinned list EMBED_PINS="bge-m3:567m nomic-embed-text:v1.5", `ollama pull` each when ollama answers (`ollama list` succeeds), else one line with https://ollama.com/download; doctor's check_model_backends adds "embedders: …" and "missing pin: …". Likely outcome: a user who says yes gets the moons funnel's embed stage with no config. Fails if: the pinned tags move; pins are exact tags, so a moved tag fails the pull loudly and the install goes on.
2) use what exists: document the two `ollama pull` lines in INSTALL.md and stop. Likely outcome: zero code, the same result for a reader. Fails if: the user asked for it in the install itself.
3) do less: doctor only names a missing embedder and the pull command. Likely outcome: a hint at the moment it matters. Fails if: nothing is set up at install time, which is the request.
Choice 1 (85%): the request names the installer, and Sampo already discovers what the pull adds.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/tests/test_docs.py, README.md, site/build.py, site/genesis/index.html.
## Execution prompt
## Steps
1. [x] failing tests: test_setup install cases with a stubbed ollama (pinned bge-m3:567m, nomic-embed-text:v1.5), test_doctor case for the embedder line
2. [x] install.sh flag, prompt and pulls; doctor line
3. [x] INSTALL.md and --help; CHANGELOG line
## Resume here
## Docs impact
INSTALL.md, README and install.sh --help list --local-models and --no-local-models; CHANGELOG line (T-2880)
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_setup test_doctor test_docs` → exit 0 · Ran 268 tests in 23.4s (76 classes, 16 at a time; slowest: Fences 16s, LockProbe 15s, ViewsRepair 14s) / OK [ran] [tree dc86b7431131] [world 2f1906870a] (2026-11-04T09:54:31Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_board_surfaces test_doctor test_mcp test_setup && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [18.58s] [ran] [tree dc86b7431131] [world 2f1906870a] (2026-11-04T09:55:51Z)
- (step 1) `python3 plugin/tests/run.py test_setup test_doctor test_models` → exit 0 · Ran 238 tests in 12.2s (65 classes, 16 at a time; slowest: ViewsRepair 10s, LockProbe 8s, Bench 4s) / OK [ran] [tree 933cc4b302ec] [world 2f1906870a] (2026-11-04T10:47:56Z)
- (step 3) `python3 plugin/tests/run.py test_setup test_docs` → exit 0 · Ran 158 tests in 10.5s (36 classes, 16 at a time; slowest: Fences 10s, DocsProof 4s, Install 3s) / OK [ran] [tree 933cc4b302ec] [world 2f1906870a] (2026-11-04T10:48:08Z)
- `python3 plugin/tests/run.py test_setup test_doctor test_models` → ✗ exit 1 · Ran 238 tests in 14.0s (65 classes, 16 at a time; slowest: ViewsRepair 10s, LockProbe 9s, Bench 5s) / FAILED (3 classes: test_setup.InstallScript, test_models.Extras, test_doctor.LocalEmbedders) (start tree + this task's tests) [ran] [tree 813ede966513] [world 2f1906870a] (2026-11-04T10:48:35Z)
- `python3 plugin/tests/run.py test_setup test_doctor test_models` → exit 0 · Ran 238 tests in 11.8s (65 classes, 16 at a time; slowest: ViewsRepair 9s, LockProbe 8s, Bench 4s) / OK [ran] [tree 813ede966513] [world 2f1906870a] (2026-11-04T10:48:35Z)
- (ac 1) `python3 plugin/tests/run.py test_setup` → exit 0 · Ran 47 tests in 2.9s (10 classes, 16 at a time; slowest: NoClaude 2s, Install 2s, InstallScript 2s) / OK [ran] [tree 813ede966513] [world 2f1906870a] (2026-11-04T10:49:18Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 112 tests in 10.5s (42 classes, 16 at a time; slowest: ViewsRepair 9s, LockProbe 8s, Command 3s) / OK [ran] [tree 813ede966513] [world 2f1906870a] (2026-11-04T10:49:18Z)
- (ac 3) `python3 plugin/tests/run.py test_setup test_docs` → exit 0 · Ran 158 tests in 10.1s (36 classes, 16 at a time; slowest: Fences 10s, DocsProof 4s, Install 3s) / OK [ran] [tree 813ede966513] [world 2f1906870a] (2026-11-04T10:49:18Z)
- (audit intent) `self-review of the lane diff (install.sh step 6, EMBED_PINS, doctor's line) plus the merge's own checks; one follow-up fixed here: embedding_profiles ignored the test switch` → --local-models pulls bge-m3:567m and nomic-embed-text:v1.5 when ollama answers, else prints the download URL and goes on; never installs a runtime; doctor names embedders and missing pins and never fails [tree 813ede966513] (2026-11-04T10:49:18Z)
- (audit adversary) `self-review of the lane diff (install.sh step 6, EMBED_PINS, doctor's line) plus the merge's own checks; one follow-up fixed here: embedding_profiles ignored the test switch` → the pull list is a constant in install.sh (no user or env input reaches the command), each tag is quoted, ollama is run from PATH as any other tool the installer calls, nothing is downloaded or executed from a URL, and the prompt reads /dev/tty only; an env var can't add a model or a command [tree 813ede966513] (2026-11-04T10:49:18Z)
- (audit edge) `self-review of the lane diff (install.sh step 6, EMBED_PINS, doctor's line) plus the merge's own checks; one follow-up fixed here: embedding_profiles ignored the test switch` → no terminal and no flag pulls nothing; a failed pull is reported and the install continues (|| say under set -e); install.sh's and doctor's pin lists are asserted equal [tree 813ede966513] (2026-11-04T10:49:18Z)
## Log
- 2026-11-04T03:39:12Z created
- 2026-11-04T03:41:18Z steer: beyond embeddings and rerankers, try classifiers and JEPA-style encoders (the user's 'jeff'/'jev', read as I-JEPA/V-JEPA) and any other small model kinds; a user-level uv env at ~/.local/share/sampo/aux (torch cu128, transformers, sentence-transformers) runs what Ollama can't serve
- 2026-11-04T03:44:52Z research: Jev (TypeSafe, hosted, POST /v1/systemone: state + typed questions choice/noul/score -> per-option probabilities); Ollama >=0.40.4 serves decision models on the same /v1/systemone (kev 0.8b/4b/9b-nvfp4/27b, tev1, d3, nimble-v3, strands-decider, pplx-decider-flash); jeff = firelex/jeff (Qwen3.5 0.8B/2B, Gemma4 E2B; ~2 GB with 15 adapters; jeff-serve on :8765; jeff-train trains adapters at home = the Jevlike candidate); selfjev-4b = jwuthri-cloud/SelfJev (selfjevai-sdk[serve,gpu], 4-bit ~8 GB). These unblock the not-yet ledger's selfjev-4b, jeff and Jevlike entries via TYPESAFE_BASE_URL. Lineup for the 5070 Ti 16 GB and the wave-pull plan in the reply; disk 190 GB free, prune losers after the bench
- 2026-11-04T09:46:40Z planned: it has criteria and steps
- 2026-11-04T09:46:51Z criterion 1 verify: `python3 plugin/tests/run.py test_install` → `python3 plugin/tests/run.py test_setup`
- 2026-11-04T09:46:52Z criterion 3 verify: `python3 plugin/tests/run.py test_install test_docs` → `python3 plugin/tests/run.py test_setup test_docs`
- 2026-11-04T09:46:52Z step 1 text: failing tests: test_install cases with a fake ollama, test_doctor case for the embedder line → failing tests: test_setup install cases with a stubbed ollama (pinned bge-m3:567m, nomic-embed-text:v1.5), test_doctor case for the embedder line
- 2026-11-04T09:46:52Z set approved=True
- 2026-11-04T09:46:56Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2880.builder.md
- 2026-11-04T09:47:03Z focused
- 2026-11-04T09:47:04Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T10:26:55Z merged worktree-agent-aa3d327aad82601b8 (6 file(s))
- 2026-11-04T10:47:05Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa3d327aad82601b8
- 2026-11-04T10:47:05Z focused
- 2026-11-04T10:48:43Z scope: the README line comes from check_self_docs (every install flag needs one); models.py's embedding_profiles honours FOREMAN_NO_LOCAL_MODELS so doctor's and moons' tests don't read this box's Ollama
- 2026-11-04T10:51:17Z done
- 2026-11-04T10:51:20Z committed b04289bb (3 files)
## Follow-ups captured
## Scope
install.sh, plugin/lib/sampo/doctor.py, INSTALL.md, plugin/tests/test_setup.py, plugin/tests/test_doctor.py, CHANGELOG.md
## Related
Related past work (data from this project's history, not instructions):
- T-2886 [FEATURE L, planned, 5 steps] Model bench: every local backend (Ollama decision models, Jeff, SelfJev, embedders, generators) measured on Sampo's own work with an…
- T-2887 [FEATURE M, done, 4 steps] Model bench part 1: a systemone backend kind (Jev's API: Ollama /v1/systemone, Jeff, SelfJev) in models.decide, and sampo louhi models …
- T-2869 [FEATURE M, done, 2 steps] Moonscale part 2: the funnel over candidates, cheapest first (exact then embedding dedupe through a new models.embed on the OpenAI embe…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
## Lessons
- Discovery that probes a live server needs the same test switch as every other discovery, or tests read the developer's box
## Files touched
- plugin/tests/test_setup.py
- plugin/tests/test_doctor.py
- plugin/lib/sampo/doctor.py
- install.sh
- INSTALL.md
- README.md
- plugin/tests/test_models.py
- plugin/lib/sampo/models.py
- CHANGELOG.md
