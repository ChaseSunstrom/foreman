---
name: optuna
title: Optuna
area: ml
tags: [optuna, hyperparameters, tuning, pruning, studies, reproducibility]
detect: [dep:optuna]
related: [sklearn-pipelines, lightgbm, xgboost, pytorch, wandb]
---
Hyperparameter search with Optuna: a cross-validated objective, sensible search spaces, pruning, persistent studies and a final untouched test.

## Verify
- `pytest -q tests/test_objective.py`: the objective runs for 2 trials on tiny data and returns a finite float.
- `python tune.py --n-trials 5`: a smoke study completes and prints the best params.
- `optuna-dashboard sqlite:///study.db`: trials and importances are inspectable (when the dashboard is installed).

## Test first
```python
import optuna
from app.tune import objective

def test_objective_returns_finite_score():
    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=0))
    study.optimize(objective, n_trials=2)
    assert all(t.value is not None and t.value == t.value for t in study.trials)
```

## Do
- Define the space inside `objective(trial)` with `suggest_float(..., log=True)` for rates and regularisation, `suggest_int` and `suggest_categorical` otherwise.
- Score with cross-validation or a dedicated validation split; never with the final test set.
- Set `direction` to match the metric and seed the sampler for reproducible searches.
- Store studies with `storage="sqlite:///study.db"` and `load_if_exists=True` so runs resume and parallel workers share one study.
- Prune with a pruner (`MedianPruner`) and `trial.report(value, step)` plus `trial.should_prune()` inside training loops.
- Narrow ranges after a first pass using importances and the best region.
- Retrain the best configuration on the full training data and score once on the test set.
- Record the best params, study name and package versions with the model.

## Avoid
- Tuning against the test set: the reported score is optimistic. Hold it out.
- Linear scale for learning rate or regularisation: wasted trials. Use `log=True`.
- Non-deterministic objectives without fixed seeds: noisy comparisons. Seed models and splits.
- Search spaces with conditional params defined outside the trial: errors. Branch inside `objective`.
- Unlimited `n_trials` with no `timeout`: unbounded compute. Set both.
- Reporting the study's best value as expected performance: it is selection-biased. Confirm on held-out data.

## Review
- [ ] Objective uses validation data only.
- [ ] Log scale for rates; ranges justified.
- [ ] Study stored; resume works.
- [ ] Pruning used for iterative models.
- [ ] Final score from an untouched test set.
