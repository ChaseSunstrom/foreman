---
id: T-1360
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmmodels.py, plugin/tests/test_models.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:51Z
updated: 2026-10-23T07:40:21Z
base: 34f381487b152343e9d26981c99a6ae30a9d33ee
base_tree: 2448bd8151688685dc8d9ec6161b906581c21ad5
plan0_at: 2026-10-23T07:34:14Z
plan0_scope: [plugin/lib/fmmodels.py, plugin/tests/test_models.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Local models' real context: a local server's profile takes its context from the server (Ollama /api/show, llama.cpp /props, vLLM's model row, LM Studio's model), falling back to 8192
## Raw request
> Local models' real context (R24): a local profile's context comes from the server (Ollama /api/show, llama.cpp /props, vLLM /v1/models), falling back to 8192, and fm code's caps follow it
## Interpretation
fm code assumes 8192 tokens for any local model it finds; the server knows what it really serves, and fm code's prompt caps should follow that number, not a guess.
## Assumptions (confidence)
## Acceptance criteria
- [x] a probed Ollama, llama.cpp, vLLM or LM Studio server's profile carries the context it says it serves (Ollama's num_ctx, else its 4096 default), and 8192 when it says nothing usable — verify with `python3 plugin/tests/run.py test_models.LocalContext`
## Non-goals
## Approach (options → choice → why)
One more request per probed server, only once /models answered: Ollama POST /api/show (parameters num_ctx; without it Ollama serves its default, 4096, whatever the model could take), llama.cpp GET /props (default_generation_settings.n_ctx), vLLM's /models row (max_model_len, no extra call), LM Studio GET /api/v0/models/ID (loaded_context_length); any failure or an implausible number keeps LOCAL_CONTEXT. fm code's caps already follow the profile's context (run.cap halves under SMALL_CONTEXT), so nothing else changes. Options: (1) ask each server (chosen); (2) a table of model families' contexts (wrong whenever the server is configured differently, which is the common case for Ollama); (3) a models.json context only (already possible; the request is the probed profiles). ponytail: OLLAMA_CONTEXT_LENGTH set on the server isn't in /api/show, so such a server reads as 4096.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests red: each server's answer, a server that fails the ask
2. [x] fmmodels: _local_context in _probe
3. [x] docs: CHANGELOG, MASTER
## Resume here
## Docs impact
CHANGELOG, MASTER
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_models.LocalContext` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: LocalContext 0s) / OK [ran] [tree cca4d146da77] (2026-10-23T07:39:37Z)
- (step 2) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 54 tests in 3.6s (7 classes, 16 at a time; slowest: Bench 3s, OpenAIShape 1s, ExtractJson 0s) / OK [ran] [tree cca4d146da77] (2026-10-23T07:39:41Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 69 tests in 8.8s (17 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 2s, Site 1s) / OK [ran] [tree e3b2c266d563] (2026-10-23T07:39:51Z)
- (audit intent) `self: request re-read` → pass: each local server's own context, 8192 fallback; fm code's caps already follow the profile's context [tree e3b2c266d563] (2026-10-23T07:39:58Z)
- (ac 1) `python3 plugin/tests/run.py test_models.LocalContext` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: LocalContext 0s) / OK [ran] [tree e3b2c266d563] (2026-10-23T07:39:58Z)
- (audit intent) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → the criterion met; caps follow through the existing SMALL_CONTEXT rule [tree e3b2c266d563] (2026-10-23T07:39:58Z)
- (audit adversary) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → the extra ask goes only to the local server that already answered /models, through the same opener (no redirects to metadata addresses), 1 MB and 1 s at most; the model name is URL-quoted into LM Studio's path [tree e3b2c266d563] (2026-10-23T07:39:58Z)
- (audit edge) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → a failed or odd answer keeps 8192; a number outside 512..10M is ignored; Ollama without num_ctx reads as its 4096 default (its server-wide setting isn't visible, noted) [tree e3b2c266d563] (2026-10-23T07:39:58Z)
## Log
- 2026-10-21T03:47:51Z created
- 2026-10-23T07:33:40Z planned from capture
- 2026-10-23T07:33:42Z set scope=['plugin/lib/fmmodels.py', 'plugin/tests/test_models.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T07:34:13Z focused
- 2026-10-23T07:40:19Z done
- 2026-10-23T07:40:21Z committed 78292f04 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1211 [FEATURE M, done, 2 steps] fm code: fmmodels, one stdlib client for OpenAI-compatible and Anthropic endpoints with model profiles and local-server detection — les…
- T-1210 [FEATURE L, dropped, 4 steps] fm code round 1: stdlib model client and the harness-run loop, proved end to end on a fake model server
- T-1207 [FEATURE L, blocked, 3 steps] Foreman Code: fm code runs Foreman's loop itself on any model or CLI
- decision 2026-10-23: A broken code.toml: fm code config falls back to defaults and names the line; runs keep refusing it
- the similar finished task took 2 steps
- start here (files T-1211 touched): plugin/tests/test_models.py, plugin/lib/fmmodels.py, MASTER.md, CHANGELOG.md
- likely tests for the scope: plugin/tests/test_models.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, plugin/lib/fmmodels.py, plugin/tests/test_models.py; re-ground the plan against them before editing
## Lessons
- A local server knows its own serving context; asking it beats a family table, which is wrong whenever the server is configured
## Files touched
- plugin/tests/test_models.py
- plugin/lib/fmmodels.py
- CHANGELOG.md
- MASTER.md
