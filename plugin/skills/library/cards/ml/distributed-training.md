---
name: distributed-training
title: Distributed training
area: ml
tags: [distributed, ddp, fsdp, deepspeed, multi-gpu, training]
detect: [dep:deepspeed, dep:accelerate, dep:horovod]
related: [pytorch, lightning, ray-train, cuda, wandb]
---
Multi-GPU and multi-node training with DDP, FSDP or DeepSpeed: correct process setup, sharded data, rank-aware IO and resumable checkpoints.

## Verify
- `torchrun --nproc_per_node=2 train.py --max-steps 5`: two-process smoke run finishes without hangs.
- `pytest -q tests/test_sampler.py`: ranks see disjoint, complete data shards.
- `python -m tools.resume_check`: training resumed from a checkpoint reproduces the next-step loss.

## Test first
```python
from app.data import shard_indices

def test_shards_disjoint_and_cover():
    shards = [set(shard_indices(100, rank=r, world=4, seed=0)) for r in range(4)]
    assert set().union(*shards) == set(range(100))
    assert sum(len(s) for s in shards) == 100
```

## Do
- Launch with `torchrun`; read `LOCAL_RANK` and call `torch.cuda.set_device` before building the model.
- Initialise the process group once with `nccl` for GPUs and destroy it on exit.
- Use `DistributedSampler` and call `set_epoch(epoch)` every epoch.
- Wrap the model in DDP, or FSDP when parameters, grads and optimiser state do not fit; choose wrapping policy and mixed precision explicitly.
- Do logging, evaluation writes and checkpoint saves on rank 0 only, behind a barrier where needed; save full or sharded state consistently with the loading code.
- Scale learning rate and warmup with the effective batch size; use gradient accumulation with `no_sync` where applicable.
- Seed per rank deterministically; log the effective batch size and world size.
- Test resume: model, optimiser, scheduler, scaler and sampler position.

## Avoid
- Forgetting `set_epoch`: every epoch shuffles identically. Call it each epoch.
- Different control flow per rank (rank-only collectives, unequal batch counts): hangs. Keep collectives symmetric.
- Every rank writing the same checkpoint or log file: corruption. Gate on rank 0.
- Evaluating on one rank's shard and reporting it as global: wrong metric. Reduce across ranks.
- Unused parameters under DDP without `find_unused_parameters` handled: error or hang. Remove them or set it knowingly.
- Saving only model weights and expecting exact resume: restore optimiser and scheduler too.

## Review
- [ ] Launch via `torchrun` with rank-aware device setup.
- [ ] Sampler epoch set; shards verified.
- [ ] Rank-0 IO only; metrics reduced.
- [ ] Resume tested end to end.
- [ ] Effective batch size and lr documented.
