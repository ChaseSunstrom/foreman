---
name: shap
title: SHAP explanations
area: ml
tags: [shap, explainability, feature-importance, interpretability, trees, attribution]
detect: [dep:shap]
related: [sklearn-pipelines, xgboost, lightgbm, model-cards, scikit-learn]
---
Explain model predictions with SHAP: choose the right explainer, a sound background set, and treat attributions as model behaviour, not causation.

## Verify
- `pytest -q tests/test_explain.py`: additivity holds and shapes match the data.
- `python -m tools.explain --sample 500`: summary values computed on a held-out sample with a fixed seed.
- `python -c "import shap; print(shap.__version__)"`: the version in use, recorded with results.

## Test first
Check additivity: base value plus attributions equals the model output.
```python
import numpy as np
import shap

def test_shap_values_sum_to_prediction(model, X):
    ex = shap.TreeExplainer(model)
    sv = ex.shap_values(X)
    pred = model.predict(X)
    np.testing.assert_allclose(np.asarray(sv).sum(axis=1) + ex.expected_value, pred, atol=1e-3)
```

## Do
- Use `TreeExplainer` for tree ensembles, `LinearExplainer` for linear models, `DeepExplainer` or `GradientExplainer` for networks, and the generic `Explainer` with a masker otherwise.
- Be explicit about the output explained (log-odds versus probability, class index) and state it on plots.
- Use a representative background sample (tens to a few hundred rows via `shap.sample` or k-means) for model-agnostic methods.
- Explain a held-out sample, and subsample large sets with a seed; cache the values.
- Pass the preprocessed matrix the model actually sees; map transformed column names back to originals.
- Check consistency: global mean absolute SHAP versus permutation importance.
- Read local plots for individual decisions and summary or dependence plots for global behaviour.
- Pin the shap and model library versions together.

## Avoid
- Reading SHAP values as causal effects: they describe the model. Use causal methods for interventions.
- Confusing log-odds and probability scales: misread magnitudes. Label the scale.
- A biased or tiny background set in model-agnostic explainers: distorted baselines. Use a representative sample.
- Explaining the training data only: shows fit, not generalisation. Use held-out data.
- Correlated features splitting credit arbitrarily: group them or say so.
- Computing KernelExplainer on thousands of rows: very slow. Subsample or use a specific explainer.

## Review
- [ ] Explainer matches the model type.
- [ ] Output scale and class stated.
- [ ] Background and sample sizes documented.
- [ ] Additivity check in tests.
- [ ] Claims avoid causal language.
