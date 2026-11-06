---
id: T-3011
type: FEATURE
tier: L
status: captured
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T19:34:08Z
updated: 2026-11-04T20:15:22Z
---
# Big-model abilities on this box (60 GB RAM + 16 GB VRAM): (1) run a ~100B open MoE whole…
## Raw request
> Big-model abilities on this box (60 GB RAM + 16 GB VRAM): (1) run a ~100B open MoE whole with experts offloaded to RAM (candidates gpt-oss-120b, Qwen3-Next-80B-A3B, GLM-4.5-Air; 4-bit, about 45-60 GB on /models) through Ollama/llama.cpp and bench it on Louhi against the 27B, gemma 12B and the frontier arm; (2) lossless speed: speculative decoding with an EAGLE-style draft trained on the big model's own outputs; (3) verified compression, new: profile expert routing on Sampo's verified workloads, keep hot experts at higher precision, quantize cold ones to 2-3 bit or merge/prune them, in a loop that stops when Louhi held-out pass rate drops past a set margin, aiming for a copy that fits the GPU; (4) logit distillation of the big model into a 4-9B for the fast tier. User: 'what about you compacting those big models while keeping their abilities? you can create new tech to do this, don't just say it's impossible'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T19:34:08Z created
- 2026-11-04T19:35:48Z steer (user: 'if the smaller models work with that compression, we can try the humungous frontier open source ones down to one that's runnable on a single gpu like what I have'): phase 5, gated on phase 3 holding on the ~100B MoE (held-out pass rate within the margin at a footprint that fits): the largest open MoEs (DeepSeek-class ~670B, Kimi ~1T, GLM's largest) profiled by streaming weights from /models NVMe through llama.cpp mmap (slow is fine for routing statistics on a few thousand tokens of verified workloads), then the same verified prune/quantize loop to a 16 GB VRAM + 60 GB RAM footprint; report retained ability per scenario kind against the frontier arm
- 2026-11-04T20:15:22Z phase 1 probe: qwen3-next:80b (50 GB) under Ollama on 16 GB VRAM + RAM, host load ~40: load 140 s, prompt 5.2 tok/s, generation 2.1 tok/s (200 tokens), think:false ignored (it reasons in prose). Ollama splits whole layers, not experts; next: a quiet-host rerun, then llama.cpp-style expert offload (attention and shared weights on GPU, routed experts in RAM) before any Louhi bench, since 2 tok/s cannot finish a Smith run
## Follow-ups captured
