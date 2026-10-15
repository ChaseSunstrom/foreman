---
name: pandas
title: pandas
area: python
tags: [python, dataframe, pandas, data, analysis, vectorization]
detect: [dep:pandas]
related: [numpy, polars, pytest, jupyter, hypothesis]
---
pandas DataFrames: vectorized transforms, indexing, dtypes, groupby, merges and I/O.

## Verify
- `python -c "import pandas as pd; print(pd.__version__)"`: the major version (2.x differs from 1.x on copy and dtype behavior).
- `python -W error::FutureWarning -m pytest -q`: upcoming-behavior changes fail the suite now.
- `python -c "import pandas as pd; pd.options.mode.copy_on_write = True"` in tests: code works under copy-on-write semantics.
- `pytest -q`: the suite with `pandas.testing` assertions.

## Test first
Compare frames with `pandas.testing`, never `==`.
```python
import pandas as pd
from pandas.testing import assert_frame_equal
from app.etl import add_total

def test_add_total():
    df = pd.DataFrame({"q": [1, 2], "p": [10.0, 5.0]})
    out = add_total(df)
    assert_frame_equal(out, df.assign(total=[10.0, 10.0]))
    assert "total" not in df.columns  # input untouched
```

## Do
- Vectorize: column arithmetic, `.str.*`, `.dt.*`, `np.where`, `.map` on a Series. Loop only as a last resort.
- Select with `.loc[rows, cols]` and `.iloc`; assign with `.loc` or `df.assign(...)`.
- Chain steps with `.pipe`, `.assign`, `.query` to keep functions pure and returning new frames.
- Set dtypes on read: `read_csv(..., dtype=..., parse_dates=[...], usecols=[...])`; use `category` for low-cardinality strings and nullable dtypes (`Int64`, `string`) for missing values.
- Use `groupby(...).agg(name=("col", "sum"))` with named aggregation.
- Validate merges: `merge(..., validate="one_to_one", indicator=True)`.
- Read big files with `chunksize=` or switch to Parquet (`read_parquet`).

## Avoid
- `df[df.a > 1]["b"] = 0` (chained assignment): writes to a copy or warns. Use `df.loc[df.a > 1, "b"] = 0`.
- `DataFrame.append` and `iteritems`: removed in 2.x. Use `pd.concat` and `items`.
- `iterrows()` and `apply(axis=1)` for math: orders of magnitude slower. Vectorize.
- `inplace=True`: no speed gain and blocks chaining. Reassign.
- Comparing floats or frames with `==`: use `assert_frame_equal` with tolerances.
- Growing a frame in a loop (`concat` each pass): quadratic. Collect rows in a list and build once.
- `.values` where `.to_numpy()` is meant: unclear dtype and copy behavior.

## Review
- [ ] Transforms are vectorized and return new frames without mutating inputs.
- [ ] Dtypes and parse options are explicit at read time.
- [ ] Merges state a `validate=` cardinality and handle unmatched keys.
- [ ] No chained assignment, `inplace`, or removed APIs.
- [ ] Tests use `pandas.testing` and cover empty and NaN-bearing frames.
