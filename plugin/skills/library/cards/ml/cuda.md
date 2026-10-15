---
name: cuda
title: CUDA and GPU environments
area: ml
tags: [cuda, gpu, nvidia, drivers, memory, profiling]
detect: [ext:.cu, ext:.cuh, file:CMakeLists.txt, dep:nvidia-*, dep:cupy*]
related: [pytorch, jax, vllm, onnx, lightning]
---
NVIDIA GPU work: matching driver, toolkit and framework builds, memory budgeting, device placement and profiling.

## Verify
- `nvidia-smi`: the driver sees the GPUs, shows memory use and the maximum supported CUDA version.
- `nvcc --version`: which toolkit compiles `.cu` files.
- `python -c "import torch; print(torch.version.cuda, torch.cuda.is_available(), torch.cuda.device_count())"`: the framework build matches the driver.
- `compute-sanitizer ./a.out`: no memory errors or races in a CUDA binary.

## Test first
Write a CPU reference and compare the GPU path against it. Skip GPU tests cleanly where no device exists.
```python
import pytest, torch
from mypkg.ops import fused_op

@pytest.mark.skipif(not torch.cuda.is_available(), reason="needs GPU")
def test_gpu_matches_cpu_reference():
    x = torch.randn(1024, 64)
    ref = fused_op(x)
    got = fused_op(x.cuda()).cpu()
    torch.testing.assert_close(got, ref, rtol=1e-4, atol=1e-5)
```

## Do
- Match the framework wheel's CUDA build to the driver: the driver must support that CUDA version, and the full toolkit is needed only for compiling.
- Select devices with `CUDA_VISIBLE_DEVICES` and refer to them as `cuda:0` inside the process.
- Budget memory: parameters, optimizer state, activations and cache. Use bf16 or fp16, gradient checkpointing and smaller microbatches.
- Check kernel errors with `CUDA_LAUNCH_BLOCKING=1` when a failure is reported on the wrong line.
- Profile with `nsys profile` for timelines and `ncu` for kernels, and `torch.profiler` for frameworks, before optimizing.
- In custom kernels, check every API call's return code, bound-check thread indices and call `cudaDeviceSynchronize` before timing or reading results.
- Compile for the target architecture with `-arch=sm_XX` or CMake `CMAKE_CUDA_ARCHITECTURES`.
- Free memory deliberately and monitor with `nvidia-smi` in a separate shell.

## Avoid
- Installing a framework build for a newer CUDA than the driver supports: `is_available()` returns false. Install a matching build or update the driver.
- Timing GPU code without synchronizing: launches are asynchronous. Synchronize first.
- Calling `torch.cuda.empty_cache()` to fix out-of-memory: it frees only unused cache. Reduce batch size or use checkpointing.
- Per-element host to device copies: transfer-bound. Batch the copies and use pinned memory.
- Ignoring return codes in CUDA C: errors surface later and elsewhere. Wrap calls in a check macro.
- Mixing multiple CUDA toolkits on `PATH` and `LD_LIBRARY_PATH`: wrong library loaded. Set them explicitly.
- Assuming bitwise determinism across GPUs and kernels: tolerate small differences.

## Review
- [ ] Driver, toolkit and framework builds are compatible and documented.
- [ ] GPU results are tested against a CPU reference with tolerances.
- [ ] Tests skip cleanly without a GPU.
- [ ] Memory use is measured, not guessed.
- [ ] Performance claims come from a profiler run with synchronization.
