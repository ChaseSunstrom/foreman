---
name: poetry
title: Poetry
area: python
tags: [python, packaging, poetry, lockfile, dependencies, build]
detect: [file:poetry.lock, dep:poetry-core]
related: [python-packaging, uv, pytest, ruff, nox-tox]
---
Poetry: dependency management, virtualenvs, lockfile and build/publish driven by `pyproject.toml`.

## Verify
- `poetry check --lock`: `pyproject.toml` is valid and `poetry.lock` matches it.
- `poetry install --sync`: the environment matches the lock exactly, removing extras.
- `poetry run pytest -q`: tests run in the Poetry environment.
- `poetry build`: sdist and wheel build from the project metadata.

## Test first
For a dependency change, the failing check is the lock and an import:
```
poetry add httpx
poetry run python -c "import httpx"
poetry check --lock
```
For code, write the pytest test first and run it with `poetry run pytest tests/test_x.py -q`.

## Do
- Add with `poetry add PKG` and `poetry add --group dev PKG`; Poetry edits `pyproject.toml` and the lock.
- Commit `poetry.lock` for applications; decide deliberately for libraries.
- Use dependency groups (`[tool.poetry.group.dev.dependencies]`) rather than the old `dev-dependencies` table.
- Bound the Python range under `python = ">=3.X,<4"`; caret and tilde constraints (`^1.2`) follow semver rules.
- After editing `pyproject.toml` by hand, run `poetry lock` before installing.
- Install in CI with `poetry install --no-interaction` (add `--only main` for production).
- Set `virtualenvs.in-project true` to get a `.venv` that editors and Docker can find.
- Use `poetry export` (needs the export plugin) when a requirements file is required.

## Avoid
- `pip install` inside the Poetry venv: untracked packages that vanish on `--sync`. Use `poetry add`.
- Hand-edited `poetry.lock`: breaks the content hash. Run `poetry lock`.
- Old `poetry lock --no-update` in 2.x docs and scripts: the flag is gone in newer releases. Use `poetry lock` and `poetry update PKG` for targeted upgrades.
- A `[tool.poetry]` table assumed to be the only metadata source: 2.x supports the standard `[project]` table. Do not define the same field in both.
- Unpinned `^0.x` constraints: caret on `0.x` only allows the minor you named, which then blocks resolution. Widen deliberately.
- `poetry install` with a stale lock in CI: it errors; fix the lock instead of removing the check.

## Review
- [ ] `poetry check --lock` passes and the lock is committed with `pyproject.toml`.
- [ ] Dev tooling sits in a group, not the main dependencies.
- [ ] The Python constraint matches what CI tests.
- [ ] Metadata has one source (`[project]` or `[tool.poetry]`), not both.
- [ ] CI installs from the lock and runs through `poetry run`.
