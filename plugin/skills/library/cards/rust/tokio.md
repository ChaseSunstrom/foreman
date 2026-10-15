---
name: tokio
title: Tokio
area: rust
tags: [rust, async, tokio, runtime, concurrency, channels]
detect: [dep:tokio]
related: [axum, cargo, clippy, rust-unsafe, sqlx]
---
Tokio async runtime: tasks, channels, timeouts, cancellation, and keeping blocking work off the executor.

## Verify
- `cargo clippy --all-targets -- -D warnings`: catches `await_holding_lock` and `await_holding_refcell_ref`.
- `cargo test`: async tests through `#[tokio::test]`.
- `cargo tree -i tokio -e features`: which features are enabled and by whom.
- `RUSTFLAGS="--cfg tokio_unstable" cargo check`: only if the code uses tokio-console or other unstable APIs.

## Test first
Use `#[tokio::test]`. Pause the clock so time-based tests are instant (needs the `test-util` feature).
```rust
use std::time::Duration;

#[tokio::test(start_paused = true)]
async fn times_out_slow_call() {
    let slow = tokio::time::sleep(Duration::from_secs(60));
    let r = tokio::time::timeout(Duration::from_secs(1), slow).await;
    assert!(r.is_err());
}
```
Tests live in the module or `tests/`. `#[tokio::test]` uses a current-thread runtime by default.

## Do
- Enable only needed features (`rt-multi-thread`, `macros`, `net`, `time`, `sync`) rather than `full` in libraries.
- Move blocking or CPU-heavy work to `spawn_blocking`, or a rayon pool.
- Bound channels (`mpsc::channel(n)`) so a slow consumer applies backpressure.
- Wrap external calls in `tokio::time::timeout`.
- Cancel with `CancellationToken` (tokio-util) or by dropping the `JoinHandle`'s task via `abort`. Join handles to observe panics.
- Use `tokio::select!` only over cancel-safe futures. Read each branch's docs.
- Use `JoinSet` for a dynamic group of tasks, and `tokio::sync::Mutex` only when a guard must live across `.await`.

## Avoid
- `std::thread::sleep` or blocking I/O in async code: it stalls a worker. Use `tokio::time::sleep` or `spawn_blocking`.
- Holding a `std::sync::Mutex` guard across `.await`: deadlock risk and a non-`Send` future. Scope the guard, or use the tokio mutex.
- `tokio::spawn` with borrowed data: it needs `'static`. Move owned or `Arc` data in.
- Unbounded channels as a default: memory grows without limit. Bound them.
- `block_on` inside a runtime: it panics. Make the caller async.
- Dropping a `JoinHandle` and assuming the task stops: it detaches and keeps running.
- Using `#[tokio::main]` in library code: the binary owns the runtime.

## Review
- [ ] No blocking calls on async paths and no lock guard held over `.await`.
- [ ] Every channel is bounded or its growth is justified.
- [ ] Tasks have a shutdown path and their errors are surfaced.
- [ ] External I/O has a timeout.
- [ ] `select!` branches are cancel-safe.
