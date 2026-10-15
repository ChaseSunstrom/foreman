---
name: go
title: Go
area: lang
tags: [go, golang, modules, testing, goroutines, vet]
detect: [ext:.go, file:go.mod, file:go.sum]
related: [docker, grpc]
---
Go baseline: go vet, gofmt, table-driven tests with the race detector, modules, explicit error handling and context propagation.

## Verify
- `go build ./...`: everything compiles.
- `go vet ./...`: suspicious constructs (printf verbs, copied locks, lost cancels).
- `gofmt -l .`: lists unformatted files (should print nothing).
- `go test -race ./...`: tests with the data-race detector.
- `go mod tidy && git diff --exit-code go.mod go.sum`: module files are tidy.

## Test first
Standard `testing`, files `*_test.go` beside the code. Table-driven with subtests.
```go
func TestParsePort(t *testing.T) {
	for _, in := range []string{"", "0", "70000", "abc"} {
		t.Run(in, func(t *testing.T) {
			if _, err := ParsePort(in); err == nil {
				t.Fatalf("ParsePort(%q): want error", in)
			}
		})
	}
}
```

## Do
- Return `error` as the last value; wrap with `fmt.Errorf("load config: %w", err)`; test with `errors.Is` and `errors.As`.
- Pass `context.Context` as the first parameter and honour cancellation; always `defer cancel()`.
- Accept interfaces, return structs; define interfaces at the consumer.
- Close what you open with `defer` right after the error check (files, `resp.Body`, rows).
- Use `t.Helper()`, `t.Cleanup` and `t.TempDir()` in tests; mark parallel-safe tests `t.Parallel()`.
- Bound goroutines with `errgroup` or a `sync.WaitGroup`, and give each a clear exit path.
- Use `log/slog` for structured logs.

## Avoid
- Ignoring errors (`_ = f()`) or logging and also returning them: lost failures or duplicate noise. Handle once.
- Capturing the loop variable in a goroutine in pre-1.22 modules: all goroutines see the last value. Copy it (`v := v`) or check the `go` directive in go.mod.
- `http.Get` and the default client: no timeout, can hang forever. Use an `http.Client{Timeout: ...}` and context requests.
- Forgetting `resp.Body.Close()`: leaks connections.
- Sending on or closing a channel from multiple owners: panics. One sender closes.
- Returning a typed nil pointer as an `error` interface: the result is non-nil. Return a literal `nil`.
- `panic` for expected failures: use errors; reserve panic for programmer bugs.
- `time.After` in a hot loop: timers pile up. Use `time.NewTimer` and stop it.

## Review
- [ ] Every error is checked or deliberately dropped with a comment.
- [ ] Goroutines have an exit and are covered by `-race` tests.
- [ ] HTTP clients and servers set timeouts; contexts flow through calls.
- [ ] Resources closed via `defer`.
- [ ] `go.mod` and `go.sum` tidy; exported names documented.
