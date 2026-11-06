---
id: T-3013
type: FIX
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T19:36:07Z
updated: 2026-11-05T06:16:23Z
group: Ollama store loss and test embedder
base: 01efe2f47203ca5bc96c047078c7834e8c6bc86a
---
# mimo-v2.6:9b and lfm3:1.7b are back in Ollama, so the gpu-mimo9 and gpu-lfm3 profiles answer
## Raw request
> Restore mimo-v2.6:9b and lfm3:1.7b: not in Ollama's registry after the store was lost (they were imported from Hugging Face GGUF files); find their sources, import them into Ollama on /models, or drop the gpu-mimo9 and gpu-lfm3 profiles
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] both models are in Ollama's registry (re-imported from their Hugging Face GGUF files) and each answers a one-line prompt — verify with `curl -s -m 5 localhost:11434/api/tags | grep -q '"mimo-v2.6:9b"' && curl -s -m 5 localhost:11434/api/tags | grep -q '"lfm3:1.7b"' && curl -sf -m 120 localhost:11434/api/generate -d '{"model":"lfm3:1.7b","prompt":"Say ok.","stream":false,"options":{"num_predict":8}}' | grep -q response`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] check both are listed and answer (they were re-imported from hf.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF and hf.co/LiquidAI/LFM3-1.7B-GGUF)  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `curl -s -m 5 localhost:11434/api/tags | grep -q '"mimo-v2.6:9b"' && curl -s -m 5 localhost:11434/api/tags | grep -q '"lfm3:1.7b"' && curl -sf -m 120 localhost:11434/api/generate -d '{"model":"lfm3:1.7b","prompt":"Say ok.","stream":false,"options":{"num_predict":8}}' | grep -q response` → ✗ exit 1 · (no output) [ran] [tree d1a1ef0c4759] [world 2f1906870a] (2026-11-05T02:55:51Z)
- (step 1) `curl -s -m 5 localhost:11434/api/tags | grep -q '"mimo-v2.6:9b"' && curl -s -m 5 localhost:11434/api/tags | grep -q '"lfm3:1.7b"' && curl -sf -m 120 localhost:11434/api/generate -d '{"model":"lfm3:1.7b","prompt":"Say ok.","stream":false,"options":{"num_predict":8}}' | grep -q response` → ✗ exit 1 · (no output) [ran] [tree d1a1ef0c4759] [world 2f1906870a] (2026-11-05T02:55:52Z)
## Log
- 2026-11-04T19:36:07Z created
- 2026-11-04T20:00:49Z premise corrected: never installed (earlier pulls used bad tags), not lost in the move; sources are hf.co/LiquidAI/LFM3-1.7B-GGUF and hf.co/bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF (Q4_K_M), pulled and copied to the profiles' tags so models.json stays as is
- 2026-11-04T20:11:00Z mimo-v2.6:9b: the GGUF's Jinja template gave empty replies under Ollama; rebuilt with Qwen 3.5's renderer and parser (it is a Qwen3.5-9B distill), answers 'Ready'. lfm3:1.7b: pulled, but this Ollama's llama.cpp has no 'lfm3' architecture (error loading model); needs an Ollama upgrade, the user's to install
- 2026-11-05T02:55:46Z planned from capture
- 2026-11-05T02:55:46Z set approved=True
- 2026-11-05T02:55:51Z start point recorded late (no focus had kept one): its diff starts at 01efe2f
- 2026-11-05T02:56:25Z dropped: its check required lfm3:1.7b to answer, but Ollama 0.40.11 can't load the lfm3 architecture; recreated: keep mimo, drop the gpu-lfm3 profile
- 2026-11-05T06:16:23Z follow-up 2026-11-05: mimo-v2.6:9b ran with Ollama's default 4,096 context (its Modelfile set none) while models.json says 32768, so long moons prompts were cut; rebuilt with PARAMETER num_ctx 32768
## Follow-ups captured
