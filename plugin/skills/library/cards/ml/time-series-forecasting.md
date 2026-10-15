---
name: time-series-forecasting
title: Time-series forecasting
area: ml
tags: [forecasting, time-series, backtesting, leakage, baselines, prophet]
detect: [dep:prophet, dep:sktime, dep:darts, dep:statsforecast, dep:neuralforecast]
related: [statsmodels, scikit-learn, sklearn-pipelines, optuna, llm-evals]
---
Forecast with time-aware splits, naive baselines and rolling-origin backtests so a model has to earn its place.

## Verify
- `pytest -q tests/test_features.py`: lag and rolling features use only past data.
- `python -m evals.backtest --folds 5`: rolling-origin errors (MAE, MASE or sMAPE) per horizon beat the seasonal-naive baseline.
- `python -m evals.coverage`: prediction interval coverage is near its nominal level.

## Test first
Prove a feature cannot see the future.
```python
import pandas as pd
from app.features import add_lags

def test_lag_feature_uses_only_past():
    s = pd.DataFrame({"y": [1, 2, 3, 4]})
    out = add_lags(s, lags=[1])
    assert out["y_lag1"].tolist()[1:] == [1, 2, 3] and pd.isna(out["y_lag1"].iloc[0])
```

## Do
- Compute naive, seasonal-naive and moving-average baselines first; report skill against them.
- Split by time only; backtest with an expanding or sliding window and the real forecast horizon.
- Build features with `shift` so every value is known at forecast time; document the information cutoff.
- Handle the calendar: regular frequency, missing timestamps, time zones, DST, holidays and known future regressors.
- Use scale-free metrics (MASE, sMAPE) for comparing series; log the metric per horizon step.
- Produce prediction intervals and check empirical coverage.
- For many series, fit a global model with series ids and compare it to per-series models.
- Refit on all data after validation and monitor error drift in production.

## Avoid
- Random `train_test_split` or shuffled k-fold: future leaks into training. Use time splits.
- Scaling or imputing on the full series before splitting: leakage. Fit transforms on training folds only.
- Rolling features computed with centred windows: they see the future. Use trailing windows.
- Judging by one holdout period: an easy period misleads. Use multiple origins.
- MAPE with zeros or tiny values: infinite or distorted. Use MASE or MAE.
- Using actual future covariates not available at forecast time: use forecasts of them or exclude.

## Review
- [ ] Baselines beaten on a multi-fold backtest.
- [ ] No feature or transform sees data after the cutoff.
- [ ] Metric suits the data (zeros, scales).
- [ ] Intervals checked for coverage.
- [ ] Frequency, gaps and time zones handled.
