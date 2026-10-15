---
name: criterion
title: criterion benchmarks
area: rust
tags: [rust, benchmark, criterion, performance, profiling]
detect: [dep:criterion, dep:divan]
related: [rayon, proptest, cargo, clippy]
---
Criterion benchmarks: statistically sound timings, black_box, baselines and CI-safe comparison.

## Verify
- `cargo bench`: benchmarks build and run; reports land under `target/criterion`.
- `cargo bench -- --save-baseline before`: records a baseline to compare after the change.
- `cargo bench -- --baseline before`: compares against it and reports regression or improvement.
- `cargo bench --no-run`: benches at least compile (cheap CI check).

## Test first
Write the bench and a correctness test for the same function first; a fast wrong function is worthless.
```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn bench_parse(c: &mut Criterion) {
    let input = include_str!("../tests/data/sample.txt");
    c.bench_function("parse_sample", |b| b.iter(|| parse(black_box(input))));
}
criterion_group!(benches, bench_parse);
criterion_main!(benches);
```
Register in `Cargo.toml`: `[[bench]] name = "parse"  harness = false`, file at `benches/parse.rs`.

## Do
- Set `harness = false` for every `[[bench]]`; without it criterion's main is not used.
- Wrap inputs in `black_box` and results are consumed by `iter` return values, so the optimizer can't delete the work.
- Build setup outside `b.iter`; use `iter_batched(setup, routine, BatchSize::SmallInput)` when each run needs fresh state.
- Compare variants with `benchmark_group` and `bench_with_input(BenchmarkId::new("name", n), ..)` across sizes.
- Report throughput with `group.throughput(Throughput::Bytes(n))`.
- Benchmark in release with realistic data; pin CPU frequency and close other load when comparing.
- Record before/after numbers in the PR with the baseline name.

## Avoid
- Timing a debug build: meaningless. `cargo bench` uses the bench profile (optimized), so don't use `cargo run`.
- Benchmarking a constant the compiler folds away: results near 0 ns. Use `black_box` on inputs.
- Including allocation or file I/O of setup in the timed closure: measures the wrong thing. Use `iter_batched`.
- Reading a single run as truth: noise. Trust the confidence interval and `p` value, rerun if "changed" is borderline.
- Using the unstable `#[bench]`: needs nightly. Use criterion.
- Failing CI on small percent changes from shared runners: flaky. Compare locally or use wide thresholds.

## Review
- [ ] Each `[[bench]]` has `harness = false`.
- [ ] Inputs go through `black_box`, setup is outside the timed closure.
- [ ] A correctness test covers the benched function.
- [ ] Before/after baseline numbers are recorded.
- [ ] Sizes vary to reveal scaling, not just one point.
