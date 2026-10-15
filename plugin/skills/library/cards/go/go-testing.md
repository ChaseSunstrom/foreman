---
name: go-testing
title: Go testing
area: go
tags: [go, testing, table-tests, race, benchmarks, fuzzing]
detect: [ext:.go, file:*_test.go]
related: [go-modules, go-concurrency, gin, chi]
---
Go's testing package: table-driven subtests, the race detector, httptest, fuzzing and benchmarks.

## Verify
- `go test ./... -race -count=1`: all tests with the race detector, caching bypassed.
- `go test ./... -cover`: coverage per package.
- `go vet ./...`: includes copylocks and loop-variable checks.
- `go test -run '^$' -bench . -benchmem ./pkg`: benchmarks only, with allocations.
- `go test -fuzz FuzzParse -fuzztime 30s ./pkg`: fuzz a parser for a short run.

## Test first
Write a table-driven test with named subtests. Run it and see it fail.
```go
func TestSlug(t *testing.T) {
	tests := []struct{ name, in, want string }{
		{"spaces", "a b", "a-b"},
		{"empty", "", ""},
	}
	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			t.Parallel()
			if got := Slug(tc.in); got != tc.want {
				t.Errorf("Slug(%q) = %q, want %q", tc.in, got, tc.want)
			}
		})
	}
}
```
Files are `x_test.go` in the same package, or `package x_test` for black-box tests. Select with `-run 'TestSlug/spaces'`.

## Do
- Use `t.Helper()` in assertion helpers, `t.Cleanup` for teardown and `t.TempDir()` for files.
- Use `t.Setenv` instead of `os.Setenv`, and `t.Context()` where the toolchain supports it.
- Test HTTP handlers with `httptest.NewRecorder` and `httptest.NewServer`.
- Compare structures with `cmp.Diff` (go-cmp) or `reflect.DeepEqual`, and print got and want in that order.
- Inject clocks, randomness and I/O through small interfaces, not package globals.
- Keep `t.Fatal` for setup failures and `t.Error` where the test can continue.
- Put slow integration tests behind `testing.Short()` or a build tag.

## Avoid
- Capturing the loop variable in parallel subtests on old toolchains (Go before 1.22 shares it): copy with `tc := tc`. Newer `go` directives scope it per iteration.
- `t.Parallel()` with shared mutable fixtures: races and flakes. Give each case its own state.
- `time.Sleep` to wait for goroutines: flaky. Use channels, `sync.WaitGroup` or `Eventually`-style polling with a deadline.
- Calling `t.Fatal` from a goroutine other than the test's: it does not stop the test. Use `t.Error` and return, or send the error back.
- Testing unexported details so refactors break tests: assert through the public API.
- Omitting `-race` in CI.
- Leaving cached results hide flakes locally: use `-count=1`.

## Review
- [ ] Each behaviour has a named subtest and at least one failure case.
- [ ] No sleeps, global state or order dependence between tests.
- [ ] Helpers call `t.Helper()` and cleanup uses `t.Cleanup`.
- [ ] CI runs with `-race`.
- [ ] Error messages show input, got and want.
