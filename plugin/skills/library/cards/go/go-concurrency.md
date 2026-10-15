---
name: go-concurrency
title: Go concurrency
area: go
tags: [go, concurrency, goroutines, channels, context, race]
detect: [dep:golang.org/x/sync, ext:.go]
related: [go-testing, go-modules, gin, chi]
---
Goroutines, channels, context and sync: lifetimes, cancellation and race-free sharing.

## Verify
- `go test ./... -race -count=1`: the race detector on all tests.
- `go vet ./...`: copylocks, lost cancel functions and misuse of `sync` types.
- `go test -race -count=50 -run TestName ./pkg`: repeats a concurrent test to surface flakes.
- `go test ./... -run X -timeout 30s`: a deadlock fails fast with goroutine dumps instead of hanging.

## Test first
Write a test that exercises the concurrent path under `-race` and a deadline. Watch it fail.
```go
func TestWorkerStopsOnCancel(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	done := make(chan struct{})
	go func() { Run(ctx); close(done) }()
	cancel()
	select {
	case <-done:
	case <-time.After(time.Second):
		t.Fatal("worker did not stop")
	}
}
```

## Do
- Give every goroutine an owner and an exit path: a context, a closed channel or a `WaitGroup`.
- Pass `context.Context` as the first parameter, derive with `WithTimeout` or `WithCancel`, and always `defer cancel()`.
- Use `errgroup.WithContext` (golang.org/x/sync) for fan-out that fails fast, and `SetLimit` to bound concurrency.
- Let the sender close a channel, never the receiver, and close only once.
- Protect shared state with `sync.Mutex` or `RWMutex` held for the shortest scope, with `defer Unlock`. Keep the mutex next to the data it guards.
- Use `sync/atomic` types (`atomic.Int64`) for counters and flags, and `sync.Once` or `sync.OnceValue` for one-time init.
- Use buffered channels or `select` with `ctx.Done()` on sends so producers never block forever.
- Use `signal.NotifyContext` in `main` for graceful shutdown.

## Avoid
- Fire-and-forget `go f()` in request handlers: leaks, lost errors, panics that crash the process. Track with errgroup or WaitGroup and recover where needed.
- Loop variable capture in goroutines on a pre-1.22 `go` directive: all goroutines see the last value. Pass it as an argument.
- `wg.Add(1)` inside the goroutine: races with `Wait`. Call it before `go`.
- Copying a `sync.Mutex` or `WaitGroup` by value (value receivers, struct copies): `go vet` flags it. Use pointers.
- Sending on a nil or full unbuffered channel with no receiver: a permanent block. Pair every send with a receiver or `select` on `ctx.Done()`.
- `time.After` in a loop: each call allocates a timer until it fires. Use `time.NewTimer` and `Reset`, or a `Ticker`.
- Reading a map while another goroutine writes: a fatal error, not just a race. Guard it or use `sync.Map` for the right workload.
- Using `context.WithValue` for optional parameters: use arguments.

## Review
- [ ] Every goroutine has a defined stop condition and its errors are collected.
- [ ] Cancel functions are always called and ctx is passed down.
- [ ] Shared data has one clear guard, and tests ran under `-race`.
- [ ] Channel ownership is clear: who closes and who blocks.
- [ ] Concurrency is bounded, not one goroutine per input item.
