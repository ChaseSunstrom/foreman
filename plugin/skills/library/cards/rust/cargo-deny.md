---
name: cargo-deny
title: cargo-deny
area: rust
tags: [rust, supply-chain, licenses, advisories, cargo-deny, security]
detect: [file:deny.toml, file:.cargo/audit.toml]
related: [cargo, cargo-workspaces, clippy, rust-unsafe]
---
cargo-deny policy gate: advisories, licenses, banned and duplicate crates, and allowed sources, enforced in CI.

## Verify
- `cargo deny check`: runs advisories, bans, licenses and sources together; must exit 0.
- `cargo deny check advisories`: RustSec vulnerabilities and yanked crates only.
- `cargo deny check licenses`: every dependency license is on the allow list.
- `cargo deny check bans sources`: banned crates, duplicates and registry origins.
- `cargo deny list`: licenses actually present, to build the allow list from.

## Test first
The failing check is the policy itself. Add the rule, then prove it bites by adding a violating dep (or a temporary ban of a crate you use) and seeing it fail.
```toml
# deny.toml
[bans]
multiple-versions = "warn"
deny = [{ crate = "openssl" }]
```
`cargo deny check bans` must fail if `openssl` appears in `cargo tree -i openssl`, and pass once removed.

## Do
- Generate a starting file with `cargo deny init`, then review every section; keep it committed at the repo root.
- `[licenses]`: use an explicit `allow = ["MIT", "Apache-2.0", ...]` list of SPDX ids; handle exceptions per crate with `exceptions`.
- `[advisories]`: fail on vulnerabilities and yanked crates; document each `ignore = ["RUSTSEC-..."]` with a reason and review date in a comment.
- `[bans]`: ban crates you replaced (for example a duplicate TLS stack) and set `wildcards = "deny"` so `*` versions fail.
- `[sources]`: `unknown-registry = "deny"` and `unknown-git = "deny"`, allow only known registries and git orgs.
- Run in CI on each PR and on a schedule, since new advisories appear without code changes.
- Use `skip` / `skip-tree` for duplicates you can't fix yet, with a comment.

## Avoid
- A broad `ignore` list with no reasons: hides real vulnerabilities. Justify each, remove when fixed.
- Allowing licenses by guess: copyleft sneaks in. Derive from `cargo deny list` and legal policy.
- Running only on PRs: new advisories land later. Add a scheduled run.
- Pinning an out-of-date advisory database offline: stale results. Allow the fetch in CI.
- Config keys from old tutorials (removed `vulnerability`/`unmaintained` severity keys in newer versions): run `cargo deny check` and follow its diagnostics for your installed version.
- `git` dependencies on forks without allowlisting: sources check fails. List them deliberately.

## Review
- [ ] `cargo deny check` passes in CI and on a schedule.
- [ ] License allow list is explicit and justified.
- [ ] Every advisory ignore has a reason and owner.
- [ ] Unknown registries and git sources are denied by default.
- [ ] Duplicate-version warnings are reviewed, not ignored.
