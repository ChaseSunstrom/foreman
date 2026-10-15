---
name: thiserror-anyhow
title: thiserror and anyhow
area: rust
tags: [rust, errors, thiserror, anyhow, result, library]
detect: [dep:thiserror, dep:anyhow]
related: [cargo, clippy, tracing, axum]
---
Rust error handling: typed enums with thiserror in libraries, anyhow with context at application edges.

## Verify
- `cargo clippy --all-targets -- -D warnings`: lints, including needless error conversions and `unwrap` misuse.
- `cargo test`: error paths and `Display` text are asserted.
- `cargo doc --no-deps`: `# Errors` sections render for public fallible fns.
- `grep -rn "unwrap()\|expect(" src`: panics left in non-test code are deliberate.

## Test first
Unit tests next to the code assert the variant, not the message.
```rust
#[test]
fn parse_rejects_empty_port() {
    let err = parse_addr("host:").unwrap_err();
    assert!(matches!(err, AddrError::BadPort { .. }));
    assert_eq!(err.to_string(), "invalid port in `host:`");
}
```

## Do
- Libraries: one `#[derive(Debug, thiserror::Error)]` enum per module boundary, with `#[error("...")]` on each variant.
- Wrap sources with `#[from]` for plain conversion, or `#[source]` when you add fields. `?` then converts automatically.
- Binaries and `main`: return `anyhow::Result<()>` and add `.context("reading config")` or `.with_context(|| format!(...))` at each layer.
- Lowercase error messages with no trailing period, and don't repeat the source text: the chain prints it.
- Match on the typed error when callers need to branch; use `err.downcast_ref::<T>()` on anyhow only at the edge.
- Mark enums `#[non_exhaustive]` in published crates so adding variants is not breaking.
- Print chains with `{:#}` (one line) or `{:?}` (multi-line with backtrace when `RUST_BACKTRACE=1`).

## Avoid
- `anyhow::Error` in a library's public API: callers can't match. Return a thiserror enum.
- A single giant `Error` enum for the whole crate: variants unrelated to a fn leak into its signature. Split per module.
- `#[error("{0}")]` with `#[from]` on the same source: the message is printed twice in chains. Give own context or use `#[error(transparent)]`.
- `Box<dyn Error>` plus `.to_string()` mapping: loses the source chain. Keep `#[source]`.
- `unwrap()` on user input or I/O: panics in production. Propagate with `?`.
- `map_err(|_| MyError::Io)`: discards the cause. Use `#[from]` or keep the error as a field.
- Deriving `PartialEq` on an enum holding `io::Error`: won't compile; compare with `matches!`.

## Review
- [ ] Library public fns return typed errors; only `main`/handlers use anyhow.
- [ ] Every `?` crossing a boundary has context or a `#[from]` with a clear message.
- [ ] No `unwrap`/`expect` on fallible runtime input outside tests.
- [ ] Error enums are `#[non_exhaustive]` where published, and `Send + Sync + 'static`.
- [ ] Tests assert variants for each failure path.
