---
name: go-errors
title: Go error handling
area: go
tags: [go, errors, wrapping, sentinel, errors-is, errors-as]
detect: []
related: [go-testing, go-context, go-http-server, pgx]
---
Go errors: wrap with %w, compare with errors.Is and errors.As, handle or return exactly once.

## Verify
- `go vet ./...`: flags bad `fmt` verbs and `%w` misuse.
- `go test ./...`: error paths asserted by identity, not text.
- `staticcheck ./...`: error-string style (ST1005) and unchecked errors (when installed).
- `golangci-lint run` with `errcheck` enabled (if configured): ignored return errors.

## Test first
Assert the sentinel or type through the wrap chain.
```go
func TestLoadWrapsNotFound(t *testing.T) {
	_, err := Load("missing")
	if !errors.Is(err, ErrNotFound) {
		t.Fatalf("want ErrNotFound, got %v", err)
	}
	var pe *os.PathError
	if !errors.As(err, &pe) {
		t.Fatal("underlying PathError lost")
	}
}
```

## Do
- Add context with `fmt.Errorf("load config %q: %w", name, err)`: say what you were doing, not "failed to".
- Export sentinels as `var ErrNotFound = errors.New("not found")` and test with `errors.Is`.
- Use a custom type with `Error()` (and `Unwrap()` if it wraps) when callers need fields; extract with `errors.As(err, &target)`.
- Combine independent failures with `errors.Join` or multiple `%w` in one `Errorf`.
- Lowercase messages without trailing punctuation.
- Handle an error once: log or return, not both.
- Check `defer f.Close()` results on writes: capture into a named return.
- Translate to transport codes at the boundary (HTTP status, gRPC code), keeping details in logs.

## Avoid
- `%v` or `%s` when you want to wrap: breaks `errors.Is`/`As`. Use `%w`.
- Comparing `err.Error() == "..."` or `strings.Contains`: brittle. Use sentinels or types.
- `err == ErrX` on wrapped errors: false after wrapping. Use `errors.Is`.
- `panic` for expected failures: reserve for programmer errors.
- Returning a typed nil pointer as `error`: `var e *MyErr = nil; return e` is non-nil. Return a literal `nil`.
- Stuttering chains ("failed to X: failed to Y: failed to Z"): each layer adds new information only.
- Swallowing with `_ = f()` on meaningful errors: handle or comment why safe.
- Leaking internals (SQL text, paths) to clients: map to safe messages.

## Review
- [ ] Wrapped with `%w` where callers may inspect.
- [ ] No string matching on errors.
- [ ] Each error is logged or returned, not both.
- [ ] Close errors on written files are checked.
- [ ] Boundary maps errors to status codes without leaking details.
