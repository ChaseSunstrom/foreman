---
name: characterization-tests
title: Characterization tests
area: testing
tags: [characterization, legacy, refactoring, pinning, approval, seams]
detect: []
related: [golden-files, snapshot-testing, regression-tests, tdd]
---
Characterization tests record what legacy code does today, right or wrong, so you can refactor with a safety net.

## Verify
- `pytest -q tests/characterization`: the pinned behavior still holds after the refactor.
- `git diff --stat -- tests/characterization`: a refactor commit changes no expected values.
- `pytest --cov=legacy_module --cov-branch --cov-report=term-missing`: the pinned tests reach the lines you intend to change.
- `go test ./legacy/...` (or `npm test`): the same suite passes before and after each small step.

## Test first
Call the code with a real input, observe the output, then pin it.
```python
def test_legacy_invoice_total_for_mixed_cart():
    cart = load_fixture("mixed_cart.json")
    # first run: assert result == None to read the actual value, then pin it
    assert compute_total(cart) == Decimal("107.35")   # observed, not specified
```
Place them under `tests/characterization/` so they are recognizable and deletable later.

## Do
- Find a seam (parameter, constructor, subclass, module boundary) to inject fakes for the clock, database and network.
- Write a failing assertion with a dummy expected value, run it, copy the actual value in, and mark it as observed.
- Cover the inputs real users send: sample production data, boundary values, odd branches.
- Use golden files or snapshots for large outputs, and normalize the volatile parts.
- Refactor in small steps, rerunning after each; commit at green.
- Replace characterization tests with intent-revealing unit tests as you learn what the behavior should be.
- Record suspected bugs as a note beside the pinned test instead of silently fixing them.

## Avoid
- "Fixing" odd behavior while pinning: the test then no longer describes reality, and callers break. Pin first, fix as a separate change with its own test.
- Pinning nondeterministic output (time, ids, ordering): flaky net. Freeze or scrub it.
- Calling real production services in the pinning tests: side effects. Fake them at the seam.
- Treating pinned values as requirements: they may encode bugs. Label them observed.
- Refactoring with no coverage on the branch you are touching: check coverage of that path first.
- Leaving them forever: they obscure intent. Replace with specified tests.

## Review
- [ ] Each pinned value was observed from the unmodified code.
- [ ] Volatile inputs and outputs are frozen or scrubbed.
- [ ] Refactor commits do not alter expected values.
- [ ] Suspected bugs are noted, not fixed in the same change.
- [ ] Coverage includes the lines being refactored.
