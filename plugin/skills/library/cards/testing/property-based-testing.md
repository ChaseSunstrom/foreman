---
name: property-based-testing
title: Property-based testing
area: testing
tags: [property, generators, shrinking, hypothesis, fast-check, invariants]
detect: [dep:hypothesis, dep:fast-check, dep:proptest, dep:quickcheck, dep:pgregory.net/rapid]
related: [unit-test-design, fuzzing, mutation-testing, regression-tests]
---
State invariants that hold for all inputs, let a generator hunt counterexamples, and keep the shrunk failure as a fixed regression.

## Verify
- `pytest -q --hypothesis-show-statistics`: Hypothesis ran many examples and shows generation stats.
- `npx jest` (or `vitest run`) with `fc.assert(fc.property(...))`: fast-check passes, printing seed and path on failure.
- `cargo test`: proptest cases run and failures persist to a regressions file.
- `go test -rapid.checks=1000 ./...`: rapid runs more checks than the default.

## Test first
Write the invariant before the code: round trip, idempotence, ordering, oracle comparison.
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_is_idempotent_and_ordered(xs):
    once = my_sort(xs)
    assert my_sort(once) == once
    assert all(a <= b for a, b in zip(once, once[1:]))
```
Keep property tests in the normal test dir beside example tests.

## Do
- Pick properties: encode/decode round trip, idempotence, commutativity, "never raises", output invariants, agreement with a slow simple oracle.
- Build domain generators from primitives (`st.builds`, `fc.record`) so they emit only valid inputs.
- Pin a found counterexample as an explicit example (`@example(...)`, a plain unit test) so it stays covered.
- Commit the failure database or regressions file when the team shares it (`.hypothesis/`, `proptest-regressions/`).
- Set deterministic seeds in CI logs so a failure reproduces; print the seed.
- Constrain generation with strategies, not `assume` filters.

## Avoid
- Reimplementing the function in the property: you test the code against itself. Use an invariant or an independent oracle.
- Heavy `assume`/`filter` rejection: health check failures and thin coverage. Generate valid data directly.
- Unbounded sizes and slow properties: CI timeouts. Cap `max_size` and example count.
- Mutating shared state between examples: shrinking replays break. Build fresh state per run.
- Ignoring shrunk output: always read the minimal case before debugging.
- Deleting a flaky property: usually a real nondeterminism bug (dict order, time). Fix the source.

## Review
- [ ] Each property states an invariant, not a restated implementation.
- [ ] Generators produce valid domain values with few rejections.
- [ ] Known counterexamples are pinned as explicit tests.
- [ ] Seeds and failure artifacts are reproducible from CI output.
- [ ] Runtime is bounded.
