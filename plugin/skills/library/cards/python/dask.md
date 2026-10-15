---
name: dask
title: Dask
area: python
tags: [python, dask, parallel, dataframe, distributed, big-data]
detect: [dep:dask, dep:distributed, dep:dask-expr]
related: [pandas, numpy, polars, ray, pytest]
---
Dask: lazy partitioned DataFrames, arrays and delayed tasks, scheduled locally or on a distributed cluster.

## Verify
- `python -c "import dask.dataframe as dd; print(dd.from_pandas(__import__('pandas').DataFrame({'a':[1,2]}), npartitions=1).a.sum().compute())"`: Dask runs end to end.
- `pytest -q`: tests with a small `LocalCluster` or the synchronous scheduler.
- `python -c "import dask; dask.config.set(scheduler='synchronous')"` in tests: single-threaded, debuggable, real tracebacks.
- `dask.visualize(obj)` (needs graphviz): the task graph size is sane before you compute.

## Test first
Run on the synchronous scheduler with tiny partitions and compare to pandas.
```python
import dask
import dask.dataframe as dd
import pandas as pd
from pandas.testing import assert_frame_equal
from app.etl import clean

def test_clean_matches_pandas():
    pdf = pd.DataFrame({"k": [1, 1, 2], "v": [1.0, None, 3.0]})
    ddf = dd.from_pandas(pdf, npartitions=2)
    with dask.config.set(scheduler="synchronous"):
        got = clean(ddf).compute().reset_index(drop=True)
    assert_frame_equal(got, clean(pdf).reset_index(drop=True))
```

## Do
- Stay lazy until the end: chain operations, then one `.compute()` (or `dask.compute(a, b)` to share work), or write out with `to_parquet`.
- Read and write Parquet with `dd.read_parquet(path, columns=[...])`: it prunes columns and pushes filters.
- Aim for partitions around 100 MB: adjust with `repartition(partition_size="100MB")`.
- Use `ddf.map_partitions(func, meta=...)` for custom pandas logic and always pass `meta`.
- Use `Client()` from `dask.distributed` for the dashboard and real parallelism. Create it under `if __name__ == "__main__":`.
- Call `.persist()` for data reused several times that fits in cluster memory.
- Set indexes sparingly: `set_index` shuffles. Sort once and save to Parquet.
- Use `dask.delayed` or `client.submit` for non-DataFrame work.

## Avoid
- `.compute()` on large results: pulls everything into one process. Aggregate first or write to disk.
- Calling `len(ddf)` or `.head()` repeatedly: each triggers computation. Compute once and reuse.
- Thousands of tiny partitions: scheduler overhead dominates. Repartition.
- Creating a `Client` at module import with the spawn start method: child processes re-run the module. Guard with `__main__`.
- Closures capturing large objects in tasks: serialized per task. Use `client.scatter` or load data inside the task.
- Omitting `meta`: Dask runs your function on fake data to guess types and can error or mis-type.
- Assuming pandas semantics for `iloc` row indexing and row order: partitions have no global positions.

## Review
- [ ] One compute per pipeline and outputs written lazily.
- [ ] Partition sizes are measured, not default.
- [ ] `meta` is declared for custom functions.
- [ ] Tests use the synchronous scheduler and compare with pandas.
