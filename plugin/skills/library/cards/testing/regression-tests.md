---
name: regression-tests
title: Regression tests
area: testing
tags: [regression, bugfix, reproduction, tdd, root-cause, prove]
detect: []
related: [tdd, characterization-tests, fuzzing, property-based-testing]
---
Every bug fix ships with a test that fails on the old code for the reported reason and passes on the fix.

## Verify
- `git stash push -- src && pytest -q tests/test_bug.py; git stash pop`: the regression test fails with the fix removed (adjust path and runner).
- `pytest -q tests/test_bug.py`: it passes with the fix applied.
- `go test -run TestRegression ./...` (or `npm test -- -t "regression"`): the targeted regression runs on its own.
- `git log --oneline -1 -- tests/`: the test is committed in the same change as the fix.

## Test first
Reproduce the report as the smallest test; confirm it fails with the reported symptom.
```python
def test_issue_482_empty_cart_checkout_does_not_crash():
    cart = Cart(items=[])
    result = checkout(cart)
    assert result.status == "rejected"   # reported: ZeroDivisionError
```
Place it with the unit's other tests, named for the behavior and the issue id.

## Do
- Reproduce first from the report: inputs, environment, version; reduce to the minimal case.
- Assert the correct behavior, not just the absence of the exception.
- Run it against the unfixed code and record the failure message before touching production code.
- Fix the root cause where all callers route through, then add a sibling case for similar callers.
- Name the test for the behavior and reference the issue or ticket id in a comment.
- Keep the test's inputs as literals; do not generate them.
- Add the failing input from fuzz or property runs as a permanent example.

## Avoid
- A test written after the fix and never seen failing: it may not exercise the bug. Revert the fix and watch it fail.
- A test that fails for a different reason than the report: it proves nothing about the bug. Match the symptom.
- Asserting only that no error is raised: wrong output passes. Assert the result.
- Fixing the symptom in one caller: sibling paths stay broken. Fix the shared cause and test two callers.
- Mocking away the component where the bug lives: the test cannot fail. Exercise the real code.
- Deleting or weakening an existing test to make the fix pass: first decide which behavior is right.

## Review
- [ ] Test failed on the pre-fix code with the reported symptom.
- [ ] It asserts correct output, not just no crash.
- [ ] It lives in the same commit as the fix.
- [ ] Neighboring callers or inputs have cases.
- [ ] No existing assertion was loosened.
