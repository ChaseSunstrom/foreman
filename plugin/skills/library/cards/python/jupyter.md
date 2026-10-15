---
name: jupyter
title: Jupyter notebooks
area: python
tags: [python, jupyter, notebooks, ipynb, reproducibility, nbconvert]
detect: [ext:.ipynb, dep:jupyter, dep:jupyterlab, dep:notebook, dep:ipykernel]
related: [pandas, numpy, pytest, ruff, uv]
---
Jupyter notebooks: reproducible execution, clean diffs, logic moved to importable modules.

## Verify
- `jupyter nbconvert --to notebook --execute NB.ipynb --output /tmp/out.ipynb`: the notebook runs top to bottom in a fresh kernel.
- `pytest --nbmake NB.ipynb`: executes notebooks as tests, only with nbmake installed.
- `jupyter nbconvert --clear-output --inplace NB.ipynb`: strips outputs before commit.
- `ruff check NB.ipynb`: lints notebook cells (Ruff supports `.ipynb`).

## Test first
Move logic into a module and test that with pytest; the notebook only calls it.
```python
# tests/test_features.py
from app.features import clean

def test_clean_drops_negative_ages():
    assert clean([{"age": -1}, {"age": 30}]) == [{"age": 30}]
```
Then the notebook has `from app.features import clean`. The notebook's own check is a clean top-to-bottom `nbconvert --execute`.

## Do
- Run Restart Kernel and Run All before committing; the notebook must pass in order.
- Pin a seed and data paths relative to the repo; read data from files, not absolute locations.
- Put functions and classes in `src/` modules and use `%load_ext autoreload` with `%autoreload 2` during development.
- Strip outputs and execution counts before commit (`nbstripout` or `nbconvert --clear-output`), unless outputs are the deliverable.
- Use `jupytext` to pair a notebook with a `.py` file when diffs and review matter.
- Install the kernel from the project env: `python -m ipykernel install --user --name PROJECT`.
- Keep one idea per notebook, with a first cell describing inputs and the environment.
- Parameterize runs with `papermill` when notebooks run on a schedule.

## Avoid
- Hidden state: running cells out of order so results depend on deleted or reordered cells. Restart and run all.
- Secrets, tokens and API keys in cells or saved outputs: they land in git. Read env vars and clear outputs.
- `!pip install` inside cells in committed notebooks: unpinned and untracked. Declare dependencies in `pyproject.toml`.
- Large embedded outputs (images, DataFrames): bloats diffs and the repo. Strip or save to files.
- Copy-pasted logic across notebooks: drifts. Import it from a module.
- Committing notebooks that need a local GPU, VPN or private path with no note: others cannot run them.
- `asyncio.run()` in a cell: the kernel already has a running loop. Use top-level `await`.

## Review
- [ ] Restart-and-run-all succeeds with no manual cell order.
- [ ] No secrets or personal paths in sources or outputs.
- [ ] Reusable logic lives in tested modules, not cells.
- [ ] Outputs are stripped (or intentionally kept) and the diff is readable.
- [ ] Dependencies and kernel environment are declared in the project.
