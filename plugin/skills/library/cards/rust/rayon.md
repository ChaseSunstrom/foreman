---
name: rayon
title: rayon
area: rust
tags: [rust, parallel, rayon, performance, threads, iterators]
detect: [dep:rayon]
related: [tokio, criterion, clippy, rust-unsafe]
---
rayon data parallelism: par_iter for CPU-bound work, thread-pool control, determinism and the async boundary.

## Verify
- `cargo test`: results match the sequential version.
- `RAYON_NUM_THREADS=1 cargo test`: single-thread run still passes (catches hidden ordering and lock assumptions).
- `cargo bench` (criterion): the parallel version is actually faster for realistic input sizes.
- `cargo clippy --all-targets -- -D warnings`: lints.

## Test first
Prove equivalence with the sequential result before optimizing.
```rust
#[test]
fn parallel_sum_matches_sequential() {
    let v: Vec<u64> = (0..100_000).collect();
    let seq: u64 = v.iter().map(|x| x * x).sum();
    let par: u64 = v.par_iter().map(|x| x * x).sum();
    assert_eq!(seq, par);
}
```

## Do
- Swap `.iter()` for `.par_iter()` (`use rayon::prelude::*`) only where per-item work is substantial; measure first.
- Prefer `map`/`filter`/`reduce`/`sum`/`collect` over shared mutation. `collect::<Vec<_>>()` on an indexed iterator keeps order.
- Use `reduce(|| identity, op)` with an associative op and a true identity; `fold` + `reduce` for per-thread accumulators.
- Build a dedicated pool for isolation: `ThreadPoolBuilder::new().num_threads(n).build()?` then `pool.install(|| ...)`.
- Tune granularity with `.with_min_len(n)` for cheap items; use `par_chunks` for slices.
- Use `rayon::join` and `rayon::scope` for divide and conquer.
- Use `try_for_each`/`try_reduce` to short-circuit on errors.

## Avoid
- Parallelizing tiny work: scheduling cost exceeds gain. Benchmark; add `with_min_len`.
- `Mutex` around a shared Vec pushed to from every item: serializes. Use `collect` or `fold`/`reduce`.
- Non-associative reduce ops (e.g. subtraction, float order sensitivity treated as exact): results vary run to run. Make ops associative or tolerate error.
- Blocking I/O or `.await`/`block_on` inside rayon closures: starves the pool. Keep rayon for CPU only.
- Calling rayon on a tokio worker directly for long jobs: blocks the runtime. Use `spawn_blocking` then rayon, or a oneshot from a pool thread.
- `for_each` with println ordering assumptions: output interleaves. Collect then print.
- `par_iter` on `HashMap` expecting order: iteration order is arbitrary.

## Review
- [ ] A benchmark shows a speedup at production input size.
- [ ] Output order and results do not depend on thread count (tested with `RAYON_NUM_THREADS=1`).
- [ ] No lock contention in hot closures.
- [ ] Rayon work does not block an async runtime thread.
- [ ] Reduction ops are associative with a real identity.
