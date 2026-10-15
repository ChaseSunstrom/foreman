---
name: keras
title: Keras
area: ml
tags: [python, deep-learning, keras, training, layers, tensorflow]
detect: [dep:keras, dep:tensorflow, dep:tensorflow-cpu]
related: [jax, pytorch, onnx, mlflow]
---
Keras 3 models: Sequential, Functional and subclassed models, compile and fit, callbacks, multi-backend.

## Verify
- `python -c "import keras; print(keras.__version__, keras.backend.backend())"`: the version and the active backend.
- `pytest -q`: model output shape and training smoke tests pass.
- `python -c "import mypkg.model as m; m.build().summary()"`: the graph builds and shapes line up.
- `ruff check . && ruff format --check .`: lint and format.

## Test first
Build the model with a tiny input, check the output shape, and overfit one batch.
```python
import numpy as np
from mypkg.model import build

def test_overfits_tiny_batch():
    x = np.random.rand(16, 8).astype("float32")
    y = np.random.randint(0, 3, size=16)
    m = build(input_dim=8, classes=3)
    hist = m.fit(x, y, epochs=60, batch_size=16, verbose=0)
    assert hist.history["loss"][-1] < hist.history["loss"][0] * 0.5
```

## Do
- Import `keras` directly for new code. Use `keras.ops` for backend-agnostic math inside custom layers and losses.
- Compile with an explicit `loss`, `optimizer` and `metrics`. Use `from_logits=True` when the last layer has no activation.
- Save with `model.save("m.keras")` and reload with `keras.saving.load_model`. Register custom classes with `@keras.saving.register_keras_serializable()` and implement `get_config`.
- Use `keras.utils.set_random_seed(seed)` for reproducible runs.
- Feed `tf.data` or `keras.utils.PyDataset` pipelines for large data instead of loading arrays whole.
- Put normalization and augmentation in preprocessing layers so they ship with the model.
- Use `ModelCheckpoint`, `EarlyStopping` and `ReduceLROnPlateau` callbacks with a monitored metric that exists.

## Avoid
- `import tensorflow.keras` or `tf.keras` in a Keras 3 project: it can pick the legacy path. Use `import keras`.
- Saving as `.h5` or SavedModel folders by habit: use the `.keras` format.
- Calling `tf.*` ops in a custom layer when the backend is JAX or PyTorch: it fails off TensorFlow. Use `keras.ops`.
- Softmax on the output plus `from_logits=True`: double activation hurts training. Pick one.
- Custom layers without `get_config`: loading the saved model fails. Implement it.
- `model.predict` on the whole dataset in one call when it is huge: memory spikes. Pass `batch_size` or a dataset.
- `shuffle=True` with a generator or dataset that already shuffles: harmless but misleading. Shuffle in one place.

## Review
- [ ] Loss matches the last-layer activation and label encoding (sparse versus one-hot).
- [ ] Custom layers serialize and a save and reload round trip is tested.
- [ ] Backend-specific code is isolated or uses `keras.ops`.
- [ ] Seed is set and the smoke test runs on CPU.
- [ ] Preprocessing travels inside the saved model.
