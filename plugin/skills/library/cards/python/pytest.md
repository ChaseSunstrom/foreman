---
name: pytest
title: pytest
area: python
tags: [python, testing, pytest, fixtures, parametrize, mocking]
detect: [dep:pytest, file:pytest.ini, file:conftest.py]
related: [hypothesis, nox-tox, httpx, uv, ruff]
---
pytest suites: plain asserts, fixtures, parametrization, markers, `tmp_path`, `monkeypatch`, coverage.

## Verify
- `pytest -q`: the whole suite.
- `pytest --collect-only -q`: tests are discovered, so import errors and bad names show up.
- `pytest -x --lf`: rerun last failures first and stop at the first.
- `pytest --strict-markers --strict-config -q`: unknown markers and config keys fail instead of passing silently.
- `pytest --cov=PKG --cov-report=term-missing`: coverage gaps, only with pytest-cov installed.

## Test first
Tests live in `tests/`, named `test_*.py`, with shared fixtures in `conftest.py`.
```python
import pytest
from app.pricing import total

@pytest.mark.parametrize("qty,expected", [(1, 10), (10, 90), (0, 0)])
def test_bulk_discount(qty, expected):
    assert total(qty, unit=10) == expected

def test_negative_qty_rejected():
    with pytest.raises(ValueError, match="qty"):
        total(-1, unit=10)
```
Run it and see the failure message before writing the code.

## Do
- Use bare `assert`; pytest rewrites it into a diff. Use `pytest.raises(..., match=...)` for errors and `pytest.approx` for floats.
- Share setup with fixtures; give them the smallest scope that works, and `yield` for teardown.
- Use `tmp_path`, `monkeypatch` and `capsys` rather than touching real paths, env or stdout.
- Parametrize with `ids=` when the values read badly, instead of loops inside a test.
- Declare custom markers in config (`markers =` in `pytest.ini` or `[tool.pytest.ini_options]`) and run with `--strict-markers`.
- Configure once in `pyproject.toml` (`testpaths`, `addopts`, `filterwarnings = ["error"]`).
- Mock at the boundary you own with `monkeypatch.setattr` or `unittest.mock.patch` where the name is looked up.

## Avoid
- `unittest` assertion methods (`assertEqual`) in new pytest code: lose rewritten diffs. Use `assert`.
- Patching where an object is defined instead of where it is used: the patch has no effect. Patch `app.module.name`.
- Mutable state in module-level fixtures or session scope shared across tests: order-dependent failures. Reset it or narrow the scope.
- `try/except` around the code with an `assert False` inside: use `pytest.raises`.
- `@pytest.fixture` called directly (`my_fixture()`): errors. Request it as an argument.
- Tests that pass only in file order: run `pytest -p no:randomly` vs random order (pytest-randomly) to find the coupling.
- `async def` tests with no plugin: they are skipped or warn. Add `pytest-asyncio` or `anyio` and mark them.

## Review
- [ ] Each new behaviour has a test that failed before the change.
- [ ] No test depends on order, wall clock, network or real home directory.
- [ ] Fixtures have the narrowest scope and clean up after themselves.
- [ ] Markers are registered and `--strict-markers` is on.
- [ ] Mocks target the lookup site and are limited to external boundaries.
