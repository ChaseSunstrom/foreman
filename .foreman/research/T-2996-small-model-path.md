1. **Answer**

The best realistic path is to start from Qwen3.5-9B or 4B (Apache-2.0) and not pretrain anything. Do LoRA SFT on rejection-sampled, test-verified data, with the remote Qwen 27B as the generator and unit tests or the repo's own checks as the filter. Defer RL and latent reasoning. Ollama 0.40 has speculative decoding only on some paths, and I could not confirm that any of them apply to a CUDA GPU. My evidence this session was thin: several searches returned weak or aggregator sources, and I did not verify the items in section 4 against the papers.

2. **Findings**

**Q1: Bases**
- Qwen3.5-9B is Apache-2.0. It is a hybrid Gated DeltaNet plus gated attention model, and the card lists LiveCodeBench v6 at 65.6. https://huggingface.co/Qwen/Qwen3.5-9B (undated; the citation says Feb 2026; primary). I took this from a fetch summary, not a verbatim quote. Confidence: medium.
- The small Qwen3.5 sizes are 0.8B, 2B, 4B and 9B, all Apache-2.0. Artificial Analysis lists Intelligence Index scores of 32 for the 9B and 27 for the 4B. https://artificialanalysis.ai/articles/qwen3-5-small-models (5 Mar 2026; secondary). Confidence: medium.
- Gemma 4 launched on 2 Apr 2026 under Apache-2.0, with E2B, E4B, 26B MoE and 31B dense. Aggregators put E4B at about 52% and E2B at about 44% on LiveCodeBench v6. https://webscraft.org/blog/gemma-4-povniy-oglyad-rozmiri-litsenziya-porivnyannya-z-gemma-3?lang=en (2026; community). Confidence: low-medium. One source claimed 80% for E4B, which I discounted.
- I found no SWE-bench Verified or HumanEval+ numbers for any ≤9B base, and I did not search for newer leaders. Treat Qwen3.5-9B as the likely leader, but that is not verified.

**Q2: Data**
- OpenCodeReasoning is mostly CC-BY-4.0 with some Apache and MIT samples. It is distilled from DeepSeek-R1, which is not Claude or GPT. https://huggingface.co/datasets/nvidia/OpenCodeReasoning (secondary mirrors). Confidence: medium.
- The Nemotron SWE trajectories (~51k, CC-BY-4.0 or BSD-3) and SWE-Hero (CC-BY-4.0) were generated with Qwen3-Coder-480B. https://huggingface.co/datasets/nick007x/Nemotron-SWE-v1 (2026; community mirror). Confidence: medium.
- Scale-SWE has about 20k executable tasks with fail-to-pass tests. It also ships 71k DeepSeek v3.2 trajectories. I could not confirm its licence. https://huggingface.co/datasets/AweAI-Team/Scale-SWE (primary). Confidence: low on licence.
- I did not check SWE-smith, rStar-Coder, Nemotron-Cascade, or math sets with checkable answers.
- Avoid any Claude or GPT-distilled set. I could not name specific ones from this search, so check each card's "generated with" line.

**Q3: Fit on 16 GB (mostly inference, not measured)**
- A 4B model in bf16 is about 8 GB of weights. LoRA SFT with gradient checkpointing and sequences of 2–4k tokens should fit. This is my estimate. One guide puts 16-bit LoRA at about 8 GB for 3B at rank 16, batch 1. https://insiderllm.com/pdfs/lora-training-consumer-hardware.pdf (community). Confidence: medium.
- Rejection-sampling fine-tuning (RFT) is just SFT on filtered samples, so it fits wherever SFT fits. Generation is served by the remote 27B.
- GRPO has no critic, but it needs rollouts. Rollouts from the same 4B plus a LoRA fit only with short completions, and there is no trl installed. That means a hand-written loop, or installing trl. I found no published 4B GRPO run on 16 GB. Confidence: low.

**Q4: Latent reasoning**
- An Apr 2026 paper finds a Coconut model can extract answers directly from the question representations, with comparable accuracy and no latent tokens. https://arxiv.org/html/2604.06374v1 (secondary). Confidence: medium.
- Coconut needs staged training that swaps chain-of-thought steps for continuous thoughts. Its published tasks are small (GSM8K-style math, ProntoQA, ProsQA). https://arxiv.org/abs/2412.06769 (Dec 2024; older than a year; primary). Confidence: medium.
- Looped-transformer gains are shown for systematic generalisation and depth extrapolation, at small scale. I did not verify this against the papers.
- A single GPU can test Coconut on ProsQA or GSM8K with a 0.5–1B model. It will not help a coding agent.

**Q5: Ollama**
- v0.40.7 (18 Oct 2026): "More draft models now work with speculative decoding". https://github.com/ollama/ollama/releases (primary). Confidence: medium.
- v0.40.12 (27 Oct 2026): "Speculative decoding now supports DFlash2 draft models on MLX". MLX is the Apple runtime, so this likely does not apply to your CUDA card. Confidence: medium.
- v0.40.10 (23 Oct 2026): a Gemma 4-based Nemotron model "includes a DFlash draft for speculative decoding". Confidence: medium.
- The latest stable release is v0.40.14 (3 Nov 2026).
- These quotes came through a fetch summary, so the main thread should check them against the release notes.
- Adapter import: the old docs list only Llama, Mistral and Gemma 1/2 for safetensors adapters. The newer docs list Qwen3 and Gemma 3 for model import, not clearly for adapters. https://docs.ollama.com/import.md (primary). I found nothing on Qwen3.5 or Gemma 4 adapters. Confidence: low.
- The fallback is to merge the LoRA into the base and convert to GGUF, or to run llama.cpp's `convert_lora_to_gguf.py`.
- I found no 4B/9B speedup numbers with 0.5–1B drafts.

3. **Risks / surprises**
- The Qwen3.5 hybrid Gated DeltaNet architecture may have weaker PEFT, llama.cpp and Ollama support than plain-attention models. Test a 50-step LoRA, a merge and a GGUF round trip before committing.
- Most SWE trajectory sets are distilled from other open models, such as Qwen3-Coder and DeepSeek. Check each teacher's own terms.
- If the 27B is Qwen, its outputs are Apache-licensed. Confirm which model it actually is.

4. **Not checked**
- Newer leaders such as Phi, SmolLM, Granite or Nemotron.
- Per-dataset licences.
- Published GRPO results for small models.
- Real speedup numbers.
- Whether Ollama's CUDA runner supports draft models.
- Whether the Qwen3.5 benchmark numbers on the card are reproducible.

**Ranked recommendation**
1. **RFT/LoRA SFT on Qwen3.5-4B or 9B.** Generate with the 27B on your own tasks, keep only samples that pass the tests, and train with PEFT (a plain loop or Trainer is enough). The expected gain is a clear lift on your narrow task. The risk is moderate, mostly from the hybrid-architecture toolchain.
2. **Verify the deployment path first, in one day.** That means LoRA merge, GGUF conversion and an Ollama run of the same model. The gain is avoiding a dead end. The risk is low.
3. **Speculative decoding or an n-gram draft in llama.cpp directly.** The expected gain is a modest speedup. The risk is low to moderate, because Ollama may not expose it on CUDA.

**Not achievable here:** pretraining a competitive model, full-parameter training of 9B, large-scale RL with agent rollouts, and a latent-reasoning coding model.

Noticed: none
