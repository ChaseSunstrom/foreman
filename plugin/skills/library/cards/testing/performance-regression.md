---
name: performance-regression
title: Performance regression tests
area: testing
tags: [testing, performance, regression, benchmark, budget, ci, latency]
detect: []
related: [benchmarking, k6, gatling, locust, test-observability]
---
Guard speed with repeatable measurements against a stored baseline and a tolerance, not one-off timings or wall-clock asserts.

## Verify
- `pytest --benchmark-compare --benchmark-compare-fail=mean:10%`: fails when the mean regresses over ten percent against a saved run (needs pytest-benchmark).
- `go test -bench . -benchmem -count=10 ./... | tee new.txt && benchstat old.txt new.txt`: statistical comparison of old and new benchmarks (needs benchstat).
- `hyperfine --warmup 3 --runs 20 './tool input'`: command-line timing with warmup and variance.
- `k6 run --summary-export out.json test.js`: load results to compare p95 against thresholds.

## Test first
State the budget as a failing assertion, then optimize until it passes.
```python
def test_search_stays_under_budget(benchmark, big_index):
    result = benchmark(big_index.search, "needle")
    assert result
    assert benchmark.stats["median"] < 0.005   # 5 ms budget on the CI runner
```
Prefer comparing to a saved baseline over a fixed number when runners vary.

## Do
- Measure a defined workload on fixed data size, and record machine and commit with each result.
- Warm up first, repeat many runs, and compare medians and percentiles, not a single sample.
- Store baselines from the main branch and compare each change against it with a tolerance (5 to 10 percent) wider than the noise.
- Count deterministic proxies where possible: query count, allocations, bytes transferred, operations. They do not flake.
- Run on stable dedicated runners, one job at a time, with consistent CPU settings.
- Profile before optimizing, and add the benchmark that shows the hotspot first.
- Track trends over time, and alert on gradual drift, not only single-step jumps.
- Put load-test thresholds (p95, error rate) in the load tool so it exits non-zero.

## Avoid
- Wall-clock asserts like `elapsed < 0.1` on shared CI: flaky. Use baselines with tolerance or deterministic counters.
- One run and an average: noise dominates. Repeat and compare distributions.
- Benchmarking with tiny or unrealistic data: the result does not transfer. Use production-shaped data.
- Letting the compiler or JIT remove the work: the benchmark measures nothing. Consume the result (`black_box`, `b.N` loop, `benchmark` fixture).
- Comparing runs from different machines: false regressions. Compare on the same runner class.
- Optimizing without a failing benchmark first: no proof of gain. Measure before and after.

## Review
- [ ] A benchmark or budget exists for each hot path changed.
- [ ] Comparison uses a baseline, repeats and a tolerance.
- [ ] Data and environment are fixed and recorded.
- [ ] Deterministic counters back up timing where possible.
- [ ] CI fails on regression.
