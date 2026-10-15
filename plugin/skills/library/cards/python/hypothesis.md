---
name: hypothesis
title: Hypothesis
area: python
tags: [python, testing, property-based, hypothesis, fuzzing, strategies]
detect: [dep:hypothesis, file:.hypothesis]
related: [pytest, pydantic, numpy, pandas]
---
Property-based testing with Hypothesis: strategies generate inputs, failures shrink to a minimal example.

## Verify
- `pytest -q --hypothesis-show-statistics`: how many examples ran and how many were invalid or filtered.
- `pytest -q --hypothesis-seed=0`: a fixed seed reproduces a flaky run.
- `pytest -q -p no:cacheprovider`: runs without cached state when checking determinism.
- `python -c "import hypothesis; print(hypothesis.__version__)"`: the installed version, since strategy names differ across releases.

## Test first
State an invariant, not examples. Round trips, idempotence and oracle comparisons find the most bugs.
```python
from hypothesis import given, strategies as st
from app.codec import encode, decode

@given(st.text())
def test_decode_inverts_encode(s):
    assert decode(encode(s)) == s

@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs):
    assert my_sort(my_sort(xs)) == my_sort(xs)
```
Tests live beside the unit tests and run under pytest.

## Do
- Build inputs with strategies: `st.integers(min_value=0)`, `st.text()`, `st.builds(Model, ...)`, `st.from_type(T)`.
- Combine with `st.lists`, `st.dictionaries`, `st.one_of`, `st.sampled_from`, and `@st.composite` for dependent values.
- Register a `settings` profile in `conftest.py` (`settings.register_profile("ci", max_examples=500, deadline=None)`) and load it by env.
- Pin found bugs with `@example(...)` so they stay as regression cases.
- Use `assume()` sparingly, and constrain the strategy itself instead.
- Commit the `.hypothesis/examples` database only if the team wants shared replays; otherwise gitignore it.
- Use `hypothesis.stateful.RuleBasedStateMachine` for stateful APIs.

## Avoid
- Re-implementing the function under test as the assertion: it mirrors the bug. Check a property or compare to a trusted oracle.
- Heavy `assume()` or `.filter()`: `FailedHealthCheck: filter_too_much`. Generate valid values directly.
- Non-determinism in the test (clock, random, network): Hypothesis reports `Flaky` and stops. Seed and fake those.
- Slow tests tripping the `deadline` (200 ms default): `DeadlineExceeded` on noisy machines. Set `deadline=None` or fix the slowness.
- Function-scoped pytest fixtures with `@given`: the fixture runs once, not per example, and a health check fails. Create state inside the test.
- Catching the failing assertion to silence it: shrunk examples are the point. Fix the code or the property.

## Review
- [ ] Each test asserts an invariant a reader can state in one sentence.
- [ ] Strategies produce valid domain values without heavy filtering.
- [ ] Past failures are pinned with `@example`.
- [ ] CI and local profiles set `max_examples` and `deadline` deliberately.
- [ ] No fixtures or global state leak between generated examples.
