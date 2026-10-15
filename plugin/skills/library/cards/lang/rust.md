---
name: rust
title: Rust
area: lang
tags: [rust, cargo, clippy, rustfmt, ownership, tokio]
detect: [ext:.rs, file:Cargo.toml, file:Cargo.lock]
related: [tokio, serde, c, cpp]
---
Rust baseline: cargo check, clippy with warnings denied, rustfmt, unit and integration tests, and errors as values.

## Verify
- `cargo check --all-targets`: fast compile of lib, bins, tests and benches.
- `cargo clippy --all-targets -- -D warnings`: lints as errors.
- `cargo fmt --check`: formatting.
- `cargo test`: unit, integration and doc tests.

## Test first
Unit tests in a `#[cfg(test)] mod tests` beside the code; integration tests in `tests/*.rs` using only the public API.
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_rejects_empty() {
        assert!(parse_port("").is_err());
    }
}
```

## Do
- Return `Result<T, E>`; use `thiserror` for library error enums and `anyhow` in binaries.
- Propagate with `?` and add context (`.context("reading config")` with anyhow).
- Borrow (`&str`, `&[T]`) in parameters; return owned types.
- Derive `Debug`, `Clone`, `PartialEq` where sensible; use `#[must_use]` on results callers could ignore.
- Prefer iterators and `match` over index loops and flag variables; make illegal states unrepresentable with enums.
- Keep `unsafe` in small, commented blocks with a `// SAFETY:` justification.
- Commit `Cargo.lock` for binaries; set `edition` and `rust-version` in Cargo.toml.

## Avoid
- `.unwrap()` and `.expect()` on fallible runtime input: panics in production. Return the error; reserve them for proven invariants and tests.
- `.clone()` to quiet the borrow checker: hidden cost and often a design smell. Restructure ownership or borrow.
- Holding a `std::sync::Mutex` guard across `.await`: deadlocks and non-Send futures. Scope the guard or use an async mutex.
- Blocking calls (`std::fs`, `thread::sleep`) inside async tasks: stall the executor. Use async APIs or `spawn_blocking`.
- Indexing `v[i]` or slicing strings by byte offsets on untrusted input: panics. Use `.get(i)` and `char_indices`.
- `as` for numeric narrowing: silent truncation. Use `try_from`.
- `#[allow(...)]` to silence clippy without a reason: fix or document the exception.

## Review
- [ ] No new `unwrap`/`expect`/`panic!` on paths driven by input.
- [ ] Clippy and rustfmt clean; no blanket `allow`.
- [ ] Every `unsafe` block has a `SAFETY` comment and a test or proof of the invariant.
- [ ] Errors carry context and public error types are stable.
- [ ] Async code holds no sync lock across an await and does no blocking I/O.
