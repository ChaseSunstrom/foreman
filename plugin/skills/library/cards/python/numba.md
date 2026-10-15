---
name: numba
title: Numba
area: python
tags: [python, numba, jit, performance, numpy, parallel]
detect: [dep:numba]
related: [numpy, cython, pandas, pytest]
---
Numba: JIT-compile numeric NumPy loops with `@njit`, avoiding object mode and measuring after warm-up.

## Verify
- `NUMBA_DISABLE_JIT=1 pytest -q`: the pure-Python semantics are correct and debuggable.
- `pytest -q`: the compiled behaviour matches.
- `python -c "import numba; print(numba.config.THREADING_LAYER)"`: the threading layer resolves for `parallel=True`.
- `python -m numba -s`: environment report (CPU, versions, threading) when behaviour differs across machines.

## Test first
Compare the jitted function against `.py_func` and test warm-up separately.
```python
import numpy as np
from app.kernels import moving_sum

def test_matches_python_reference():
    x = np.random.default_rng(1).random(1000)
    got = moving_sum(x, 5)
    ref = moving_sum.py_func(x, 5)
    np.testing.assert_allclose(got, ref)

def test_edge_window_larger_than_input():
    assert moving_sum(np.ones(3), 5).size == 0
```

## Do
- Use `@njit` (same as `@jit(nopython=True)`), which fails loudly when it cannot compile.
- Pass NumPy arrays, scalars and tuples. Keep loops explicit: loops are fast in Numba.
- Use `@njit(parallel=True)` with `prange` for independent iterations, and `cache=True` to persist compiled code across runs.
- Keep dtype stable across calls: each new type signature triggers recompilation. Cast at the boundary.
- Benchmark after one warm-up call, so compile time is excluded.
- Use `@vectorize` or `@guvectorize` for element-wise ufuncs.
- Use `numba.typed.List` and `numba.typed.Dict` for containers inside jitted code.
- Use `fastmath=True` only where non-IEEE reordering is acceptable.
- Seed random numbers inside jitted code with `np.random.seed` called within a jitted function: Numba has its own generator state.

## Avoid
- Calling pandas, `print` of large objects, or arbitrary Python libraries inside `@njit`: `TypingError`. Pass arrays in and out.
- Plain `@jit` without `nopython`: can silently fall back to slow object mode on older setups. Use `@njit`.
- Timing the first call: includes compilation. Warm up first.
- Race conditions in `prange` writing the same index or accumulating into shared lists: wrong results. Use reductions on scalars or per-iteration outputs.
- Mixing int and float types in one variable inside a function: unification errors or slowdowns. Initialize with the right literal (`0.0`).
- Relying on exceptions with rich messages in jitted code: only simple raises work. Validate in Python wrappers.
- `cache=True` on functions defined in notebooks or stdin: no source file to cache.

## Review
- [ ] Tests compare to `py_func` and run once with `NUMBA_DISABLE_JIT=1`.
- [ ] Benchmarks exclude compile time.
- [ ] `parallel=True` loops have no shared writes.
- [ ] Input dtypes are normalised before the jitted call.
