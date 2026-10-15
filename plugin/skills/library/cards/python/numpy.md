---
name: numpy
title: NumPy
area: python
tags: [python, numpy, arrays, numerics, vectorization, dtype]
detect: [dep:numpy]
related: [pandas, polars, pytest, hypothesis, jupyter]
---
NumPy arrays: vectorized math, broadcasting, dtypes, views versus copies, random generators.

## Verify
- `python -c "import numpy as np; print(np.__version__)"`: the major version; 2.x removed several aliases.
- `python -W error::DeprecationWarning -m pytest -q`: deprecated NumPy calls fail now.
- `python -c "import numpy as np; np.show_config()"`: the BLAS backend, when performance is surprising.
- `pytest -q`: the suite using `numpy.testing`.

## Test first
Use `numpy.testing` for arrays; plain `==` on arrays is ambiguous.
```python
import numpy as np
from numpy.testing import assert_allclose
from app.stats import zscore

def test_zscore_mean_zero_unit_std():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    z = zscore(x)
    assert_allclose(z.mean(), 0.0, atol=1e-12)
    assert_allclose(z.std(), 1.0)
```

## Do
- Replace Python loops with array expressions, `np.where`, boolean masks, `np.einsum` and `np.add.reduce`/axis arguments.
- Make shapes explicit: check `x.shape`, use `keepdims=True` on reductions to broadcast cleanly.
- Set dtypes deliberately (`dtype=np.float64`, `np.int64`) and watch integer overflow, which wraps silently.
- Use the new random API: `rng = np.random.default_rng(seed)` then `rng.normal(...)`, `rng.integers(...)`.
- Preallocate (`np.empty`, `np.zeros`) and fill, rather than appending in a loop.
- Compare floats with `np.isclose`, `np.allclose`, `assert_allclose` and an explicit tolerance.
- Use `np.copy()` when a function must not mutate its input; know that slices are views.

## Avoid
- `np.random.seed` and `np.random.rand` global state: not thread-safe and not reproducible across modules. Pass a `Generator`.
- Removed aliases: `np.float`, `np.int`, `np.bool`, `np.object`, `np.product`, `np.in1d` (2.x). Use `float`, `int`, `bool`, `np.prod`, `np.isin`.
- `if arr:` or `arr == other` as a condition: "truth value is ambiguous". Use `.any()`, `.all()`, `np.array_equal`.
- `a == np.nan`: always False. Use `np.isnan`.
- Modifying a slice expecting a copy: it changes the parent. Call `.copy()`.
- Ragged lists passed to `np.array`: an error in recent versions. Use `dtype=object` on purpose or pad.
- `np.matrix`: discouraged. Use 2-D `ndarray` and the `@` operator.

## Review
- [ ] No Python-level loops over elements where an array operation exists.
- [ ] Dtypes are explicit where overflow or precision matters.
- [ ] Randomness comes from a seeded `default_rng` passed in.
- [ ] Float comparisons use tolerances and NaN handling is deliberate.
- [ ] Functions do not mutate inputs unless documented.
