---
name: lightgbm
title: LightGBM
area: ml
tags: [python, gradient-boosting, tabular, trees, early-stopping, lgbm]
detect: [dep:lightgbm]
related: [xgboost, scikit-learn, mlflow]
---
LightGBM leaf-wise gradient boosting: sklearn API or Dataset and train, callbacks for early stopping, categorical features.

## Verify
- `python -c "import lightgbm as lgb; print(lgb.__version__)"`: installed version.
- `pytest -q`: training and prediction tests pass.
- `python -W error::FutureWarning -m pytest -q`: no deprecated usage.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Train a small model, assert accuracy above baseline, and round-trip the saved booster.
```python
import numpy as np, lightgbm as lgb
from sklearn.datasets import make_classification

def test_learns_and_roundtrips(tmp_path):
    X, y = make_classification(400, 8, random_state=0)
    m = lgb.LGBMClassifier(n_estimators=40, num_leaves=7, random_state=0, verbose=-1).fit(X, y)
    assert (m.predict(X) == y).mean() > 0.85
    m.booster_.save_model(str(tmp_path / "m.txt"))
    b = lgb.Booster(model_file=str(tmp_path / "m.txt"))
    assert np.allclose(b.predict(X), m.predict_proba(X)[:, 1])
```

## Do
- Use callbacks for early stopping: `callbacks=[lgb.early_stopping(50), lgb.log_evaluation(50)]`, with `eval_set` or `valid_sets`.
- Control complexity with `num_leaves`, `min_child_samples` and `max_depth` together. `num_leaves` should stay below `2**max_depth`.
- Pass categorical columns as pandas `category` dtype or `categorical_feature`. Keep category codes consistent between train and predict.
- Set `random_state` and `deterministic=True` where repeatable runs matter.
- Handle imbalance with `is_unbalance`, `scale_pos_weight` or sample weights, and judge with PR AUC.
- Use `Dataset(..., reference=train_set)` for validation sets so bin boundaries match.
- Save with `save_model` and load with `Booster(model_file=...)`.

## Avoid
- `early_stopping_rounds` and `verbose_eval` arguments to `fit` or `train`: removed in newer releases. Use the callbacks.
- Large `num_leaves` on small data: overfits fast. Raise `min_child_samples` and lower `num_leaves`.
- Early stopping against the test set: leakage. Hold out a validation split.
- Label-encoding categoricals as plain integers without declaring them: treated as numeric. Declare the category dtype.
- Feature names with special JSON characters: errors on training. Sanitize column names.
- Validation `Dataset` built without `reference`: bins mismatch. Pass `reference`.
- Comparing `predict` raw scores to probabilities: apply the sigmoid or use `predict_proba`.

## Review
- [ ] Early stopping uses callbacks and a separate validation set.
- [ ] `num_leaves` and `min_child_samples` fit the data size.
- [ ] Categorical handling is identical in training and serving.
- [ ] Seeds and determinism flags are set where needed.
- [ ] Saved model reload is tested.
