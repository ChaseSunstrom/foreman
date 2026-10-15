---
name: pytorch
title: PyTorch
area: ml
tags: [python, deep-learning, training, tensors, gpu, autograd]
detect: [dep:torch, dep:torchvision, dep:torchaudio]
related: [lightning, cuda, onnx, transformers, lora-fine-tuning]
---
PyTorch models and training loops: nn.Module, DataLoader, autograd, device placement, checkpoints.

## Verify
- `python -c "import torch; print(torch.__version__, torch.cuda.is_available())"`: the install and the GPU build match the machine.
- `pytest -q`: shape, gradient and determinism tests pass on CPU.
- `python -m pytest -q -k overfit`: the model can drive loss to near zero on one small batch.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Tests run on CPU with tiny tensors. Assert shapes, finite loss and that gradients reach every parameter.
```python
import torch
from mypkg.model import Net

def test_every_param_gets_grad():
    torch.manual_seed(0)
    m = Net(in_dim=8, out_dim=3)
    loss = m(torch.randn(4, 8)).sum()
    loss.backward()
    missing = [n for n, p in m.named_parameters() if p.grad is None]
    assert not missing
```

## Do
- Seed with `torch.manual_seed` and build the `DataLoader` generator and `worker_init_fn` so runs repeat.
- Call `model.train()` and `model.eval()` explicitly, and wrap evaluation in `torch.inference_mode()`.
- Order each step `optimizer.zero_grad(set_to_none=True)`, `loss.backward()`, `optimizer.step()`, then `scheduler.step()`.
- Move the model first, then the optimizer is built from its parameters. Use one `device` variable and `.to(device)` for batches.
- Use `torch.autocast` with `GradScaler` for fp16. bf16 needs no scaler.
- Save `state_dict()` for model, optimizer, scheduler and epoch. Load with `torch.load(path, map_location="cpu", weights_only=True)`.
- Use `clip_grad_norm_` after `backward()` and before `step()`.

## Avoid
- Accumulating `loss` into a Python list without `.item()`: it keeps the whole graph alive and leaks memory. Store `loss.item()` or `loss.detach()`.
- Forgetting `model.eval()` for validation: dropout and batch norm stay in training mode, so metrics are noisy. Toggle it and restore `train()`.
- `torch.load` on untrusted files with default settings: pickle executes code. Pass `weights_only=True`.
- Applying `softmax` before `CrossEntropyLoss`: the loss expects raw logits. Remove the softmax.
- In-place ops on tensors autograd needs (`x += 1`, `relu_`): error at backward. Use the out-of-place form.
- `DataLoader(num_workers>0)` with CUDA tensors created in `__getitem__`: workers cannot share them. Return CPU tensors and move in the loop.
- Saving the whole model object with `torch.save(model)`: breaks on refactors. Save `state_dict`.

## Review
- [ ] Train and eval modes are set, and eval runs under `inference_mode`.
- [ ] Loss and metrics logged as Python floats, not live tensors.
- [ ] Checkpoints hold optimizer and scheduler state, and resume is tested.
- [ ] Seeds, device and dtype are configured in one place.
- [ ] Shape and gradient tests run on CPU without a GPU.
