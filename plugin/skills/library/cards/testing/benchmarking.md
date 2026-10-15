---
name: benchmarking
title: Benchmarking
area: testing
tags: [benchmark, performance, microbenchmark, regression, statistics, profiling]
detect: [dep:pytest-benchmark, dep:criterion, dep:tinybench, file:benches/*, file:*_bench_test.go]
related: [k6, locust, unit-test-design, flaky-tests]
---
Benchmarks compare the cost of code before and after a change, with warmup, repeated samples and a stored baseline, not one stopwatch run.

## Verify
- `go test -bench=. -benchmem -count=10 ./pkg`: Go samples with allocations; compare runs with `benchstat old.txt new.txt`.
- `cargo bench`: Criterion reports a change versus the saved baseline.
- `pytest --benchmark-only --benchmark-compare`: pytest-benchmark compares against a saved run.
- `npx vitest bench`: Vitest benchmark mode runs `bench()` cases.

## Test first
Measure the current behavior before optimizing and keep that number.
```go
func BenchmarkParse(b *testing.B) {
	in := loadFixture("large.json")
	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		_, _ = Parse(in)
	}
}
```
Benchmarks live with the code (`*_test.go`, `benches/`, `tests/bench_*.py`).

## Do
- Record a baseline on the same machine, then change one thing and rerun.
- Use realistic input sizes and shapes; benchmark several sizes to see the growth curve.
- Run many samples and compare distributions (median, spread), not one mean.
- Keep setup outside the timed region; prevent dead-code elimination by consuming results (`black_box`, assign to a sink).
- Pin the environment: fixed CPU frequency or idle machine, same toolchain, no other load.
- Profile (pprof, perf, py-spy, flamegraph) to find the hotspot before optimizing.
- Check correctness with a normal test alongside, so a faster wrong answer fails.

## Avoid
- Timing with a single `time.time()` or `Date.now()` pair: noise dominates. Use the benchmark harness with repeats.
- Letting the compiler or JIT remove the work (unused result): impossible numbers. Consume the output.
- Benchmarking on a laptop with other load, or in shared CI without noise controls: unstable. Compare relative to a baseline run in the same job.
- Optimizing without a baseline: no proof it helped. Save before and after.
- Hard failing CI on small percentage changes: flaky. Use wide thresholds or report only.
- Microbenchmarks standing in for end-to-end performance: confirm with a load test.

## Review
- [ ] Baseline and result are from the same environment.
- [ ] Inputs are realistic and sizes vary.
- [ ] Results are consumed so the work cannot be elided.
- [ ] Correctness tests still pass.
- [ ] The claimed speedup exceeds measured noise.
