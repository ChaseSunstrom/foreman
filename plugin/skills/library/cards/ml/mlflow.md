---
name: mlflow
title: MLflow
area: ml
tags: [python, experiment-tracking, model-registry, mlops, artifacts, mlflow]
detect: [dep:mlflow, dep:mlflow-skinny, file:MLproject]
related: [wandb, scikit-learn, pytorch, onnx]
---
MLflow tracking and registry: runs with params, metrics and artifacts, logged models, and registered versions with aliases.

## Verify
- `python -c "import mlflow; print(mlflow.__version__)"`: installed version.
- `pytest -q`: training code logs the expected params and metrics to a temp store.
- `mlflow ui --backend-store-uri ./mlruns`: the UI starts against a local store (stop it after checking).
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Point tracking at a temp directory and assert what the run recorded.
```python
import mlflow
from mypkg.train import train

def test_run_logs_params_and_metric(tmp_path):
    mlflow.set_tracking_uri(f"file://{tmp_path}")
    mlflow.set_experiment("t")
    train(lr=0.1, epochs=2)
    run = mlflow.search_runs(output_format="list")[0]
    assert run.data.params["lr"] == "0.1"
    assert "val_loss" in run.data.metrics
```

## Do
- Set `MLFLOW_TRACKING_URI` (or `mlflow.set_tracking_uri`) explicitly and name the experiment.
- Wrap training in `with mlflow.start_run():`. Log params once, metrics with `step=`, and artifacts such as plots and configs.
- Log the git commit, data version and dependency file as tags or artifacts.
- Log models with the flavor function (`mlflow.sklearn.log_model`, `mlflow.pytorch.log_model`) and include an input example, so a signature is inferred.
- Register with `mlflow.register_model` and promote through aliases rather than stage names.
- Use autolog (`mlflow.sklearn.autolog()`) for quick coverage, and check what it logs.
- Load for serving through `mlflow.pyfunc.load_model("models:/name@alias")`.
- Put the tracking server behind authentication.

## Avoid
- Relying on the default local `./mlruns` in shared or CI environments: runs scatter. Set the tracking URI.
- Nested or leaked runs from forgetting to end them: metrics land in the wrong run. Use the context manager.
- Logging metrics without `step`: you get one point and no curve. Pass the step.
- Registry stages (`Staging`, `Production`) in new code: deprecated. Use model version aliases and tags.
- Logging models with no signature or input example: serving breaks on bad input. Provide one.
- Logging secrets as params: visible to everyone with UI access. Keep them out.
- `mlflow ui` or the server exposed without auth on a public host.

## Review
- [ ] Tracking URI and experiment are explicit.
- [ ] Runs log params, stepped metrics, code version and data version.
- [ ] Models carry signature and input example and are registered with aliases.
- [ ] No secrets in params or tags.
- [ ] Tests assert logged values against a temp store.
