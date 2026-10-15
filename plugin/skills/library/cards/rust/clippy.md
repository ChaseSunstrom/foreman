---
name: clippy
title: Clippy and rustfmt
area: rust
tags: [rust, lint, clippy, rustfmt, ci, quality]
detect: [file:clippy.toml, file:.clippy.toml, file:rustfmt.toml, file:.rustfmt.toml]
related: [cargo, rust-unsafe, tokio]
---
Clippy lints and rustfmt: a warnings-as-errors gate that stays quiet because suppressions are explained.

## Verify
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`: lints everything, tests included, warnings fatal.
- `cargo fmt --all --check`: formatting differences without rewriting files.
- `cargo clippy --fix --allow-dirty --allow-staged`: applies machine-fixable lints (review the diff).
- `cargo doc --no-deps`: docs build with no broken intra-doc links.

## Test first
The check that fails first is the lint itself: reproduce the warning, then fix it.
```bash
cargo clippy --all-targets -- -D warnings 2>&1 | head -40
# expect: error: this `if` has identical blocks / needless_range_loop / etc.
```
After the change the same command must exit 0. For a project-wide lint policy, add it to `Cargo.toml` and see the build fail first:
```toml
[workspace.lints.clippy]
unwrap_used = "warn"
```
Members opt in with `[lints] workspace = true`.

## Do
- Run clippy in CI with `-D warnings` and the same toolchain as local (pin it in `rust-toolchain.toml`).
- Configure lints centrally in `[lints.rust]` and `[lints.clippy]` (or `[workspace.lints]`) rather than scattered attributes.
- Use `#[expect(clippy::lint_name, reason = "...")]` over `#[allow]` so stale suppressions get flagged.
- Set `msrv` in `clippy.toml` so lints don't suggest newer APIs.
- Commit a `rustfmt.toml` only for settings you really need. Stable options only.
- Enable pedantic lints per module when useful, not blanket `clippy::pedantic` on an existing codebase.
- Fix the lint at its cause. Prefer iterator, `?` and pattern idioms clippy points to.

## Avoid
- Crate-wide `#![allow(clippy::all)]`: it hides real bugs. Allow one lint at one item with a reason.
- `cargo clippy` without `--all-targets`: test and bench code goes unlinted.
- Nightly-only rustfmt options in `rustfmt.toml`: stable `cargo fmt` warns and ignores them.
- `cargo clippy --fix` and committing blindly: it can change semantics (for example `needless_return` is safe, others are not). Read the diff.
- Silencing `unwrap_used` in lib code to get green: return a `Result` instead.
- Formatting by hand-aligning code: rustfmt reverts it. Use `#[rustfmt::skip]` sparingly on a tabular item.

## Review
- [ ] Every suppression is narrow and has a reason.
- [ ] CI runs fmt check and clippy with `-D warnings` over all targets and features.
- [ ] Lint policy lives in one place (workspace lints or crate root).
- [ ] The toolchain is pinned so lints don't shift under the team.
