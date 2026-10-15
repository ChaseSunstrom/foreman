---
name: triton-inference
title: Triton Inference Server
area: ml
tags: [triton, inference, serving, batching, gpu, model-repository]
detect: [dep:tritonclient, file:config.pbtxt]
related: [tensorrt, onnx, vllm, cuda, quantization]
---
Serve models with NVIDIA Triton: a validated model repository, dynamic batching tuned on measurements and clients that match the config.

## Verify
- `curl -s -o /dev/null -w "%{http_code}" localhost:8000/v2/health/ready`: server reports ready (200).
- `curl -s localhost:8000/v2/models/<name>/config`: the loaded config matches the repository file.
- `perf_analyzer -m <name> --concurrency-range 1:8`: throughput and latency across concurrency levels.
- `pytest -q tests/test_client.py`: client outputs match the reference framework on fixed inputs.

## Test first
```python
import numpy as np
import tritonclient.http as http

def test_triton_matches_reference():
    c = http.InferenceServerClient("localhost:8000")
    x = np.random.RandomState(0).rand(1, 3, 224, 224).astype("float32")
    inp = http.InferInput("input", x.shape, "FP32"); inp.set_data_from_numpy(x)
    out = c.infer("resnet", [inp]).as_numpy("output")
    np.testing.assert_allclose(out, reference(x), rtol=1e-3, atol=1e-3)
```

## Do
- Lay out `models/<name>/config.pbtxt` and numbered version directories holding the model file.
- Declare `platform` or `backend`, `max_batch_size`, and every input and output with exact names, dtypes and dims.
- Enable `dynamic_batching` with `preferred_batch_size` and `max_queue_delay_microseconds` chosen from `perf_analyzer` runs.
- Set `instance_group` count and kind per GPU; test one versus multiple instances.
- Use ensembles or Python backend for pre and post processing only if needed; keep them thin.
- Watch the metrics endpoint (port 8002) for queue time and failures.
- Pin the server image tag and the model file hashes; load with explicit model control in production.
- Warm up models with a warmup config before taking traffic.

## Avoid
- Mismatched tensor names or dtypes between client and config: opaque errors. Read the config from the server.
- Guessing batching settings: latency spikes or idle GPUs. Measure.
- Treating `max_batch_size: 0` as batching: it disables the batch dimension handling. Set intentionally.
- Unpinned `latest` image: behaviour changes on pull. Pin.
- Skipping an accuracy comparison after conversion: numeric drift. Compare outputs.
- Exposing the server publicly: no auth by default. Front with a gateway.

## Review
- [ ] Config inputs and outputs match the model and client.
- [ ] Batching and instances tuned from measurements.
- [ ] Outputs verified against the reference.
- [ ] Health, readiness and metrics monitored.
- [ ] Image and model versions pinned.
