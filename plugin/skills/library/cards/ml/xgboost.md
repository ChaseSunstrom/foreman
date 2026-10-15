---
name: xgboost
title: XGBoost
area: ml
tags: [python, gradient-boosting, tabular, trees, early-stopping, xgb]
detect: [dep:xgboost]
related: [lightgbm, scikit-learn, mlflow]
---
XGBoost gradient-boosted trees: sklearn-style estimators or native DMatrix training, early stopping, and model persistence.

## Verify
- `python -c "import xgboost as xgb; print(xgb.__version__)"`: installed version.
- `pytest -q`: training smoke and prediction tests pass.
- `python -W error::FutureWarning -m pytest -q`: no deprecated parameters are used.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Train a small model on a fixture, assert the metric beats a baseline and a save and load round trip.
```python
import numpy as np, xgboost as xgb
from sklearn.datasets import make_classification

def test_learns_and_roundtrips(tmp_path):
    X, y = make_classification(300, 8, random_state=0)
    m = xgb.XGBClassifier(n_estimators=30, max_depth=3, random_state=0).fit(X, y)
    assert (m.predict(X) == y).mean() > 0.85
    m.save_model(tmp_path / "m.json")
    m2 = xgb.XGBClassifier(); m2.load_model(tmp_path / "m.json")
    assert np.allclose(m.predict_proba(X), m2.predict_proba(X))
```

## Do
- Pass `early_stopping_rounds` to the estimator constructor, with a separate validation set in `fit(eval_set=[(Xv, yv)])`.
- Set `eval_metric` explicitly and keep `learning_rate` low with a higher `n_estimators` ceiling.
- Use `tree_method="hist"` and `device="cuda"` for GPU training.
- Handle imbalance with `scale_pos_weight` or sample weights, and evaluate with PR AUC.
- Save with `save_model("m.json")` (the JSON format) and load with `load_model`.
- Use `enable_categorical=True` with pandas category dtype instead of hand-coding integers.
- Check `feature_importances_` against domain sense, and use SHAP for attribution.

## Avoid
- Passing `early_stopping_rounds` to `fit()`: removed in recent versions. Set it on the constructor.
- Early stopping against the test set: it leaks. Hold out a separate validation split.
- `gpu_hist` or `gpu_id` parameters: deprecated. Use `tree_method="hist"` with `device="cuda"`.
- Saving with pickle across versions: breaks. Use the JSON or UBJSON model files.
- Relying on default `max_depth` and `n_estimators` without tuning: over or underfits. Tune with CV.
- One-hot encoding high-cardinality columns blindly: wide sparse input. Use native categorical support.
- Using `predict` (class labels) to compute AUC: use `predict_proba`.

## Review
- [ ] Early stopping uses a validation set separate from the test set.
- [ ] `eval_metric`, imbalance handling and seeds are explicit.
- [ ] Model is saved in JSON and the reload round trip is tested.
- [ ] No removed or deprecated parameters are in use.
- [ ] Features at inference match training columns and order.
