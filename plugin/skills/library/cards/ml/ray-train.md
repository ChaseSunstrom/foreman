---
name: ray-train
title: Ray Train
area: ml
tags: [ray, distributed-training, pytorch, checkpoints, scaling, cluster]
detect: [dep:ray]
related: [distributed-training, pytorch, lightning, optuna, wandb]
---
Scale PyTorch training with Ray Train: a per-worker loop, ScalingConfig, reported checkpoints and fault-tolerant restarts.

## Verify
- `pytest -q tests/test_train_loop.py`: the loop runs on CPU with 1 or 2 workers and a tiny dataset.
- `python train.py --num-workers 2 --epochs 1`: end to end on a small cluster or local Ray.
- `python -c "import ray; ray.init(); print(ray.cluster_resources())"`: resources the scheduler can see.

## Test first
```python
from ray.train import ScalingConfig
from ray.train.torch import TorchTrainer
from app.train import train_loop

def test_two_worker_run_reports_loss():
    t = TorchTrainer(train_loop, train_loop_config={"epochs": 1, "tiny": True},
                     scaling_config=ScalingConfig(num_workers=2, use_gpu=False))
    assert "loss" in t.fit().metrics
```

## Do
- Write the per-worker loop as `train_loop_per_worker(config)` and wrap the model and loader with `ray.train.torch.prepare_model` and `prepare_data_loader`.
- Set `ScalingConfig(num_workers=..., use_gpu=...)` and per-worker resources explicitly.
- Report metrics and checkpoints together with `ray.train.report(metrics, checkpoint=...)` each epoch.
- Configure `RunConfig` with a storage path on shared storage and `FailureConfig(max_failures=...)` for restarts.
- Resume by reading `ray.train.get_checkpoint()` at loop start; restore model, optimiser and epoch.
- Shard data with Ray Data or a distributed sampler; seed per worker.
- Keep the loop importable and the config serialisable; log from rank 0 only.
- Check the installed Ray version's docs, since module paths changed across releases.

## Avoid
- Saving checkpoints to the worker's local disk: lost on failure. Use shared or cloud storage.
- Forgetting to call `report` with the checkpoint: no resume. Report each epoch.
- Closing over huge objects in the loop: serialised to every worker. Load inside the loop.
- Each worker logging or writing the same file: races. Guard with rank 0.
- No `max_failures`: a spot preemption kills the job. Configure retries.
- Mixing global batch size assumptions: effective batch scales with workers. Scale lr deliberately.

## Review
- [ ] Model and loader are prepared for distribution.
- [ ] Checkpoints on shared storage and resume tested.
- [ ] Failure config set.
- [ ] Per-worker seeds and rank-0 logging.
- [ ] Effective batch size and lr documented.
