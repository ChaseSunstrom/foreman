---
name: polars
title: Polars
area: python
tags: [python, dataframe, polars, lazy, expressions, parquet]
detect: [dep:polars, dep:polars-lts-cpu]
related: [pandas, numpy, pytest, jupyter]
---
Polars DataFrames: expression API, lazy queries (`scan_*`, `collect`), strict dtypes, Parquet-first I/O.

## Verify
- `python -c "import polars as pl; print(pl.__version__)"`: the installed version, since method names changed across 0.x and 1.x.
- `pytest -q`: the suite using `polars.testing`.
- `python -c "import app.q as q; print(q.build().explain())"`: the lazy plan shows pushdowns (filters and projections near the scan).
- `python -W error::DeprecationWarning -m pytest -q`: renamed or deprecated methods fail now.

## Test first
Compare with `polars.testing.assert_frame_equal`.
```python
import polars as pl
from polars.testing import assert_frame_equal
from app.etl import add_total

def test_add_total():
    df = pl.DataFrame({"q": [1, 2], "p": [10.0, 5.0]})
    expected = df.with_columns(total=pl.col("q") * pl.col("p"))
    assert_frame_equal(add_total(df), expected)
```

## Do
- Write transforms as expressions: `df.with_columns(...)`, `.filter(pl.col("a") > 1)`, `.select(...)`, `.group_by("k").agg(...)`.
- Use `pl.scan_parquet`/`scan_csv` and `.collect()` at the end so the optimizer can push filters down; use `.collect(engine="streaming")` for larger-than-memory work where supported.
- Prefer Parquet or IPC for storage; pass `schema=` or `schema_overrides=` when reading CSV.
- Use `pl.when(...).then(...).otherwise(...)` for conditionals.
- Use window expressions (`.over("k")`) instead of join-backs.
- Name outputs with `.alias()` or keyword args to keep schemas explicit.
- Check schemas in tests with `df.schema` so dtype drift fails.

## Avoid
- `pandas` idioms: `df["c"] = ...`, `df[mask]`, index alignment, `inplace`. There is no index; use `with_columns` and `filter`.
- `groupby` and `apply` with Python lambdas: renamed to `group_by`, and `map_elements` runs row-by-row without vectorization. Use expressions.
- `collect()` early then continuing eagerly: loses pushdown. Stay lazy.
- Relying on implicit casts: integer-float mixing raises. Cast with `.cast(pl.Float64)`.
- Iterating with `for row in df.iter_rows()` for math: slow. Express it as a column operation.
- `df.to_pandas()` in the middle of a pipeline just to finish the job: round-trips copy data. Stay in Polars and convert only at an interface.
- Assuming stable row order after `group_by`: pass `maintain_order=True` or sort.

## Review
- [ ] Transformations are expressions and lazy until the final `collect`.
- [ ] Schemas and dtypes are explicit at read and checked in tests.
- [ ] No `map_elements` where a native expression exists.
- [ ] Order-dependent results sort or set `maintain_order`.
- [ ] No deprecated names for the pinned Polars version.
