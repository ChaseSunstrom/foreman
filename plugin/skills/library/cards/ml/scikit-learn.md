---
name: scikit-learn
title: scikit-learn
area: ml
tags: [python, machine-learning, pipelines, cross-validation, metrics, sklearn]
detect: [dep:scikit-learn]
related: [xgboost, lightgbm, mlflow, pytorch]
---
scikit-learn: estimators, Pipeline and ColumnTransformer, cross-validation, metrics, and leakage-free evaluation.

## Verify
- `python -c "import sklearn; sklearn.show_versions()"`: installed versions of sklearn and its numeric stack.
- `pytest -q`: pipeline and metric tests pass.
- `python -W error::FutureWarning -m pytest -q`: no deprecated sklearn APIs are in use.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Fit the full pipeline on a tiny fixture and assert the score floor and that it round-trips.
```python
import numpy as np, joblib
from sklearn.datasets import make_classification
from mypkg.model import make_pipeline

def test_pipeline_learns_and_roundtrips(tmp_path):
    X, y = make_classification(200, 6, random_state=0)
    p = make_pipeline().fit(X, y)
    assert p.score(X, y) > 0.8
    joblib.dump(p, tmp_path / "m.pkl")
    assert np.array_equal(joblib.load(tmp_path / "m.pkl").predict(X), p.predict(X))
```

## Do
- Put every preprocessing step in a `Pipeline` or `ColumnTransformer` so fitting happens only on the training fold.
- Use `train_test_split(..., stratify=y, random_state=...)` for classification and set `random_state` on every stochastic estimator.
- Choose the CV splitter to match the data: `StratifiedKFold`, `GroupKFold` for grouped rows, `TimeSeriesSplit` for time.
- Tune with `GridSearchCV` or `RandomizedSearchCV` over the whole pipeline using `step__param` names, with an explicit `scoring`.
- Use `OneHotEncoder(handle_unknown="ignore")` for categoricals seen at inference.
- Report metrics suited to the task: PR AUC or F1 for imbalance, not accuracy alone.
- Persist with `joblib` and record the sklearn version beside the file.

## Avoid
- `fit_transform` on the full dataset before splitting: leakage inflates scores. Fit inside a pipeline.
- Scaling or imputing on test data separately: mismatched statistics. Use the fitted transformer's `transform`.
- Random `KFold` on grouped or time-ordered rows: leakage. Use `GroupKFold` or `TimeSeriesSplit`.
- `fit_transform` on the test set, or `fit` on the validation set used for selection: optimistic results. Keep a final untouched test set.
- Loading pickles from untrusted sources: arbitrary code execution. Only load your own artifacts.
- Reading `accuracy_score` on imbalanced classes: a majority-class model looks good. Use `classification_report` and PR metrics.
- Calling `predict_proba` outputs calibrated without checking: use `CalibratedClassifierCV` and a reliability check.

## Review
- [ ] All fitted preprocessing lives inside the pipeline.
- [ ] The CV splitter matches grouping and time structure.
- [ ] Metric fits the class balance and the business cost.
- [ ] `random_state` is set where results must repeat.
- [ ] A final held-out set was scored once.
