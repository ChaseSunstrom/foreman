---
name: cargo-workspaces
title: Cargo workspaces
area: rust
tags: [rust, cargo, workspace, monorepo, dependencies, features]
detect: [file:Cargo.lock, dep:cargo-workspaces]
related: [cargo, cargo-deny, clippy, rust-unsafe]
---
Cargo workspaces: shared lockfile, workspace dependencies and lints, feature unification and per-crate checks.

## Verify
- `cargo check --workspace --all-targets`: every member and target compiles.
- `cargo test --workspace`: all member tests.
- `cargo clippy --workspace --all-targets -- -D warnings`: lints everywhere.
- `cargo metadata --no-deps --format-version 1`: members and their manifests resolve.
- `cargo tree -d`: duplicate versions of the same crate (candidates to unify).
- `cargo check -p NAME --no-default-features`: one member builds without default features.

## Test first
The failing check is the build or the dependency tree. For a new crate, first add a test that imports it.
```rust
// crates/core/tests/smoke.rs
#[test]
fn core_exposes_version() {
    assert!(!core_lib::version().is_empty());
}
```
Run `cargo test -p core-lib` and watch it fail before adding the function.

## Do
- Root `Cargo.toml`: `[workspace] members = ["crates/*"] resolver = "2"` (resolver "3" only on editions and toolchains that support it).
- Declare versions once under `[workspace.dependencies]`; members use `serde = { workspace = true }` and can add `features` locally.
- Share metadata with `[workspace.package]` (`version`, `edition`, `license`) and inherit with `version.workspace = true`.
- Share lint policy with `[workspace.lints]` and `[lints] workspace = true` in each member.
- Use path plus version for publishable internal deps: `core = { path = "../core", version = "0.1" }`.
- Commit `Cargo.lock` for workspaces that ship binaries.
- Use `default-members` so plain `cargo build` skips heavy or platform-specific crates.
- Keep `cargo test -p` and `--features` explicit in CI; test feature combos that matter.

## Avoid
- Version numbers repeated in every member: they drift. Use `workspace = true`.
- Assuming per-crate feature isolation: features unify across the workspace in one build, so a crate may compile with features another member turned on. Check with `cargo check -p` and `-Zfeatures`-free per-package builds.
- Path-only deps in a published crate: `cargo publish` rejects them. Add `version`.
- Virtual manifest plus `[dependencies]` at root: not allowed. Put deps in members.
- Circular dependencies between members: extract the shared part to a third crate.
- Setting `resolver` only in members: ignored. Set it in the root.

## Review
- [ ] Shared dependencies and package metadata are declared once at the root.
- [ ] `cargo tree -d` shows no avoidable duplicates.
- [ ] Each member builds alone (`-p`) and with default features off where relevant.
- [ ] Dependency graph has a clear direction with no cycles.
- [ ] CI runs workspace check, test and clippy.
