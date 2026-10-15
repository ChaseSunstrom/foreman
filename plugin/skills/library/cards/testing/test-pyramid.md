---
name: test-pyramid
title: Test pyramid
area: testing
tags: [pyramid, strategy, layers, speed, cost, confidence]
detect: []
related: [unit-test-design, integration-testing, e2e-strategy, coverage, contract-testing]
---
Many fast unit tests, fewer integration tests, a handful of end-to-end journeys: put each check at the cheapest layer that can catch the bug.

## Verify
- `pytest -q --durations=15`: the slowest tests, to see which layer is bloated.
- `pytest -q -m "not integration and not e2e"`: the fast tier runs alone and finishes in seconds.
- `go test -short ./...`: short mode runs the fast tier (tests honor `testing.Short()`).
- `npx jest --listTests | wc -l`: rough test counts per project; compare layers when run once per tier.

## Test first
Ask which layer can fail for this bug, and write the test there.
```python
# rule/logic bug -> unit test, no I/O
def test_tax_rounds_half_up():
    assert tax(Decimal("0.125"), rate=Decimal("0.1")) == Decimal("0.01")
# wiring bug -> integration test, one real DB
# journey bug -> one e2e test, only if no lower layer can see it
```
Keep tiers separate by directory or marker (`tests/unit`, `tests/integration`, `tests/e2e`).

## Do
- Put business rules, branching and edge cases in unit tests with no I/O.
- Use integration tests for boundaries: database queries, serialization, message handlers, HTTP routes.
- Use contract tests between services instead of full-system tests for every pair.
- Keep e2e to critical user journeys; push everything else down.
- Run tiers in order in CI: unit, integration, e2e, so failures arrive fast.
- Delete or demote an e2e test when a lower-layer test covers the same risk.
- Track runtime per tier and set budgets, for example unit under a minute.

## Avoid
- The ice-cream cone (mostly e2e, few unit tests): slow, flaky, vague failures. Move checks down.
- Duplicating the same assertion at every layer: cost without confidence. Test each risk once at its lowest layer.
- Testing logic through the UI: slow and brittle. Call the function.
- Relying only on unit tests with heavy mocks: wiring bugs ship. Add integration tests at boundaries.
- Counting tests per layer as the goal: the shape serves feedback speed, not a quota.
- One shared slow suite run on every save: developers stop running it. Offer a fast tier.

## Review
- [ ] Each test sits at the lowest layer that can detect its failure.
- [ ] The fast tier runs locally in seconds to minutes.
- [ ] Boundaries have integration or contract tests.
- [ ] E2E tests map to named critical journeys.
- [ ] No behavior is tested identically at several layers.
