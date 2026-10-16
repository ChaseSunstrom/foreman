---
name: scipy
title: SciPy
area: python
tags: [python, scipy, numerics, signal, optimize, statistics, sparse]
detect: [dep:scipy]
related: [numpy, pandas, matplotlib, pytest, numba]
---
SciPy: scientific routines on NumPy arrays (signal, optimize, stats, sparse, interpolate, linalg, integrate).

## Verify
- `python -c "import scipy; print(scipy.__version__)"`: the installed version, before trusting docs or examples.
- `python -W error::DeprecationWarning -m pytest -q`: deprecated SciPy calls fail now.
- `python -c "import scipy; scipy.show_config()"`: the BLAS/LAPACK backend, when performance is surprising.
- `pytest -q`: the suite, with numeric checks via `numpy.testing`.

## Test first
Test numeric results against a known closed-form answer, with an explicit tolerance.
```python
import numpy as np
from numpy.testing import assert_allclose
from scipy import integrate

def test_area_under_sine_is_two():
    value, err = integrate.quad(np.sin, 0, np.pi)
    assert_allclose(value, 2.0, rtol=1e-8)
    assert err < 1e-8
```

## Do
- Import the submodule you need (`from scipy import signal, optimize`); submodules are not all loaded by `import scipy`.
- Check the result object of `optimize.minimize` and `root`: read `res.success` and `res.message` before using `res.x`.
- Use `scipy.sparse` for mostly-zero matrices, building with COO or LIL and converting to CSR or CSC for arithmetic.
- Use `signal.butter` with `output="sos"` and `signal.sosfiltfilt` for stable filtering.
- Use `scipy.stats` distributions and tests with a fixed `random_state` or a `numpy.random.Generator` where accepted.
- Give `interpolate` and `optimize` sensible bounds and initial guesses; the answer depends on them.
- Compare floats with `assert_allclose`, never `==`.

## Avoid
- Treating a failed optimizer run as a result: `res.x` is returned even when `res.success` is False. Check it.
- Dense conversion of large sparse matrices (`.toarray()`): memory blows up. Keep sparse operations sparse.
- Using `ba` coefficients for high-order IIR filters: numerically unstable. Use second-order sections.
- Importing from removed or private paths (`scipy.misc` helpers, `scipy.signal.signaltools`): use the public submodule function.
- Feeding unsorted or duplicate x values to interpolators that require increasing x: wrong output or errors. Sort and dedupe.
- Ignoring `NaN` in input: many routines propagate or fail silently. Mask or drop them first.

## Review
- [ ] The needed submodules are imported explicitly.
- [ ] Optimizer and solver results are checked for success before use.
- [ ] Large matrices stay in a sparse format.
- [ ] Filters use stable forms and the sample rate is stated.
- [ ] Tests compare to known answers with tolerances.
