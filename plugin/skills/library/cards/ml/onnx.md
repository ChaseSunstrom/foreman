---
name: onnx
title: ONNX and ONNX Runtime
area: ml
tags: [python, onnx, inference, export, onnxruntime, deployment]
detect: [dep:onnx, dep:onnxruntime, dep:onnxruntime-gpu, ext:.onnx]
related: [pytorch, transformers, cuda, vllm, keras]
---
ONNX model export and ONNX Runtime inference: export with dynamic axes, validate the graph, and check numerical parity.

## Verify
- `python -c "import onnx; onnx.checker.check_model('model.onnx')"`: the graph is structurally valid.
- `python -c "import onnxruntime as ort; print(ort.get_available_providers())"`: which execution providers the install offers.
- `pytest -q`: parity tests between the source framework and ONNX Runtime pass.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Export, run both, and compare outputs, including a batch size different from the export example.
```python
import numpy as np, torch, onnxruntime as ort
from mypkg.model import Net

def test_onnx_matches_torch(tmp_path):
    m = Net().eval(); p = tmp_path / "m.onnx"
    torch.onnx.export(m, torch.randn(1, 8), p, input_names=["x"], output_names=["y"],
                      dynamic_axes={"x": {0: "batch"}, "y": {0: "batch"}})
    x = np.random.randn(5, 8).astype("float32")
    got = ort.InferenceSession(str(p), providers=["CPUExecutionProvider"]).run(None, {"x": x})[0]
    assert np.allclose(got, m(torch.from_numpy(x)).detach().numpy(), atol=1e-5)
```

## Do
- Call `model.eval()` before exporting, and use a representative example input.
- Name inputs and outputs, and declare `dynamic_axes` for batch and sequence dimensions.
- Run `onnx.checker.check_model`, then compare outputs against the source framework with an explicit tolerance.
- Pass `providers=[...]` to `InferenceSession` in priority order, with `CPUExecutionProvider` last.
- Create the session once and reuse it. Sessions are thread-safe for `run`.
- Quantize with `onnxruntime.quantization` (dynamic or static) and re-measure accuracy afterward.
- Pin the opset explicitly on export and record it.
- Keep preprocessing, such as tokenization and normalization, identical to training.

## Avoid
- Exporting in training mode: dropout and batch norm behave differently. Call `eval()`.
- Fixed shapes from the example input: serving another batch size fails. Set `dynamic_axes`.
- Skipping the parity test: silent numeric drift or unsupported-op fallbacks. Compare outputs.
- Omitting `providers` on recent ONNX Runtime with a GPU build: it may error or fall back silently. List providers explicitly.
- Installing both `onnxruntime` and `onnxruntime-gpu` in one environment: conflicting packages. Keep one.
- Creating a new `InferenceSession` per request: slow startup. Reuse it.
- Feeding float64 arrays to a float32 model: type errors. Cast inputs.
- Loading ONNX files of unknown origin into a production service without review.

## Review
- [ ] Model is exported in eval mode with named inputs, outputs and dynamic axes.
- [ ] Checker passes and numeric parity is tested with a tolerance.
- [ ] Providers are listed explicitly and the session is reused.
- [ ] Quantized models are re-evaluated for accuracy.
- [ ] Opset and runtime versions are recorded.
