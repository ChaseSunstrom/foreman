---
name: python
title: Python
area: lang
tags: [python, pytest, ruff, typing, packaging, venv]
detect: [ext:.py, file:pyproject.toml, file:requirements.txt, file:setup.py, file:Pipfile]
related: [pytest, ruff, uv, fastapi, django]
---
Python baseline: isolated env, ruff for lint and format, pytest, type hints checked in CI, pyproject.toml as the single manifest.

## Verify
- `python -m pytest -q`: the suite, run with the project's interpreter and installed deps.
- `ruff check . && ruff format --check .`: lint and formatting.
- `pyright` (or `mypy .`): static types.
- `python -m pip check`: installed dependencies have no conflicting requirements.

## Test first
pytest, tests in `tests/` (or beside the package), files `test_*.py`. Parametrize edge cases.
```python
import pytest
from pkg.parse import parse_port

@pytest.mark.parametrize("raw", ["", "0", "70000", "abc"])
def test_parse_port_rejects_invalid(raw):
    with pytest.raises(ValueError):
        parse_port(raw)
```

## Do
- Work inside a venv (`python -m venv .venv`) or a tool-managed one; never install into the system interpreter.
- Declare deps and tool config in `pyproject.toml`; pin application deps with a lockfile.
- Annotate public functions; use `X | None`, `list[int]` and `from __future__ import annotations` as the target version allows.
- Use `pathlib.Path`, `dataclasses`, `enum`, context managers and `logging` instead of hand-rolled equivalents.
- Use `subprocess.run([...], check=True, capture_output=True, text=True)` with an argument list.
- Raise specific exceptions and chain with `raise X from err`.

## Avoid
- Mutable default arguments (`def f(x=[])`): shared across calls. Default to `None` and create inside.
- Bare `except:` or `except Exception: pass`: hides bugs and swallows KeyboardInterrupt (bare). Catch the specific type and log.
- `subprocess.run(cmd, shell=True)` with interpolated input: injection. Pass a list.
- `yaml.load` without a safe loader, `pickle.loads` on untrusted data, `eval`: code execution. Use `yaml.safe_load` and JSON.
- `datetime.utcnow()` and naive datetimes: deprecated and ambiguous. Use `datetime.now(timezone.utc)`.
- `assert` for runtime validation: stripped under `-O`. Raise an exception.
- `open()` without `encoding="utf-8"`: platform-dependent default. Pass it explicitly.
- `pip install` into a project with no lockfile or constraints: builds drift. Lock deps.

## Review
- [ ] No mutable defaults, bare excepts, `shell=True` with variable input, or `assert` used for validation.
- [ ] New public functions have type hints and a test covering a failure path.
- [ ] Dependencies added to `pyproject.toml` and the lockfile, not just installed locally.
- [ ] Files, sockets and processes are closed via `with`.
- [ ] Timezone-aware datetimes and explicit text encodings.
