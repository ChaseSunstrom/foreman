---
id: T-2928
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T08:12:52Z
updated: 2026-11-04T08:21:00Z
base: 044e0c58dd6a617a74eb7dd27a75a68caf2c9899
base_tree: 7af41a6ce3ae16e452f28822dcf2637b88099673
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T08:12:54Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# think: false reaches Ollama: complete() also sends reasoning_effort none (Ollama's OpenAI API ignores chat_template_kwargs and think; gemma4:12b kept reasoning and ran out of budget on 7 of 10 exam scenarios)
## Raw request
> think: false reaches Ollama: complete() also sends reasoning_effort none (Ollama's OpenAI API ignores chat_template_kwargs and think; gemma4:12b kept reasoning and ran out of budget on 7 of 10 exam scenarios)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a think-false profile's request carries reasoning_effort none beside chat_template_kwargs, and a body that sets reasoning_effort wins — verify with `python3 plugin/tests/run.py test_models`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: the request body
2. [x] fix in models.complete
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_models.Extras` → ✗ exit 1 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: Extras 0s) / FAILED (1 classes: test_models.Extras) [ran] [tree fa2cc2fef20a] [world 2f1906870a] (2026-11-04T08:13:05Z)
- (step 2) `python3 plugin/tests/run.py test_models test_moons_scale` → exit 0 · Ran 117 tests in 5.7s (24 classes, 16 at a time; slowest: Bench 5s, Grow 3s, Cli 2s) / OK [ran] [tree c30e4f359a56] [world 2f1906870a] (2026-11-04T08:13:19Z)
- (ac 1) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 79 tests in 5.4s (14 classes, 16 at a time; slowest: Bench 5s, RunRoute 2s, ModelRules 1s) / OK [ran] [tree c30e4f359a56] [world 2f1906870a] (2026-11-04T08:13:29Z)
- (step 1) `python3 plugin/tests/run.py test_models.Extras` → exit 0 · Ran 4 tests in 1.3s (1 classes, 16 at a time; slowest: Extras 0s) / OK [ran] [tree c30e4f359a56] [world 2f1906870a] (2026-11-04T08:13:29Z)
- (audit edge) `red test then green; live probe: Ollama gemma4:12b answered in 4 tokens with reasoning_effort none and ~130 with chat_template_kwargs or think; the remote llama-swap endpoint accepts both fields together` → reasoning on sends no reasoning_effort (the server's default stays); a body that sets reasoning_effort wins; llama.cpp and vLLM still get chat_template_kwargs [tree c30e4f359a56] (2026-11-04T08:13:29Z)
- (audit intent) `red test then green; live probe: Ollama gemma4:12b answered in 4 tokens with reasoning_effort none and ~130 with chat_template_kwargs or think; the remote llama-swap endpoint accepts both fields together` → think false now turns reasoning off on Ollama, where every GPU model had kept reasoning and run out of budget [tree c30e4f359a56] (2026-11-04T08:13:29Z)
- (audit self) `red test then green; live probe: Ollama gemma4:12b answered in 4 tokens with reasoning_effort none and ~130 with chat_template_kwargs or think; the remote llama-swap endpoint accepts both fields together` → no findings [tree c30e4f359a56] (2026-11-04T08:13:29Z)
## Log
- 2026-11-04T08:12:52Z created
- 2026-11-04T08:12:52Z focused
- 2026-11-04T08:12:54Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T08:20:58Z done
- 2026-11-04T08:21:00Z committed b7e2edca (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2878-smithbench-gpu: `fm code bench --model PROFILE --seed-timeout 600` on an RTX 5070 Ti (16 GB) through Ollama 0.40.11, one model at a time,
- research T-2878-taxonomy: Run s0-001, train split, 10 scenarios, `sampo exam run s0-001 --agent smith --model gpu-qwen4` (qwen3.5:4b on Ollama,
- T-2601 [FEATURE S, done, 2 steps] fm exam runs lists each exam run: id, tier, scenarios and how many held out, and per agent the newest grade's gen, model and date — les…
- decision 2026-11-02: [costly] Long-tier keys: report, never rewrite
- the similar finished task took 2 steps
- start here (files T-2601 touched): plugin/tests/test_exam.py, plugin/lib/fmcli.py, plugin/lib/fmexam.py, CHANGELOG.md
## Why not caught
T-2893 probed the switch live only on the llama-swap endpoint
## Lessons
- verify a switch against each server it targets: the kwarg that worked on llama-swap was ignored by Ollama
## Plan gaps
- failed first: step 1 test: the request body
## Files touched
- plugin/tests/test_models.py
- plugin/lib/sampo/models.py.tmp.431015.31af4cf7fc69
- plugin/lib/sampo/models.py
