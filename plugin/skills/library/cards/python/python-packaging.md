---
name: python-packaging
title: Python packaging
area: python
tags: [python, packaging, pyproject, wheel, build, pypi]
detect: [file:pyproject.toml, file:setup.py, file:setup.cfg, file:MANIFEST.in]
related: [uv, poetry, pytest, ruff, nox-tox]
---
Building and publishing Python distributions: `pyproject.toml` metadata, build backends, wheels and sdists, PyPI.

## Verify
- `python -m build`: builds an sdist and a wheel into `dist/`.
- `twine check dist/*`: metadata and README render for PyPI.
- `python -m venv /tmp/v && /tmp/v/bin/pip install dist/*.whl && /tmp/v/bin/python -c "import PKG"`: the wheel installs and imports outside the source tree.
- `unzip -l dist/*.whl`: the wheel contains the package files and data you expect.

## Test first
Test the installed artifact, not the checkout. The failing check is an import or entry point from the built wheel.
```bash
python -m build --wheel
python -m venv /tmp/v && /tmp/v/bin/pip install dist/*.whl
/tmp/v/bin/python -c "import mypkg; print(mypkg.__version__)"
/tmp/v/bin/mytool --help
```
Run unit tests against that environment (nox or tox automate it).

## Do
- Put metadata in `[project]` (`name`, `version` or `dynamic`, `requires-python`, `dependencies`, `readme`, `license`, `classifiers`).
- Declare `[build-system] requires` and `build-backend` (setuptools, hatchling, flit, maturin or poetry-core).
- Use the `src/` layout so tests cannot import the source tree by accident.
- Declare optional extras under `[project.optional-dependencies]` and dev groups under `[dependency-groups]`.
- Expose commands with `[project.scripts]` and plugins with `[project.entry-points."group"]`.
- Include non-code files through the backend's data config and verify with `unzip -l`.
- Ship `py.typed` for typed libraries.
- Publish from CI with trusted publishing (OIDC) instead of long-lived tokens.
- Give libraries lower bounds and loose upper ones; give applications a lock.

## Avoid
- `python setup.py install`, `setup.py sdist` and `python setup.py test`: deprecated. Use `pip install .` and `python -m build`.
- `pip install -e .` as the only test: hides missing package data and files excluded from the wheel. Also test the built wheel.
- Missing `__init__.py` or wrong `packages` discovery: the wheel is empty or lacks subpackages. Check the file list.
- Pinning exact versions in a library's `dependencies`: conflicts for consumers. Use ranges.
- Version defined in two places that drift: use one source (`dynamic = ["version"]` from the backend or a VCS plugin).
- `twine upload` with a token in shell history or repo: use env vars or trusted publishing.
- Forgetting `requires-python`: installs on unsupported interpreters.

## Review
- [ ] A clean-venv install of the built wheel imports and runs the entry point.
- [ ] `twine check` passes and the wheel file list is as intended.
- [ ] Version, license and `requires-python` are declared once.
- [ ] Dependencies use ranges (library) or a lock (application).
- [ ] Release uses CI with trusted publishing, not a personal token.
