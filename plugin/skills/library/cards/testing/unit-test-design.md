---
name: unit-test-design
title: Unit test design
area: testing
tags: [unit, arrange-act-assert, naming, isolation, assertions]
detect: []
related: [tdd, test-doubles, test-data-factories, flaky-tests]
---
Unit tests: fast, isolated, one behavior each, structured arrange-act-assert, failing with a message that says what broke.

## Verify
- `pytest -q -p no:randomly` then `pytest -q -p randomly` (needs pytest-randomly): passes in fixed and shuffled order, so no hidden coupling.
- `go test -count=1 -shuffle=on ./...`: Go suite uncached and in random order.
- `jest --runInBand` then `jest`: same results serial and parallel.
- `pytest -q --durations=10`: no unit test is slow enough to hide I/O.

## Test first
Name the behavior and condition; assert one outcome.
```go
func TestParseDuration_RejectsNegative(t *testing.T) {
	_, err := ParseDuration("-5s")
	if err == nil {
		t.Fatal("want error for negative duration, got nil")
	}
}
```
Place tests next to the unit (`*_test.go`, `*.test.ts`) or in `tests/` mirroring `src/`. Use table-driven or parametrized cases for input variations.

## Do
- Structure each test as arrange, act, assert, separated by blank lines; one act per test.
- Name tests `unit_condition_expectedResult` or as a sentence.
- Parametrize (`pytest.mark.parametrize`, `test.each`, Go table tests) for input variants; give each case an id.
- Cover boundaries: empty, one, max, off-by-one, null, unicode, negative.
- Test error paths and the exact error type or message contract.
- Inject clock, randomness and I/O so the unit is deterministic.
- Keep the setup in the test visible; extract builders, not opaque fixtures.

## Avoid
- Logic (loops, ifs) in a test: the test itself needs tests. Use table cases.
- Assertions on everything returned: any change breaks the test. Assert what the behavior promises.
- Shared mutable fixtures or module-level state: order-dependent failures. Build fresh per test.
- Real sleeps, wall clock, network: slow and flaky. Inject fakes.
- `assert result` or `assertTrue(x)` with no message context: use equality assertions that print both values.
- Testing the framework or trivial getters: no behavior to protect.

## Review
- [ ] Each test has one reason to fail and a name that states it.
- [ ] Boundary and error cases exist, not only the happy path.
- [ ] Tests pass shuffled and in parallel.
- [ ] No test touches network, disk or the clock directly.
- [ ] Setup is readable within the test or a named builder.
