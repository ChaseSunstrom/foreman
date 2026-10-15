---
name: cargo
title: Cargo
area: rust
tags: [rust, cargo, build, workspace, dependencies, features]
detect: [file:Cargo.toml, file:Cargo.lock, ext:.rs]
related: [clippy, rust-unsafe, tokio, serde]
---
Cargo projects: workspaces, features, lockfile discipline, and the check, test and lint loop.

## Verify
- `cargo check --workspace --all-targets --locked`: everything compiles, tests and benches included, and Cargo.lock is current.
- `cargo test --workspace`: unit, integration and doc tests across members.
- `cargo fmt --all --check`: formatting.
- `cargo tree -d`: duplicate versions of one crate in the graph.
- `cargo check --no-default-features`: the feature set still builds without defaults.

## Test first
Unit tests sit in a `#[cfg(test)] mod tests` beside the code. Integration tests live in `tests/*.rs` and see only the public API. Doc examples run under `cargo test --doc`.
```rust
// src/lib.rs
pub fn parse_port(s: &str) -> Result<u16, std::num::ParseIntError> { todo!() }

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn rejects_out_of_range() {
        assert!(parse_port("70000").is_err());
    }
}
```
Run one test with `cargo test -p crate_name rejects_out_of_range`.

## Do
- Declare shared deps once in the root `[workspace.dependencies]` and use `dep.workspace = true` in members.
- Commit `Cargo.lock` for binaries. Build CI with `--locked`.
- Keep features additive: enabling one must never remove behaviour. Name them for capabilities, not crates.
- Set `rust-version` (MSRV) and `edition` in `[package]`. Use `resolver = "2"` in a virtual workspace manifest.
- Put dev-only crates in `[dev-dependencies]` and build-script crates in `[build-dependencies]`.
- Use `cargo add`, `cargo update -p NAME` and `cargo tree -i NAME` to change and inspect deps.
- Trim release size and speed in `[profile.release]` (`lto`, `codegen-units`, `panic = "abort"`) only after measuring.

## Avoid
- `cargo build` as the inner loop: use `cargo check`, which skips codegen.
- Wildcard versions (`"*"`): crates.io rejects them on publish. Use a caret range.
- Path-only deps in a published crate: add a `version` next to `path`.
- Features that are mutually exclusive: unification across the graph turns both on. Make one win or split crates.
- Running `cargo update` as a drive-by fix: it bumps everything. Update the one package.
- Committing `target/`: ignore it.
- Using `[patch]` or git deps and forgetting them: record why and the removal condition.

## Review
- [ ] Lockfile changes match the intended dependency edits only.
- [ ] New dependencies are justified, maintained and licence-checked.
- [ ] Features are additive and `--no-default-features` still builds.
- [ ] Workspace members inherit shared versions and metadata.
- [ ] CI uses `--locked` and runs fmt, clippy and tests.
