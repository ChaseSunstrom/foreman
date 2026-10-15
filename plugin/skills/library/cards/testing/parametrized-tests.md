---
name: parametrized-tests
title: Parametrized tests
area: testing
tags: [testing, parametrize, table-driven, data-driven, edge-cases, pytest, jest]
detect: []
related: [unit-test-design, property-based-testing, test-fixtures, tdd]
---
Run one behavior over a table of named cases: each case is its own test, with readable ids and the edges listed on purpose.

## Verify
- `pytest -q -k "test_parse"`: every parameter set runs as a separate test.
- `pytest --collect-only -q path/to/test.py`: the generated ids are readable and unique.
- `npx jest -t "parses"`: each `test.each` row is reported separately (Jest).
- `go test -run 'TestParse/negative' -v ./...`: a single table subtest can be run by name (Go).

## Test first
Start with the failing edge row, then add the happy rows.
```python
import pytest

@pytest.mark.parametrize("raw,expected", [
    pytest.param("1,5", 1.5, id="decimal-comma"),
    pytest.param("-0", 0.0, id="negative-zero"),
    pytest.param("", None, id="empty"),
    pytest.param("1e3", 1000.0, id="exponent"),
], )
def test_parse_number(raw, expected):
    assert parse_number(raw) == expected
```
Go: `for _, tc := range cases { t.Run(tc.name, func(t *testing.T) { ... }) }`. Jest: `test.each` with a name template.

## Do
- Give every case a name (`id=`, `name` field, `$name` template) that describes the situation.
- Cover boundaries: empty, one, max, max plus one, negative, zero, unicode, whitespace, NULL, duplicates.
- Keep the table to inputs and expected outputs; keep the test body identical for all rows.
- Include expected-error cases in a separate table or with an `expected_error` field.
- Capture `tc` inside the closure (older Go loop semantics) and call `t.Parallel()` only when cases are independent.
- Generate cases from a fixture file when the table is large, and keep each row reviewable.
- Add a regression row for every bug fixed, with a comment on what it reproduced.

## Avoid
- Logic in the table or branching in the test body (`if case == ...`): the test becomes a second implementation. Split into separate tests.
- Computing the expected value with the same function under test: always passes. Hard-code expectations.
- Unnamed index ids (`test[3]`): a failure says nothing. Give ids.
- One enormous table mixing unrelated behaviors: unreadable failures. Group by behavior.
- Cases that share mutable objects across rows: leaks between cases. Build fresh data per row.
- A table that stops at the happy path: duplicates prove nothing. Add the boundaries and failures.

## Review
- [ ] Each case has a descriptive name.
- [ ] Boundary, empty and invalid inputs are present.
- [ ] Expected values are literals, not recomputed.
- [ ] The test body has no conditionals on the case.
- [ ] Fixed bugs have a named regression row.
