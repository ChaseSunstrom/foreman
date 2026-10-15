---
name: go-context
title: Go context
area: go
tags: [go, context, cancellation, timeout, deadlines, goroutines]
detect: []
related: [go-concurrency, go-http-server, go-errors, go-grpc]
---
context.Context for cancellation and deadlines: first parameter, always cancelled, never stored, values only for request-scoped data.

## Verify
- `go vet ./...`: includes the `lostcancel` check for discarded cancel funcs.
- `go test -race ./...`: shutdown and cancel paths are race free.
- `go test -run TestCancel -count=50 ./...`: cancellation tests aren't flaky.
- `go test -v -run . -timeout 30s ./...`: a hang (missing ctx plumbing) fails fast instead of stalling CI.

## Test first
Prove the function stops when the context is cancelled.
```go
func TestFetchHonoursCancel(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	_, err := Fetch(ctx, slowSrv.URL)
	if !errors.Is(err, context.Canceled) {
		t.Fatalf("err = %v, want context.Canceled", err)
	}
}
```

## Do
- Take `ctx context.Context` as the first parameter, named `ctx`, on every function that does I/O or waits.
- `defer cancel()` immediately after `WithCancel`, `WithTimeout` or `WithDeadline`.
- Pass the caller's ctx down; derive tighter timeouts per call: `ctx, cancel := context.WithTimeout(ctx, 2*time.Second)`.
- In loops and selects, watch `<-ctx.Done()` and return `ctx.Err()`.
- Use `exec.CommandContext`, `http.NewRequestWithContext`, `db.QueryContext` and similar ctx-aware APIs.
- Use `context.WithCancelCause` and `context.Cause(ctx)` when callers need to know why.
- `context.AfterFunc` and `context.WithoutCancel` exist for cleanup that must outlive the request; use them deliberately.
- Define value keys as unexported custom types: `type ctxKey struct{}`.

## Avoid
- Storing ctx in a struct: lifetimes blur. Pass it per call (long-lived servers excepted, documented).
- `context.Background()` deep in the call chain: severs cancellation. Plumb the caller's ctx; Background only in `main`, tests, init.
- Forgetting `cancel`: leaks timers and goroutines. `defer cancel()` right away.
- Using ctx values for optional parameters or dependencies: hidden coupling. Use arguments; keep values for request IDs, auth identity, trace data.
- String keys in `WithValue`: collisions. Use private types.
- Ignoring `ctx.Err()` after a blocking call: continuing work on a dead request. Check and return.
- Passing `nil` ctx: panics. Use `context.TODO()` when unsure.
- `time.Sleep` in cancellable code: use `select` with `time.After` or a timer and `ctx.Done()`.

## Review
- [ ] Every blocking or I/O function takes ctx first and honours it.
- [ ] Every `With*` has a deferred cancel.
- [ ] No ctx in struct fields without a justification.
- [ ] No `Background()` in request paths.
- [ ] A test proves cancellation or timeout ends the work.
