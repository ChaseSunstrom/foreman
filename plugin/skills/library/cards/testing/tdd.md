---
name: tdd
title: Test-driven development
area: testing
tags: [tdd, red-green-refactor, unit, workflow, design]
detect: []
related: [unit-test-design, regression-tests, test-doubles, coverage]
---
Red, green, refactor: a failing test for one behavior comes first, then the least code to pass, then cleanup with the suite green.

## Verify
- `pytest -q -x` (or `npm test`, `go test ./...`, `cargo test`): the new test failed for the right reason before the change and passes after.
- `git stash push -- src && pytest -q path/to/test_new.py`: with the production change stashed, the new test fails (use the equivalent path for your layout).
- `pytest -q --lf` (or `jest --onlyFailures`): rerun only the last failures while iterating.

## Test first
One test, one behavior, named for the outcome. Run it and read the failure message before writing code.
```python
def test_discount_never_makes_total_negative():
    cart = Cart(items=[Item("pen", cents=100)])
    cart.apply_coupon(Coupon(percent=150))
    assert cart.total_cents() == 0   # fails: returns -50
```
Tests live beside the stack's convention (`tests/`, `*_test.go`, `*.test.ts`).

## Do
- Write the smallest next test that fails; confirm the failure text matches the missing behavior, not a typo or import error.
- Make it pass with the simplest code, even a hard-coded value, then add a second case to force generality (triangulate).
- Refactor only on green; rerun after every move.
- Start from the outside (public API or use case) and let tests pull the design inward.
- Commit at green. Keep red states local.
- For a bug, write the reproducing test first, watch it fail, then fix (see regression-tests).
- Keep the cycle under a few minutes; if stuck, take a smaller step.

## Avoid
- Writing the code first and the test after: the test then mirrors the implementation and never saw red. Revert the code, write the test, watch it fail.
- A test that fails for the wrong reason (NameError, missing fixture): fix the harness until it fails on the assertion.
- Asserting on private methods or call order: it blocks refactoring. Assert on observable results.
- Many behaviors per test: the first failure hides the rest. Split them.
- Skipping refactor: duplication piles up in tests and code. Spend the green step on it.
- Making a failing test pass by weakening the assertion: fix the code or revisit the requirement.

## Review
- [ ] Each new behavior has a test that was seen failing first.
- [ ] Failure messages name the behavior, not an implementation detail.
- [ ] No test depends on another test's order or state.
- [ ] Refactor commits change no test expectations.
- [ ] No assertion was loosened to get green.
