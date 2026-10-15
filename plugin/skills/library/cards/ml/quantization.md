---
name: quantization
title: Model quantization
area: ml
tags: [quantization, int8, int4, inference, accuracy, calibration]
detect: [dep:bitsandbytes, dep:auto-gptq, dep:autoawq, dep:optimum]
related: [lora-fine-tuning, vllm, onnx, tensorrt, llm-evals]
---
Shrink and speed up models with quantisation, accepting it only when task accuracy, latency and memory are measured against the full-precision model.

## Verify
- `python -m evals.run --model fp16 --suite dev && python -m evals.run --model quant --suite dev`: same eval, both models, side by side.
- `python -m evals.latency --model quant`: tokens per second and memory against the baseline on the target hardware.
- `pytest -q tests/test_quant_load.py`: the quantised artefact loads and produces sane output on fixed prompts.

## Test first
```python
from app.eval import score

def test_quantized_model_stays_within_budget():
    base = score("fp16", "dev")
    quant = score("int4", "dev")
    assert quant >= base - 0.02
```

## Do
- Set a quality budget up front (maximum allowed drop on your task eval) and a memory or latency target.
- Try the cheapest method first: weight-only 8-bit, then 4-bit (GPTQ, AWQ, NF4), comparing each.
- Use a calibration set that resembles production inputs where the method needs one; keep it separate from the eval set.
- Keep sensitive layers (embeddings, output head, normalisation) in higher precision if accuracy drops.
- Match the format to the serving engine (what vLLM, TensorRT or llama.cpp load) before quantising.
- Measure on the target GPU: speedups depend on kernels and batch size, and small batches are bandwidth bound.
- Record method, bits, group size, calibration data and library versions with the artefact.
- For training on quantised bases, use adapters (QLoRA style) and merge or ship them deliberately.

## Avoid
- Judging by perplexity alone: tasks like code, math and long context degrade first. Run the task eval.
- Calibrating on the eval set: inflated scores. Hold it apart.
- Assuming 4-bit is always faster: dequantisation can dominate at large batch. Benchmark.
- Quantising twice or stacking methods: compounding error. Start from full precision.
- Loading with mismatched dtype or format flags: garbage output. Verify with fixed prompts.
- Comparing at different sampling settings: noise. Use greedy or fixed seeds.

## Review
- [ ] Quality budget defined and met on the task eval.
- [ ] Latency and memory measured on target hardware.
- [ ] Calibration data disjoint from eval data.
- [ ] Format compatible with the serving stack.
- [ ] Method and versions recorded.
