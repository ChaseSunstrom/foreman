---
name: jax
title: JAX
area: ml
tags: [python, jax, autodiff, jit, accelerators, numerical]
detect: [dep:jax, dep:jaxlib, dep:flax, dep:optax]
related: [pytorch, cuda, onnx, keras]
---
JAX programs: pure functions transformed with jit, grad, vmap and pmap, with explicit PRNG keys and immutable arrays.

## Verify
- `python -c "import jax; print(jax.devices())"`: which devices JAX sees.
- `pytest -q`: numerical tests pass, including under `jax.jit`.
- `JAX_DISABLE_JIT=1 pytest -q`: the logic is right without tracing, which makes failures debuggable.
- `JAX_ENABLE_X64=1 pytest -q`: results do not depend on float32 accident.

## Test first
Compare against a plain numpy reference, with and without jit, and check gradients numerically.
```python
import jax, jax.numpy as jnp
from jax.test_util import check_grads
from mypkg.fn import loss

def test_loss_grad_and_jit_agree():
    k = jax.random.key(0)
    w = jax.random.normal(k, (4,))
    x = jnp.ones((3, 4))
    assert jnp.allclose(loss(w, x), jax.jit(loss)(w, x))
    check_grads(loss, (w, x), order=1)
```

## Do
- Keep functions pure: no globals, no printing or mutation inside `jit`. Use `jax.debug.print` to inspect traced values.
- Split PRNG keys with `jax.random.split` for every use, and thread them through functions.
- Update arrays with `x.at[i].set(v)`, and use `jnp.where`, `lax.cond`, `lax.scan` and `lax.fori_loop` for traced control flow.
- Mark Python-valued arguments that change shapes or branches with `static_argnums` or `static_argnames`.
- Use `jax.vmap` instead of Python loops over a batch.
- Call `.block_until_ready()` when timing, since dispatch is asynchronous.
- Keep shapes static across calls to avoid recompiling.

## Avoid
- Python `if` or `for` on traced values inside `jit`: raises a tracer error. Use `lax.cond` or `lax.scan`, or mark the argument static.
- Reusing one PRNG key: identical random numbers. Split it.
- In-place assignment `x[i] = v`: arrays are immutable. Use `.at[].set`.
- Benchmarking without `block_until_ready` and without a warmup call: it times dispatch and compilation. Warm up, then block.
- Passing varying shapes into a jitted function in a loop: recompiles each time. Pad or bucket the shapes.
- Closing over large arrays in a jitted function: they get baked in as constants. Pass them as arguments.
- Using `jax.pmap` for new sharding code: prefer `jax.jit` with sharding annotations.

## Review
- [ ] Jitted functions are pure and keys are split, not reused.
- [ ] Static arguments are marked and recompilation is not triggered per step.
- [ ] Tests run once with `JAX_DISABLE_JIT=1` and once jitted.
- [ ] dtype and x64 assumptions are explicit.
- [ ] Timing code blocks on results.
