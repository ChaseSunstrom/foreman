---
name: statsmodels
title: statsmodels
area: ml
tags: [statsmodels, regression, statistics, inference, arima, diagnostics]
detect: [dep:statsmodels]
related: [time-series-forecasting, scikit-learn, shap, sklearn-pipelines]
---
Statistical modelling with statsmodels: explicit design matrices, residual diagnostics, correct standard errors and honest interpretation.

## Verify
- `pytest -q tests/test_models.py`: fits on synthetic data recover known coefficients within tolerance.
- `python -m tools.diagnostics`: residual, heteroskedasticity and multicollinearity checks are printed.
- `python -c "import statsmodels.api as sm; print(sm.__version__)"`: the version used for the reported numbers.

## Test first
Recover known parameters from simulated data.
```python
import numpy as np
import statsmodels.api as sm

def test_ols_recovers_slope():
    rng = np.random.RandomState(0)
    x = rng.normal(size=500)
    y = 2.0 + 3.0 * x + rng.normal(scale=0.5, size=500)
    res = sm.OLS(y, sm.add_constant(x)).fit()
    assert abs(res.params[1] - 3.0) < 0.1
```

## Do
- Add an intercept explicitly with `sm.add_constant`, or use the formula API (`smf.ols("y ~ x1 + C(g)", data=df)`) which adds it.
- Inspect `res.summary()`, then residual plots, Q-Q plots, and tests for heteroskedasticity and autocorrelation.
- Use robust covariance (`cov_type="HC3"`, or `cluster` with groups) when assumptions fail or rows are clustered.
- Pick the family and link for the outcome in `GLM` (binomial, Poisson, negative binomial); check overdispersion.
- Check multicollinearity with variance inflation factors and condition number.
- For time series, test stationarity (ADF), inspect ACF and PACF, and compare ARIMA or SARIMAX orders by out-of-sample error as well as AIC.
- Report confidence intervals and effect sizes, not only p-values; correct for multiple comparisons.
- Use `res.get_prediction(...).summary_frame()` for prediction intervals.

## Avoid
- Forgetting the constant: forces the line through the origin and biases results. Add it.
- Interpreting p-values after trying many specifications: inflated. Pre-specify or correct.
- Ignoring non-constant variance or clustering: standard errors too small. Use robust or clustered errors.
- Passing `(X, y)` in the wrong order: statsmodels takes endog first, then exog.
- Treating coefficients as causal: associations only. State assumptions.
- Choosing ARIMA orders by AIC alone on a short series: overfit. Backtest.
- Dropping rows with missing values silently: set `missing="raise"` or handle explicitly.

## Review
- [ ] Intercept and design matrix are explicit.
- [ ] Diagnostics run and assumptions addressed.
- [ ] Standard errors suit the data structure.
- [ ] Intervals and effect sizes reported.
- [ ] Versions and specification recorded.
