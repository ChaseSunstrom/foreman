---
name: tensorrt
title: TensorRT
area: ml
tags: [tensorrt, inference, gpu, engine, fp16, onnx]
detect: [dep:tensorrt, dep:torch-tensorrt, dep:tensorrt-llm]
related: [onnx, cuda, triton-inference, quantization, pytorch]
---
Compile models to TensorRT engines: export cleanly, build per GPU, pick precision by accuracy checks and benchmark with real shapes.

## Verify
- `trtexec --onnx=model.onnx --fp16 --saveEngine=model.plan`: the engine builds and prints latency and throughput.
- `python -c "import onnx; onnx.checker.check_model(onnx.load('model.onnx'))"`: the ONNX graph is valid before building.
- `pytest -q tests/test_trt_parity.py`: engine outputs match the framework within tolerance on a fixed set.

## Test first
```python
import numpy as np
from app.trt import run_engine, run_reference

def test_engine_matches_reference():
    x = np.random.RandomState(0).rand(1, 3, 224, 224).astype("float32")
    np.testing.assert_allclose(run_engine(x), run_reference(x), rtol=1e-2, atol=1e-2)
```

## Do
- Export to ONNX with a pinned opset, named inputs and outputs, and dynamic axes only where needed.
- Build engines on the target GPU model and TensorRT version; store them as build artefacts keyed by both.
- Declare optimisation profiles (min, opt, max shapes) matching production batch and size ranges.
- Start with FP16; add INT8 only with a representative calibration set and an accuracy check.
- Compare accuracy on the real eval set, not only random tensors, after each precision change.
- Benchmark with `trtexec` and in the real pipeline including pre and post processing and host-device copies.
- Enable the timing cache to speed up rebuilds; log build and runtime versions.
- Allocate buffers and streams once; reuse execution contexts per thread.

## Avoid
- Shipping a `.plan` built on another GPU or TensorRT version: it fails to load or misbehaves. Rebuild per target.
- Calibrating INT8 on a few random images: accuracy collapse. Use a representative set and verify.
- Dynamic shapes with a profile that excludes real inputs: runtime errors. Cover the range.
- Judging speed from kernel time alone: transfers and preprocessing dominate. Measure end to end.
- Unsupported-op fallbacks hidden in logs: slow graph partitions. Read build warnings.
- Skipping the parity test after an export change: silent numeric drift.

## Review
- [ ] ONNX valid and opset pinned.
- [ ] Engines built per GPU and TensorRT version.
- [ ] Profiles cover production shapes.
- [ ] Accuracy checked at the chosen precision.
- [ ] Benchmarks include the full pipeline.
