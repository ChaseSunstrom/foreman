---
name: semver
title: Semantic versioning
area: design
tags: [semver, versioning, releases, changelog, compatibility, dependencies]
detect: [file:CHANGELOG.md, file:.changeset/config.json, file:release-please-config.json, dep:semver, dep:@changesets/cli, dep:semantic-release, dep:python-semantic-release]
related: [api-versioning, monorepo, zero-downtime-migrations]
---
MAJOR.MINOR.PATCH tied to the public API: breaking changes bump major, additions bump minor, fixes bump patch.

## Verify
- `npx semver 1.4.0 -r '^1.2.0'`: a range check returns the version if it satisfies the range (npm `semver` CLI).
- `cargo semver-checks`: detects breaking public API changes in a Rust crate (needs cargo-semver-checks installed).
- `npx changeset status`: pending changesets and the version bumps they imply (Changesets repos).
- `git tag --list 'v*' --sort=-v:refname | head -3`: tags sort as versions and the latest is what you expect.
- `go list -m -versions example.com/mod`: published versions of a Go module, where major 2 and above use a `/v2` path suffix.

## Test first
Encode the compatibility promise as a test that fails on a breaking change.
```python
def test_public_api_surface_is_unchanged():
    import mylib
    assert sorted(mylib.__all__) == ["Client", "Error", "connect"]
    sig = inspect.signature(mylib.connect)
    assert list(sig.parameters) == ["url", "timeout"]   # new params must be optional and last
```
Alternatives: `cargo semver-checks`, `api-extractor` (TypeScript), `japicmp` (Java), `apidiff` (Go).

## Do
- Define the public API first (exported symbols, CLI flags, wire formats, config keys). Only that surface is covered by the promise.
- Bump major for removals, renames, type or behavior changes that break callers. Bump minor for backward-compatible additions. Bump patch for fixes with no API change.
- Before 1.0.0 (`0.y.z`), anything may change. Say so, and move to 1.0.0 once you have users relying on it.
- Deprecate before removing: mark it in code and docs, keep it for at least one minor release, then remove in the next major.
- Keep a changelog grouped by Added, Changed, Deprecated, Removed, Fixed, Security, and generate bumps from commits or changesets.
- Tag releases as `vMAJOR.MINOR.PATCH` and publish exactly what was tagged. Never re-tag or overwrite a published version.
- Use prerelease identifiers (`2.0.0-rc.1`) for candidates. They sort below the release.
- Pin consumers with ranges that match the promise (`^1.2.0`), and lock exact versions in applications.

## Avoid
- Treating a "small" behavior change as a patch: callers depend on behavior. If a reasonable caller breaks, it is major.
- Bumping only on feature size or marketing: version communicates compatibility, not importance.
- Re-publishing different contents under an existing version: caches and lockfiles diverge. Release a new patch.
- Comparing versions as strings (`"1.10.0" < "1.9.0"`): the order is wrong. Use a semver library.
- Dropping the `/v2` suffix in Go modules when the major bumps: the import path must change for major 2 and above.
- Build metadata (`+abc`) used for ordering: it is ignored in precedence.
- Wildcard ranges (`*`, `latest`) in libraries: any upstream major lands unreviewed.

## Review
- [ ] The public surface is defined, and a tool or test guards it.
- [ ] The bump matches the change type, including behavior changes.
- [ ] Deprecations precede removals, and the changelog is updated.
- [ ] Tags match published artifacts and are never reused.
- [ ] Dependency ranges follow the dependency's promise.
