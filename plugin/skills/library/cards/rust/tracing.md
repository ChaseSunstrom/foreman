---
name: tracing
title: tracing
area: rust
tags: [rust, logging, tracing, spans, observability, opentelemetry]
detect: [dep:tracing, dep:tracing-subscriber]
related: [tokio, axum, thiserror-anyhow, tonic]
---
Structured, span-based logging with tracing and tracing-subscriber, including async correctness.

## Verify
- `cargo clippy --all-targets -- -D warnings`: lints.
- `RUST_LOG=debug cargo run`: the `EnvFilter` actually selects events (filter syntax `my_crate=debug,hyper=warn`).
- `cargo test -- --nocapture`: test subscriber output is visible.
- `grep -rn "println!\|eprintln!" src`: no stray prints bypass the subscriber.

## Test first
Assert that the event is emitted, using a capturing writer or `tracing-test` if present.
```rust
#[tracing_test::traced_test]
#[test]
fn logs_retry_with_attempt_field() {
    retry_once();
    assert!(logs_contain("retrying"));
    assert!(logs_contain("attempt=1"));
}
```
If `tracing-test` is absent, build a subscriber with `tracing_subscriber::fmt().with_writer(...)` and `tracing::subscriber::with_default`.

## Do
- Initialize once in `main`: `tracing_subscriber::registry().with(EnvFilter::from_default_env()).with(fmt::layer()).init()`.
- Use fields, not formatting: `info!(user_id = %id, attempt, "retrying")`. `%` uses Display, `?` uses Debug.
- Annotate fns with `#[instrument(skip(self, big_arg), err)]` so spans carry args and `Err` returns log automatically.
- In async code attach spans with `fut.instrument(span)`, or `#[instrument]` on the `async fn`.
- Use `tracing::Instrument` when spawning: `tokio::spawn(work.instrument(Span::current()))`.
- Write to non-blocking output in services: `tracing_appender::non_blocking` and keep its `WorkerGuard` alive to end of `main`.
- Use `tracing-opentelemetry` layer for export; shut the provider down before exit.

## Avoid
- `let _g = span.enter();` held across `.await`: the span attaches to the wrong task. Use `.instrument()`.
- Initializing the global subscriber twice (tests, libraries): panics on `init()`. Use `try_init()` in tests, never init in libraries.
- Dropping the `WorkerGuard`: buffered logs vanish. Bind it to a variable.
- Logging secrets via `#[instrument]` default capture: all args are recorded with Debug. `skip` them or use `skip_all`.
- The `log` macros alongside tracing without `tracing-log`: events are lost. Enable the bridge.
- High-cardinality values as span names: use fields.

## Review
- [ ] One subscriber init, in `main` only, with an `EnvFilter` and a sane default level.
- [ ] No `span.enter()` guard crosses an `.await`.
- [ ] Secrets and large bodies are skipped from `#[instrument]`.
- [ ] Errors are logged once, at the boundary, not at every layer.
- [ ] Async guard for non-blocking writer lives to the end of `main`.
