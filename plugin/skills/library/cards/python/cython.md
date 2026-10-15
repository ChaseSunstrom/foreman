---
name: cython
title: Cython
area: python
tags: [python, cython, performance, c, extension, typing]
detect: [dep:Cython, dep:cython, ext:.pyx, ext:.pxd]
related: [numpy, pyo3-maturin, python-packaging, numba, pytest]
---
Cython: compile typed Python to C extensions, with annotated hot loops, memoryviews and measured speedups.

## Verify
- `cython -a src/pkg/fast.pyx`: writes an HTML report; yellow lines in hot loops still touch Python objects.
- `python -m pip install -e . --no-build-isolation` (or `pip install -e .`): the extension compiles.
- `python -c "import pkg.fast"`: the compiled module imports.
- `pytest -q`: the compiled code against the pure-Python reference tests.

## Test first
Keep a pure-Python reference and test equality plus a benchmark guard.
```python
import numpy as np
import pytest
from pkg import fast, slow

@pytest.mark.parametrize("n", [0, 1, 1000])
def test_fast_matches_reference(n):
    a = np.random.default_rng(0).random(n)
    assert fast.total(a) == pytest.approx(slow.total(a))

def test_rejects_wrong_dtype():
    with pytest.raises((TypeError, ValueError)):
        fast.total(np.arange(3))
```

## Do
- Declare the build in `pyproject.toml` with `requires = ["setuptools", "cython"]` and call `cythonize("src/pkg/*.pyx", language_level=3)` from `setup.py`.
- Type hot variables: `cdef int i`, `cdef double s`, or `cpdef double f(double x)`. Use typed memoryviews `double[:] a` for arrays.
- Use `@cython.boundscheck(False)` and `@cython.wraparound(False)` only after tests pass, and only on loops that index in range.
- Release the GIL for pure C loops: `with nogil:` on `prange` from `cython.parallel` (build with OpenMP flags).
- Profile first with `cProfile` or `timeit`, then compile only the hot function.
- Keep a pure-Python fallback or `.py` plus `.pxd` augmenting file for debuggability.
- Add `include_dirs=[numpy.get_include()]` when you `cimport numpy`.
- Build wheels with `cibuildwheel` for each platform.

## Avoid
- Compiling untyped code and expecting speedups: it runs the same interpreter calls. Add types and check the `-a` report.
- Disabling `boundscheck` and `wraparound` globally: silent memory corruption on bad indices. Scope them to the function.
- Missing `language_level=3`: string and division semantics follow Python 2 rules in old setups. Set it explicitly.
- Returning memoryviews to callers with the owning array freed: dangling data. Keep a reference or return `np.asarray(view)`.
- Raising from `nogil` or `noexcept` functions unchecked: swallowed errors. Declare `except *` or a sentinel `except -1` as needed.
- Committing generated `.c` files as source of truth: stale diffs. Generate in the build.

## Review
- [ ] A reference implementation and equality tests exist.
- [ ] The annotation report shows the hot loop is white.
- [ ] Safety checks are disabled only in scoped, tested functions.
- [ ] Build metadata declares Cython and the NumPy include path.
