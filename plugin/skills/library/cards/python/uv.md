---
name: uv
title: uv
area: python
tags: [python, packaging, uv, lockfile, virtualenv, dependencies]
detect: [file:uv.lock, file:.python-version, file:pyproject.toml]
related: [python-packaging, ruff, pytest, poetry, nox-tox]
---
uv: one tool for Python versions, virtualenvs, dependency resolution and a cross-platform `uv.lock`.

## Verify
- `uv lock --check`: `uv.lock` is up to date with `pyproject.toml`.
- `uv sync --locked`: installs exactly the lockfile and fails if it is stale.
- `uv run pytest -q`: tests run in the project environment, synced first.
- `uv tree`: the resolved dependency tree, to spot duplicates and unexpected pins.

## Test first
For a dependency or packaging change, the failing check is the lock or import:
```
uv add httpx            # edits pyproject.toml and uv.lock
uv run python -c "import httpx"
uv lock --check
```
For code, write the pytest test first and run it with `uv run pytest tests/test_x.py -q`.

## Do
- Add dependencies with `uv add PKG` and dev ones with `uv add --dev PKG`; remove with `uv remove PKG`. Let uv edit `pyproject.toml`.
- Commit `uv.lock` and `.python-version`.
- Run everything through `uv run CMD` so the environment is always in sync.
- Install in CI and images with `uv sync --locked` (add `--no-dev` for production).
- Use `uv python install 3.X` for interpreters instead of system packages.
- Run one-off tools with `uvx TOOL` (for example `uvx ruff check`).
- Declare script dependencies inline (PEP 723) and run them with `uv run script.py`.
- Use `[tool.uv.workspace]` for monorepos with several packages.
- Export for tools that need a requirements file: `uv export --format requirements-txt`.

## Avoid
- `uv pip install` into the project as the normal path: it bypasses `pyproject.toml` and the lock. Use `uv add`.
- Hand-editing `uv.lock`: regenerate with `uv lock`.
- Activating the venv and calling plain `pip`: drifts from the lock. Use `uv run` or `uv sync`.
- `uv sync` (unlocked) in CI: it silently re-resolves. Use `--locked` or `--frozen`.
- Not committing the lockfile: builds are not reproducible.
- `uv lock --upgrade` to fix one package: upgrades everything. Use `uv lock --upgrade-package PKG`.
- Treating `[tool.uv] dev-dependencies` and `[dependency-groups]` as the same: the standard is `[dependency-groups]`; `uv add --dev` writes there in current releases.

## Review
- [ ] `uv.lock` and `pyproject.toml` are committed together and `uv lock --check` passes.
- [ ] CI installs with `uv sync --locked` and runs through `uv run`.
- [ ] Dev and production dependency sets are separated.
- [ ] The Python version is pinned (`.python-version` and `requires-python`).
- [ ] No `uv pip install` steps outside throwaway environments.
