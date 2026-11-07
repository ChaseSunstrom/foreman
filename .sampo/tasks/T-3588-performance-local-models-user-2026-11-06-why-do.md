---
id: T-3588
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-07T03:12:03Z
updated: 2026-11-07T03:48:52Z
lane: ~/.claude/foreman.lanes/T-3588
lane_branch: foreman/T-3588
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T03:26:51Z
plan0_scope: []
---
# PERFORMANCE local models (user 2026-11-06: why do the local models use the CPU, not the…
## Raw request
> PERFORMANCE local models (user 2026-11-06: why do the local models use the CPU, not the GPU): they do run on the GPU (mimo-v2.6:9b 33/33 layers on the RTX 5070 Ti, flash attention on, ~118 tokens/s; CPU 0% while GPU 88%), but each request spends ~1.5 s at ~300% CPU: llama.cpp's 8 worker threads busy-poll while the GPU computes every token (n_threads = 8, ollama's default), ~16 requests/min ≈ 1.2-3.7 cores; and when two models are loaded at once (gemma 12B + mimo 9B for the exam arms) both spin. For models fully on the GPU, run with 1-2 CPU threads (ollama num_thread: Sampo calls the OpenAI-compatible /v1 endpoint, which can't pass it — use /api/chat options or a model variant with PARAMETER num_thread), measure CPU per request and tokens/s before and after, keep speed within 5%
## Interpretation
Reading 1 (chosen): Sampo should ask Ollama for fewer CPU threads on its own calls to models that sit wholly in VRAM, since llama.cpp's default 8 threads only busy-poll there; Sampo calls Ollama over /v1, which drops options, so loopback-Ollama chat calls go to native /api/chat with options.num_thread=1 unless /api/ps shows the model partly in system RAM; other servers keep the OpenAI path. Reading 2 (ruled out): change the Ollama service (OLLAMA_NUM_THREAD-style env, systemd unit) or the user's models; the user said not to touch the service config or the models, and it would also slow CPU-offloaded models.
## Assumptions (confidence)
Measured (qwen3.5-4b-32k, all layers on GPU, 6x256-token requests): default threads (8) 6.3-6.5 CPU-s/req at 158-160 tok/s; num_thread=1 1.65 CPU-s/req at 162 tok/s; num_thread=2 2.43; num_thread=4 3.94. /v1 ignores options.num_thread (ollama log: no -t on the runner) (95%). Ollama reloads the runner when num_thread differs between calls, so all Sampo calls to one model must agree (95%).
## Acceptance criteria
- [ ] A chat call to the local Ollama whose model sits wholly in VRAM goes to native /api/chat with options.num_thread 1, max_tokens, think, tools and schema carried, tool calls read back — verify with `nice -n 10 python3 plugin/tests/run.py test_models.OllamaThreads`
- [ ] A model partly in system RAM, nothing loaded, a loopback server without /api/ps, or a remote server keeps the OpenAI /v1 path with no num_thread — verify with `nice -n 10 python3 plugin/tests/run.py test_models.OllamaThreads`
- [ ] The existing model and served-context tests still pass — verify with `nice -n 10 python3 plugin/tests/run.py test_models test_served_context`
## Non-goals
The live session's ~1.5 s at ~300% CPU per request figure is the symptom this measures and fixes (criterion 1 and step 3's numbers), not a separate criterion. Embedding calls (/v1/embeddings) keep Ollama's default threads.
## Approach (options → choice → why)
1) A model variant with PARAMETER num_thread via ollama create, called over /v1; likely outcome: works; fails if: the user's ollama fills with new models, which the user prefers not.
2) Native /api/chat for the loopback Ollama with options.num_thread, translating the OpenAI-shaped body and reply (tool_call args as objects, think, max_tokens->num_predict, response_format->format, sampling extras->options); likely outcome: ~75% less runner CPU at equal speed; fails if: a translation gap breaks tool calls or think.
3) Use what exists: context_variant's ollama create path already makes num_ctx variants; add num_thread to its Modelfile; fails if: profiles without ctx_variant never get it; same clutter as 1.
4) Do less: preload once natively with num_thread, then keep /v1; fails if: Ollama reloads the runner whenever num_thread differs (measured: it does), so it never sticks.
Choice 2 (80%): nothing created on the Ollama side, one gate (_ollama_ps: Ollama, model not partly in system RAM), OpenAI path untouched for every other server; every Sampo call to a model sends the same num_thread, so Sampo's own calls never make the runner reload.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in test_models.OllamaThreads (fake Ollama: /api/ps rows, native reply)
2. [x] complete(): loopback Ollama with the model wholly in VRAM -> native /api/chat with num_thread 1; reply read as the OpenAI one
3. [x] Measure llama-server CPU-s/request and tokens/s before and after on a GPU-resident model
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_models.OllamaThreads` → ✗ exit 1 · Ran 3 tests in 8.3s (1 jobs, 16 at a time; slowest: OllamaThreads 0s) / FAILED (1 classes: test_models.OllamaThreads) [ran] [tree 90952a47e065] [world 2f1906870a] (2026-11-07T03:27:59Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_models test_served_context` → exit 0 · Ran 98 tests in 88.0s (18 jobs, 16 at a time; slowest: Bench 6s, ModelRules 2s, RunRoute 2s) / OK [ran] [tree f10e2ebc2fb5] [world 2f1906870a] (2026-11-07T03:38:27Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_models.OllamaThreads` → exit 0 · Ran 3 tests in 5.5s (1 jobs, 16 at a time; slowest: OllamaThreads 0s) / OK [ran] [tree f10e2ebc2fb5] [world 2f1906870a] (2026-11-07T03:38:40Z)
- (step 3) `python3 -I scratchpad/t3588_bench.py qwen3.5-4b-32k:latest 6 d 1 2 4 d (llama-server /proc/PID/stat utime+stime per request, eval_count/eval_duration; ollama log shows -t N on the runner)` → qwen3.5-4b-32k wholly in VRAM, 6x256-token replies: Ollama default 8 threads 6.33/6.55 CPU-s per request at 160.4/158.3 tok/s, 3.7-3.8 cores busy; num_thread 1: 1.65 CPU-s at 162.4 tok/s, 0.98 cores; 2: 2.43 at 161.1; 4: 3.94 at 161.9. /v1 with options.num_thread: runner started without -t (ignored). Passive: the exam's gemma4-12b-32k runner at default threads used 3.64 CPU-s per call (52 calls in 90 s, 2.1 cores avg, incl. 3 evict-reloads). [tree f10e2ebc2fb5] (2026-11-07T03:38:41Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_models test_served_context` → exit 0 · Ran 98 tests in 7.1s (18 jobs, 16 at a time; slowest: Bench 5s, RunRoute 2s, OpenAIShape 1s) / OK [ran] [tree fcdf159a3e54] [world 2f1906870a] (2026-11-07T03:41:43Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_models test_served_context` → exit 0 · Ran 99 tests in 18.0s (18 jobs, 16 at a time; slowest: Bench 4s, RunRoute 2s, OpenAIShape 1s) / OK [ran] [tree 5e1c27c2e4fa] [world 2f1906870a] (2026-11-07T03:48:52Z)
## Log
- 2026-11-07T03:12:03Z created
- 2026-11-07T03:21:47Z set tier=M, type=PERFORMANCE
- 2026-11-07T03:24:54Z planned: it has criteria and steps
- 2026-11-07T03:24:57Z lane: ~/.claude/foreman.lanes/T-3588 on foreman/T-3588
- 2026-11-07T03:26:49Z focused
- 2026-11-07T03:26:51Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T03:42:08Z built: complete() sends loopback-Ollama calls with the model wholly in VRAM to /api/chat with num_thread 1 (lane commit db77ed3a7); transition: callers on older code (e.g. the T-2878 exam lane) send no num_thread, so a model both call reloads on each switch until those lanes rebase
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2878-taxonomy: Louhi's smith arm, `sampo exam run RUN --agent smith --model PROFILE --split all --limit 44`, on seeded exam runs of the
- research T-3006-reason-arms: Arms: `off` (thinking off, today's default), `state` (a compact thought state carried between turns, thinking on only on
- T-2935 [FEATURE M, done, 4 steps] Local models get the context their prompts need: Sampo reads an Ollama model's served… — lesson: Never trust a profile's declared conte…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
- the similar finished task took 4 steps
