---
name: go-pprof
title: Go pprof profiling
area: go
tags: [go, pprof, profiling, performance, benchmarks, tracing]
detect: []
related: [go-concurrency, go-slog, go-testing, go-http-server]
---
Profile before optimizing: benchmark profiles, live pprof endpoints, heap and goroutine leaks, and benchstat comparisons.

## Verify
- `go test -bench . -benchmem -cpuprofile cpu.out -memprofile mem.out ./pkg`: benchmark with profiles.
- `go tool pprof -top cpu.out`: hottest functions by flat and cumulative time.
- `go tool pprof -http=:0 cpu.out`: flame graph and source view.
- `go test -bench . -count=10 ./pkg > new.txt` then `benchstat old.txt new.txt`: the change is statistically real (benchstat is `golang.org/x/perf/cmd/benchstat`).
- `go build -gcflags=-m ./pkg 2>&1 | grep escapes`: why values heap-allocate.

## Test first
A benchmark with `b.ReportAllocs()` is the failing check: it records the baseline, and the goal states the target.
```go
func BenchmarkParse(b *testing.B) {
	in := loadSample()
	b.ReportAllocs()
	for b.Loop() {
		_ = Parse(in)
	}
}
```
`b.Loop()` needs a recent Go; on older toolchains use `for i := 0; i < b.N; i++`.

## Do
- Capture a baseline benchmark and profile first; change one thing; compare with `benchstat` over 10 or more runs.
- Expose live profiles on an internal-only listener: `import _ "net/http/pprof"` on a separate private mux or port, never the public one.
- Pull a 30 s CPU profile with `go tool pprof http://host:port/debug/pprof/profile?seconds=30`; heap via `/debug/pprof/heap`; goroutines via `/debug/pprof/goroutine?debug=2`.
- Compare heap snapshots with `-base old.heap` to find leaks; use `-sample_index=alloc_space` for allocation churn.
- Use `go tool trace` (from `runtime/trace`) for scheduler latency and GC pauses.
- Reduce allocations by preallocating (`make([]T, 0, n)`), reusing buffers (`sync.Pool` where measured), and avoiding interface boxing.
- Record before and after numbers in the commit or PR.

## Avoid
- Optimizing without a profile: guesses miss the real hot spot. Measure first.
- Registering pprof on the public mux (`DefaultServeMux`) via blank import: exposes internals. Use a private listener or auth.
- Single noisy benchmark runs: variance. Use `-count` and `benchstat`.
- Profiling a debug or `-race` build: distorted. Profile a normal build.
- Benchmark loops the compiler optimizes away: assign results to a package-level sink.
- `sync.Pool` as a default: adds complexity and can hurt. Keep only with measured wins.
- Reading `-top` flat only: the cost may be in cumulative callers. Check `-cum` and the graph.

## Review
- [ ] Baseline and after numbers are recorded with `-benchmem`.
- [ ] Comparison uses repeated runs and `benchstat`.
- [ ] pprof endpoints are not publicly reachable.
- [ ] The optimization targets a function the profile actually shows.
- [ ] Correctness tests still pass after the change.
