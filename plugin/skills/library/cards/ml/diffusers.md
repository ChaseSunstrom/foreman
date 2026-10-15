---
name: diffusers
title: Diffusers
area: ml
tags: [diffusers, diffusion, image-generation, pytorch, huggingface, gpu]
detect: [dep:diffusers]
related: [transformers, pytorch, cuda, lora-fine-tuning, quantization]
---
Hugging Face Diffusers pipelines for image generation: seeded, memory-aware, safety-checked and reproducible.

## Verify
- `python -c "import diffusers, torch; print(torch.cuda.is_available())"`: library imports and a GPU is visible.
- `pytest -q tests/test_pipeline.py`: a tiny pipeline with few steps produces correct shapes and is deterministic with a seed.
- `python -m app.gen --prompt test --steps 4 --seed 1`: smoke generation runs within the memory budget.

## Test first
Use a small step count and a fixed generator.
```python
import torch
from app.gen import generate

def test_same_seed_same_image():
    a = generate("a red cube", steps=2, seed=7)
    b = generate("a red cube", steps=2, seed=7)
    assert a.size == (512, 512) and list(a.getdata()) == list(b.getdata())
```

## Do
- Load once with `DiffusionPipeline.from_pretrained(..., torch_dtype=torch.float16)` on GPU; pin the model revision for reproducibility.
- Seed with `torch.Generator(device).manual_seed(seed)` and pass it as `generator=`.
- Reduce memory with `enable_model_cpu_offload()`, attention slicing or VAE tiling before shrinking the image.
- Choose the scheduler explicitly (`pipe.scheduler = ...from_config(pipe.scheduler.config)`) and record steps and guidance scale.
- Load LoRA weights with `pipe.load_lora_weights(...)` and record adapter names and scales.
- Keep the safety checker or an equivalent filter on for user-facing apps.
- Store prompt, negative prompt, seed, scheduler, steps and model revision with each output.
- Use `torch.inference_mode()` or the pipeline's default; do not track gradients.

## Avoid
- Float32 on a consumer GPU: out of memory and slow. Use float16 or bfloat16.
- Reloading the pipeline per request: very slow. Keep it resident.
- Unseeded generation in tests: flaky. Pass a generator.
- Moving the pipeline to GPU and enabling CPU offload at once: offload manages devices itself. Pick one.
- Disabling the safety checker for public services: policy risk. Replace with an equivalent filter.
- Loading untrusted pickle checkpoints: use safetensors files.

## Review
- [ ] dtype, device and offload strategy chosen and recorded.
- [ ] Seed, scheduler and revision stored with outputs.
- [ ] Tests use small steps and a fixed seed.
- [ ] Safety filtering in place.
- [ ] Weights from safetensors and trusted sources.
