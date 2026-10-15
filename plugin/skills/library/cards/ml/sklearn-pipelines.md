---
name: sklearn-pipelines
title: scikit-learn pipelines
area: ml
tags: [sklearn, pipeline, columntransformer, cross-validation, leakage, preprocessing]
detect: [dep:scikit-learn]
related: [scikit-learn, optuna, shap, lightgbm, xgboost]
---
Bundle preprocessing and model into one Pipeline with a ColumnTransformer so cross-validation never leaks and the artefact is a single object.

## Verify
- `pytest -q tests/test_pipeline.py`: fit, predict and serialise round trip pass on a toy frame.
- `python -m evals.cv --folds 5`: cross-validated score with the full pipeline inside each fold.
- `python -c "import joblib; joblib.load('model.joblib').predict(sample)"`: the saved artefact predicts on raw input columns.

## Test first
```python
import pandas as pd
from app.model import build_pipeline

def test_unseen_category_and_missing_value_do_not_crash():
    X = pd.DataFrame({"age": [1.0, None, 3.0, 4.0], "city": ["a", "b", "a", "b"]})
    pipe = build_pipeline().fit(X, [0, 1, 0, 1])
    out = pipe.predict(pd.DataFrame({"age": [None], "city": ["zzz"]}))
    assert len(out) == 1
```

## Do
- Put imputers, scalers, encoders and the estimator in `Pipeline`; route columns with `ColumnTransformer` by name.
- Use `OneHotEncoder(handle_unknown="ignore")` and `SimpleImputer` per column group; pass `set_output(transform="pandas")` when column names matter.
- Cross-validate and tune the whole pipeline (`GridSearchCV` or `cross_val_score` on the pipeline), with parameters named `step__param`.
- Choose the splitter to fit the data: `StratifiedKFold` for imbalance, `GroupKFold` for grouped rows, `TimeSeriesSplit` for time.
- Fix `random_state` on estimators and splitters; pick the metric to match the objective, not the default.
- Write custom steps as `BaseEstimator` and `TransformerMixin` classes with `fit` learning only from training data.
- Persist the whole pipeline with `joblib` along with library versions; load only trusted files.
- Keep the holdout test set untouched until the final check.

## Avoid
- Fitting a scaler or imputer on all data before splitting: leakage. Put it in the pipeline.
- Target encoding or feature selection outside the CV loop: optimistic scores. Move inside.
- Random splits on grouped rows (same user or patient): leakage. Use groups.
- Default accuracy on imbalanced data: misleading. Use precision, recall, PR-AUC or a cost metric.
- Pickles from untrusted sources: arbitrary code execution. Load only your own.
- Dropping column order assumptions: pass named DataFrames and test with shuffled columns.

## Review
- [ ] All preprocessing lives inside the pipeline.
- [ ] Splitter matches data structure.
- [ ] Metric matches the goal; seeds fixed.
- [ ] Artefact predicts from raw input and has version metadata.
- [ ] Test set untouched until the end.
