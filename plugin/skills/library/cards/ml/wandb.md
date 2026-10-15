---
name: wandb
title: Weights and Biases
area: ml
tags: [python, experiment-tracking, mlops, sweeps, artifacts, wandb]
detect: [dep:wandb, file:wandb/settings, file:sweep.yaml]
related: [mlflow, pytorch, lightning, transformers]
---
Weights and Biases tracking: runs with config and logged metrics, artifacts for datasets and models, and sweeps.

## Verify
- `python -c "import wandb; print(wandb.__version__)"`: installed version.
- `WANDB_MODE=offline pytest -q`: tests run without network or an account.
- `wandb sync --help`: the CLI is present, for uploading offline runs later.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Run in `disabled` mode and assert the code path logs what you expect, via an injected logger.
```python
import wandb
from mypkg.train import fit

def test_fit_logs_loss_each_epoch(monkeypatch):
    logged = []
    monkeypatch.setattr(wandb, "log", lambda d, **k: logged.append(d))
    run = wandb.init(mode="disabled", config={"lr": 0.1})
    fit(epochs=3, config=run.config)
    run.finish()
    assert len(logged) == 3 and all("loss" in d for d in logged)
```

## Do
- Call `wandb.init(project=..., config={...})` once, and read hyperparameters back from `wandb.config`.
- Authenticate through `WANDB_API_KEY` in the environment, never in code.
- Log dicts with `wandb.log({...}, step=...)` and set `wandb.define_metric` for custom x-axes and summaries.
- Version datasets and checkpoints as `wandb.Artifact`, log them with `run.log_artifact`, and consume with `run.use_artifact`.
- Finish runs explicitly with `run.finish()` or use the context manager, especially in notebooks and tests.
- Write sweeps as a YAML or dict with `method`, `metric` and `parameters`, and launch agents with `wandb.agent` or `wandb sweep`.
- Use `WANDB_MODE=offline` or `disabled` in CI.
- Log git state and the config file for reproducibility.

## Avoid
- `wandb.init` inside a training loop or per epoch: creates many runs. Init once.
- Hard-coding hyperparameters while a sweep controls them: the sweep has no effect. Read from `wandb.config`.
- Committing the API key or `wandb login` output: leaked credential. Use the environment variable.
- Logging large tensors or images every step: slow and costly. Log samples at intervals and use `wandb.Image`.
- Unfinished runs in notebooks and tests: runs stay open. Call `finish`.
- Mixing `step` values out of order: points are dropped. Keep steps monotonic or use `define_metric`.
- Network-dependent tests: flaky CI. Use offline or disabled mode.

## Review
- [ ] One run per training job, config read from `wandb.config`.
- [ ] Key comes from the environment and is not logged.
- [ ] Datasets and checkpoints are artifacts with lineage.
- [ ] Steps are monotonic and logging frequency is reasonable.
- [ ] CI uses offline or disabled mode.
