---
name: pandera
title: Pandera
area: data
tags: [pandera, dataframes, validation, pandas, polars, data-quality]
detect: [dep:pandera]
related: [parquet-arrow, etl-pipelines, dagster, spark]
---
Pandera: declarative DataFrame schemas that validate columns, types and rules at pipeline boundaries.

## Verify
- `pytest -q tests/test_schemas.py`: schemas accept good frames and reject bad ones.
- `python -c "import schemas; print(schemas.OrderSchema.to_schema())"`: the schema object builds and shows its checks.
- `python -c "import pandera; print(pandera.__version__)"`: confirm installed version before using import paths below.
- `pyright` (or `mypy .`): functions annotated with `DataFrame[Schema]` type-check.

## Test first
Write the failing frame before the schema.
```python
import pandas as pd, pandera as pa, pytest

def test_rejects_negative_amount():
    df = pd.DataFrame({"id": [1], "amount": [-5.0]})
    with pytest.raises(pa.errors.SchemaError):
        OrderSchema.validate(df)
```
Fails until `amount` has `pa.Check.ge(0)`.

## Do
- Define `class OrderSchema(pa.DataFrameModel)` with typed `Series[...]` fields and `pa.Field(...)` constraints (`ge`, `isin`, `unique`, `nullable`).
- Validate at boundaries: right after load and right before write.
- Use `lazy=True` to collect every violation in one `SchemaErrors` and report `failure_cases`.
- Set `strict=True` (or `"filter"`) and `coerce=True` deliberately so unexpected columns and dtypes are handled, not ignored.
- Add dataframe-level checks with `@pa.dataframe_check` for cross-column rules.
- Decorate functions with `@pa.check_types` and annotate `DataFrame[Schema]` for input and output.
- Import from the backend-specific module for Polars (`pandera.polars`) or PySpark (`pandera.pyspark`) when used.
- Keep nullable explicit; default is non-nullable.

## Avoid
- Validating once at the start and never after transforms: later steps corrupt data. Validate outputs too.
- `coerce=True` everywhere: it hides bad inputs by casting them. Coerce known loose types only.
- Old `import pandera as pa; pa.SchemaModel` and `pa.typing` idioms on new versions: use `DataFrameModel` and the current typing path.
- Raising on the first error in batch jobs: you fix one at a time. Use `lazy=True`.
- Skipping `nullable=True` on legitimately missing data, then dropping the check when it fails: model the nulls.
- Schemas without `unique` or key checks: duplicates pass silently. Add them.
- Expensive row-wise `Check(lambda ...)` on huge frames: slow. Use vectorized checks.

## Review
- [ ] Every ingest and output boundary validates against a schema.
- [ ] Schema tests include one bad frame per rule.
- [ ] Strictness and coercion are intentional and documented.
- [ ] Keys and ranges are checked, not just dtypes.
- [ ] Failures are reported with `failure_cases`.
