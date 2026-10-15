---
name: testify
title: testify
area: go
tags: [go, testing, testify, assert, require, suite, mock]
detect: [dep:github.com/stretchr/testify]
related: [go-testing, go-errors, go-fuzzing, go-concurrency]
---
testify assertions: require vs assert, error and collection helpers, suites and mocks used sparingly.

## Verify
- `go test ./...`: assertions pass.
- `go test -race -count=1 ./...`: no races and no cached results.
- `go vet ./...`: lints, including `testifylint` rules if golangci-lint runs them.
- `go mod tidy && git diff --exit-code go.mod go.sum`: dependency recorded correctly.

## Test first
Write the failing assertion, with `require` for preconditions and `assert` for checks.
```go
func TestParse(t *testing.T) {
	got, err := Parse("8080")
	require.NoError(t, err)
	assert.Equal(t, 8080, got)

	_, err = Parse("x")
	require.ErrorIs(t, err, ErrBadPort)
}
```

## Do
- Use `require` when later lines would panic or be meaningless after a failure (errors, nil checks); `assert` for independent checks.
- Put arguments in `(t, expected, actual)` order.
- Error checks: `require.NoError`, `require.ErrorIs(t, err, ErrX)`, `require.ErrorAs`, `require.EqualError` only for exact text.
- Collections: `assert.ElementsMatch` for unordered, `assert.Len`, `assert.Contains`, `assert.Empty`.
- Async: `assert.Eventually(t, cond, wait, tick)` and `require.Eventually` instead of sleeps.
- Floats: `assert.InDelta`; time: `assert.WithinDuration`.
- JSON: `assert.JSONEq` to ignore key order.
- Pass `t.Helper()`-style failures with message args: `assert.Equal(t, a, b, "user %d", id)`.
- Use `t.Run` subtests with table data; each calls its own `require` on the subtest's `t`.

## Avoid
- `assert` where the next line dereferences the result: nil panic hides the real failure. Use `require`.
- Swapped expected and actual: confusing diffs. Keep the order.
- `assert.Equal` on pointers or errors expecting deep behavior: compares by `ObjectsAreEqual`, and errors with `Equal` fail on wrap differences. Use `ErrorIs` and compare values.
- `assert.True(t, a == b)`: loses the diff. Use `Equal`.
- Using the parent `t` inside subtests or goroutines: failures attach to the wrong test or panic after finish. Use the subtest's `t`; never call `require` from a spawned goroutine (FailNow only works on the test goroutine).
- Heavy `suite` or `mock` frameworks by default: hidden setup and brittle call-order expectations. Prefer small fakes; use `mock` only for true boundaries and call `AssertExpectations(t)`.
- `time.Sleep` then assert: flaky. Use `Eventually`.

## Review
- [ ] `require` guards every precondition used later.
- [ ] Argument order is (expected, actual) everywhere.
- [ ] Error assertions use `ErrorIs` or `ErrorAs`, not string compare.
- [ ] No sleeps; async uses `Eventually`.
- [ ] Mocks (if any) assert expectations and are limited to external boundaries.
