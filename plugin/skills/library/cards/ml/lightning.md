---
name: lightning
title: PyTorch Lightning
area: ml
tags: [python, deep-learning, training, trainer, pytorch, callbacks]
detect: [dep:lightning, dep:pytorch-lightning]
related: [pytorch, mlflow, wandb, cuda]
---
Lightning training: a LightningModule holds model, step logic and optimizers, and the Trainer owns the loop, devices and checkpoints.

## Verify
- `python train.py --fast_dev_run`: one train, val and test batch run end to end (if the script exposes Trainer flags).
- `pytest -q`: module and datamodule tests pass.
- `python -c "import lightning; print(lightning.__version__)"`: which package namespace is installed.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Run the Trainer on a tiny batch with `fast_dev_run` or `overfit_batches`.
```python
import lightning as L
from mypkg.module import LitNet
from mypkg.data import ToyData

def test_one_batch_trains():
    trainer = L.Trainer(fast_dev_run=True, accelerator="cpu", logger=False)
    trainer.fit(LitNet(), datamodule=ToyData())
    assert trainer.callback_metrics["train_loss"].isfinite()
```

## Do
- Put loss in `training_step` and return it or a dict with `"loss"`. Never call `backward()` or `optimizer.step()` there unless using manual optimization.
- Log with `self.log("val_loss", v, prog_bar=True)`. Set `sync_dist=True` when training on several devices.
- Use a `LightningDataModule` for splits and transforms. Download in `prepare_data`, assign datasets in `setup`.
- Do not call `.cuda()` or `.to(device)` inside the module. Use `self.device` or `type_as` when a tensor must be created.
- Configure `ModelCheckpoint(monitor=..., mode=...)` and `EarlyStopping` with the exact logged metric name.
- Set `precision="bf16-mixed"` rather than hand-rolling autocast.
- Call `self.save_hyperparameters()` in `__init__` so checkpoints reload with `load_from_checkpoint`.

## Avoid
- Mixing `import pytorch_lightning` and `import lightning` in one project: classes come from different packages and callbacks do not match. Pick one.
- Calling `model.eval()` or `zero_grad` by hand: the Trainer does it. Remove them.
- Checkpoint `monitor` naming a metric that is never logged: the callback fails or never saves. Log the key in `validation_step`.
- Logging in `training_step` without `on_epoch=True` and expecting epoch averages: defaults are per step. Set the flag.
- Heavy work in `__init__` of the module or datamodule: it runs on every process. Move it to `setup`.
- Seeding only with `torch.manual_seed`: workers differ. Use `L.seed_everything(seed, workers=True)`.

## Review
- [ ] `fast_dev_run` passes in CI on CPU.
- [ ] Every monitored metric name is logged exactly.
- [ ] No device moves or `.cuda()` calls inside the module.
- [ ] Hyperparameters are saved and a checkpoint reload is tested.
- [ ] Distributed logging uses `sync_dist` where the metric is a mean.
