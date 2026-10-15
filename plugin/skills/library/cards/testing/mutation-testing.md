---
name: mutation-testing
title: Mutation testing
area: testing
tags: [mutation, test-quality, mutmut, stryker, pitest, survivors]
detect: [dep:mutmut, dep:@stryker-mutator/core, dep:cosmic-ray, dep:pitest-maven, file:stryker.conf.*, file:mutants.out]
related: [coverage, unit-test-design, property-based-testing]
---
Mutation testing alters code (flip a comparison, drop a call) and checks that tests fail; survivors are assertions you are missing.

## Verify
- `mutmut run` then `mutmut results`: Python mutants run and survivors are listed.
- `npx stryker run`: JS/TS mutation score and an HTML report.
- `cargo mutants`: Rust mutants run (needs cargo-mutants installed).
- `mvn org.pitest:pitest-maven:mutationCoverage`: PIT report for a Maven project.

## Test first
Start from a survivor: write the test that kills it, then confirm it fails against the mutant.
```python
# survivor: `if qty >= 10` mutated to `if qty > 10` still passed
def test_bulk_discount_starts_at_exactly_ten():
    assert price(unit=100, qty=10) == 900  # 10% off
    assert price(unit=100, qty=9) == 900
```
Assert both sides of each boundary with literal expected values.

## Do
- Run on changed or critical modules, not the whole repo each commit; scope with the tool's file or diff options.
- Read each survivor: either add an assertion, or mark it equivalent and ignore it.
- Kill boundary mutants with exact-value assertions on both sides of every comparison.
- Run mutation on a schedule or on the diff in CI, with a threshold on the changed files.
- Make unit tests fast first; mutation multiplies runtime by the mutant count.
- Exclude logging, generated code and trivial glue in config.

## Avoid
- Chasing 100% mutation score: equivalent mutants make it unreachable. Set a floor and review survivors.
- Running it on a slow integration suite: hours. Limit to fast unit tests.
- Killing mutants with assertion-free tests that merely execute lines: they pass for the wrong reason. Assert results.
- Treating line coverage as proof: a covered line can survive every mutant. Use both signals.
- Running on flaky tests: false kills. Stabilize first.
- Ignoring timeouts: a hung mutant counts as killed but may hide an infinite loop.

## Review
- [ ] Survivors in changed code are killed or justified as equivalent.
- [ ] Boundary comparisons assert both sides with literal values.
- [ ] Scope and threshold are configured, not whole-repo by default.
- [ ] Generated and trivial code is excluded.
- [ ] The baseline suite passes before mutating.
