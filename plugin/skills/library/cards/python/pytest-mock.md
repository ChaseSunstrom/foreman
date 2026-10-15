---
name: pytest-mock
title: pytest-mock
area: python
tags: [python, testing, mocking, pytest, fixtures, patch]
detect: [dep:pytest-mock]
related: [pytest, pytest-asyncio, freezegun, factory-boy, httpx]
---
pytest-mock: the `mocker` fixture wraps unittest.mock with automatic undo, so patches never leak between tests.

## Verify
- `pytest -q`: the suite, with every patch undone per test.
- `pytest -q -p no:randomly`: rule out order effects when a mock seems to leak.
- `pytest -q -k NAME -x`: iterate on one test.
- `ruff check .`: unused mock imports and shadowed names.

## Test first
```python
import app.billing as billing

def test_charge_retries_once(mocker):
    gw = mocker.patch("app.billing.gateway.charge", side_effect=[TimeoutError, "ok"])
    assert billing.charge_with_retry(5) == "ok"
    assert gw.call_count == 2
    gw.assert_called_with(5)
```
Patch the name where it is looked up (`app.billing.gateway`), not where it is defined.

## Do
- Use `mocker.patch("pkg.module.name")` and `mocker.patch.object(obj, "attr")`. No `with` or decorators needed.
- Use `autospec=True` (or `create_autospec`) so wrong signatures fail: `mocker.patch("app.mail.send", autospec=True)`.
- Use `mocker.spy(obj, "method")` to check calls while keeping real behaviour.
- Use `mocker.patch.dict(os.environ, {"KEY": "v"})` for environment and `mocker.patch.dict(sys.modules, ...)` for imports.
- Script outcomes with `return_value`, `side_effect=[a, Exception]` or a function.
- Patch async callables with `mocker.patch(..., new_callable=mocker.AsyncMock)`; recent Python makes `patch` pick `AsyncMock` automatically for `async def` targets.
- Assert with `assert_called_once_with`, `assert_not_called` and `call_args_list`.
- Mock at boundaries (HTTP, clock, filesystem, email), not your own pure functions.

## Avoid
- Patching where defined instead of where used: the code under test still sees the original. Patch `app.billing.gateway`, not `vendor.gateway`.
- Bare `Mock()` for a typed collaborator: typos like `assert_called_onc` pass silently. Use `autospec=True` or `spec=`.
- `assert mock.called_once_with(...)`: it is a no-op attribute that is always truthy. Use `assert_called_once_with`.
- Mocking so much that the test restates the implementation: assert behaviour and outputs.
- Using `unittest.mock.patch` decorators plus `mocker` in the same test: argument order confusion. Pick `mocker`.
- Using `mocker` in a module- or session-scoped fixture: it is function scoped (`ScopeMismatch`). Use `pytest.MonkeyPatch` with `MonkeyPatch.context()` there.

## Review
- [ ] Mocks use autospec or spec for real collaborators.
- [ ] Each test asserts an outcome, not only that a mock was called.
- [ ] Patch targets are the lookup path of the code under test.
- [ ] No global state survives past the test.
