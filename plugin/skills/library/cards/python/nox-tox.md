---
name: nox-tox
title: nox and tox
area: python
tags: [python, testing, nox, tox, automation, matrix]
detect: [dep:nox, dep:tox, file:noxfile.py, file:tox.ini]
related: [pytest, python-packaging, ruff, uv, mypy]
---
nox (Python sessions) and tox (INI or TOML environments): run tests, lint and builds in isolated environments across Python versions.

## Verify
- `nox -l`: lists sessions (nox).
- `nox -s tests`: runs one session in a fresh virtualenv.
- `tox l`: lists environments (tox 4; `tox -l` in older versions).
- `tox -e py`: runs the test environment on the current interpreter.
- `tox run-parallel` (or `tox -p`): environments run concurrently; confirms they do not share state.

## Test first
The test run is the check. A new session or env should fail until its dependencies and command are right.
```python
# noxfile.py
import nox

@nox.session(python=["3.11", "3.12"])
def tests(session):
    session.install(".[test]")
    session.run("pytest", "-q", *session.posargs)
```
Run `nox -s tests -- -k name` and see it fail on a broken test first.

## Do
- Install the project as a built package (`session.install(".")`) so packaging errors show up; avoid `-e` for the main test run.
- Keep sessions small and named: `tests`, `lint`, `types`, `docs`, `build`.
- Forward arguments with `*session.posargs` (nox) or `{posargs}` (tox).
- Pin interpreters via `python=[...]` (nox) or `envlist = py311,py312` (tox) matching `requires-python`.
- Use `reuse_venv` or `-R` (nox) and `--recreate` (tox) deliberately; recreate when dependencies change.
- Use `nox.options.sessions` to set the default set.
- With uv, set `nox.options.default_venv_backend = "uv"` or install `tox-uv`, to speed up env creation.
- Call tools as `session.run(...)` so they run in the session venv; fail loudly on a nonzero exit.

## Avoid
- `session.run("pytest")` without installing pytest in that session: it finds the global one or fails. Install it explicitly.
- `external=True` or `allowlist_externals` used to call global tools casually: results differ across machines. Install tools in the env.
- Environment leakage: tox and nox pass only selected variables. Use `passenv`/`pass_env` (tox) or `env=` (nox) for needed ones, not wildcards.
- Old `tox.ini` keys from tox 3 (`whitelist_externals`, `skipsdist`, `-l` flag): renamed or changed in tox 4. Check the pinned version.
- Running only one Python locally and finding failures in CI: run the matrix at least on the lowest and highest.
- Sharing a venv across sessions: hidden coupling. Keep each isolated.

## Review
- [ ] Each session installs everything it uses and runs the same command CI does.
- [ ] The interpreter matrix matches `requires-python`.
- [ ] Arguments pass through to the underlying tool.
- [ ] The project is tested as an installed package.
- [ ] CI calls `nox` or `tox` rather than duplicating the commands.
