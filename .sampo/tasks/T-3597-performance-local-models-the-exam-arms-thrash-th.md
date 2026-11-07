---
id: T-3597
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T03:38:51Z
updated: 2026-11-07T04:14:44Z
lane: ~/.claude/foreman.lanes/T-3597
base_note: 
lane_branch: foreman/T-3597
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T03:55:41Z
plan0_scope: []
---
# PERFORMANCE local models: the exam arms thrash the 16 GB GPU - gemma4-12b-32k loads with…
## Raw request
> PERFORMANCE local models: the exam arms thrash the 16 GB GPU - gemma4-12b-32k loads with -c 131072 (OLLAMA_NUM_PARALLEL=4 slots x 32k, 12.5 GiB predicted) and mimo-v2.6:9b needs 9.4 GiB, so Ollama evicts one for the other every few seconds (journal 2026-11-06 21:35-21:36: 'evicting' + a ~2.5 s llama-server start roughly every 5-45 s; 4 gemma runners in one 90 s window). Each reload costs CPU and seconds; run the arms one model at a time, or fit both (fewer slots for gemma / smaller context) (found in T-3588)
## Interpretation
Reading 1 (chosen): cut the local-model CPU waste on Sampo's side - GPU reload thrash between models that can't share the 16 GB GPU (gemma4-12b-32k at 4 slots x 32k = 12.5 GiB, mimo-v2.6:9b 9.4 GiB, evicting each other every 5-45 s), the ~2/s /api/tags poll (T-3598: Smith's per-step phase_note probes local profiles 3 times a step; systemone_profiles reaches the box's Ollama from tests) and the retried unloadable lfm3 (T-3599: an unknown-architecture 500 is retried 3x per call, each a llama-server start). Reading 2 (ruled out): retune Ollama itself (OLLAMA_NUM_PARALLEL=1, rebuild gemma with a smaller num_ctx, remove lfm3) - the user's service and models are off limits for this task.
## Assumptions (confidence)
## Acceptance criteria
- [ ] A chat call to the local Ollama waits while a model that has not shared the GPU with it is mid-call or held, gets its turn after GPU_TURN, and two models seen co-resident run at once (T-3597) — verify with `nice -n 10 python3 plugin/tests/run.py test_gpu_turn`
- [ ] /api/tags and the local /v1/models probe are read at most once a minute per process, and systemone_profiles never reaches the box's Ollama under FOREMAN_NO_LOCAL_MODELS (T-3598) — verify with `nice -n 10 python3 plugin/tests/run.py test_gpu_turn test_models_systemone`
- [ ] A model whose load fails with unknown model architecture is asked once (no retries) and then skipped without a request for 6 h, across processes (T-3599) — verify with `nice -n 10 python3 plugin/tests/run.py test_gpu_turn test_models`
## Non-goals
No change to the Ollama service (OLLAMA_NUM_PARALLEL), models, or Modelfiles; embeddings and systemone calls are not turn-held (small models).
## Approach (options → choice → why)
1) Smaller per-call num_ctx in native options. Likely outcome: shrinks the load only by cutting context: num_ctx is per slot and the server multiplies it by OLLAMA_NUM_PARALLEL (journal: predicted_num_ctx=131072 for a 32768 Modelfile); fails because even 8k slots (gemma ~8.7 + mimo 9.4 GiB) don't fit 16 GB and 32k exam prompts would be cut. 2) Run the exam arms sequentially. Likely outcome: the exam stops thrashing itself; fails if: the foresight sweep / louhi bench / night jobs call qwen or mimo meanwhile (calls.jsonl shows fm cost --sweep on qwen3.5 and mimo while the gemma exam runs). 3) A box-wide GPU turn ledger at _post, the one choke point for chat calls to the local Ollama: two models share once /api/ps showed both wholly in VRAM, else they take turns (a model keeps the GPU GPU_HOLD s past its last call; one kept waiting GPU_TURN s goes next). Likely outcome: reloads about one per turn instead of one per call; fails if: callers bypass _post (none do for chat) or waits stall a caller (bounded, fail-open). 4) Use what exists: Ollama's own scheduler and core.lock. Likely outcome: nothing changes - Ollama queues per model but evicts on every cross-model request, and core.lock is the state dir's global lock (wrong scope, would serialize all state writes); what does exist and is reused: note_call's calls.jsonl location, the box-wide place every model-calling process shares (exam Smiths under temp homes too), so the ledger sits beside it. Choice 3 (80%): it covers every job, not just the exam, and needs no server change; plus a 60 s in-process cache for _tags and _probe and systemone_profiles honoring FOREMAN_NO_LOCAL_MODELS (T-3598), and an unknown-architecture 500 not retried and remembered in the same ledger for 6 h (T-3599).
## Risks and rollback
A waiting call adds latency (bounded by GPU_TURN plus the other model's in-flight call; fail-open after GPU_WAIT_MAX or on any ledger error). Rollback: revert the commit; the ledger file (state/gpu.json) is advisory.
## Execution prompt
## Steps
1. [ ] Failing tests: test_gpu_turn (turns, tags cache, unloadable model)  <- CURRENT
2. [x] T-3598: cache _tags and _probe 60 s; systemone_profiles honors FOREMAN_NO_LOCAL_MODELS
3. [x] T-3599: unknown-architecture 500 not retried, remembered 6 h in the GPU ledger
4. [x] T-3597: GPU turn ledger around chat calls in _post; measure reloads before/after
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_gpu_turn` → ✗ exit 1 · Ran 9 tests in 18.7s (3 jobs, 16 at a time; slowest: Turns 0s, Polls 0s, Unloadable 0s) / FAILED (3 classes: test_gpu_turn.Turns, test_gpu_turn.Polls, test_gpu_turn.Unloadable) [ran] [tree 9c2420dccb1b] [world 2f1906870a] (2026-11-07T03:59:27Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_gpu_turn.Polls test_models_systemone test_ctx_variant` → exit 0 · Ran 16 tests in 74.4s (4 jobs, 16 at a time; slowest: Polls 1s, Smith 0s, Variant 0s) / OK [ran] [tree 8ed99a7df9b2] [world 2f1906870a] (2026-11-07T04:05:34Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_gpu_turn.Unloadable test_models` → exit 0 · Ran 92 tests in 122.4s (17 jobs, 16 at a time; slowest: Bench 4s, RunRoute 2s, OpenAIShape 1s) / OK [ran] [tree 8ed99a7df9b2] [world 2f1906870a] (2026-11-07T04:07:40Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_gpu_turn test_served_context` → exit 0 · Ran 14 tests in 12.4s (5 jobs, 16 at a time; slowest: Smith 1s, Turns 1s, Polls 0s) / OK [ran] [tree 8ed99a7df9b2] [world 2f1906870a] (2026-11-07T04:07:53Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_gpu_turn test_served_context` → exit 0 · Ran 17 tests in 1.5s (5 jobs, 16 at a time; slowest: Turns 1s, Smith 0s, ServedContext 0s) / OK [ran] [tree c4c752cb8024] [world 2f1906870a] (2026-11-07T04:14:36Z)
## Log
- 2026-11-07T03:38:51Z created
- 2026-11-07T03:55:05Z set type=PERFORMANCE, tier=M
- 2026-11-07T03:55:12Z planned: it has criteria and steps
- 2026-11-07T03:55:16Z lane: ~/.claude/foreman.lanes/T-3597 on foreman/T-3597
- 2026-11-07T03:55:40Z focused
- 2026-11-07T03:55:41Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T04:08:49Z measured before (real, 10 min 21:53-22:03 local, gemma exam arm + foresight sweeps on qwen/mimo): 35 llama-server starts, 35 evictions, llama-server 687 CPU-s (1.15 cores), ollama serve 38 CPU-s, 1721 /api/tags, 157 /api/show, 157 /v1/models. After (sim, fake Ollama that reloads on each switch, two jobs, time x100, scratchpad t3597/sim.py): reloads 36 -> 6 per 10 min, p50 call 32 -> 17 s, p90 42 -> 145 s; ledger poll 49-136 us (100 waiters at 1 s: 0.5-1.4% of a core); /api/tags+probe 9 -> 1 a minute per process (test_gpu_turn.Polls). Real after needs the merge: running jobs use the main checkout and the T-2878 lane.
- 2026-11-07T04:14:44Z review fixes c: waits cleaned on any exit, :latest normalised, size-based fit (GPU_FILL 0.8 of max VRAM seen in use), own-process hold exempt, monotonic cap + caller timeout, skip message names gpu.json; sim with two processes: reloads 39 -> 6 per 10 min, p50 26 -> 17 s, p90 39 -> 127 s
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3588 [PERFORMANCE M, active, 3 steps] PERFORMANCE local models (user 2026-11-06: why do the local models use the CPU, not the…
- T-2935 [FEATURE M, done, 4 steps] Local models get the context their prompts need: Sampo reads an Ollama model's served… — lesson: Never trust a profile's declared conte…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- decision 2026-11-04: T-3006's arm comparison runs on local models (gemma 12B, MiMo 9B) instead of the 27B: the Jarvis profiles need LLM_API_KEY, which is never stored, s…
- similar finished tasks took 4–4 steps
