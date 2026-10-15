---
name: conda
title: conda
area: python
tags: [python, conda, environments, packaging, mamba, reproducibility]
detect: [file:environment.yml, file:environment.yaml, file:conda-lock.yml, file:conda-lock.yaml, file:meta.yaml]
related: [uv, poetry, python-packaging, nox-tox]
---
conda environments: declarative environment.yml, pinned channels, lockfiles, and a clear split between conda and pip packages.

## Verify
- `conda env create -f environment.yml --dry-run`: the spec solves (add `-n name` to override the name).
- `conda env export --from-history`: the packages you asked for, not the full solved list.
- `conda list --explicit > spec.txt`: exact URLs for reproducing on the same platform.
- `conda run -n NAME python -m pytest -q`: tests run inside the environment with no shell activation.
- `conda list | grep pypi`: shows which packages were installed by pip.

## Test first
The check that fails first is a clean environment build plus an import smoke test.
```python
# tests/test_env.py
import importlib
import pytest

@pytest.mark.parametrize("mod", ["numpy", "pandas", "app"])
def test_core_imports(mod):
    importlib.import_module(mod)
```
In CI: `conda env create -f environment.yml` in a fresh runner, then `conda run -n NAME pytest -q`.

## Do
- Commit an `environment.yml` with `name`, explicit `channels` (for example `conda-forge`, then `nodefaults`), and `dependencies` with version ranges.
- Pin the Python version (`python=3.12`) and set `conda config --set channel_priority strict`.
- Install conda packages first. Put pip-only packages under a `- pip:` list in the same file, and run pip last.
- Create separate environments per project and never install into `base`.
- For reproducibility, generate a lockfile with `conda-lock` (`conda-lock -f environment.yml -p linux-64`) and commit it.
- Use `mamba` or `conda` with the libmamba solver for fast solves. Update the environment with `conda env update -f environment.yml --prune`.
- Remove and recreate the environment when the solve gets messy: `conda env remove -n NAME`.
- Use `conda run` or `conda activate` explicitly in scripts and CI. For Docker, copy the file first, so the layer caches.

## Avoid
- Mixing the `defaults` and `conda-forge` channels freely: ABI conflicts and odd solves. Choose one and use strict priority.
- `pip install` into an environment, then `conda install` more packages: conda is unaware of the pip files and can break them. Install conda deps first and pip last, or rebuild.
- `conda env export` as the committed spec: platform-specific build strings that fail elsewhere. Use `--from-history` or a lockfile.
- Using `sudo pip` or the base environment: pollutes the install. Use named environments.
- Unpinned Python and wide ranges in applications: surprise upgrades. Pin tightly for apps and loosely for libraries.
- Forgetting the license terms of the `defaults` channel for organizations: use conda-forge.

## Review
- [ ] `environment.yml` has explicit channels, a pinned Python and pip packages in their own section.
- [ ] A lockfile or explicit spec exists for reproducible builds.
- [ ] Fresh-environment creation runs in CI and tests run via `conda run`.
- [ ] Nothing is installed in `base`.
