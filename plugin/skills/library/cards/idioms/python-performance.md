---
name: python-performance
title: Python performance
area: idioms
tags: [python, performance, profiling, benchmark, asyncio, memory]
detect: []
related: [python, pytest, numpy, python-typing]
---
Measure first, then fix Python hot spots: algorithm and data structure, then batching, then native code.

## Verify
- `python -m cProfile -s cumtime script.py`: where the time goes, by cumulative cost.
- `python -m timeit -s "setup" "stmt"`: a micro-benchmark with repeated runs.
- `python -X importtime -c "import app"`: slow imports at startup.
- `pytest -q`: behavior is unchanged after the optimization.

## Test first
Lock behavior with a test, then a budget so the regression is caught.
```python
import time
from app.index import build_index

def test_build_index_scales_linearly():
    data = [str(i) for i in range(50_000)]
    t = time.perf_counter()
    idx = build_index(data)
    assert time.perf_counter() - t < 1.0
    assert idx["49999"] == 49999
```
Prefer a benchmark fixture (`pytest-benchmark`) when the repo has it. Time budgets on shared CI are flaky, so keep them generous.

## Do
- Profile with a realistic input and change one thing at a time.
- Fix complexity first: use `set` or `dict` for membership instead of list scans, and `collections.deque` for queues.
- Build strings with `"".join(parts)`, not repeated `+=` in a loop.
- Use generators and `itertools` for large streams, and `__slots__` or dataclasses with `slots=True` for many small objects.
- Hoist invariant work out of loops. Use `functools.lru_cache` for pure functions with bounded inputs.
- Vectorize numeric work with NumPy, or use multiprocessing for CPU-bound pure Python.
- Use `asyncio` or threads only for I/O-bound work.

## Avoid
- Optimizing without a profile: the hot spot is usually elsewhere. Run `cProfile` first.
- `lru_cache` on methods or with unbounded keys: it holds `self` and leaks memory. Cache a module-level function or set `maxsize`.
- Threads for CPU-bound work: the GIL serializes them. Use processes or native code.
- `list(x)[0]` or `len(list(gen))`: it materializes everything. Use `next(iter(x))` or `sum(1 for _ in gen)`.
- `in` against a list inside a loop: O(n squared). Convert to a set once.
- Catching exceptions in a hot loop as control flow when a cheap check exists.

## Review
- [ ] A profile or benchmark shows the before and after numbers.
- [ ] The win comes from algorithm or data structure, not a micro-trick.
- [ ] Tests still pass and edge cases (empty, one item, duplicates) are covered.
- [ ] Caches are bounded and cannot return stale or mutated shared objects.
- [ ] Added complexity is justified by the measured gain.
